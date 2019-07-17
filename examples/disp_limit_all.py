from pythonlsf import lsf

def printLimitItem(name, item):
   print(name+' :')
   print('   consumerC : {}'.format(item.consumerC))
   consumers = lsf.limitConsumerArray_frompointer(item.consumerV)
   for j in range (item.consumerC) :
       print('       [{}] type : {}'.format(j, consumers[j].type))
       print('       [{}] name : {}'.format(j, consumers[j].name))
   print('   resourceC : {}'.format(item.resourceC))
   resources = lsf.limitResourceArray_frompointer(item.resourceV)
   for j in range (item.resourceC) :
       print('       [{}] name : {}'.format(j, resources[j].name))
       print('       [{}] type : {}'.format(j, resources[j].type))
       print('       [{}] val : {}'.format(j, resources[j].val))

   return 0

def printLimit():
   if lsf.lsb_init("test") > 0:
       return -1;

   req = lsf.limitInfoReq()
   req.name = " ";
   pp_ents = lsf.calloc_limitInfoEntPtrPtr()
   intp_size = lsf.copy_intp(0)
   lsinfo = lsf.lsInfo()

   rc = lsf.lsb_limitInfo(req, pp_ents, intp_size, lsinfo)
   if rc == -1 :
       print('call lsf failed')
       return -1;

   ents = lsf.limitInfoEntPtrPtr_value(pp_ents)
   size = lsf.intp_value(intp_size)

   print("{} limits in the cluster.".format(size))

   for i in range(size) :
       ent = lsf.limitInfoEntArray_getitem(ents, i)
       # print limit name
       print('Limit No.{} : {}'.format(i, ent.name))

       # print confInfo in the limit
       printLimitItem('confInfo', ent.confInfo)

       # print usageC in the limit
       print('usageC : {}'.format(ent.usageC))
       # print usageInfo in the limit
       all_usageInfo = lsf.limitItemArray_frompointer(ent.usageInfo)
       for j in range (ent.usageC) :
           printLimitItem('usageInfo', all_usageInfo[j])

       # print ineligible in the limit
       print('ineligible : {}\n\n'.format(ent.ineligible))

   return 0

if __name__ == '__main__':
   print("LSF Clustername is : {}".format(lsf.ls_getclustername()))
   printLimit()

