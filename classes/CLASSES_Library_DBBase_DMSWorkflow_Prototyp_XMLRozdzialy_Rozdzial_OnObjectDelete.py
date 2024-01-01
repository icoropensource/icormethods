# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   wobj=None
   aobj=aclass[OID]
   bobj=aobj.AsObject()
   while not wobj and bobj:
      wobj=bobj.Struktura
      bobj=bobj.NadRozdzial
   awoid=''
   if wobj:
      awoid=str(wobj.OID)
   aclass.DoRefreshChapterInfo(awoid,OID,'DELETE')
   aclass.PodRozdzialy.DeleteReferencedObjects(OID)
   aclass.ChapterEvents.DeleteReferencedObjects(OID)
   aclass.ChapterView.DeleteReferencedObjects(OID)
   aclass.Models.DeleteReferencedObjects(OID)
   return



