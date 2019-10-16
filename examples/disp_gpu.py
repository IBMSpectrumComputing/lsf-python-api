from pythonlsf import lsf
if __name__ == '__main__':
   print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
   if lsf.lsb_init("test") > 0:
       exit -1;
   host_names = None
   num_hosts = lsf.new_intp()
   lsf.intp_assign(num_hosts, 0)
   host_data = lsf.lsb_hostinfo_ex(host_names, num_hosts, "", 4096)
   all_host_data = lsf.hostInfoEntArray_frompointer(host_data)
   for i in range(0, lsf.intp_value(num_hosts)):
     hostname = all_host_data[i].host
     print(hostname)
     gpudata = all_host_data[i].gpuData
     print("ngpus avail_shared_gpus avail_excl_gpus")
     print("   {}              {}              {}". \
                format(gpudata.ngpus, gpudata.avail_shared_ngpus, gpudata.avail_excl_ngpus))
