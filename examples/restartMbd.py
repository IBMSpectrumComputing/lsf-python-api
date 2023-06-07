from pythonlsf import lsf

req = lsf.mbdCtrlReq()
req.opCode = 0
req.message = ""
req.name = "mbd"

if lsf.lsb_init("test") > 0 :
    print("failed to initialize")
    exit
if lsf.lsb_reconfig(req) == 0 :
    print("mbd restarted successfully")
else :
    print("failed to restart mbd")

