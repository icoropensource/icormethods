# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:12:30

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil
import icorlib.projekt.mcrmbase as mcrmbase
from icorlib.projekt.mcrmxmlinterface import *

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None,avalue=''):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Wzorzec',adisplayed='Wzorzec zapytania',atype=mt_Memo,acols=112,arows=24,avalue=avalue)
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   file.write('<hr>')
   return 1

def GetCRMByDocument(aobj):
   pobj=aobj.Projekt
   acrm=mcrmbase.MCRM(pobj.Nazwa,acreatetables=0,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   acrm.PreProcess(pobj,adir)
   return acrm

def OnWWWAction(aobj,amenu,file):
   if amenu.Action=='ObjectApplyMethods':
      acrm=GetCRMByDocument(aobj)
      adocument=acrm.documents[aobj.OID]
      aresponse=CLASSES_Library_ICORBase_Interface_ICORUtil.Response()
      adocument.DumpAsXML(aresponse,{})
      axml=aresponse.AsText(aashtmlstring=0)
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None,axml)
      awwweditor.Write()
   return 1 # show back reference to main object

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      acrm=GetCRMByDocument(aobj)
      aparser=ICORXMLCRMQueryDefinitionParser(acrm)
      aparser.Parse(awwweditor['Wzorzec'])
      asql=aparser.AsSQL()
      file.write('<h1>Zapytanie SQL:</h1>')
      file.write('<pre>')
      aparser.querysql.AsHTML(file)
      file.write('</pre>')
#      file.write('<pre>%s</pre>'%CLASSES_Library_NetBase_Utils_XMLUtil.GetAsXMLStringNoPL(awwweditor['Wzorzec']))
      awwweditor.WriteObjectView(aobj,asbutton=1)



