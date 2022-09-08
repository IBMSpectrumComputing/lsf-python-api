from pythonlsf import lsf

def printGuaranteedResourcePools():
    if lsf.lsb_init("test") > 0:
        print("Unable to init LSF API")
        return -1;

    intp_size = lsf.copy_intp(0)
    req = lsf.guaranteedResourcePoolInfoReq()
    strArr = lsf.new_stringArray(1);
    lsf.stringArray_setitem(strArr, 0, "");
    req.poolsC = 0
    req.poolNames = strArr;
    req.queueName = ""
    pp_ents = lsf.calloc_guaranteedResourcePoolEntPtrPtr()

    rc = lsf.lsb_guaranteedResourcePoolInfo(req,pp_ents,intp_size)

    if rc == -1 :
        print('Call LSF API failed')
        return -1;

    ents = lsf.guaranteedResourcePoolEntPtrPtr_value(pp_ents)
    size = lsf.intp_value(intp_size)

    print("{} guaranteed resource pools in the cluster.".format(size))

    for i in range(size) :
        ent = lsf.guaranteedResourcePoolEntArray_getitem(ents, i)
        print("Pool name: {}".format(ent.name))
        print("Resource type: {}".format(ent.type))
        print("Pool status: {}".format(ent.status))
        print("Total resources in pool: {}".format(ent.total))
        print("Free resources in pool: {}".format(ent.free))
        currentHostList = lsf.char_p_p_to_pylist(ent.currentHosts,ent.currentHostsC)
        print('Current hosts in the resource pool: ' + ' '.join(currentHostList))

    lsf.delete_stringArray(strArr);
    lsf.free_guaranteedResourcePoolEntPtrPtr(pp_ents);

    return 0

if __name__ == '__main__':
    print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
    printGuaranteedResourcePools()
    
