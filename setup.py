#!/usr/bin/env python

# 
# (C) Copyright IBM Corporation 2013
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the Eclipse Public License.
# 
import os, sys, re
import time
from distutils.core import setup, Extension
from distutils.command.bdist_rpm import bdist_rpm
from distutils.command.install import INSTALL_SCHEMES

class bdist_rpm_custom(bdist_rpm):
      """bdist_rpm that sets custom RPM options"""
      def finalize_package_data (self):
            if self.release is None:
                  self.release = lsfversion
            if self.vendor is None:
                  self.vendor = 'IBM Corporation'
            if self.packager is None:
                  self.packager = 'IBM Corporation'
            # Disable autoreq in case LSF is installed from a tarball
            self.no_autoreq = 1
            bdist_rpm.finalize_package_data(self)

def get_lsf_libdir():
    try:
        _lsf_envdir = os.environ['LSF_ENVDIR'] 
    except KeyError:
        print('Error: LSF environment variables are not setup.')
        sys.exit()

    try:
        _lsf_libdir = os.environ['LSF_LIBDIR'] 
    except KeyError:
        if _lsf_envdir is not None :
            with open('{}/lsf.conf'.format(_lsf_envdir), 'r') as f:
                _lsf_libdir = re.search('LIBDIR=(.*)', f.read()).group(1).strip()    
    
    return _lsf_libdir
  
def is_keyvalue_defined(lsbatch_h_path):
    cc = None
    with open(lsbatch_h_path, 'r') as f:
        cc = re.search('[\s]*typedef struct keyVal[\s]*', f.read())
    return cc

gccflag_lsfversion = '-DNOLSFVERSION' 
def set_gccflag_lsf_version():
    global gccflag_lsfversion 
    _lsf_envdir = os.environ['LSF_ENVDIR']
    with open('{0}/lsf.conf'.format(_lsf_envdir), 'r') as f:
        _lsf_version = re.search('LSF_VERSION=(.*)', f.read()).group(1).strip() 
    if _lsf_version == '10.1' :
        gccflag_lsfversion= '-DLSF_VERSION_101'
        

if os.uname()[0] == 'Linux' and os.uname()[4] == 'ppc64le' :
    found_xlc = False
    for path in os.environ["PATH"].split(os.pathsep):
        xlc_path = os.path.join(path, 'xlc')
        if os.access(xlc_path, os.F_OK):
            found_xlc = True
            os.environ["LDSHARED"]  = "%s -pthread -shared -Wl,-z,relro" % xlc_path
            break
    if found_xlc == False:
        print('''
Error: Cannot find IBM XL C/C++ compiler. To download and install the Community 
       Edition of the IBM XL C/C++ compiler at no charge, 
       refer to https://ibm.biz/BdYHna.
''')
        sys.exit()

LSF_LIBDIR = get_lsf_libdir()
if LSF_LIBDIR is None :
    print('Error: LSF_LIBDIR can not be got.')
    sys.exit()

set_gccflag_lsf_version()

LSF_INCDIR = LSF_LIBDIR + '/../../include/lsf'
gccflag_keyvaluet = '-DNOTDEFINEFLAG_PYTHONAPI_KEYVALUE_T' 
if is_keyvalue_defined(LSF_INCDIR + '/lsbatch.h') is not None:
    gccflag_keyvaluet = '-DFLAG_PYTHONAPI_KEYVALUE_T'

if os.access(LSF_LIBDIR + "/liblsbstream.a", os.F_OK):
    lsf_static_lib = [ LSF_LIBDIR + '/liblsbstream.a']
    lsf_dynamic_lib = ['c', 'nsl', 'rt']
    warning_msg = ""
else:
    lsf_static_lib = []
    lsf_dynamic_lib = ['c', 'nsl', 'lsbstream', 'lsf', 'bat', 'rt']
    warning_msg = '''
Warning: The compatibility of the LSF Python API package is not guaranteed 
         if you update LSF at a later time. This is because your current 
         version of LSF does not release the
         %s/liblsbstream.a file.
         To avoid this compatibility issue, update LSF to version 10.1.0.3, 
         or later, then rebuild and reinstall the LSF Python API package. 
''' % (LSF_LIBDIR)

if sys.argv[1] == 'bdist_rpm' :
    lsidout = os.popen('lsid | head -1').readlines()
    lsfversion = lsidout[0].split()[4].split(',')[0]

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['platlib']

inc_path = os.path.abspath('pythonlsf')

if 'LSF_PYTHONAPI_INCPATH' not in os.environ:
    os.environ['LSF_PYTHONAPI_INCPATH'] = inc_path
else:
    inc_path = os.environ['LSF_PYTHONAPI_INCPATH']

setup(name='lsf-pythonapi',
      version='1.0.6',
      description='Python binding for IBM Spectrum LSF APIs',
      long_description='Python binding for IBM Spectrum LSF APIs',
      license='EPL',
      keywords='LSF,Grid,Cluster,HPC',
      url='https://github.com/IBMSpectrumComputing/lsf-python-api',
      ext_package='pythonlsf',
      data_files=[('pythonlsf', ['LICENSE'])],
      ext_modules=[Extension('_lsf', ['pythonlsf/lsf.i'],
                               include_dirs=['/usr/include/python2.4', inc_path],
                               library_dirs=[LSF_LIBDIR],
                               swig_opts=['-I' + LSF_LIBDIR + '/../../include/lsf/', 
                                       #   '-DLSF_SIMULATOR',
                                          '-DOS_HAS_THREAD -D_REENTRANT', 
                                            gccflag_keyvaluet, gccflag_lsfversion],
                               extra_compile_args=['-m64', 
                                    '-I' + LSF_LIBDIR + '/../../include/lsf/', 
                                    '-Wno-strict-prototypes', gccflag_keyvaluet,
                                    gccflag_lsfversion,
                                    '-DOS_HAS_THREAD -D_REENTRANT', #For multi-thread lib, lserrno
                                    '-Wp,-U_FORTIFY_SOURCE', #The flag needs -O option. Undefine it for warning.
                                    '-O0'], 
                               extra_link_args=['-m64'],
                               extra_objects=lsf_static_lib,
                               libraries=lsf_dynamic_lib)],
      py_modules=['pythonlsf.lsf'],
      cmdclass = { 'bdist_rpm': bdist_rpm_custom },
      classifiers=["Development Status :: 2 - Pre-Alpha",
                     "License :: OSI Approved :: Eclipse Public License",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python",
                     "Topic :: Internet",
                     "Topic :: Scientific/Engineering",
                     "Topic :: Software Development",
                     "Topic :: System :: Distributed Computing",
                     "Topic :: Utilities",
                     ],
     )

if warning_msg :
    print(warning_msg)
