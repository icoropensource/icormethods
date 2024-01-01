# -*- coding: windows-1250 -*-
# saved: 2023/03/02 22:45:11

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.Sections.DeleteReferencedObjects(OID)
   return
