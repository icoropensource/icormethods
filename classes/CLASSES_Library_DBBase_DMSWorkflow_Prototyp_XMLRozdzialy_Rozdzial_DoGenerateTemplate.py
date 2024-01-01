# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:17:04

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
import CLASSES_Library_ICORBase_External_MLog as MLog

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   alogfname=MLog.GetLogTempFileName('status_chaptergentemplate')
   try:
      s='DoGenerateTemplate: %d - %s - %d - %s'%(CID,FieldName,OID,Value)
      MLog.Log(s,fname=alogfname,aconsole=0)
      wobj=sclass[int(FieldName)]
      if wobj:
         pobj=wobj.Projekt
         acrm=mcrmbase.MCRM(pobj.Nazwa,acreatetables=0,abasenamemodifier=pobj.BaseNameModifier)
         adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
         acrm.PreProcess(pobj,adir)
         if wobj:
            acrm.ProcessWWWMenuStruct(wobj,asingle=1)
            for awwwmenustruct in acrm.wwwmenustruct:
               awwwmenustruct.WriteSingle(acrm.BaseDirectory,aobj)
      MLog.Log('Gen OK',fname=alogfname,aconsole=0)
   except:
      MLog.LogException(fname=alogfname,aconsole=0)
      raise
   return 'OK'

