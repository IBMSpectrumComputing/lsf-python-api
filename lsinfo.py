from pythonlsf import lsf
import sys

def printLsInfo(argList):
    if lsf.lsb_init("test") > 0:
        return -1;

    valueList=["Boolean","Numeric","String","Dynamic","External"]
    orderList=["Inc","Dec","N/A"]
    allInfo = lsf.ls_info_py()
    print("Current cluster has {} resources in total.".format(allInfo["nRes"]))
    print("Current cluster has {} types in total.".format(allInfo["nTypes"]))
    print("Current cluster has {} models in total.".format(allInfo["nModels"]))
    resTable = allInfo["resTable"]

    matchList = []
    unMatchList = []
    showAll = 0
    mFlag = 0
    mmFlag = 0
    rFlag = 0
    tFlag = 0
    resFound = 0
    if "-m" in argList:
        mFlag = 1
    if "-M" in argList:
        mFlag = 1
        mmFlag = 1
    if "-r" in argList:
        rFlag = 1
    if "-t" in argList:
        tFlag = 1

    if len(argList) > 0:
        for target in argList:
            if target[0] != "-":
                resFound = 0
                for i in range(len(resTable)):
                    if resTable[i].name == target :
                        matchList.append(i)
                        resFound = 1
                        break
                if resFound == 0:
                    unMatchList.append(target)

    if len(argList) == 0 and len(unMatchList) == 0:
        showAll = 1

    if (showAll == 1 or rFlag > 0 or len(matchList) > 0 or len(unMatchList) > 0) :
        print("ESOURCE_NAME             TYPE         ORDER           DESCRIPTION")
        if len(matchList) == 0 and len(unMatchList) == 0:
            for i in range(len(resTable)):
                print("{}             {}             {}                 {}".format(resTable[i].name, valueList[resTable[i].valueType], orderList[resTable[i].orderType], resTable[i].des))
            
        else:
            for i in range(len(resTable)):
                if i in matchList :
                    print("{}             {}             {}                 {}".format(resTable[i].name, valueList[resTable[i].valueType], orderList[resTable[i].orderType], resTable[i].des))
            for target in unMatchList :
                print("{}: resource name not found.".format(target))
    if (showAll == 1 or tFlag > 0):
        hostTypes = allInfo["hostTypes"]
        print("TYPE_NAME")
        for i in range(len(hostTypes)):
            print("{}".format(hostTypes[i]))
    if mFlag > 0 :
        hostModels = allInfo["hostModels"]
        hostArchs = allInfo["hostArchs"]
        modelRefs = allInfo["modelRefs"]
        cpuFactor = allInfo["cpuFactor"]
        print("MODEL_NAME      CPU_FACTOR      ARCHITECTURE")
        for i in range(allInfo["nModels"]):
            if (mmFlag > 0 or modelRefs[i] > 0):
                print("{}        {}        {}".format(hostModels[i],cpuFactor[i],hostArchs[i]))
    if (showAll == 0 and len(matchList) == 0 and mFlag == 0 and mmFlag == 0 and rFlag == 0 and tFlag == 0):
        print("No match resource found.")

        
    return 0

if __name__ == '__main__':
    print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
    argList = []
    if len(sys.argv) > 1 :
        for i in range(1,len(sys.argv)):
            argList.append(sys.argv[i])
    printLsInfo(argList)

