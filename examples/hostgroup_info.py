#! /usr/bin/env python

from pythonlsf import lsf

def queryHostGroupInfo():
    """
    "query host group info"
    """
    if lsf.lsb_init("queryHostGroupInfo") > 0:
        return -1;

    strArr = lsf.new_stringArray(2);
    lsf.stringArray_setitem(strArr, 0, "hg1");
    lsf.stringArray_setitem(strArr, 1, "hg2");
    for hgroupInfo in lsf.get_hostgroup_info_by_name(strArr,2):
        if hgroupInfo != None:
            print 'hgroup name = %s' % hgroupInfo.group;
            print 'hgroup list = %s' % hgroupInfo.memberList;
        else:
            print 'hgroupInfo is null'
            return -1;

    return 0;

if __name__ == '__main__':
    queryHostGroupInfo();
