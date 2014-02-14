/* 
* (C) Copyright IBM Corporation 2013
* 
* This library is free software; you can redistribute it and/or
* modify it under the terms of the Eclipse Public License.
* 
*/

/* File: lsf.i */
%module lsf
%include "cpointer.i"
%include "carrays.i"

FILE *fopen(char *filename, char *mode);
int fclose(FILE *f);

%{
#define SWIG_FILE_WITH_INIT
#include "lsf.h"
#include "lsbatch.h"
%}

%pointer_functions(int, intp)
%pointer_functions(float, floatp)

//helper function for conversion between char ** and python list
%inline %{
PyObject * char_p_p_from_pylist(PyObject* list){
  PyObject * result = 0;
  char ** ptr = 0;
  if (list == Py_None) {
    return NULL;
  } else if (PyList_Check(list)) {
    int size = PyList_Size(list);
    int i = 0;
    ptr = (char **) calloc(size, sizeof(char *));
    for(i = 0; i < size; i++) {
      PyObject *item = PyList_GetItem(list,i);
      if (PyString_Check(item)){
        char* str = PyString_AsString(item);
        char* newstr = strdup(str);
        ptr[i] = newstr;
      }else {
        PyErr_SetString(PyExc_TypeError,"list must contain strings");
        int j = 0;
        for(j = 0; j < i-1; j++){
            if(ptr[j])
                free(ptr[j]);
        }
        free(ptr);
        return NULL;
      }
    }
    result = SWIG_NewPointerObj(SWIG_as_voidptr(ptr), SWIGTYPE_p_p_char, 0);
    return result;
  } else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}
PyObject * char_p_p_to_pylist(PyObject* ptrobj, int size){
      void* cptr = 0;
      int res = 0;
      PyObject * list = 0;
      int i = 0;
      res = SWIG_ConvertPtr(ptrobj, &cptr,SWIGTYPE_p_p_char, 0 |  0 );
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
void char_p_p_free(PyObject* ptrobj, int size){
    void* cptr = 0;
    int res = 0;
    int i = 0;
    res = SWIG_ConvertPtr(ptrobj, &cptr,SWIGTYPE_p_p_char, 0 |  0 );
    if (!SWIG_IsOK(res)) {
    PyErr_SetString(PyExc_TypeError,"not a SWIGTYPE_p_p_char"); 
    return ;
    }
    for (i = 0; i < size; i++) {
      if(((char**)cptr)[i])
          free(((char**)cptr)[i]);
    }
    free(cptr);
}
%}

%array_class(struct queueInfoEnt, queueInfoEntArray);
%array_class(struct hostInfoEnt, hostInfoEntArray);

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
    free((time_t *) $1);
}

%typemap(out) time_t {
    $result = PyLong_FromLong((long)$1);
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

// Following are ignored from lsbatch.h

%ignore lsb_readstatusline;

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

PyObject * get_load_of_hosts() {
    struct hostLoad *hostload; 
    char   *resreq; 
    int    numhosts = 0; 
    int    options = 0; 
    
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
%}
