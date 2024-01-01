# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   uclass=aICORDBEngine.Classes['CLASSES_System_User']
   aoid=-1
   if Value:
      aoid=uclass.UserName.Identifiers(Value)
   return str(aoid)

