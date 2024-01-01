# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   arefs=aclass.Groups.GetRefList(UID)
   brefs=aclass.Groups.GetRefList(OID)
   if arefs.RefsExists(brefs):
      return '1'
   return '0'


