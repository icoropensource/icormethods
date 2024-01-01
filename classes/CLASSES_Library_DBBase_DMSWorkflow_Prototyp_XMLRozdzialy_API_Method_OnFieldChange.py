# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Parameters',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID,aupdaterefs=1)
   elif FieldName=='Nazwa':
      aclass.NazwaID[OID]=ICORUtil.MakeIdentifier(aclass.Nazwa[OID],asimple=1)
   return

