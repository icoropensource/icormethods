# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.JednostkaOrganizacyjna.UpdateReferencedObjects(OID,adeleterefs=1,aupdaterefs=1)
   aclass.Czynnosci.DeleteReferencedObjects(OID)
   return


