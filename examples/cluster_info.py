from pythonlsf import lsf

if lsf.lsb_init("test") > 0:
    exit(1)

print('\n Hosts in cluster: %s' % lsf.get_host_names())

print('\n Clustername: {0:30s} \n'.format(lsf.ls_getclustername()))

print('{0:15s} {1:20s} {2:20s} {3:5s} {4:4s}'.format('Hostname', 'Type',
                                                     'Model', 'Cores', 'Load'))

for info in lsf.get_host_info():

    if info.isServer == '\x00': #just skip LSF client host
        continue

    #Deal with the case when hostname contain "-".
    if '-' in info.hostName:
        load = lsf.get_host_load("hname=" + "'" + info.hostName + "'", lsf.R15M)
    else:
        load = lsf.get_host_load("hname=" + info.hostName, lsf.R15M)
    
    if load >= 65535:
        load = -1

    print('{0:15s} {1:20s} {2:20s} {3:5d} {4:4.2f}'.format(info.hostName,
                                                           info.hostType,
                                                           info.hostModel,
                                                           info.cores * info.pprocs,
                                                           load))

    resources = ""
    index = 0;
    if info.nRes > 0:
        while(1):
            item = lsf.stringArray_getitem(info.resources,index)
            if(item):
                resources += item +" "
                index += 1
            else:
               break;
        print(' +--> Resources:', resources)
