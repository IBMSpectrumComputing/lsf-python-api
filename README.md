# platform-python-lsf-api

* Readme file for: IBM Spectrum LSF
* Product/Component Release: 10.1
* Version: 1.0.4
* Publication date: 16 October 2013
* Last modified: 6 January 2017

## Python wrapper for LSF APIs

# Contents

* Introduction
* Installation
* Release Notes
* Community Contribution
* Copyright
 
## Introduction

This library allows you to call the LSF APIs (https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/New%20IBM%20Platform%20LSF%20Wiki/page/Integrations%2C%20APIs%2C%20and%20samples) from Python. The wrapper is created with SWIG. 

You are encouraged to contribute your own Python wrappers to the open source LSF APIs for Python, and you may find some examples in  IBM Platform LSF Wiki (https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/New%20IBM%20Platform%20LSF%20Wiki/page/Using%20the%20Python%20wrapper%20for%20LSF%20API).

IBM provides formal support for this software  
to entitled clients via the normal IBM support channels.

This software is under the Eclipse Public License.

Please note you must use lsf.lsb_init before any other LSBLIB library routine in your application.

## Installation

Before compiling the library, set the LSF environment variables.

To compile and install the library, go to the main source directory
and type:

`$ python setup.py build`
`$ sudo python setup.py install`

## Release Notes

* Release 1.0.1

- This is the first release from IBM Platform Computing.
- Tested with LSF 9.1.2 on Linux 2.6.
- In addition to the wrapper for LSF APIs, the following routines were added:
  * get_load_of_hosts() - Returns a list of hostLoad objects.
  * get_host_names()    - Returns the name of the hosts in the cluster.
  * get_host_info()     - Returns a list of hostInfo objects.
  * get_host_load()     - Returns the current values for the resources of a host.

* Release 1.0.2

-  Fix a compliation error

* Release 1.0.3

-  Added 2 extra routines below :
    * lsb_fseek()
    * lsb_ftell()

* Release 1.0.4

- Fixed a bug for using lsf.lsb_readstream()
- Added a new example, readstream.py
    
## Community Contribution Guidelines

Community contributions to this branch must follow the IBM Developer's Certificate of Origin (DCO) process:

 1. Contributor proposes new code to community.

 2. Contributor signs off on contributions 
    (i.e. attachs the DCO to ensure contributor is either the code 
    originator or has rights to publish. The template of the DCO is included in
    this package).
 
 3. IBM Spectrum LSF development reviews contribution to check for:
    i)  Applicability and relevancy of functional content 
    ii) Any obvious issues

 4. If accepted, posts contribution. If rejected, work goes back to contributor and is not posted.


## Copyright

(C) Copyright IBM Corporation 2016-2017

U.S. Government Users Restricted Rights - Use, duplication or disclosure 
restricted by GSA ADP Schedule Contract with IBM Corp.

IBM(R), the IBM logo and ibm.com(R) are trademarks of International Business Machines Corp., 
registered in many jurisdictions worldwide. Other product and service names might be trademarks 
of IBM or other companies. A current list of IBM trademarks is available on the Web at 
"Copyright and trademark information" at www.ibm.com/legal/copytrade.shtml.
