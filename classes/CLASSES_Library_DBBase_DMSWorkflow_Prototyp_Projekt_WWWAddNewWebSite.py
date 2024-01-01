# -*- coding: windows-1250 -*-
# saved: 2023/03/05 18:31:37

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

import icorupgrade.appcmsbuilder as appcmsbuilder

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None,bwwweditor=None,wobj=None):
   if bwwweditor is None:
      bwwweditor={}
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   aCMS_NAME=bwwweditor.get('aCMS_NAME','')
   if wobj:
      aCMS_NAME=wobj.Nazwa
   awwweditor.RegisterField('aCMS_NAME',adisplayed='Nazwa CMS/Aplikacji',atype=mt_String,avalue=aCMS_NAME)
   avalue=bwwweditor.get('aPRETTY_CMS_NAME','')
   if wobj:
      avalue=wobj.Title
   awwweditor.RegisterField('aPRETTY_CMS_NAME',adisplayed='Nazwa CMS/Aplikacji d�uga',atype=mt_String,avalue=avalue)
   avalue=bwwweditor.get('aHEAD_TITLE','')
   if wobj:
      avalue=wobj.Title
   awwweditor.RegisterField('aHEAD_TITLE',adisplayed='Tytu�',atype=mt_String,avalue=avalue)
   avalue=bwwweditor.get('aMETA_AUTHOR','')
   mobj=None
   if wobj:
      mobj=wobj.MetaTemplate
      if mobj:
         avalue=mobj.Author
   awwweditor.RegisterField('aMETA_AUTHOR',adisplayed='Autor',atype=mt_String,avalue=avalue)
   avalue=bwwweditor.get('aMETA_DESCRIPTION','')
   if mobj:
      avalue=mobj.Description
   awwweditor.RegisterField('aMETA_DESCRIPTION',adisplayed='Opis Meta',atype=mt_String,avalue=avalue)
   avalue=bwwweditor.get('aMETA_KEYWORDS','ICOR, BIP')
   if mobj:
      avalue=mobj.Keywords
   awwweditor.RegisterField('aMETA_KEYWORDS',adisplayed='S�owa kluczowe',atype=mt_String,avalue=avalue)
   avalue=bwwweditor.get('aEMAIL','')
   if mobj:
      aUserClass=aICORDBEngine.Classes['CLASSES_System_User']
      uoid=aUserClass.UserName.Identifiers(aCMS_NAME+'Admin')
      if uoid>=0:
         avalue=aUserClass.VCFEMail[uoid]
   awwweditor.RegisterField('aEMAIL',adisplayed='e-mail do Admina',atype=mt_String,avalue=avalue)
   avalue=bwwweditor.get('aHOME_PAGE_ADDRESS','')
   if wobj:
      hobj=wobj.AppPaths
      if hobj:
         avalue=hobj.AdresZewnetrznyWWW
   awwweditor.RegisterField('aHOME_PAGE_ADDRESS',adisplayed='Nazwa w DNS',atype=mt_String,avalue=avalue)
   return awwweditor

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

def OnWWWAction(aobj,amenu,file,wobj=None):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None,None,wobj)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file,dparams=None):
   if dparams is None:
      dparams={
         'CreateDirs':1,
         'CopyFiles':1,
         'CreateSecurity':1,
         'ImpersonateAdmin':1,
         'CreateCMS10':1,
         'CreateObjectsTables10':1,
         'CreateObjectsTables20':1,
         'CreatePlugin_BibliotekaStandardowa':1,
         'CreatePlugin_ModulBezpieczenstwa':1,
         'CreatePluginTables':1,
         'CreatePlugin_Abstrakty':1,
         'CreatePlugin_Kalendarium':1,
         'CreatePlugin_Geolokalizacja':1,
         'CreatePlugin_Wyszukiwarka':1,
         'CreatePlugin_Multimedia':1,
         'CreatePlugin_KategorieTresci':1,
         'CreatePlugin_TabeleTresci':1,
         'CreatePlugin_NarzedziaSEO':1,
         'CreateRozdzialy':1,
      }
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
   abuilder=appcmsbuilder.AppCMSBuilder(aobj,amenu.uid,file,awwweditor,dparams=dparams)
   if abuilder.Validate(anew=0):
      bwwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport,awwweditor)
      bwwweditor.Write()
      return
   try:
      abuilder.Process()
   except:
      import traceback
      traceback.print_exc()
      raise
   abuilder.Dump()

