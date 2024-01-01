# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Rodzaj',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID,aupdaterefs=1)
   if FieldName in ['Skins',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName!='OstatnieZmiany':
      aclass.OstatnieZmiany[OID]=ICORUtil.tdatetime()
   return

