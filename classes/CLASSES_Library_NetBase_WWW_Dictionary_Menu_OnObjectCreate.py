# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   alp=aICORDBEngine.Variables._LastMenuProfileSelected
   ama=aICORDBEngine.Variables._LastMenuActionSelected
   if alp:
      aclass.Profile[OID]=alp
   if ama:
      aclass.Action[OID]=ama
   return



