# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['PluginEvents','PluginSkin',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName=='Nazwa':
      v=aclass.Nazwa[OID]
      if v in ['Biblioteka standardowa','Moduł bezpieczeństwa']:
         aclass.Grupa[OID]='Serwis'
   return

