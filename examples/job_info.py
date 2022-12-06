from pythonlsf import lsf


def get_single_job_info(jobid: int) -> lsf.jobInfoEnt:
    """
    Get the jobInfoEnt struct for a single lsf job using its jobId

    This function does not work for array jobs, only single jobs
    """
    if lsf.lsb_init("job_info") > 0:
        print("could not initialise the api")
        return

    # openjobinfo opens a connection to mbatchd and returns the amount of
    # jobs in the connection.
    num_jobs_found = lsf.lsb_openjobinfo(jobid, "", "all", "", "", 0x2000)

    # make and assign an int pointer to the record of the jobs found
    int_ptr = lsf.new_intp()
    lsf.intp_assign(int_ptr, num_jobs_found)

    # read the info at int_ptr and assign to a python object so we can read it.
    job_info = lsf.lsb_readjobinfo(int_ptr)

    # close the connection to avoid a memory leak
    lsf.lsb_closejobinfo()

    return job_info


if __name__ == "__main__":
    id = input("enter a job id:\n")
    job_info = get_single_job_info(int(id))

    print(f"job id: {job_info.jobId}\njob name: {job_info.jName}\n"
          f"status: {job_info.status:#x}")
