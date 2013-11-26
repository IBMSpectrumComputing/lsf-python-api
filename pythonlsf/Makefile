# 
# (C) Copyright IBM Corporation 2013
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the Eclipse Public License.
# 

CC = gcc
#LSF_LIBDIR = /opt/platform/lsf/8.0/x86-64-sol10/lib
PYTHON_INCLUDE = /usr/include/python2.4
LSF_INCLUDE = $(LSF_LIBDIR)/../../include/lsf/

PROJECT = _lsf.so
OBJECTS = lsf_wrap.o

CFLAGS  = -m64 -fPIC -I$(PYTHON_INCLUDE) -I$(LSF_INCLUDE)
LDFLAGS = $(LSF_LIBDIR)/liblsf.a $(LSF_LIBDIR)/libbat.a $(LSF_LIBDIR)/libfairshareadjust.so $(LSF_LIBDIR)/liblsbstream.so -lc -lnsl

all: $(PROJECT)

.c.o:
	$(CC) $(CFLAGS) -c $<

$(PROJECT): swig $(OBJECTS)
	ld -shared $(OBJECTS) -o $(PROJECT) $(LDFLAGS)

swig:
	swig -python -I$(LSF_INCLUDE) lsf.i

clean:
	rm -rf _lsf.so lsf.py lsf.pyc lsf_wrap.c lsf_wrap.o
