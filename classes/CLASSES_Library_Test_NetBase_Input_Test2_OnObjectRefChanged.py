# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   print 'OnObjectRefChanged:',CID,FieldName,OID,Value,UID
   return
   if not aclass.ObjectExists(OID):
      return
   amode,boid,bcid=eval(Value)
   afield=aclass.FIELD_NAME
   rclass=afield.ClassOfType
   if bcid==rclass.CID:
      if amode==1:
         afield.AddRefs(OID,[boid,bcid],asortedreffield=rclass.SORT_FIELD_NAME,ainsertifnotexists=1,dosort=1)
      else:
         afield.DeleteRefs(OID,[boid,bcid])
   return
