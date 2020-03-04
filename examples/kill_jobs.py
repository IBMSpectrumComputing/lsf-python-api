from pythonlsf import lsf
import sys


def kill_jobs():
    """
    Kill multiple jobs...
    """
    signalbulkjobs = lsf.signalBulkJobs()
    signalbulkjobs.signal = 9
    signalbulkjobs.njobs = 3 
    signalbulkjobs.jobs = lsf.new_LS_LONG_INTArray(3)
    lsf.LS_LONG_INTArray_setitem(signalbulkjobs.jobs, 0, 1797)
    lsf.LS_LONG_INTArray_setitem(signalbulkjobs.jobs, 1, 1798)
    lsf.LS_LONG_INTArray_setitem(signalbulkjobs.jobs, 2, 1799)
    #signalbulkjobs.flags = 0
    #signalbulkjobs.numkvs = 0
    #signalbulkjobs.kvs = None

    if lsf.lsb_init("test") > 0:
        exit(1)

    
    result = lsf.lsb_killbulkjobs(signalbulkjobs)
    return result


if __name__ == '__main__':
    print("LSF Clustername is :", lsf.ls_getclustername())

    print(kill_jobs())
