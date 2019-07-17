from pythonlsf import lsf
import ctypes

def printHostInfo():
    if lsf.lsb_init("test") > 0:
        return -1;

    intp_nhosts = lsf.new_intp()
    lsf.intp_assign(intp_nhosts, 0) 
    hostsdata = lsf.ls_load(None, intp_nhosts, 0, None)
    nhosts = lsf.intp_value(intp_nhosts)
    all_lsload_data = lsf.hostLoadArray_frompointer(hostsdata)

    print("{} hosts in the cluster.".format(nhosts))

    for i in range(nhosts) :
        host = all_lsload_data[i]
        hostname = ctypes.cast( host.hostName, ctypes.c_char_p)
        print('No.{} host name : {}'.format(i, hostname.value))

    return 0

if __name__ == '__main__':
    print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
    printHostInfo()

