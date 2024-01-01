# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Dokumenty','BazyZrodlowe','Kreatory','PagesHTML','JednostkaOrganizacyjna','UserTSQL','TabliceZewnetrzne','SzablonyGenerowania','WWWMenuStruct','SecurityMap','SMSServers','SMTPServers','ListyWysylkowe','MapServers','AddIns','CDNServers','SSHServers',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   return



