# -*- coding: windows-1250 -*-
# saved: 2023/03/04 14:54:45

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.Rozdzialy.DeleteReferencedObjects(OID)
   aclass.UserTSQL.DeleteReferencedObjects(OID)
   aclass.UserCode.DeleteReferencedObjects(OID)
   aclass.RozdzialyUsuniete.DeleteReferencedObjects(OID)
   aclass.GrupyRozdzialow.DeleteReferencedObjects(OID)
   aclass.RSSInfo.DeleteReferencedObjects(OID)
   aclass.Plugins.DeleteReferencedObjects(OID)
   aclass.MapServices.DeleteReferencedObjects(OID)
   aclass.Alerty.DeleteReferencedObjects(OID)
   aclass.UserXML.DeleteReferencedObjects(OID)
   aclass.UserXSL.DeleteReferencedObjects(OID)
   aclass.UserXSD.DeleteReferencedObjects(OID)
   aclass.APILibraries.DeleteReferencedObjects(OID)
   aclass.PageTemplate.DeleteReferencedObjects(OID)
   return



