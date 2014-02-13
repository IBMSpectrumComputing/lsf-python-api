#!/usr/local/bin/python2.7

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
        execHostList = lsf.char_p_p_to_pylist(execHosts, numHosts)
        hoststr = ""
        for host in execHostList:
            hoststr += host + " "
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
    print("LSF Clustername is :", lsf.ls_getclustername())
    read_eventrec("/opt/lsf8.0.1/work/cluster1/logdir/lsb.events")
