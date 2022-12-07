from pythonlsf import lsf

def printRsvInfo():
    if lsf.lsb_init("test") > 0:
        return -1;

    intp_nent = lsf.new_intp()
    ents = lsf.lsb_reservationinfo(None,intp_nent,0)
    nent = lsf.intp_value(intp_nent)

    print("{} rsvInfo in the cluster.".format(nent))

    for i in range(nent) :
        ent = lsf.rsvInfoEntArray_getitem(ents, i)
        print('No.{} rsvId : {}'.format(i, ent.rsvId))
        print('No.{} name : {}'.format(i, ent.name))
        print('No.{} state : {}'.format(i, ent.state))
        print('No.{} options : {}'.format(i, ent.options))
        print('No.{} timeWindow : {}'.format(i, ent.timeWindow))
        print('No.{} numRsvJobs : {}'.format(i, ent.numRsvJobs))
        print('No.{} numRsvHosts : {}'.format(i, ent.numRsvHosts))
        
        for j in range(ent.numRsvHosts):
            hostInfo_ent = lsf.hostRsvInfoEntArray_getitem(ent.rsvHosts, j)
            print('   [{}] host : {}'.format(j, hostInfo_ent.host))
            print('   [{}] numCPUs : {}'.format(j, hostInfo_ent.numCPUs))
            print('   [{}] numSlots : {}'.format(j, hostInfo_ent.numSlots))
            print('   [{}] numRsvProcs : {}'.format(j, hostInfo_ent.numRsvProcs))
            print('   [{}] numusedRsvProcs : {}'.format(j, hostInfo_ent.numusedRsvProcs))
            print('   [{}] numUsedProcs : {}'.format(j, hostInfo_ent.numUsedProcs))

    return 0
    
if __name__ == '__main__':
    print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
    printRsvInfo()
