# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Meta_Profile_ProfileLib as ProfileLib
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import string
import cStringIO
import pythoncom
import CLASSES_Library_ICORBase_External_MLog as MLog
import cPickle

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   fout2=FilePathAsSystemPath(r'%ICOR%\log\templateinstall_log.txt')
   saveout=MLog.MemorySysOutWrapper(fout2=fout2)
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   sok='OK'
   smessage='Generowanie wtyczki zakończono powodzeniem'
   pythoncom.CoInitialize()
   try:
      d=cPickle.loads(Value)
      try:
         ret=string.find(FieldName,'!')
         astate=''
         if ret>=0:
            FieldName,astate=FieldName[:ret],FieldName[ret+1:]
         pparser=ProfileLib.ProfileParser(UID,d['_mode'])
         pparser.ParseParameters(aobj.Template.InstallParameters)
         for sn,sv in d.items():
            if sn=='_mode':
               continue
            pparser.Variables[sn]=sv
         aprofilename=pparser.Variables.get('PROFILE_NAME','')
         pparser.ParseData(aobj.Template.InstallScript,adump=1)
      except:
         sok='BAD'
         smessage='Wystąpił błąd podczas generowania'
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
      pythoncom.CoUninitialize()
      aobj.Status=saveout.read()
      aobj.Class.StatusDateTime.SetValuesAsDateTime(OID,ICORUtil.tdatetime())
      saveout.Restore()
      import win32api
      try:
         win32api.Beep(4000,100)
         win32api.Beep(2000,120)
         win32api.Beep(3000,150)
      except:
         pass
   return

