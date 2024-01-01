# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura_Main as DataGenerator
import CLASSES_Library_ICORBase_External_MLog as MLog

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   ret=aICORDBEngine.SysBase.GetCMSChapterGenerateNext()
   if ret is None:
      return
   saveout=MLog.MemorySysOutWrapper()
   try:
      try:
         soid,achapterid,aoperationoid=ret
         sobj=aclass[soid]
         lchapters=[achapterid]
         DataGenerator.MainChapters(sobj,lchapters,astatusupdate=0,aoperationoid=aoperationoid)
      except:
         saveout.ICORStdOutPrint=1
         saveout.LogException()
   finally:
      saveout.Restore()
   return

