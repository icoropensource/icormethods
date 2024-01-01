# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ProcessChapter(robj,tables):
   tname=robj.NazwaTabeli
   if tables.has_key(tname):
      robj.Class.TabelaZrodlowa[robj.OID]=tables[tname]
   sobj=robj.PodRozdzialy
   while sobj:
      ProcessChapter(sobj,tables)
      sobj.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aoid=aclass.Nazwa.Identifiers('???')
   if aoid<0:
      return
   aobj=aclass[aoid]
   tobj=aobj.TabeleZrodlowe
   tables={}
   while tobj:
      tables[tobj.Nazwa]=[tobj.OID,tobj.CID]
      tobj.Next()
   robj=aobj.Rozdzialy
   while robj:
      ProcessChapter(robj,tables)
      robj.Next()
   return



