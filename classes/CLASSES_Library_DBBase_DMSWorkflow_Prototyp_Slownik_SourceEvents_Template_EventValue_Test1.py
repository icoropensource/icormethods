# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return

   le=[
'OnSchedulerMinute11',
'OnSchedulerMinute23',
'OnSchedulerMinute31',
]
   ld=[
#'OnCMSWriteChapterText',
#'OnCMSWriteChapterXSLSingle',
#'OnCMSWriteChapterXSLTable',
#'OnCMSWriteChapterCSS',
#'OnCMSWriteChapterJS',
#'OnCMSWriteCSS',
#'OnCMSWriteJS',
#'OnCMSWriteCSSSingle',
#'OnCMSWriteChapterAfter',
#'OnCMSWriteXML',
#'OnCMSWriteXSL',
#'OnCMSWriteXSD',

'OnSchedulerMinute1',
'OnSchedulerMinute2',
'OnSchedulerMinute3',
'OnSchedulerMinute4',
#'OnSchedulerMinute5',
'OnSchedulerMinute6',
'OnSchedulerMinute7',
'OnSchedulerMinute8',
'OnSchedulerMinute9',
'OnSchedulerMinute10',
'OnSchedulerMinute15',
'OnSchedulerMinute20',
'OnSchedulerMinute25',
'OnSchedulerMinute30',
'OnSchedulerMinute35',
'OnSchedulerMinute40',
'OnSchedulerMinute45',
'OnSchedulerMinute50',
'OnSchedulerMinute55',
]
   lc=[
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Template_EventKind',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Plugin_EventKind',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_AddInTemplate_EventKind',
'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_AddIn_EventKind',
]
   for sc in lc:
      print sc
      bclass=aICORDBEngine.Classes[sc]
      for se in ld:
         boid=bclass.EventName.Identifiers(se)
         if boid>=0:
            print '  -',boid,se
            bclass.DeleteObject(boid)
      for se in le:
         if bclass.EventName.Identifiers(se)<0:
            boid=bclass.GetNextFreeObjectID(1,200)
            print '  +',boid,se
            bclass.CreateObjectByID(boid)
            bclass.EventName[boid]=se
            boid=boid+1
   return
   aobj=aclass.GetFirstObject()
   while aobj:
      if aobj.EventDescription:
         atext=aobj.EventSource
         if atext[:3]=='<%\n':
            atext='<%\n#'+aobj.EventDescription+'\n\n'+atext[3:]
            print aobj.OID
#            aobj.EventSource=atext
      aobj.Next()
   return


