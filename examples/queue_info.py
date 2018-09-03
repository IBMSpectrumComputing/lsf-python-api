from pythonlsf import lsf

def query_queue(queue_name):
    """
    "query queue info"
    """

    if lsf.lsb_init("test") > 0:
        return -1;

    intp_num_queues = lsf.new_intp();
    lsf.intp_assign(intp_num_queues, 1);
    strArr = lsf.new_stringArray(1);
    #print lsf.intp_value(intp_num_queues);
    lsf.stringArray_setitem(strArr, 0, queue_name);
    #print lsf.stringArray_getitem(strArr, 0);
    queueInfo = lsf.lsb_queueinfo(strArr,intp_num_queues,None,None,0);
    if queueInfo != None:
        print('queueInfo is not null')
    else:
        print('queueInfo is null')
        return -1;

    print('queue name = %s' % queueInfo.queue)
    print('queue description = %s' % queueInfo.description)

    return 0;

def printQueueInfo():
    if lsf.lsb_init("test") > 0:
        return -1;

    strArr = lsf.new_stringArray(1); #array length is 2
    lsf.stringArray_setitem(strArr, 0, "normal");
#    lsf.stringArray_setitem(strArr, 1, "short");

    for info in lsf.get_queue_info_by_name(strArr, 1):
        print(info.queue)
        print(info.description)
        print('')

    return 0;
    
if __name__ == '__main__':
    print("LSF Clustername is :", lsf.ls_getclustername())
    print(query_queue("normal"))
    printQueueInfo()
