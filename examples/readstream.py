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
    elif eventrec.type == lsf.EVENT_JOB_FORCE:
        username = eventrec.eventLog.jobForceRequestLog.userName
        jobid = eventrec.eventLog.jobForceRequestLog.jobId
        numhosts = eventrec.eventLog.jobForceRequestLog.numExecHosts
        exechosts = eventrec.eventLog.jobForceRequestLog.execHosts
        hoststr = ""
        for i in range(0,numhosts):
            hoststr += lsf.stringArray_getitem(exechosts, i) + ""
        print("EVENT_JOB_FORCE jobid<%d>, execHost<%s>, username<%s>" %(jobid, hoststr, username))

    else:
        print("event type is %d" %(eventrec.type))

def read_eventrec(path):
    """
    read lsb.streams
    """

    if lsf.lsb_init("test") > 0:
        exit(1)

    s = lsf.lsbStream()
    s.streamFile = path;
    s.maxStreamSize = 1024*1024*1024
    s.maxStreamFileNum = 10;

    cc = lsf.lsb_openstream(s)
    if cc < 0 :
        print("Cannot open the file %s. Ensure you are the file owner." % (path))
        exit(1);

    lineNum = lsf.new_intp()
    lsf.intp_assign(lineNum, 0)
    flag = 1

    while flag > 0:
        log = lsf.lsb_readstream(lineNum)
        if log:
            display(log)
        else:
            flag = 0

def read_streamline(path):
    """
    Use lsb_readstreamline() to parse the file
    """

    if lsf.lsb_init("test") > 0:
        exit(1)

    file = open(path)
 
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            log = lsf.lsb_readstreamline(line)
            if log:
                display(log)
            else:
                break

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: %s full_path_lsb.stream_file" % (sys.argv[0]))
        sys.exit(0)

    print("LSF Clustername is :", lsf.ls_getclustername())
#    read_eventrec("/home/youname/lsf_top/work/yourcluster/logdir/stream/lsb.stream")
#    read_streamline("/home/youname/lsf_top/work/yourcluster/logdir/stream/lsb.stream")
    #read_streamline(sys.argv[1])
    read_eventrec(sys.argv[1])
