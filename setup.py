#!/usr/bin/env python

# 
# (C) Copyright IBM Corporation 2013
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the Eclipse Public License.
# 
import os
import time
from distutils.core import setup, Extension
from distutils.command.bdist_rpm import bdist_rpm

class bdist_rpm_custom(bdist_rpm):
      """bdist_rpm that sets custom RPM options"""
      def finalize_package_data (self):
            if self.release is None:
                  self.release = time.strftime("%Y%m%d")+"%{?dist}"
            if self.vendor is None:
                  self.vendor = 'IBM Corporation'
            if self.packager is None:
                  self.packager = 'IBM Corporation'
            # Disable autoreq in case LSF is installed from a tarball
            self.no_autoreq = 1
            bdist_rpm.finalize_package_data(self)

setup(name='spectrum-lsf-python-api',
      version='1.0.4',
      description='Python binding for Spectrum LSF APIs',
      long_description='Python binding for Spectrum LSF APIs',
      license='LGPL',
      keywords='LSF,Grid,Cluster,HPC',
      url='https://github.com/IBMSpectrumComputing/lsf-python-api',
      ext_package='pythonlsf',
      ext_modules=[Extension('_lsf', ['pythonlsf/lsf.i'],
                               include_dirs=['/usr/include/python2.4'],
                               library_dirs=[os.environ['LSF_LIBDIR']],
                               swig_opts=['-I' + os.environ['LSF_LIBDIR'] + '/../../include/lsf/'],
                               extra_compile_args=['-m64', '-I' + os.environ['LSF_LIBDIR'] + '/../../include/lsf/', '-Wno-strict-prototypes'],			
                               extra_link_args=['-m64'],
                               extra_objects=[os.environ['LSF_LIBDIR'] +'/liblsf.a', os.environ['LSF_LIBDIR'] +'/libbat.a'],
                               libraries=['c', 'nsl', 'rt', 'fairshareadjust', 'lsbstream'])],
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

