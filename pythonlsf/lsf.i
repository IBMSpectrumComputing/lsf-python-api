/* 
* (C) Copyright IBM Corporation 2013
* 
* This library is free software; you can redistribute it and/or
* modify it under the terms of the Eclipse Public License.
* 
*/

/* File: lsf.i */
%module lsf
%include "cmalloc.i"
%include "cpointer.i"
%include "carrays.i"

#ifdef WIN32
%include <windows.i>
#endif

FILE *fopen(char *filename, char *mode);
int fclose(FILE *f);

%{
#define SWIG_FILE_WITH_INIT
//#define LSF_SIMULATOR
#include "lsf.h"
#include "lsbatch.h"
#include "lib.table.h"
%}

%pointer_functions(int, intp)
%pointer_functions(float, floatp)
%pointer_functions(long, longp)
%pointer_functions(LS_LONG_INT, LS_LONG_INT_POINTER)
%pointer_functions(limitInfoEnt *, limitInfoEntPtrPtr)
%pointer_functions(guaranteedResourcePoolEnt *, guaranteedResourcePoolEntPtrPtr)

%allocators(limitInfoEnt *, limitInfoEntPtrPtr);
%allocators(guaranteedResourcePoolEnt *, guaranteedResourcePoolEntPtrPtr);

%array_functions(int, intArray)
%array_functions(float, floatArray)
%array_functions(struct dependJobs, dependJobsArray)
%array_functions(long, longArray)
%array_functions(struct eventRec *, eventRecPtrArray)
%array_functions(limitInfoEnt, limitInfoEntArray)
%array_functions(struct appInfoEnt, appInfoEntArray)
%array_functions(struct shareAcctInfoEnt, shareAcctInfoEntArray)
#ifdef LSF_VERSION_101
%array_functions(struct gpuRusage, gpuRusageArray)
#endif
%array_functions(LS_LONG_INT, LS_LONG_INTArray)
%array_functions(guaranteedResourcePoolEnt, guaranteedResourcePoolEntArray)
%array_functions(struct rsvInfoEnt, rsvInfoEntArray)
%array_functions(struct hostRsvInfoEnt, hostRsvInfoEntArray)

