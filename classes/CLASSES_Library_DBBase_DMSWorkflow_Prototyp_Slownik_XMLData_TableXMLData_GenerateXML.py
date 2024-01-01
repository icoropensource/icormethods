# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:16:34

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil
import icorlib.projekt.mcrmbase as mcrmbase
from icorlib.projekt.mcrmxmlinterface import *

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def GetCRMByItem(aobj):
   pobj=aobj.Projekt
   acrm=mcrmbase.MCRM(pobj.Nazwa,acreatetables=0,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   acrm.PreProcess(pobj,adir)
   return acrm

def OnWWWAction(aobj,amenu,file):
#   awwweditor=RegisterFields(aclass,amenu,file)
   if amenu.Action=='ObjectApplyMethods':
      acrm=GetCRMByItem(aobj.Dotyczy)
      aparser=ICORXMLCRMQueryDefinitionParser(acrm)
      aparser.Parse(aobj.XMLSource)
      asql=aparser.AsSQL()
      if aparser.querysql.OutputType=='owc pivot':
         file.write('<h1>Zapytanie SQL wykorzystane w tabeli przestawnej:</h1>')
         aparser.querysql.AsHTML(file)
         axmldata=mcrmbase.XMLData(acrm)
         axmldata.Process(aobj,anamemodifier='BZR')
         axmldata.Write(acrm.BaseDirectory,aoverrideautogenerate=1)
         ahref=acrm.AppPath+axmldata.PageFile+'.asp'
         file.write('<A class=reflistoutnavy href="%s">Tabela przestawna</A>'%ahref)
      elif aparser.querysql.OutputType=='owc chart':
         file.write('<h1>Zapytanie SQL:</h1>')
         aparser.querysql.AsHTML(file)
      else:
         file.write('<h1>Zapytanie SQL:</h1>')
         aparser.querysql.AsHTML(file)
#      awwweditor.Write()
   return 1 # show back reference to main object

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


