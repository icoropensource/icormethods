# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:14:13

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icorlib.projekt.msqlsecurity as MSQLSecurity

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      return ''
   aclass=aICORDBEngine.Classes[CID]
   pobj=aclass[OID]
   if not pobj:
      return ''
   auacl=MSQLSecurity.GetUserACL(pobj,UID)
   return auacl



