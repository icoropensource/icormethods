# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if 0:
      aclass=aICORDBEngine.Classes[CID]
      aobj=aclass.GetFirstObject()
      l=[]
      while aobj:
         l.append(aobj.EventName)
         aobj.Next()
      l.sort()
      for s in l:
         print s
      return
   if 0:
      aclass1=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Plugin_EventKind']
      aclass2=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Template_EventKind']
      l=[
         'OnCMSPageContentBeforeEnd',
         'OnCMSPageContentAfterStart',
      ]
      for aclass in [aclass1,aclass2]:
         for s in l:
            aoid=aclass.AddObject()
            aclass.EventName[aoid]=s
      return

