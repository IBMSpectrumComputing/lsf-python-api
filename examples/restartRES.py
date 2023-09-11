import sys,socket
from pythonlsf import lsf

def restartres(hostlist):
    if lsf.ls_initdebug("resrestart") < 0:
       print("ls_initdebug failed!")
       return -1
    num_port = len(hostlist) * 2
    if lsf.ls_initrex(num_port, 0) < num_port :
        lsf.ls_perror("ls_initrex")
        return -1
    for host in hostlist:
        rc=lsf.ls_rescontrol(host, lsf.RES_CMD_REBOOT, 0)
    
        if rc < 0:
            lsf.ls_perror("lsf.ls_rescontrol")
            print("failed restart res on {}".format(host))
        else :
            print("res on {} restarted".format(host))
    return 

if __name__ == '__main__':
    if len(sys.argv) > 1 :
        hostlist = sys.argv[1:]
    else :
        hostlist = [socket.gethostname()]
    restartres(hostlist)