//helper function for transforming char** to python list
%inline %{
PyObject * char_p_p_to_pylist(PyObject* ptrobj, int size){
      void* cptr = 0;
      int res = 0;
      PyObject * list = 0;
      int i = 0;
      res = SWIG_ConvertPtr(ptrobj, &cptr,SWIGTYPE_p_p_char, 0);
      if (!SWIG_IsOK(res)) {
        PyErr_SetString(PyExc_TypeError,"not a SWIGTYPE_p_p_char");
        return NULL;
      }
      list = PyList_New(size);
      for (i = 0; i < size; i++) {
          PyList_SetItem(list,i,PyString_FromString(((char**)cptr)[i]));
      }
      return list;
}

PyObject * string_array_to_pylist(PyObject* ptrobj, int size){
    return char_p_p_to_pylist(ptrobj,size);
}

/* For compatibility issue, the following 2 functions are added in LSF10.
   So they don't exist on LSF9.1.3 or earlier*/
#ifdef WIN32
    typedef __int64 LSF_LONG_INT;
    typedef unsigned __int64 LSF_UNS_LONG_INT;
    typedef __int64 uid_t;
    typedef __int64 gid_t;
    #define LSF_LONG_FORMAT "%I64d"
    #define LSF_UNS_LONG_FORMAT "%I64u"
#elif defined (__alpha)
    typedef long long int LSF_LONG_INT;
    typedef unsigned long long LSF_UNS_LONG_INT;
    #define LSF_LONG_FORMAT ("%ld")
    #define LSF_UNS_LONG_FORMAT ("%lu")
#else
    typedef long long int LSF_LONG_INT;
    typedef unsigned long long LSF_UNS_LONG_INT;
    #define LSF_LONG_FORMAT ("%lld")
    #define LSF_UNS_LONG_FORMAT ("%llu")
#endif /* WIN32 */

static hEnt * h_addEntByNumber_pythonapi(hTab *tabPtr, LSF_LONG_INT key, int *newPtr) {

    char skey[64]; /* The space is big enough. The length of 64bit uint is 20bits.*/

    sprintf(skey, LSF_UNS_LONG_FORMAT, key);

    return h_addEnt_(tabPtr, skey, newPtr);
}

static hEnt * h_getEntByNumber_pythonapi(hTab *tabPtr, LSF_LONG_INT key) {

    char skey[64]; /* The space is big enough. The length of 64bit uint is 20bits.*/

    sprintf(skey, LSF_UNS_LONG_FORMAT, key);

    return h_getEnt_(tabPtr, skey);
}

static struct hTab stringArraySize_htab;
static int stringArraySize_htab_init_flag;

static char ** new_stringArray(size_t nelements) {
    
    char ** ret = NULL;
    
    if ( !stringArraySize_htab_init_flag) {
        stringArraySize_htab_init_flag = 1;
        h_initTab_(&stringArraySize_htab, 1024);
    }

    ret = (char **)calloc(nelements, sizeof(char *));

    if ( ret) {
        hEnt * ent = h_addEntByNumber_pythonapi(&stringArraySize_htab, (LSF_LONG_INT)ret, NULL);

        ent->hData = (int *) malloc(sizeof(int));
        *ent->hData = nelements;
    }

    return ret;
}

static void delete_stringArray(char * *ary) {
    if( stringArraySize_htab_init_flag) {
        hEnt * ent = h_getEntByNumber_pythonapi(&stringArraySize_htab, (LSF_LONG_INT) ary);

        if (ent) {
            int i = 0, nelements = *ent->hData;
            for(; i<nelements; i++) {
                if (ary[i]) {
                    free(ary[i]);
                    ary[i] = NULL;
                }
            }
            h_delEnt_(&stringArraySize_htab, ent); 
        }
    }

    free((char*)ary);
}

static char * stringArray_getitem(char * *ary, size_t index) {
  return ary[index];
}
static void stringArray_setitem(char * *ary, size_t index, char * value) {
  ary[index] = strdup(value);
}

#if defined(FLAG_PYTHONAPI_KEYVALUE_T)
  static struct keyVal *new_keyValArray(size_t nelements) {
    return (struct keyVal *)malloc((nelements)*sizeof(struct keyVal));
  }

  static void delete_keyValArray(struct keyVal *ary) {
    free((char*)ary);
  }

  static struct keyVal keyValArray_getitem(struct keyVal *ary, size_t index) {
    return ary[index];
  }
  static void keyValArray_setitem(struct keyVal *ary, size_t index, struct keyVal value) {
    ary[index] = value;
  }
#endif

%}

%array_class(struct queueInfoEnt, queueInfoEntArray);
%array_class(struct hostInfoEnt, hostInfoEntArray);
%array_class(struct hostLoad, hostLoadArray);
%array_class(struct _limitItem, limitItemArray)
%array_class(struct _limitConsumer, limitConsumerArray)
%array_class(struct _limitResource, limitResourceArray)

// handle int arrays
%typemap(in) int [ANY] (int temp[$1_dim0]) {
  int i;
  for (i = 0; i < $1_dim0; i++) {
    PyObject *o = PySequence_GetItem($input,i);
      temp[i] = (int) PyInt_AsLong(o);
  }
  $1 = temp;
}

// See github issue 1
//%typemap(freearg) int [ANY] {
//  free((int *) $1);
//}

%typemap(out) int [ANY] {
  int i;
  $result = PyList_New($1_dim0);
  for (i = 0; i < $1_dim0; i++) {
    PyObject *o = PyLong_FromDouble((int) $1[i]);
    PyList_SetItem($result,i,o);
  }
}

// typemap for time_t
%typemap(in) time_t {
    $1 = (time_t) PyLong_AsLong($input);
}

%typemap(freearg) time_t {
    if ($1) free((time_t *) $1);
}

%typemap(out) time_t {
    $result = PyLong_FromLong((long)$1);
}

