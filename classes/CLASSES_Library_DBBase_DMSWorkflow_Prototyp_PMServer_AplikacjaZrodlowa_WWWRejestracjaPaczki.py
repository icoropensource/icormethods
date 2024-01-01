# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppUtil as AppUtil
import os
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None,lfiles=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   for aname,asize in lfiles:
      adesc=aname+' (rozmiar '+ICORUtil.GetKBSize(asize)+')'
      awwweditor.RegisterField('LPF_'+aname,adisplayed=adesc,atype=mt_Boolean,avalue=0)
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
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

def GetFiles(aobj):
   adir=FilePathAsSystemPath(aobj.SciezkaDanych)
   ldirs=os.listdir(adir)
   lnames=[]
   for afname in ldirs:
      aname,aext=os.path.splitext(afname.lower())
      if aext=='.xml':
         ahash,asize,alastline=AppUtil.GetPackageFileInfo(adir+'/'+afname,anohash=1)
         if alastline:
            lnames.append((aname,asize))
   return lnames

def OnWWWAction(aobj,amenu,file):
   try:
      lnames=GetFiles(aobj)
   except:
      file.write('<h1>Wystąpił problem z dostępem do katalogu: %s</h1>'%(aobj.SciezkaDanych,))
      return 2
   if not lnames:
      file.write('<h1>brak plików do rejestracji</h1>')
      return 2
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None,lfiles=lnames)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      try:
         lnames=GetFiles(aobj)
      except:
         file.write('<h1>Wystąpił problem z dostępem do katalogu: %s</h1>'%(aobj.SciezkaDanych,))
         return
      aobj.StatusRejestracji=''
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport,lfiles=lnames)
      w=0
      for aname,asize in lnames:
         if ICORUtil.str2bool(awwweditor['LPF_'+aname]):
            w=1
            file.write('<h2>zaznaczyłeś : %s</h2>'%aname)
            aobj.Class.DoRegisterPackage('',aobj.OID,aname)
      if w:
         file.write('<h1>Serwer jest w trakcie procesu rejestracji. W zależności od wielkości paczek może to potrwać od kilku sekund do kilkunastu minut.</h1>')
      else:
         file.write('<h1>Brak paczek do rejestracji.</h1>')
#      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
#      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])



