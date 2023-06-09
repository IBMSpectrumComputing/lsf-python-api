from pythonlsf import lsf


def run_job(command):
    """
    Run a job...
    """
    submitreq = lsf.submit()
    submitreq.command = command
    #submitreq.options = 0
    submitreq.options2 = 0

    limits = []
    for i in range(0, lsf.LSF_RLIM_NLIMITS):
        limits.append(lsf.DEFAULT_RLIMIT)

    submitreq.rLimits = limits
 
    submitreq.beginTime = 0
    submitreq.termTime = 0
    submitreq.numProcessors = 1
    submitreq.maxNumProcessors = 1

    # below 2 lines section is for using -R rusage to request GPU
    #submitreq.resReq = "rusage[ngpus_physical=2:gmodel=K80#12G:nvlink=yes]"
    #submitreq.options = lsf.SUB_RES_REQ

    # below section is for using -gpu to request GPU
    submit_ext = lsf.submit_ext()
    submitreq.options2 = lsf.SUB2_MODIFY_PEND_JOB
    submitreq.options4 = lsf.SUB4_GPU_REQ 
    gpuOpt = {}
    gpuOpt[lsf.JDATA_EXT_GPU_NUM] = "2"
    gpuOpt[lsf.JDATA_EXT_GPU_MODE] = "3"
    #gpuOpt[lsf.JDATA_EXT_GPU_MPS_ENABLE] = "-1"
    #gpuOpt[lsf.JDATA_EXT_GPU_JOB_EXCLUSIVE] = "-1"
    #gpuOpt[lsf.JDATA_EXT_GPU_MODEL] = ""
    #gpuOpt[lsf.JDATA_EXT_GPU_MEM] = ""
    #gpuOpt[lsf.JDATA_EXT_GPU_TILE] = ""
    #gpuOpt[lsf.JDATA_EXT_GPU_AFFBIND] = "-1"
    #gpuOpt[lsf.JDATA_EXT_GPU_BLOCK] = "-1"
    #gpuOpt[lsf.JDATA_EXT_GPU_GPACK] = "-1"
    #gpuOpt[lsf.JDATA_EXT_GPU_GVENDOR] = "-1"
    #gpuOpt[lsf.JDATA_EXT_GPU_RSRC_TYPE] = "0"
    #gpuOpt[lsf.JDATA_EXT_GPU_GI_SLICE] = "-1"
    #gpuOpt[lsf.JDATA_EXT_GPU_CI_SLICE] = "-1"

    submit_ext.keys = lsf.new_intArray(len(gpuOpt))
    submit_ext.values = lsf.new_stringArray(len(gpuOpt))
    for i, (key, value) in enumerate(gpuOpt.items()):
        lsf.intArray_setitem(submit_ext.keys, i, key)
        lsf.stringArray_setitem(submit_ext.values, i, value)
    submit_ext.num = len(gpuOpt)
    submitreq.submitExt = submit_ext
    print(submitreq.submitExt.num)

    # submit the job request
    submitreply = lsf.submitReply()

    if lsf.lsb_init("test") > 0:
        exit(1)

    job_id = lsf.lsb_submit(submitreq, submitreply)
    return job_id


if __name__ == '__main__':
    print("LSF Clustername is :", lsf.ls_getclustername())
    print(run_job("/bin/sleep 10"))
