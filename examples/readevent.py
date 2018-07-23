#! /usr/bin/env python

from pythonlsf import lsf
import sys


def display(eventrec):
    """
    display event record
    """
    if eventrec.type == lsf.EVENT_JOB_NEW:
        jobid = eventrec.eventLog.jobNewLog.jobId
        fromHost = eventrec.eventLog.jobNewLog.fromHost
        queue = eventrec.eventLog.jobNewLog.queue
        cwd = eventrec.eventLog.jobNewLog.cwd
        print("EVENT_JOB_NEW jobid<%d>, fromHost<%s>, to Queue<%s>, CWD<%s>" %(jobid, fromHost, queue, cwd))
    elif eventrec.type == lsf.EVENT_JOB_START:
        numHosts = eventrec.eventLog.jobStartLog.numExHosts
        execHosts = eventrec.eventLog.jobStartLog.execHosts
        hoststr = ""
        for i in range(0,numHosts):
            hoststr += lsf.stringArray_getitem(execHosts, i) + ""
        print("EVENT_JOB_START execHosts<%s>" %(hoststr))
    else:
        print("event type is %d" %(eventrec.type))

def read_eventrec(path):
    """
    read lsb.events
    """
    lineNum = lsf.new_intp()
    lsf.intp_assign(lineNum, 0)
    fp = lsf.fopen(path, "r")
    flag = 1

    if lsf.lsb_init("test") > 0:
        exit(1)

    while flag > 0:
        log = lsf.lsb_geteventrec(fp, lineNum)
        if log:
            display(log)
        else:
            flag = 0


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s full_path_lsb.events_file" % (sys.argv[0]))
        sys.exit(0)

    print("LSF Clustername is :", lsf.ls_getclustername())
    #read_eventrec("/opt/lsf8.0.1/work/cluster1/logdir/lsb.events")
    read_eventrec(sys.argv[1])
