#! /usr/bin/env python
from pythonlsf import lsf

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
    read lsb.streams
    """
    s = lsf.lsbStream()
    s.streamFile = path;
    s.maxStreamSize = 1024*1024*1024
    s.maxStreamFileNum = 10;

    lsf.lsb_openstream(s)

    lineNum = lsf.new_intp()
    lsf.intp_assign(lineNum, 0)
    flag = 1

    if lsf.lsb_init("test") > 0:
        exit(1)

    while flag > 0:
        log = lsf.lsb_readstream(lineNum)
        if log:
            display(log)
        else:
            flag = 0


if __name__ == '__main__':
    print("LSF Clustername is :", lsf.ls_getclustername())
    read_eventrec("/home/youname/lsf_top/work/yourcluster/logdir/stream/lsb.stream")
