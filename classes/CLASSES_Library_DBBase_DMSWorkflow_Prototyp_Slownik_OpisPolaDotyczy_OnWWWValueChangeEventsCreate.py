# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:14:59

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.projekt.msqllib as MSQLLib

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

def OnWWWAction(aobj,amenu,file):
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      aclass=aobj.Class
      aMaxDictValueLen,aDictValues,aDictValuesParents=MSQLLib.GetCSVDictValues(aobj.WartosciSlownika)
      levents=[]
      for akey,avalue in aDictValues:
         lvalue=aDictValuesParents.get(akey,['',])
         for bkey in lvalue:
            levents.append([bkey,akey])
      eobj=aobj.FieldEvents
      oevents=[]
      while eobj:
         if eobj.EventKind.EventName in ['SchedulerOnValueChange','ASPSourceOnValueChange']:
            afromvalue=eobj.EventFromValue
            oevents.append([afromvalue,eobj.EventToValue])
            if not afromvalue:
               oevents.append(['',eobj.EventToValue]) #'START'
         eobj.Next()
      eclass=aclass.FieldEvents.ClassOfType
      kclass=eclass.EventKind.ClassOfType
      koid=kclass.EventName.Identifiers('ASPSourceOnValueChange')
      lrefs=[]
      if koid>=0:
         for afromvalue,atovalue in levents:
            if not afromvalue:
               afromvalue='' #'START'
            if not [afromvalue,atovalue] in oevents:
               eoid=eclass.AddObject()
               eclass.EventKind[eoid]=[koid,kclass.CID]
               eclass.EventFromValue[eoid]=afromvalue
               eclass.EventToValue[eoid]=atovalue
               lrefs.append([eoid,eclass.CID])
         aclass.FieldEvents.AddRefs(aobj.OID,lrefs,ainsertifnotexists=1)
      if lrefs:
         file.write('<h3>Zdarzenia dodane<h3>')
      else:
         file.write('<h3>Brak zdarzeń do dodania<h3>')
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

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   OID=35617 # graf
   return
   aobj=aclass[OID]
   aMaxDictValueLen,aDictValues,aDictValuesParents=MSQLLib.GetCSVDictValues(aobj.WartosciSlownika)
   levents=[]
   for akey,avalue in aDictValues:
      lvalue=aDictValuesParents.get(akey,['',])
      for bkey in lvalue:
         levents.append([bkey,akey])
   eobj=aobj.FieldEvents
   oevents=[]
   while eobj:
      if eobj.EventKind.EventName in ['SchedulerOnValueChange','ASPSourceOnValueChange']:
         afromvalue=eobj.EventFromValue
         oevents.append([afromvalue,eobj.EventToValue])
         if not afromvalue:
            oevents.append(['START',eobj.EventToValue])
      eobj.Next()
   eclass=aclass.FieldEvents.ClassOfType
   kclass=eclass.EventKind.ClassOfType
   koid=kclass.EventName.Identifiers('ASPSourceOnValueChange')
   if koid>=0:
      lrefs=[]
      for afromvalue,atovalue in levents:
         if not afromvalue:
            afromvalue='START'
         if not [afromvalue,atovalue] in oevents:
            eoid=eclass.AddObject()
            eclass.EventKind[eoid]=[koid,kclass.CID]
            eclass.EventFromValue[eoid]=afromvalue
            eclass.EventToValue[eoid]=atovalue
            lrefs.append([eoid,eclass.CID])
      aclass.FieldEvents.AddRefs(OID,lrefs,ainsertifnotexists=1)

