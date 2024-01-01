# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:13:26

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import string
import os

def MainI(pclass,poid,pobj,aproject,acreatetables=0,alog=None):
   acrm=mcrmbase.MCRM(aproject,acreatetables=acreatetables,abasenamemodifier=pobj.BaseNameModifier,alogger=alog)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   asqldir=FilePathAsSystemPath('%ICOR%/sql/'+aproject)
   if not os.path.exists(asqldir):
      os.makedirs(asqldir)
   if not alog is None:
      alog.Log('Process')
   acrm.Process(pobj,adir)
   if not alog is None:
      alog.Log('Write')
   acrm.Write()
   if not alog is None:
      alog.Log('CreateTables')
   acrm.CreateTables(asqldir=asqldir,aservercreate=acreatetables)
   if not alog is None:
      alog.Log('Koniec')
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   saveout=MLog.MemorySysOutWrapper()
   afname=MLog.GetLogTempFileName('projectgen')
   alog=MLog.MLog(afname,aconsole=0)
   alog.Log('Main - FieldName: '+FieldName+', OID: '+str(OID)+', Value: '+Value+', UID: '+str(UID))
   sok='OK'
   smessage='Generowanie projektu zako�czono powodzeniem'
   try:
      try:
         acreatetables=0
         ret=string.find(FieldName,'!')
         astate=''
         if ret>=0:
            FieldName,astate=FieldName[:ret],FieldName[ret+1:]
         if FieldName=='1':
            acreatetables=1
         pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
         poid=pclass.Nazwa.Identifiers(Value)
         if poid>=0:
            pobj=pclass[poid]
            if not pobj['SGIsDisabled']:
               MainI(pclass,poid,pobj,Value,acreatetables=acreatetables,alog=alog)
      except:
         sok='BAD'
         smessage='Wyst�pi� b��d podczas generowania projektu'
         alog.LogException(smessage)
         import traceback
         traceback.print_exc()
         import win32api
         try:
            for i in range(100):
               win32api.Beep(500-i*2,2)
         except:
            pass
   finally:
      if astate:
         bstate=ICORSync.ICORState(int(astate))
         bstate.Name=smessage
         bstate.Value=sok
      if poid>=0:
         pclass.Status[poid]=saveout.read()
         pclass.DataOstatniegoGenerowania.SetValuesAsDateTime(poid,CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime())
      alog.Log('Koniec pracy')
      saveout.Restore()
      import win32api
      try:
         win32api.Beep(5000,100)
         win32api.Beep(3000,150)
      except:
         pass
   return




