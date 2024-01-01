# -*- coding: windows-1250 -*-
# saved: 2023/03/02 22:41:32

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Sections',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   return
