# -*- coding: windows-1250 -*-
# saved: 2023/03/05 18:30:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt_WWWAddNewWebSite as WWWAddNewWebSite

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWAction(aobj,amenu,file):
   pobj=aobj.Projekt
   return WWWAddNewWebSite.OnWWWAction(pobj,amenu,file,wobj=aobj)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   pobj=aobj.Projekt
   dparams={
      'CreateDirs':0,
      'CopyFiles':0,
      'CreateSecurity':1,
      'ImpersonateAdmin':1,
      'CreateCMS10':1,
      'CreateObjectsTables10':1,
      'CreateObjectsTables20':0,
      'CreatePlugin_BibliotekaStandardowa':0,
      'CreatePlugin_ModulBezpieczenstwa':0,
      'CreatePluginTables':1,
      'CreatePlugin_Abstrakty':1,
      'CreatePlugin_Kalendarium':1,
      'CreatePlugin_Geolokalizacja':1,         
      'CreatePlugin_Wyszukiwarka':1,
      'CreatePlugin_Multimedia':1,
      'CreatePlugin_KategorieTresci':1,
      'CreatePlugin_TabeleTresci':1,
      'CreatePlugin_NarzedziaSEO':1,
      'CreatePlugin_WWWSite':1,
      'CreateRozdzialy':0,
   }
   return WWWAddNewWebSite.OnWWWActionSubmit(pobj,amenu,areport,file,dparams=dparams)

