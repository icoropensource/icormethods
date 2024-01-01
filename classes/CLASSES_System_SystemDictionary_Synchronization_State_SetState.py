# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      return '-1'
   astate=ICORSync.ICORState(OID)
   astate.Name=FieldName
   astate.Value=Value
   return str(astate.OID)

