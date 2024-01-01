# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   bclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_AddIn_EventKind']
   sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Template_EventKind']
   sobj=sclass.GetFirstObject()
   while sobj:
      sname=sobj.EventName
      if aclass.EventName.Identifiers(sname)<0:
         aoid=aclass.AddObject()
         aclass.EventName[aoid]=sname
         print sname
      if bclass.EventName.Identifiers(sname)<0:
         boid=bclass.AddObject()
         bclass.EventName[boid]=sname
      sobj.Next()
   return