%typemap(arginit) time_t {
   $1 = 0;
}

/* 
 The following routines are not wrapped because SWIG has issues generating 
 proper code for them 
 */

// Following are ignored from lsf.h

%ignore getBEtime;
%ignore ls_gethostrespriority;
%ignore ls_loadoftype;
%ignore ls_lostconnection;
%ignore ls_nioclose;
%ignore ls_nioctl;
%ignore ls_niodump;
%ignore ls_nioinit;
%ignore ls_niokill;
%ignore ls_nionewtask;
%ignore ls_nioread;
%ignore ls_nioremovetask;
%ignore ls_nioselect;
%ignore ls_niosetdebug;
%ignore ls_niostatus;
%ignore ls_niotasks;
%ignore ls_niowrite;
%ignore ls_placeoftype;
%ignore ls_readrexlog;
%ignore ls_verrlog;
%ignore lsb_globalpolicy;
%ignore lsb_jobidindex2str;
%ignore LOG_VERSION;
%ignore ls_errmsg;
%ignore lsf_suite_edition;

// Following are ignored from lsbatch.h

%ignore lsb_readstatusline;
%ignore lsb_rc_hostinfo;
%ignore lsb_rc_free_hostinfo;
%ignore getHostGpuNvlinkInfoFromStr;
%ignore fairshare_adjustment;
%ignore FairAdjustPairArrayName;
%ignore lsb_switch;
%ignore lsb_liveconfigPack;

// Now include the rest...

%include "lsf.h"
%include "lsbatch.h"

%inline %{
PyObject * get_host_names() {
    struct hostInfo *hostinfo; 
    char   *resreq; 
    int    numhosts = 0; 
    int    options = 0; 
    
    resreq="";

    hostinfo = ls_gethostinfo(resreq, &numhosts, NULL, 0, options);      
    
    PyObject *result = PyList_New(numhosts);
    int i;
    for (i = 0; i < numhosts; i++) { 
        PyObject *o = PyString_FromString(hostinfo[i].hostName);
        PyList_SetItem(result,i,o);
    }
    
    return result;
}

PyObject * get_host_info() {
    struct hostInfo *hostinfo; 
    char   *resreq; 
    int    numhosts = 0; 
    int    options = 0; 
    
    resreq = "";

    hostinfo = ls_gethostinfo(resreq, &numhosts, NULL, 0, options);     
         
    PyObject *result = PyList_New(numhosts);
    int i;
    for (i = 0; i < numhosts; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&hostinfo[i]), 
                                         SWIGTYPE_p_hostInfo, 0 |  0 );
        PyList_SetItem(result,i,o);
    }
    
    return result;
}    

/* taken form stdio.h */
#define SEEK_SET    0   /* Seek from beginning of file.  */
#define SEEK_CUR    1   /* Seek from current position.  */
#define SEEK_END    2   /* Seek from end of file.  */
PyObject * lsb_fseek(PyObject *obj0, PyObject *obj1, PyObject *obj2){
  FILE *arg1 = (FILE *) 0 ;
  void *argp1 = 0 ;
  long val2 = 0 ;
  int val3 = 0 ;
  int res1 = 0 ;
  int res2 = 0 ;
  int res3 = 0 ;
  PyObject *resultobj = 0;
  int result;

  res1 = SWIG_ConvertPtr(obj0, &argp1,SWIGTYPE_p_FILE, 0 |  0 );
  if (!SWIG_IsOK(res1)) {
    SWIG_exception_fail(SWIG_ArgError(res1), "in method '" "fseek" "', argument " "1"" of type '" "FILE *""'");
  }
  arg1 = (FILE *)(argp1);

  res2 = SWIG_AsVal_long(obj1, &val2 );
  if (!SWIG_IsOK(res2)) {
    SWIG_exception_fail(SWIG_ArgError(res2), "in method '" "fseek" "', argument " "2"" of type '" "long *""'");
  }

  res3 = SWIG_AsVal_int(obj2, &val3 );
  if (!SWIG_IsOK(res3)) {
    SWIG_exception_fail(SWIG_ArgError(res3), "in method '" "fseek" "', argument " "3"" of type '" "int *""'");
  }

  result = (int)fseek(arg1,val2,val3);
  resultobj = SWIG_From_int((int)(result));
  return resultobj;
fail:
  return NULL;
}

