# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if not aclass.ObjectExists(OID):
      return
   amode,boid,bcid=eval(Value)
   for afieldname,asortedreffieldname in [['GroupAccessLevels','Name'],['GroupItemAccessLevels','Name']]:
      afield=aclass.FieldsByName(afieldname)
      rclass=afield.ClassOfType
      if bcid==rclass.CID:
         asortedreffield=rclass.FieldsByName(asortedreffieldname)
         if amode==1:
            afield.AddRefs(OID,[boid,bcid],asortedreffield=asortedreffield,ainsertifnotexists=1,dosort=1)
         else:
            afield.DeleteRefs(OID,[boid,bcid])
   return

