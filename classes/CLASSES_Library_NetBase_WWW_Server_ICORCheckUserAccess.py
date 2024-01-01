# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   w=ICORSecurity.CheckAccessLevelForUser(Value,UID)
   #print 'ICORCheckUserAccess:',Value,'uid=',UID,'w=',w
   return str(w)



