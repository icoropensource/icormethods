# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aICORDBEngine.Variables._AllowObjectExport='1'
   if (OID>=35000 and OID<36000):
      aICORDBEngine.Variables._AllowObjectExport='0'
   return

