# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.Dokumenty.DeleteReferencedObjects(OID)
   aclass.PagesHTML.DeleteReferencedObjects(OID)
   aclass.JednostkaOrganizacyjna.DeleteReferencedObjects(OID)
   aclass.BazyZrodlowe.DeleteReferencedObjects(OID)
   aclass.Kreatory.DeleteReferencedObjects(OID)
   aclass.UserTSQL.DeleteReferencedObjects(OID)
   aclass.TabliceZewnetrzne.DeleteReferencedObjects(OID)
   aclass.SzablonyGenerowania.DeleteReferencedObjects(OID)
   aclass.WWWMenuStruct.DeleteReferencedObjects(OID)
   aclass.SecurityMap.DeleteReferencedObjects(OID)
   aclass.SMTPServers.DeleteReferencedObjects(OID)
   aclass.SMSServers.DeleteReferencedObjects(OID)
   aclass.SSHServers.DeleteReferencedObjects(OID)
   aclass.MapServers.DeleteReferencedObjects(OID)
   aclass.ListyWysylkowe.DeleteReferencedObjects(OID)
   aclass.AddIns.DeleteReferencedObjects(OID)
   aclass.CDNServers.DeleteReferencedObjects(OID)
   return



