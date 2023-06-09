from pythonlsf import lsf

def print_job_cputime(jobid):

    if lsf.lsb_init("job_info") > 0:
        print("failed to initialise the api")
        return

    num_jobs_found = lsf.lsb_openjobinfo(jobid, "", "all", "", "", 0x2000)
    print('num_jobs_found: {}'.format(num_jobs_found))

    if num_jobs_found == -1:
        print("no job was found")
        return

    int_ptr = lsf.new_intp()
    lsf.intp_assign(int_ptr, num_jobs_found)

    job_info = lsf.lsb_readjobinfo(int_ptr)

    lsf.lsb_closejobinfo()

    print('jobId: {}'.format(job_info.jobId))
    print('jobStatus: {}'.format(job_info.status))

    # Get CPU time from run Rusage
    time_sum = float(job_info.runRusage.utime) + float(job_info.runRusage.stime)
    if time_sum > 0:
        print('The CPU time used is: {} seconds'.format(time_sum))

    # Get CPU time from host Rusage of each execution host
    if job_info.numhRusages > 0:
        hRusages = job_info.hostRusage
        for i in range(0,job_info.numhRusages):
            hRusage = lsf.hRusageArray_getitem(hRusages, i)
            cpu_time = float(hRusage.utime) + float(hRusage.stime)
            print('HOST: {}, CPU_TIME: {} seconds'.format(hRusage.name, cpu_time))

    return

if __name__ == "__main__":
    id = input("Enter a running job id:\n")
    print_job_cputime(int(id))