PyObject * lsb_ftell(PyObject *obj0){
  FILE *arg1 = (FILE *) 0 ;
  void *argp1 = 0 ;
  int res1 = 0 ;
  PyObject *resultobj = 0;
  long result;

  res1 = SWIG_ConvertPtr(obj0, &argp1,SWIGTYPE_p_FILE, 0 |  0 );
  if (!SWIG_IsOK(res1)) {
    SWIG_exception_fail(SWIG_ArgError(res1), "in method '" "fseek" "', argument " "1"" of type '" "FILE *""'");
  }
  arg1 = (FILE *)(argp1);

  result = (long)ftell(arg1);
  resultobj = SWIG_From_long((long)(result));
  return resultobj;
fail:
  return NULL;
}

PyObject * get_load_of_hosts() {
    struct hostLoad *hostload; 
    char   *resreq; 
    int    numhosts = 0; 
    
    resreq = "";

    hostload = ls_loadofhosts(resreq, &numhosts, 0, NULL, NULL, 0);
         
    PyObject *result = PyList_New(numhosts);
    int i;
    for (i = 0; i < numhosts; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&hostload[i]),
                                         SWIGTYPE_p_hostLoad, 0 |  0 );
        PyList_SetItem(result,i,o);
    }
    
    return result;
}

PyObject * get_host_load(char *resreq, int index) {
    struct hostLoad *hosts; 

    int    numhosts = 0; 

    int    options = 0; 

    char   *fromhost = NULL; 

    hosts = ls_load(resreq, &numhosts, options, fromhost); 

    if (hosts == NULL || numhosts > 1) { 
        ls_perror("ls_load"); 
        exit(-1); 
    }

    PyObject *result = PyFloat_FromDouble(hosts[0].li[index]);
    return result;
}

PyObject * get_host_load_from_batch (
                               char * resreq, 
                                int   index) {

                   int   numhosts = 0; 
    struct hostInfoEnt * hinfo    = NULL;

    hinfo = lsb_hostinfo_ex (NULL, &numhosts, resreq, 0);
    if (hinfo == NULL || numhosts > 1) { 
        lsb_perror("lsb_hostinfo_ex"); 
        exit(-1); 
    }

    PyObject *result = PyFloat_FromDouble(hinfo[0].load[index]);
    return result;
}


PyObject * ls_load_py(char *resreq, int *numhosts, int options, char *fromhost) {

    struct hostLoad * hosts = NULL; 
    int i = 0, j = 0;

    hosts = ls_load(resreq, numhosts, options, fromhost); 

    if (hosts == NULL) { 
        ls_perror("ls_load_py"); 
        exit(-1); 
    }

    /* Python3 can not handle dirty string.*/
    for (i = 0; i < *numhosts; i++) {
        int size_string = sizeof(hosts[i].hostName);
        int len_string  = strlen(hosts[i].hostName);
        for ( j = len_string; j < size_string; j++) hosts[i].hostName[j] = 0;
    }

    PyObject * result = PyList_New(*numhosts);
    for (i = 0; i < *numhosts; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&hosts[i]),
                                         SWIGTYPE_p_hostLoad, 0 |  0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}

