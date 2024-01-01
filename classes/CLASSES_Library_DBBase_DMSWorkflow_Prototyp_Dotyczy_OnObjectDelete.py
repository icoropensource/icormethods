# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   wobj=aobj.Projekt.WWWMenuStruct
   while wobj:
      wobj.Class.TabeleZrodlowe.DeleteRefs(wobj.OID,[[OID,CID],])
      wobj.Next()
   aclass.Pola.DeleteReferencedObjects(OID)
   aclass.AddedHTML.DeleteReferencedObjects(OID)
   aclass.PolaczeniaDoTabel.DeleteReferencedObjects(OID)
   aclass.Zakladki.DeleteReferencedObjects(OID)
   aclass.Dotyczy.UpdateReferencedObjects(OID,adeleterefs=1,aupdaterefs=1)
   aclass.XMLData.DeleteReferencedObjects(OID)
   aclass.TableEvents.DeleteReferencedObjects(OID)
   return



