from pythonlsf import lsf

def sub_pack_job():


    limits1 = []
    for i in range(0, lsf.LSF_RLIM_NLIMITS):
        limits1.append(lsf.DEFAULT_RLIMIT)

    submitreq1 = lsf.submit()
    submitreq1.command = "sleep 10"
    submitreq1.options = 0
    submitreq1.options2 = 0
    submitreq1.rLimits = limits1

    limits2 = []
    for i in range(0, lsf.LSF_RLIM_NLIMITS):
        limits2.append(lsf.DEFAULT_RLIMIT)

    submitreq2 = lsf.submit()
    submitreq2.command = "sleep 20"
    submitreq2.options = 0
    submitreq2.options2 = 0
    submitreq2.rLimits = limits2


    pack_submitreq = lsf.packSubmit()
    pack_submitreq.num = 2
    submits = lsf.new_submitArray(2)
    lsf.submitArray_setitem(submits, 0, submitreq1)
    lsf.submitArray_setitem(submits, 1, submitreq2)
    pack_submitreq.reqs = submits

    pack_submitreply = lsf.packSubmitReply()
    intp_acceptedNum = lsf.copy_intp(0)
    intp_rejectedNum = lsf.copy_intp(0)


    if lsf.lsb_init("test") > 0:
        exit(1)

    result = lsf.lsb_submitPack(pack_submitreq, pack_submitreply, intp_acceptedNum, intp_rejectedNum)
    print(result)
    print(lsf.intp_value(intp_acceptedNum))
    print(lsf.intp_value(intp_rejectedNum))

    return result

if __name__ == '__main__':
    print("LSF Clustername is :", lsf.ls_getclustername())
    sub_pack_job()
