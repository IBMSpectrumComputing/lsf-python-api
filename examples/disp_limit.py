from pythonlsf import lsf

def printLimit():
    if lsf.lsb_init("test") > 0:
        return -1;

    req = lsf.limitInfoReq()
    req.name = " ";
    pp_ents = lsf.calloc_limitInfoEntPtrPtr()
    intp_size = lsf.copy_intp(0)
    lsinfo = lsf.lsInfo()

    rc = lsf.lsb_limitInfo(req, pp_ents, intp_size, lsinfo)
    if rc == -1 :
        print('call lsf failed')
        return -1;

    ents = lsf.limitInfoEntPtrPtr_value(pp_ents)
    size = lsf.intp_value(intp_size)

    print("{} limits in the cluster.".format(size))

    for i in range(size) :
        ent = lsf.limitInfoEntArray_getitem(ents, i)
        print('No.{} limit name : {}'.format(i, ent.name))

    return 0
    
if __name__ == '__main__':
    print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
    printLimit()
