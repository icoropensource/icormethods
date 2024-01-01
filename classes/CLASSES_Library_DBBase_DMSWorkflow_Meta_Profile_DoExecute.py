# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

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
   fout2=FilePathAsSystemPath(r'%ICOR%\log\metaprofile_log.txt')
   saveout=MLog.MemorySysOutWrapper(fout2=fout2)
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   sok='OK'
   smessage='Generowanie projektu zakończono powodzeniem'
   pythoncom.CoInitialize()
   try:
      d=cPickle.loads(Value)
      try:
         ret=string.find(FieldName,'!')
         astate=''
         if ret>=0:
            FieldName,astate=FieldName[:ret],FieldName[ret+1:]
         pparser=ProfileLib.ProfileParser(UID,d['_mode'])
         pparser.ParseParameters(aobj.XMLParameters)
         for sn,sv in d.items():
            if sn=='_mode':
               continue
            pparser.Variables[sn]=sv
         aprofilename=pparser.Variables.get('PROFILE_NAME','')
         w=1
         if not aprofilename:
            w=0
            print 'Brak określonej nazwy profilu'
         if not ICORUtil.IsIdentifier(aprofilename):
            w=0
            print 'Nazwa profilu nie jest poprawnym identyfikatorem'
         if d['_mode'] in ['build','undo']:
            pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
            poid=pclass.Nazwa.Identifiers(aprofilename)
            if poid>=0:
               alocked=pclass.SGIsLocked.ValuesAsInt(poid)
               if alocked:
                  w=0
                  print 'Wybrany profil jest zabezpieczony przed modyfikacja'
               adisabled=pclass.SGIsDisabled.ValuesAsInt(poid)
               if adisabled:
                  w=0
                  print 'Wybrany profil jest wyłączony'
         if d['_mode']=='build' and w:
            pparser.ParseData(aobj.XMLData,adump=1)
         elif d['_mode']=='undo' and w:
            pparser.ParseData(aobj.XMLDataClean,adump=1)
         elif d['_mode']=='check':
            pparser.ParseData(aobj.XMLData,adump=1)
            pparser.ParseData(aobj.XMLDataClean,adump=1)
      except:
         sok='BAD'
         smessage='Wystąpił błąd podczas generowania projektu'
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
      aobj.Class.DataOstatniegoGenerowania.SetValuesAsDateTime(OID,ICORUtil.tdatetime())
      saveout.Restore()
      import win32api
      try:
         win32api.Beep(4000,100)
         win32api.Beep(2000,120)
         win32api.Beep(3000,150)
      except:
         pass
   return




