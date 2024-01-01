# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Replication_RevRefs_CheckDictObjects import DictClassChecker

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      return
   bclass=aICORDBEngine.Classes[OID]
   if bclass is None:
      return
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   if not aclass.EditObject(aoid,acaption='Obsługa obiektów słownikowych w klasie '+aclass.NameOfClass):
      return
   ClearStdOut()
   aobj=aclass[aoid]
   aremove=aobj['RemoveObjects',mt_Integer]
   aignorebackreffields=aobj['IgnoreBackRefFields',mt_Integer]
   ashowfullreport=aobj['ShowFullReport',mt_Integer]
   acrefs=DictClassChecker(aremove=aremove,aignorebackreffields=aignorebackreffields,ashowfullreport=ashowfullreport)
   acrefs.Process(bclass)
   acrefs.Dump()
   return

