from pythonlsf import lsf
import sys

def showJobStat(stat) :
    if stat == "" or stat == lsf.JOB_STAT_NULL :
        return "NULL"
    elif stat == lsf.JOB_STAT_PEND :
        return "PEND"
    elif stat == lsf.JOB_STAT_PSUSP :
        return "PSUSP"
    elif stat == lsf.JOB_STAT_RUN :
        return "RUN"
    elif stat == lsf.JOB_STAT_SSUSP :
        return "SSUSP"
    elif stat == lsf.JOB_STAT_USUSP :
        return "USUSP"
    elif stat == lsf.JOB_STAT_EXIT :
        return "EXIT"
    elif stat == lsf.JOB_STAT_DONE or stat == (lsf.JOB_STAT_DONE + lsf.JOB_STAT_PDONE) or \
stat == (lsf.JOB_STAT_DONE + lsf.JOB_STAT_PERR) :
        return "DONE"
    elif stat == lsf.JOB_STAT_UNKWN :
        return "UNKWN"
    elif stat == (lsf.JOB_STAT_RUN + lsf.JOB_STAT_PROV) :
        return "PROV"
    else :
        return "ERROR"


def get_job_info(list) :
    if lsf.lsb_init("test") > 0:
        print("failed to initialize")
        return
    if len(list) > 0 :
        print("request below job's info: {}".format(list))
    else :
        print("request all job's info")
    clusterName = lsf.ls_getclustername()
    print("retrieve cluster name : {}".format(clusterName))
    reasonLevel = 3
    more = lsf.new_intp()
    jobInfoPtr = lsf.jobInfoHeadExt()
    req = lsf.jobInfoReq()
    req.reasonLevel = reasonLevel
    req.sourceClusterName = clusterName
    req.userName = "all"
    req.options = lsf.ALL_JOB
    if len(list) > 1 :
        req.jobId = 0
        jobList = ""
        cluList = ""
        for j in range(len(list)):
            jobList += list[j] + ","
            cluList += clusterName + ","
        req.submitExt = lsf.submit_ext()
        submitDict = {}
        submitDict[lsf.JDATA_EXT_JOBIDS] = jobList
        submitDict[lsf.JDATA_EXT_SOURCECLUSTERS] = cluList
        submitDict[lsf.JDATA_EXT_AFFINITYINFO] = ""
        submitDict[lsf.JDATA_EXT_DATAINFO] = ""
        submitDict[lsf.JDATA_EXT_EST_RESULTS] = ""
        submitDict[lsf.JDATA_EXT_APS_DETAIL] = ""
        req.submitExt.keys = lsf.new_intArray(6)
        req.submitExt.values = lsf.new_stringArray(6)
        for p, (key, value) in enumerate(submitDict.items()):
            lsf.intArray_setitem(req.submitExt.keys, p, key)
            lsf.stringArray_setitem(req.submitExt.values, p, value)
        req.submitExt.num = 6
    elif len(list) == 1 :
        req.jobId = int(list[0])
    else :
        req.jobId = 0
    jobInfoPtr = lsf.lsb_openjobinfo_req(req)
    foundJob = False
    if jobInfoPtr != None :
        if jobInfoPtr.jobInfoHead != None :
            foundJob = True
    if not foundJob :
        print("failed to query jobs")
    else :
        print("found job number : {}".format(jobInfoPtr.jobInfoHead.numJobs))
        if jobInfoPtr.jobInfoHead.numJobs > 0 :
            job = lsf.jobInfoEnt()
            job = lsf.lsb_readjobinfo_cond(more, jobInfoPtr);
            if job == None:
                print("no job found")
            while job != None:
                if job.status != lsf.JOB_STAT_PEND and job.status != lsf.JOB_STAT_PSUSP :
                    print("job <{}> from user ({}) status is <{}>".format(lsf.lsb_jobid2str(job.jobId),job.user, showJobStat(job.status)))
                else :
                    pendreasons = lsf.lsb_pendreason_ex(reasonLevel, job, jobInfoPtr.jobInfoHead, job.clusterId)
                    print("job <{}> from user ({}) pending in status <{}>\n with pending reason:\n {}".format(lsf.lsb_jobid2str(job.jobId),job.user, showJobStat(job.status), pendreasons))

                job = lsf.lsb_readjobinfo_cond(more, jobInfoPtr);


if __name__ == "__main__":
    joblist = []
    if len(sys.argv) >= 2:
        for jobid in sys.argv[1:]:
            joblist.append(jobid)
    if len(joblist) > 0 :
        print("get job pending reason for: ", joblist)
    else :
        print("get all job pending reason info")
    get_job_info(joblist)
