# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:16:27

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
from icorlib.projekt.mcrmxmlinterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def GetCRMByDocument(aobj):
   pobj=aobj.Projekt
   acrm=mcrmbase.MCRM(pobj.Nazwa,acreatetables=0,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   acrm.PreProcess(pobj,adir)
   return acrm

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   if amenu.Action=='ObjectAdd':
      acrm=GetCRMByDocument(awwweditor.ParamObj)
      adocument=acrm.documents[awwweditor.ParamObj.OID]
      aresponse=ICORUtil.Response()
      adocument.DumpAsXML(aresponse,{})
      axml=aresponse.AsText(aashtmlstring=0)
      afield=awwweditor.Fields('XMLSource')
      afield.FieldValue=axml
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()


