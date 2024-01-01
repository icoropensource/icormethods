# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:16:08

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import time
import os

PROFILE=0
if PROFILE:
   import CLASSES_Library_ICORBase_External_MProfile as MProfile

def MainT(sobj,ltables,acreatetables=0,acreatesp=0,acreatevar=0,adisablechaptercreate=0,aDisableGenerateDependentTables=0):
   pobj=sobj.Projekt
   aproject=pobj.Nazwa
   acrm=mcrmbase.MCRM(aproject,acreatetables=acreatetables,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   asqldir=FilePathAsSystemPath('%ICOR%/sql/'+aproject)
   if not os.path.exists(asqldir):
      os.makedirs(asqldir)
   acrm.PreProcess(pobj,adir)
   acrm.ProcessBazyZrodloweByList(ltables,agenerateenable=1)
   acrm.ProcessCMSEvents('OnCMSInit')
   acrm.Write()
   acrm.CreateTables(asqldir=FilePathAsSystemPath('%ICOR%/sql/'+aproject),aservercreate=acreatetables,acreatesp=acreatesp,acreatevar=acreatevar,aDisableGenerateDependentTables=aDisableGenerateDependentTables)
   return

def MainI(tobj,acreatetables=0):
   pobj=tobj.Projekt
   aproject=pobj.Nazwa
   acrm=mcrmbase.MCRM(aproject,acreatetables=acreatetables,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   asqldir=FilePathAsSystemPath('%ICOR%/sql/'+aproject)
   if not os.path.exists(asqldir):
      os.makedirs(asqldir)
   aDisableGenerateDependentTables=tobj['DisableTableGen']
   print '$$ CRM PreProcess aDisableGenerateDependentTables =',aDisableGenerateDependentTables
   acrm.PreProcess(pobj,adir)
   acrm.ProcessBazyZrodlowe(tobj.TabeleZrodlowe,agenerateenable=1)
   acrm.ProcessPages(tobj.ProjectPageHTML)
#   acrm.ProcessWizards(tobj.Kreatory)
   acrm.ProjectVars['DisableGenerateChapter']=tobj['DisableChapterGen']
   acrm.ProjectVars['GenerateJSLib']=tobj['GenerujJSLib']
   acrm.ProjectVars['GenerateDeploy']=tobj['GenerujScenariusze']
   acrm.ProjectVars['GenerateSP']=tobj['GenerujSP']
   acrm.ProjectVars['GenerateVar']=tobj['GenerujVar']
   acrm.ProjectVars['DisableGenerateDependentTables']=tobj['DisableTableGen']
   wobj=tobj.WWWStruktura
   if wobj:
      while wobj:
         acrm.ProcessBazyZrodlowe(wobj.TabeleZrodlowe)
         wobj.Next()
      wobj=tobj.WWWStruktura
      acrm.ProcessWWWMenuStruct(wobj)
   elif not aDisableGenerateDependentTables:
      z1refs=tobj.TabeleZrodlowe.AsRefs()
      wobj=pobj.WWWMenuStruct
      while wobj:
         z2refs=wobj.TabeleZrodlowe.AsRefs()
         if z2refs.RefsExists(z1refs):
            acrm.ProcessWWWMenuStruct(wobj,asingle=1,awritedisabled=1)
         wobj.Next()
   acrm.ProcessUserTSQL(tobj.UserTSQL)
   acrm.ProcessCMSEvents('OnCMSInit')
   adisablechaptercreate=tobj['DisableChapterGen']
   acrm.Write(adisablechaptercreate=adisablechaptercreate,aDisableGenerateDependentTables=aDisableGenerateDependentTables)
   acreatesp=tobj['GenerujSP']
   acreatevar=tobj['GenerujVar']
   acrm.CreateTables(asqldir=FilePathAsSystemPath('%ICOR%/sql/'+aproject),aservercreate=acreatetables,acreatesp=acreatesp,acreatevar=acreatevar,adisablechaptercreate=adisablechaptercreate,aDisableGenerateDependentTables=aDisableGenerateDependentTables)
   tobj.Class.DataOstatniegoGenerowania.SetValuesAsDateTime(tobj.OID,CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime())
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if PROFILE:
      MProfile.Start()
   saveout=MLog.MemorySysOutWrapper()
   sok='OK'
   smessage='Generowanie szablonu zakończono powodzeniem'
   try:
      try:
         ret=FieldName.find('!')
         astate=''
         if ret>=0:
            FieldName,astate=FieldName[:ret],FieldName[ret+1:]
         acreatetables=0
         if FieldName=='1':
            acreatetables=1
         sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SzablonGenerowania']
         sobj=sclass[OID]
         MainI(sobj,acreatetables=acreatetables)
      except:
         sok='BAD'
         smessage='Wystąpił błąd podczas generowania szablonu'
         saveout.LogException()
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
      if OID>=0:
         sclass.Status[OID]=saveout.read()
         sclass.DataOstatniegoGenerowania.SetValuesAsDateTime(OID,ICORUtil.tdatetime())
      saveout.Restore()
      import win32api
      try:
         win32api.Beep(5000,100)
         win32api.Beep(3000,150)
      except:
         pass
   if PROFILE:
      MProfile.Stop('d:\\icor\\log\\generowanie01.py')
   return



