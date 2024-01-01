# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
#   awwweditor.RegisterField('Nazwa',aoid=aoid)
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
      try:
         aobj.Class.DoGenerujPotwierdzeniaOdbioru(Value='SIGID')
         file.write('<h1>Potwierdzenia odbioru zostały wygenerowane</h1>')
      except:
         file.write('<h1><font color="red">Wystąpił błąd podczas generowania pliku z potwierdzeniami odbioru. Skontaktuj się z administratorem</font></h1>')
#      awwweditor.Write()
   return 2 # show back reference to main object (1-link, 2-button)

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


