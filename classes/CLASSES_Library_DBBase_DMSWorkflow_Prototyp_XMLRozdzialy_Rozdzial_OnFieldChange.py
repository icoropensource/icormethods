# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['PodRozdzialy',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID,'NadRozdzial')
   if FieldName in ['ChapterEvents',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName in ['Naglowek',]:
      aclass.DoRefreshChapterInfo(FieldName,OID,'UPDATE')
   if FieldName in ['IsAutoGenerate',]:
      aclass.DoRefreshChapterInfo(FieldName,OID,'IsAutoGenerate')
   if FieldName in ['ChapterView','Models',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName=='PodRozdzialy':
      aobj=aclass[OID]
      robj=aobj.PodRozdzialy
      atabid=10
      while robj:
         robj.SGTabID=atabid
         atabid=atabid+10
         robj.Next()
   if FieldName in ['ScheduledGenerate',]:
      wobj=None
      aobj=aclass[OID]
      sobj=aobj.ScheduledGenerate
      while not wobj and aobj:
         wobj=aobj.Struktura
         aobj=aobj.NadRozdzial
      if wobj:
         if sobj:
            wobj.Class.ScheduledChapters.AddRefs(wobj.OID,[[OID,CID],])
         else:
            wobj.Class.ScheduledChapters.DeleteRefs(wobj.OID,[[OID,CID],])
   return

