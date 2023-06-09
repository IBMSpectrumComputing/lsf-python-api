from pythonlsf import lsf
import sys

def get_job_info(list) :
    if lsf.lsb_init("test") > 0:
        print("failed to initialize")
        return
    if len(list) == 0 :
        print("no valid job id given")
        return
    print("request below job's info: {}".format(list))
    clusterName = lsf.ls_getclustername()
    print("retrieve cluster name : {}".format(clusterName))
    query = "jobIds=("
    for l in list:
        query += l +","
    query = query[:-1]
    query += ")jobSouceClusterNames=("
    for i in range(len(list)):
        query += clusterName + ","
    query = query[:-1]
    query += ") options=" + str(lsf.ALL_JOB) + " "

    jobQuery = lsf.jobInfoQuery()
    jobQuery.nCols = 10
    jobQuery.colIndexs = lsf.buildQueryColIndexs()

    jobQuery.query = query
    jobQuery.submitExt = lsf.submit_ext()
    more = lsf.new_intp()
    print("request: {}".format(jobQuery.query))
    jobInfoPtr = lsf.jobInfoHeadExt()
    jobInfoPtr = lsf.lsb_queryjobinfo_ext_2(jobQuery, clusterName)
    foundJob = False
    if jobInfoPtr != None :
        if jobInfoPtr.jobInfoHead != None :
            foundJob = True
    if not foundJob :
        print("faild to query jobs")
    else :
        print("found job number : {}".format(jobInfoPtr.jobInfoHead.numJobs))
        if jobInfoPtr.jobInfoHead.numJobs > 0 :
            job = lsf.jobInfoEnt()
            job = lsf.lsb_fetchjobinfo(more, jobQuery.nCols, jobQuery.colIndexs, jobQuery.query)
            if job == None:
                print("no job found")
            while job != None:
                print("job <{}> from user ({}) status is {}".format(lsf.lsb_jobid2str(job.jobId),job.user, job.status))
                job = lsf.lsb_fetchjobinfo(more, jobQuery.nCols, jobQuery.colIndexs, jobQuery.query)


if __name__ == "__main__":
    joblist = []
    if len(sys.argv) < 2:
        joblist = ['0']
    else:
        for jobid in sys.argv[1:]:
            joblist.append(jobid)
    joblist = ['3530','3531']
    get_job_info(joblist)
