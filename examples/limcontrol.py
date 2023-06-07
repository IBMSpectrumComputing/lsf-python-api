from pythonlsf import lsf


# the hostname you want to operate lim running on
host = "your_hostname"

# set opCode to 1 if you need to reboot lim
#set to 2 if you want to shutdown it
opCode = 1

if lsf.lsb_init("test") > 0:
    print("failed to initialize")
    exit
if lsf.ls_limcontrol(host, opCode) == 0 :
    print("host operated successfully")
else :
    print("host operated failed")

