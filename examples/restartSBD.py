from pythonlsf import lsf
import sys


def restartSBD(opCode, message, hosts) :
    if lsf.lsb_init("test") > 0:
        print("failed to initialize")
        return
    req = lsf.hostCtrlReq()
    req.opCode = opCode
    req.message = message
    if len(hosts) > 0 :
        for h in hosts:
            print("restarting sbatchd daemon on host <{}> ...".format(h))
            req.host = h
            cc = lsf.lsb_hostcontrol(req)
            if cc == 0 :
                print("sbatchd daemon restarted successfully.")
            elif cc == -1 :
                print("ERROR: sbatchd daemon failed to restart.")
            else :
                print("ERROR: return {} while trying to restart sbatchd.".format(cc))
    else :
        print("restarting sbatchd daemon on local host ...")
        cc = lsf.lsb_hostcontrol(req)
        if cc == 0 :
            print("sbatchd daemon restarted successfully.")
        elif cc == -1 :
            print("ERROR: sbatchd daemon failed to restart.")
        else :
            print("ERROR: return {} while trying to restart sbatchd.".format(cc))
    

if __name__ == "__main__":
    opCode = lsf.HOST_REBOOT
    message = "reboot according to python-api"
    if len(sys.argv) > 1 :
        hosts = sys.argv[1:]
    else :
        hosts = []
    restartSBD(opCode, message, hosts)

