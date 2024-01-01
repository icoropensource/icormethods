# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Publikuj dane',atype=mt_Boolean,avalue='1')
   #awwweditor.RegisterField('Field2',adisplayed='Publikuj załączniki',atype=mt_Boolean,avalue='1')
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
      file.write('<h1>Publikowanie w toku</h1>')

#      kclass=aICORDBEngine.Classes['CLASSES_System_SystemDictionary_External_DaemonParameters']
      sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      if 0:
         toid=-1
         tobj=aobj.TabelaZrodlowa
         if tobj:
            toid=tobj.OID
         sclass.Main('0',toid,'$'+str(aobj.OID))
         try:
            lmr=aICORDBEngine.SysBase.ExecutorMethodGetReadyList()
            lmp=aICORDBEngine.SysBase.ExecutorMethodGetProcessingList()
            file.write('<b>Zlecenie zostało dołączone do kolejki. Ilość zadań przetwarzanych %d, ilość zadań w kolejce: %d </b><br>'%(len(lmp),len(lmr),))
         except:
            print '$$ pobranie danych o kolejce zadan - rozdzial'
      else:
         wobj=None
         bobj=aobj.AsObject()
         while not wobj and bobj:
            wobj=bobj.Struktura
            bobj=bobj.NadRozdzial
         if wobj:
            rclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
            rclass.DoSetChapterState(str(wobj.OID),aobj.OID,'',amenu.uid)
            file.write('<h3>Zlecenie generowania danych zostało dołączone do kolejki.</h3><br>')
         else:
            file.write('<h3>UWAGA: zlecenie generowania danych nie zostało dołączone do kolejki.</h3><br>')

#      file.write('<h1>Step 0</h1>')
#      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
#      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
#      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])