PyObject * ls_info_py() {
    struct resItem * allRes = NULL;
    struct lsInfo * allInfo = NULL;
    char *type = NULL;
    char *model = NULL;
    char *arch = NULL;
    
    int i = 0, j = 0;

    allInfo = ls_info();
    if (allInfo == NULL) {
        ls_perror("ls_info_py");
        exit(-1);
    }

    PyObject * result = PyDict_New();
    PyObject * nRes = Py_BuildValue("i",allInfo->nRes);
    PyDict_SetItemString(result, "nRes",nRes);
    PyObject * nTypes = Py_BuildValue("i", allInfo->nTypes);
    PyDict_SetItemString(result, "nTypes", nTypes);
    PyObject * nModels = Py_BuildValue("i", allInfo->nModels);
    PyDict_SetItemString(result, "nModels", nModels);
    PyObject * numIndx = Py_BuildValue("i", allInfo->numIndx);
    PyDict_SetItemString(result, "numIndx", numIndx);
    PyObject * numUsrIndx = Py_BuildValue("i", allInfo->numUsrIndx);
    PyDict_SetItemString(result, "numUsrIndx", numUsrIndx);

    allRes = allInfo->resTable;
    for (i = 0; i < allInfo->nRes; i++) {
        int size_string = sizeof(allRes[i].name);
        int len_string = strlen(allRes[i].name);
        for (j = len_string; j < size_string; j++) {
            allRes[i].name[j] = 0;
        }
        size_string = sizeof(allRes[i].des);
        len_string = strlen(allRes[i].des);
        for (j = len_string; j < size_string; j++) {
            allRes[i].des[j] = 0;
        }
    }
    
    PyObject * resRst = PyList_New(allInfo->nRes);
    for (i = 0; i < allInfo->nRes; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&allRes[i]),
                                      SWIGTYPE_p_resItem, 0 | 0);
        PyList_SetItem(resRst,i,o);
    }
    PyDict_SetItemString(result, "resTable", resRst);

    PyObject * typeRst = PyList_New(allInfo->nTypes);
    for (i = 0; i < allInfo->nTypes; i++) {
        type = strdup(allInfo->hostTypes[i]);
        int size_string = sizeof(type);
        int len_string = strlen(type);
        for (j = len_string; j < size_string; j++) {
            type[j] = 0;
        }
        PyObject * pyType = Py_BuildValue("s",type);
        PyList_SetItem(typeRst,i,pyType);
        if (type != NULL) {
            free(type);
        }
    }
    PyDict_SetItemString(result, "hostTypes", typeRst);

    PyObject * modelRst = PyList_New(allInfo->nModels);
    PyObject * archRst = PyList_New(allInfo->nModels);
    PyObject * refRst = PyList_New(allInfo->nModels);
    PyObject * factorRst = PyList_New(allInfo->nModels);

    for (i = 0; i < allInfo->nModels; i++) {
        model = strdup(allInfo->hostModels[i]);
        int size_string = sizeof(model);
        int len_string = strlen(model);
        for (j = len_string; j < size_string; j++) {
            model[j] = 0;
        }
        PyObject *pyModel = Py_BuildValue("s",model);
        PyList_SetItem(modelRst,i,pyModel);

        arch = strdup(allInfo->hostArchs[i]);
        size_string = sizeof(arch);
        len_string = strlen(arch);
        for (j = len_string; j < size_string; j++) {
            arch[j] = 0;
        }
        PyObject *pyArch = Py_BuildValue("s",arch);
        PyList_SetItem(archRst,i,pyArch);

        PyObject *pyRef = Py_BuildValue("i",allInfo->modelRefs[i]);
        PyList_SetItem(refRst,i,pyRef);

        PyObject *pyFactor = Py_BuildValue("f",allInfo->cpuFactor[i]);
        PyList_SetItem(factorRst,i,pyFactor);
    }
    
    PyDict_SetItemString(result,"hostModels",modelRst);
    PyDict_SetItemString(result,"hostArchs",archRst);
    PyDict_SetItemString(result,"modelRefs",refRst);
    PyDict_SetItemString(result,"cpuFactor",factorRst);
    
    return result;
}

      
PyObject * get_queue_info_by_name(char** name, int num) {
    struct queueInfoEnt* queueinfo;
    int    numqueues = num;
    int    options = 0;

    queueinfo = lsb_queueinfo(name, &numqueues, NULL, 0, options);

    PyObject *result = PyList_New(numqueues);
    int i;
    for (i = 0; i < numqueues; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&queueinfo[i]),
                                         SWIGTYPE_p_queueInfoEnt, 0 |  0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}

