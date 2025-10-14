from pythonlsf import lsf
if __name__ == '__main__':
   if lsf.lsb_init("test") > 0:
       exit -1;
   num_hosts = lsf.new_intp()
   lsf.intp_assign(num_hosts, 0)
   hosts = lsf.ls_gethostgpuinfo(None, num_hosts, None, 0, 0)
   hostGpuInfos = lsf.hostGpuInfoArray_frompointer(hosts)
   for i in range(0, lsf.intp_value(num_hosts)):
     hostGpuInfo = hostGpuInfos[i]
     print("Host: {}". format(hostGpuInfo.hostName))
     numGpus = hostGpuInfos[i].gpuC
     if numGpus <= 0:
        continue
     gpuAttrData = hostGpuInfo.gpuAttrV
     gpuLoadData = hostGpuInfo.gpuLoadV
     gpuAttrs = lsf.hostGpuAttrArray_frompointer(gpuAttrData)
     gpuLoads = lsf.hostGpuLoadArray_frompointer(gpuLoadData)
     print("      gBrand     gModel   gBusId       gMode  gUsedMem  gStatus")
     for j in range(0, numGpus):
        print("      {} {} {} {} {} {} ". \
           format(gpuAttrs[j].gBrand, gpuAttrs[j].gModel, gpuAttrs[j].gBusId,
                gpuLoads[j].gMode, gpuLoads[j].gUsedMem, gpuLoads[j].gStatus))
