# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:15:14

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.projekt.msqllib as MSQLLib
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Pola',adisplayed='Opisy stanów',atype=mt_Memo,avalue='')
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
   return ''

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 2 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
   aMaxDictValueLen,aDictValues,aDictValuesParents=MSQLLib.GetCSVDictValues(awwweditor['Pola'])
   eclass=aobj.Class.FieldEvents.ClassOfType
   kclass=eclass.EventKind.ClassOfType
   koid=kclass.EventName.Identifiers('ASPSourceOnValueGetInfo')
   lrefs=[]
   if koid>=0:
      for akey,avalue in aDictValues:
         eoid=eclass.AddObject()
         eclass.EventKind[eoid]=[koid,kclass.CID]
         eclass.EventFromValue[eoid]=akey
         avalue=string.replace(avalue,'&amp;#10;','<br>')
         avalue=string.replace(avalue,'&#10;','<br>')
         eclass.EventSource[eoid]=avalue
         lrefs.append([eoid,eclass.CID])
      if lrefs:
         aobj.Class.FieldEvents.AddRefs(aobj.OID,lrefs,ainsertifnotexists=1)
         file.write('<h3>Zdarzenia dodane<h3>')
      else:
         file.write('<h3>Brak zdarzeń do dodania<h3>')
   awwweditor.WriteObjectView(aobj,asbutton=1)