PyObject * get_hostgroup_info_by_name(char** name, int num) {
    struct groupInfoEnt* hostgroupinfo;
    int    numgroups = num;
    int    options = 0;

    hostgroupinfo = lsb_hostgrpinfo(name, &numgroups, options);

    PyObject *result = PyList_New(numgroups);
    int i;
    for (i = 0; i < numgroups; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&hostgroupinfo[i]),
                                         SWIGTYPE_p_groupInfoEnt, 0 |  0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}

PyObject * get_conf_value(char *name, char *path) {
    struct config_param param[2];
    param[0].paramName = name;
    param[0].paramValue = NULL;
    param[1].paramName = NULL;
    param[1].paramValue = NULL;
    if (ls_readconfenv(&param[0],path) == 0) {
        return Py_BuildValue("s", param[0].paramValue);
    } else {
        Py_RETURN_NONE;
    }
}

PyObject * get_app_info_all() {
    struct appInfoEnt* appinfo;
    int    numapps = 0;

    appinfo = lsb_appInfo(&numapps);

    PyObject *result = PyList_New(numapps);
    int i;
    for (i = 0; i < numapps; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&appinfo[i]),
                                         SWIGTYPE_p_appInfoEnt, 0 |  0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}

PyObject * get_user_info_all() {
    struct userInfoEnt* userinfo;
    int    numusers = 0;

    userinfo = lsb_userinfo(NULL,&numusers);

    PyObject *result = PyList_New(numusers);
    int i;
    for (i = 0; i < numusers; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&userinfo[i]),
                                         SWIGTYPE_p_userInfoEnt, 0 |  0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}

PyObject * get_usergroup_info_all() {
    struct groupInfoEnt* groupinfo;
    int    numgrps = 0;

    groupinfo = lsb_usergrpinfo(NULL,&numgrps,GRP_ALL);

    PyObject *result = PyList_New(numgrps);
    int i;
    for (i = 0; i < numgrps; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&groupinfo[i]),
                                         SWIGTYPE_p_groupInfoEnt, 0 |  0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}

PyObject * get_queue_info_all() {
    struct queueInfoEnt *queueinfo;
    char **queues = NULL;
    int numqueues = 0;
    int options = 0;

    // Return queries as C queueInfoEnt*
    queueinfo = lsb_queueinfo(queues, &numqueues, NULL, 0, options);

    PyObject *result = PyList_New(numqueues);     // Create PyObject * to get C returns
    int i;
    for (i = 0; i < numqueues; i++) {             // Save queries in a loop to result
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&queueinfo[i]),
                                         SWIGTYPE_p_queueInfoEnt, 0 | 0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}

int get_lsb_errno() {
    return lsberrno;
}

char * get_lsb_sysmsg() {
    return lsb_sysmsg();
}

PyObject * get_pids_from_stream(struct jRusage * jrusage) {
    struct pidInfo *pidInfo;
    pidInfo = jrusage->pidInfo;
    int i = 0;
    PyObject *result = PyList_New(jrusage->npids);
    for (i = 0; i < jrusage->npids; i++) {
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&pidInfo[i]),
                                         SWIGTYPE_p_pidInfo, 0 | 0 );
        PyList_SetItem(result, i, o);
    }
    return result;
}

PyObject * get_host_info_all() {
    struct hostInfoEnt *hostinfo;
    char **hosts = NULL;
    int numhosts = 0;

    // Return queries as C hostInfoEnt*
    hostinfo = lsb_hostinfo(hosts, &numhosts);

    PyObject *result = PyList_New(numhosts);     // Create PyObject * to get C returns
    int i;
    for (i = 0; i < numhosts; i++) {             // Save queries in a loop to result
        PyObject *o = SWIG_NewPointerObj(SWIG_as_voidptr(&hostinfo[i]),
                                         SWIGTYPE_p_hostInfoEnt, 0 | 0 );
        PyList_SetItem(result,i,o);
    }

    return result;
}
      
%}
