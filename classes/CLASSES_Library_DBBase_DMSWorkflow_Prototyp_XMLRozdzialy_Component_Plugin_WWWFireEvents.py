# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:16:47

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_ICORBase_External_MLog as MLog

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

def MainI(uobj):
   ret=''
   sobj=uobj.Struktura
   pobj=sobj.Projekt
   aproject=pobj.Nazwa
   acrm=mcrmbase.MCRM(aproject,acreatetables=0,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   asqldir=FilePathAsSystemPath('%ICOR%/sql/'+aproject)
   if not os.path.exists(asqldir):
      os.makedirs(asqldir)
   acrm.PreProcess(pobj,adir)
   acrm.Table_Kreator=acrm.ProcessKreatory()
#   acrm.ProcessBazyZrodlowe(tobj.TabeleZrodlowe)
#   acrm.ProcessPages(tobj.ProjectPageHTML)
#   acrm.ProcessWizards(tobj.Kreatory)
#   acrm.ProcessNewsletters(pobj.ListyWysylkowe)
   wobj=sobj.AsObject()
   if wobj:
      while wobj:
         acrm.ProcessBazyZrodlowe(wobj.TabeleZrodlowe)
         wobj.Next()
      acrm.ProcessWWWMenuStruct(sobj.AsObject())
#   acrm.ProcessUserTSQL(tobj.UserTSQL)
   for awwwmenustruct in acrm.wwwmenustruct:
      if awwwmenustruct.OID==sobj.OID:
         ret=awwwmenustruct.ProcessEventsInternal('OnCMSWrite',dd=None,akey='',asinglepluginoid=uobj.OID)
#   acrm.Write()
#   acreatesp=tobj['GenerujSP']
#   acreatevar=tobj['GenerujVar']
#   acrm.CreateTables(asqldir=FilePathAsSystemPath('%ICOR%/sql/'+aproject),aservercreate=acreatetables,acreatesp=acreatesp,acreatevar=acreatevar)
#   tobj.Class.DataOstatniegoGenerowania.SetValuesAsDateTime(tobj.OID,CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime())
   return ret

def OnWWWAction(aobj,amenu,file):
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      saveout=MLog.MemorySysOutWrapper()
      try:
         ret=MainI(aobj)
      finally:
         ret=saveout.read()
         saveout.Restore()
      file.write('<pre>')
      file.write(ret)
      file.write('</pre>')
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
