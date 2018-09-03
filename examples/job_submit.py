from pythonlsf import lsf


def run_job(command):
    """
    Run a job...
    """
    submitreq = lsf.submit()
    submitreq.command = command
    submitreq.options = 0
    submitreq.options2 = 0

    limits = []
    for i in range(0, lsf.LSF_RLIM_NLIMITS):
        limits.append(lsf.DEFAULT_RLIMIT)

    submitreq.rLimits = limits
 
    submitreq.beginTime = 0
    submitreq.termTime = 0
    submitreq.numProcessors = 1
    submitreq.maxNumProcessors = 1

    submitreply = lsf.submitReply()

    if lsf.lsb_init("test") > 0:
        exit(1)

    job_id = lsf.lsb_submit(submitreq, submitreply)
    return job_id


if __name__ == '__main__':
    print("LSF Clustername is :", lsf.ls_getclustername())
    print(run_job("/bin/sleep 10"))
