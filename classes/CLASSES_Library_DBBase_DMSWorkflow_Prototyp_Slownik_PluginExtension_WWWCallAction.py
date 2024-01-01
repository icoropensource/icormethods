# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:15:33

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.projekt.mcrmbasesimple as MCRMBaseSimple

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Nazwa',aoid=aoid)
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

def OnWWWActionGetLink(aobj,amenu):
   ret=''
   bclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Component_Plugin']
   if amenu.BackRefCID==bclass.CID and amenu.BackRefOID>=0:
      ret=aobj.ActionURLParms
   return ret

def OnWWWAction(aobj,amenu,file):
   bclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Component_Plugin']
   if amenu.BackRefCID==bclass.CID and amenu.BackRefOID>=0:
      lobj=bclass[amenu.BackRefOID]
      sobj=lobj.Struktura
      pobj=sobj.Projekt
      aSimpleCMS=MCRMBaseSimple.CMS()
      acmsproject=aSimpleCMS.GetProject(pobj)
      aCMSWWWMenuStruct=acmsproject.GetWWWMenuStruct(sobj)
      aPlugin=aCMSWWWMenuStruct.GetPlugin(lobj)
      ret=aPlugin.ProcessExtensionAction(aobj)
      file.write(ret)
#      file.write('<html><body><h1>aaa</h1><p>aaaaaa bakdjas kdj dhalskdjh alskdhaslkdjh</p></body></html>')
   else:
      file.write('<html><body><font color=red><h1>Uruchomienie tylko z poziomu wtyczki.</h1></font></body></html>')
   return 0
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
#   if amenu.Action=='ObjectApplyMethods':
#      awwweditor.Write()
#   return 2 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 0</h1>')
      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])
