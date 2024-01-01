# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:17:10

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
import CLASSES_Library_ICORBase_Interface_ICORUtil

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Publikuj dane',atype=mt_Boolean,avalue='1')
   #awwweditor.RegisterField('Field2',adisplayed='Publikuj załączniki',atype=mt_Boolean,avalue='1')
   awwweditor.RegisterField('Field3',adisplayed='Publikuj szablon',atype=mt_Boolean,avalue='1')
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
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      #wdane,wzalaczniki,wszablon=ICORUtil.str2bool(awwweditor['Field1']),ICORUtil.str2bool(awwweditor['Field2']),ICORUtil.str2bool(awwweditor['Field3'])
      wdane,wszablon=ICORUtil.str2bool(awwweditor['Field1']),ICORUtil.str2bool(awwweditor['Field3'])
      sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      wobj=None
      bobj=aobj.AsObject()
      while not wobj and bobj:
         wobj=bobj.Struktura
         bobj=bobj.NadRozdzial
      rclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
      if wdane and wobj: # or wzalaczniki:
         #sclass.Main('0',toid,'$'+str(aobj.OID))
         rclass.DoSetChapterState(str(wobj.OID),aobj.OID,'',amenu.uid)
         file.write('<h3>Zlecenie generowania danych zostało dołączone do kolejki.</h3><br>')
      if wszablon:
         apriority='N03'
         prefs=rclass.Priorytet.GetRefList(aobj.OID)
         if prefs:
            apriority=prefs.Nazwa[prefs.OID]
         rclass.DoGenerateTemplate(str(wobj.OID),aobj.OID,'',amenu.uid,apriority=apriority)
      file.write('<h3>Zlecenie generowania szablonu zostało dołączone do kolejki.</h3>')
#      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
#      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
#      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])

