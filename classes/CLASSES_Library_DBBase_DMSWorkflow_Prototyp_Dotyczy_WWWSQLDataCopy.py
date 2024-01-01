# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy_XMLProcessLib as XMLProcessLib
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import os

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Uruchom',adisplayed='Uruchom eksport danych',atype=mt_Bool,avalue='')
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

def OnWWWAction(aobj,amenu,file):
#   file.write('<h1>Funkcja nieaktywna</h1>')
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      if ICORUtil.str2bool(awwweditor['Uruchom']):
         apath=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)
         adir=aobj.Projekt.AppPath
         if adir[-1:]!='/':
            adir=adir+'/'
         adir=adir+'XMLData'
         if not os.path.exists(apath+adir):
            os.makedirs(apath+adir)
         afilename='table_%d_%s.xml'%(aobj.OID,ICORUtil.tdatetime2fmtstr(adelimiter='',atimedelimiter='',apartdelimiter='-'))
         ret=XMLProcessLib.Main(aobj.OID,apath+adir+'/'+afilename)
         if ret:
            file.write('<h1>Dane wygenerowane poprawnie.</h1>')
            file.write('<a href="/icormanager/%s">Plik XML z danymi do pobrania</a>'%(adir+'/'+afilename))
         else:
            file.write('<h1>Wystąpił problem z generowaniem danych. Skontaktuj się z administratorem systemu.</h1>')
         file.write('<br><br>')
      awwweditor.WriteObjectView(aobj,asbutton=1)
#      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
#      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])


