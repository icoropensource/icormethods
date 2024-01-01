# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aoid=-1
   if FieldName and Value:
      aoid=ICORSecurity.GetUIDByUserPassword(FieldName,Value,awwwuser=1)
   return str(aoid)

