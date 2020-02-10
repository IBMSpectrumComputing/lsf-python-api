from pythonlsf import lsf

def printSLA():
    if lsf.lsb_init("test") > 0:
        return -1;

    req = lsf.guaranteedResourcePoolInfoReq()
    req.poolsC = 0;
    #req.poolNames = lsf.new_stringArray(1);
    req.queueName = "";
    pp_ents = lsf.calloc_guaranteedResourcePoolEntPtrPtr()
    intp_nents = lsf.copy_intp(0)

    rc = lsf.lsb_guaranteedResourcePoolInfo(req, pp_ents, intp_nents)
    if rc == -1 :
        errno = lsf.lsb_errno()
        print('call lsf failed {}'.format(errno))
        return -1;

    ents = lsf.guaranteedResourcePoolEntPtrPtr_value(pp_ents)
    nents = lsf.intp_value(intp_nents)

    print("Totally {} Guaranteed Resource Pools in the cluster.".format(nents))

    for i in range(nents) :
        ent = lsf.guaranteedResourcePoolEntArray_getitem(ents, i)
        # print Guaranteed Resource Pool name
        print('-------- Pool {} --------'.format(i))
        print('    name : {}'.format(ent.name))
        print('    description : {}'.format(ent.description))
        print('    type : {}'.format(ent.type))
        print('    rsrcName : {}'.format(ent.rsrcName))
        print('    slotsPerHost : {}'.format(ent.slotsPerHost))
        print('    status : {}'.format(ent.status))
        print('    configuredHosts : {}'.format(ent.configuredHosts))
        print('    total resources in : {}'.format(ent.total))
        print('    free resources in : {}'.format(ent.free))
        print('    total guaranteed resources : {}'.format(ent.guar))
        print('    unused guaranteed resources : {}'.format(ent.unused))
        consumers = lsf.guarConsumerArray_frompointer(ent.consumerV)
        print('    {} consumers :'.format(ent.consumerC))
        for j in range (ent.consumerC) :
            print('        name: {}, deserved: {}, guarUsed: {}, totalUsed: {}' \
                  .format(consumers[j].name, consumers[j].deserved, \
                  consumers[j].guarUsed, consumers[j].totalUsed))
        currentHosts = lsf.string_array_to_pylist(ent.currentHosts, ent.currentHostsC)
        print('    current hosts :')
        for j in range (ent.currentHostsC) :
            print('        {}'.format(currentHosts[j]))

    return 0
    
if __name__ == '__main__':
    print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
    printSLA()
