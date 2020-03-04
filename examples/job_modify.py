from pythonlsf import lsf
import sys


def modify_job(job_id):
    """
    Modify a job...
    """
    submitreq = lsf.submit()
    submitreq.command = str(job_id);
    submitreq.options = 0
    submitreq.resReq = "rusage[mem=3500]"
    submitreq.options |= lsf.SUB_MODIFY
    submitreq.options |= lsf.SUB_RES_REQ
    submitreq.options2 = 0
    submitreq.options3 = 0
    submitreq.options4 = 0

    limits = []
    for _ in range(0, lsf.LSF_RLIM_NLIMITS):
        limits.append(lsf.DEFAULT_RLIMIT)
    submitreq.rLimits = limits

    submitreply = lsf.submitReply()

    if lsf.lsb_init("test") > 0:
        exit(1)

    
    job_id = lsf.lsb_modify(submitreq, submitreply, -1)
    return job_id


if __name__ == '__main__':
    print("LSF Clustername is :", lsf.ls_getclustername())
    job_id = int(sys.argv[1])
    print("job_id = ", str(job_id))
    print(modify_job(job_id))
