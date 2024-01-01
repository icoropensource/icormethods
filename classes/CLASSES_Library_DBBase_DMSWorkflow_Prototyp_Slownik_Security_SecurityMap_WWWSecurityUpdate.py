# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import CLASSES_Library_ICORBase_Replication_Security_DoLoad as SecurityLoad
import cStringIO

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   svalue=''
   if areport is None:
      bfile=cStringIO.StringIO()
      asecprofile=ICORSecurity.ICORSecurityProfile()
      asecprofile.SetByUser(amenu.uid)
      asecprofile.DumpXML(bfile)
      svalue=bfile.getvalue()
      bfile.close()
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
#   awwweditor.RegisterField('Nazwa',aoid=aoid)
   awwweditor.RegisterField('Ustawienia',adisplayed='Ustawienia',atype=mt_Memo,avalue=svalue)
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
      asecload=SecurityLoad.ICORXMLSecurityReplicationParser()
      asecload.Parse(awwweditor['Ustawienia'])
      file.write('<pre>')
      asecload.Dump(file,anoprint=1)
      file.write('</pre>')
      awwweditor.WriteObjectView(aobj,asbutton=1)



