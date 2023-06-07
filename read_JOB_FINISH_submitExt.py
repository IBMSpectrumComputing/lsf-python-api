#!/usr/bin/env python3

from pythonlsf import lsf
import sys

# Define function to get key and pair values from the eventrec.eventLog.jobFinishLog.submitExt
def get_pair_from_submit_ext(submit_ext, id):
    if submit_ext is None:
        return None


    values_as_list = lsf.string_array_to_pylist(submit_ext.values, submit_ext.num)
    for i in range(submit_ext.num):
        key = lsf.intArray_getitem(submit_ext.keys, i)
        if key  == id:
            return values_as_list[i]

    return None


def display(eventrec):
    """
    display event record, this example to get the user group (-G) value from the JOB_FINISH record
    """
    if eventrec.type == lsf.EVENT_JOB_FINISH:
        jobid = eventrec.eventLog.jobFinishLog.jobId
        fromHost = eventrec.eventLog.jobFinishLog.fromHost
        submit_ext=eventrec.eventLog.jobFinishLog.submitExt
        userGroup = get_pair_from_submit_ext(submit_ext,lsf.JDATA_EXT_USRGROUP)
#        jobgroup = eventrec.eventLog.jobFinishLog.jgroup
#        jobgroup = eventrec.eventLog.jobFinishLog.submitExt.values[1075]
        print("EVENT_JOB_FINISH jobid<%d>, fromHost<%s>, to jobgroup <%s>" %(jobid, fromHost, userGroup))
    else:
        print("event type is %d" %(eventrec.type))

def read_eventrec(path):
    """
    read lsb.events
    """
    lineNum = lsf.new_intp()
    lsf.intp_assign(lineNum, 0)
    fp = lsf.fopen(path, "r")
    if fp is None:
        print("The file %s does not exist." % path)
        sys.exit(1)

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
