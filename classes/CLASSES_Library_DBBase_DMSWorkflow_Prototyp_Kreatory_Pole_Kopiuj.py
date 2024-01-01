# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      return
   aoid=aclass.AddObject(OID)
   fl=['Nazwa', 'TypPola', 'Dokument', 'BazaZrodlowa', 'NazwaPolaWZrodleDanych', 'SGTabIndex', 'SGIsObligatory', 'SGIsAliased', 'SGIsSearch', 'WartosciSlownika', 'SGIsIndexed', 'Opis', 'SGIsInteractive']
   for afname in fl:
      afield=aclass.FieldsByName(afname)
      afield[aoid]=afield[OID]



