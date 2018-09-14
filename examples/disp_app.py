from pythonlsf import lsf

def printAppInfo():
    if lsf.lsb_init("test") > 0:
        return -1;

    intp_nent = lsf.new_intp()
    ents = lsf.lsb_appInfo(intp_nent)
    nent = lsf.intp_value(intp_nent)

    print("{} apps in the cluster.".format(nent))

    for i in range(nent) :
        ent = lsf.appInfoEntArray_getitem(ents, i)
        print('No.{} app name : {}, description: {}'.format(i, ent.name, ent.description))

    return 0
    
if __name__ == '__main__':
    print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
    printAppInfo()
