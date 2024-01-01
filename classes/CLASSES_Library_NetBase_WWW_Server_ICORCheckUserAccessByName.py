# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   sclass=aICORDBEngine.Classes['CLASSES_System_GroupAccessLevel']
   srefs=ICORSecurity.GetStringAsAccessLevelRefs(Value,sclass)
   if not srefs.len and Value:
      return '0'
   w=ICORSecurity.CheckAccessLevelForUser(srefs,UID)
   return str(w)

