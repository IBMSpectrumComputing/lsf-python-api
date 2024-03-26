# LSF Python API

These python wrappers allow customers to submit and control jobs and obtain status of queues, hosts and other LSF attributes from Python directly.  They work with various versions of LSF and are maintained by LSF developement, though we take contributions from the Open Source community.

If you plan or would like to contribute to the library, you must follow the DCO process in the attached [DCO Readme file](https://github.com/IBMSpectrumComputing/platform-python-lsf-api/blob/master/IBMDCO.md) in the root of this repository.  It essentially requires you to provide a Sign Off line in the notes of your pull request stating that the work is clear of infinging work by others.  Again, for more details, please see the DCO Readme file.

## Release Information

* IBM Spectrum LSF Python Wrappers
* Supporting LSF Release: 10.1
* Wrapper Version: 1.0.6
* Publication date: 16 October 2013
* Last modified: 31 August 2018

## Contents

* Introduction
* Supported Environment
* Compatibility
* Installation
* Release Notes
* Community Contribution Requirements
* Copyright

## Introduction

This library allows you to call the LSF APIs directly through Python. You can find [some examples here](https://github.com/IBMSpectrumComputing/lsf-python-api/tree/master/examples). The wrapper is created using Pythons SWIG interface and links directly to LSF's shared libraries. 

You are encouraged to contribute your own Python wrappers to the Open Source LSF APIs for Python, and you may find more information and usage notes in [IBM Knowledge Center](https://www.ibm.com/support/knowledgecenter/SSWRJV_10.1.0/best_practices/Using%20the%20Python%20wrapper%20for%20LSF%20API.html) and [IBM Support Community](https://www.ibm.com/mysupport/s/ibm-community-support-search-results?q=LSF+Python+API&page=1&sort=0).

IBM provides formal support for this software to entitled clients via the normal IBM support channels.

This software is Licensed under the Eclipse Public License.

Please note you must use lsf.lsb_init before any other LSBLIB library routine in your application.

## Supported Environment

 - OS
 
   	This package is only tested on Linux platforms.

        Supported operating systems: 
		Linux 2.6 glibc 2.3 x86 64 bit: RHEL 6.2, RHEL6.4, RHEL6.5, RHEL6.8
		Linux 3.10 glibc 2.17 x86 64 bit: Red Hat 7.4, 7.5, 8.8, 8.9
		Linux for Power Systems Servers 8 Little Endian (Linux 3.10, glibc 2.17): RHEL 7.4
		Linux for Power Systems Servers 9 Little Endian (Linux 4.14, glibc 2.17): RHEL 7.5

 - SWIG

        SWIG version 2.0, or 3.0

	The following versions are tested:
		SWIG: 2.0.10, 3.0.12
        
    If isntalling SWIG with pip or pip3, please specify 3.0.12 version.
    `$ pip3 install swig==3.0.12`

 - Python

        Python2 and Python3 are all supported.

	The following versions are tested:
		Python 2.6.6, 2.7.15, 3.0, 3.6.0, 3.7.0, 3.12.2

## Compatibility

        For LSF 10.1.0.2 or earlier version, the compatibility is not guaranteed
      	if you update LSF at a later time. To avoid this compatibility issue, 
      	update LSF to version 10.1.0.3, or later, then rebuild and reinstall the 
      	LSF Python API package.
        

## Installation

Before compiling the library, set the LSF environment variables:

`$ source profile.lsf`

If using python version higher than 3.10, distutils has been deprecated, install setuptools:

`$ pip3 install setuptools`

To compile and install the library, go to the main source directory
and type:

`$ python setup.py build`
or `$ python3 setup.py build`

`$ sudo python setup.py install`
or `$ sudo python3 setup.py install`

To instead build an RPM:

`$ python setup.py bdist_rpm`
or `$ python3 setup.py bdist_rpm`

Resulting RPMs will be placed in the dist directory


## Release Notes

### Release 1.0.6
- Support Python3
    * If you install Python2 and Python3 in the different directories on the same host, 
      you may build & install LSF Python API package separately with Python2 and Python3. 
      After doing this, you can run Python2 script or Python3 script by using 
         `$ python your_lsf_script`
      or `$ python3 your_lsf_script`.

### Release 1.0.5
- Resolve compatibility issue
    * The issue is due to dynamic library. From now on, the static library will 
      be used by LSF Python API pacakge.
    * For Linux ppc64le, IBM XL C/C++ compiler should be installed firstly.
    * For LSF 10.1.0.2 or earlier version, the compatibility is not guaranteed
      if you update LSF at a later time. To avoid this compatibility issue, 
      update LSF to version 10.1.0.3, or later, then rebuild and reinstall the 
      LSF Python API package.
    * The code is tested on Linux x86_64 & ppc64le platform with Python2.7
    * For creating RPM package on Linux ppc64le platform, executing the following 
      instruction not to create debug information package due to compatibility issue:
          `$ echo '%debug_package %{nil}' >> ~/.rpmmacros`

- Release RPM binary package for ppc64le platform

    * lsf-pythonapi-10.1.0.6.csm.ppc64le.rpm

### Release 1.0.4

- Fixed a bug for using lsf.lsb_readstream()
- Added a new example, readstream.py

### Release 1.0.3

-  Added 2 extra routines below :
    * lsb_fseek()
    * lsb_ftell()

### Release 1.0.2

-  Fix a compliation error

### Release 1.0.1

- This is the first release from IBM Platform Computing.
- Tested with LSF 9.1.2 on Linux 2.6.
- In addition to the wrapper for LSF APIs, the following routines were added:
  * get_load_of_hosts() - Returns a list of hostLoad objects.
  * get_host_names()    - Returns the name of the hosts in the cluster.
  * get_host_info()     - Returns a list of hostInfo objects.
  * get_host_load()     - Returns the current values for the resources of a host.

## Community Contribution Requirements

Community contributions to this repository must follow the [IBM Developer's Certificate of Origin (DCO)](https://github.com/IBMSpectrumComputing/platform-python-lsf-api/blob/master/IBMDCO.md) process and only through GitHub Pull Requests:

 1. Contributor proposes new code to community.

 2. Contributor signs off on contributions 
    (i.e. attachs the DCO to ensure contributor is either the code 
    originator or has rights to publish. The template of the DCO is included in
    this package).
 
 3. IBM Spectrum LSF development reviews contribution to check for:
    i)  Applicability and relevancy of functional content 
    ii) Any obvious issues

 4. If accepted, posts contribution. If rejected, work goes back to contributor and is not merged.

## Copyright

(C) Copyright IBM Corporation 2016-2020

U.S. Government Users Restricted Rights - Use, duplication or disclosure 
restricted by GSA ADP Schedule Contract with IBM Corp.

IBM(R), the IBM logo and ibm.com(R) are trademarks of International Business Machines Corp., 
registered in many jurisdictions worldwide. Other product and service names might be trademarks 
of IBM or other companies. A current list of IBM trademarks is available on the Web at 
"Copyright and trademark information" at www.ibm.com/legal/copytrade.shtml.
