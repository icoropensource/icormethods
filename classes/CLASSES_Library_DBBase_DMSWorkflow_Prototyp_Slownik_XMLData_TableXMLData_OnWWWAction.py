# -*- coding: windows-1250 -*-
# saved: 2023/03/11 16:10:41

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
from icorlib.projekt.mcrmxmlinterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import string

def GetCRMByItem(aobj):
   pobj=aobj.Projekt
   acrm=mcrmbase.MCRM(pobj.Nazwa,acreatetables=0,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   acrm.PreProcess(pobj,adir)
   return acrm

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   if amenu.Action=='ObjectAdd':
      acrm=GetCRMByItem(awwweditor.ParamObj)
      asrctable=acrm.sourcetables[awwweditor.ParamObj.OID]
      aresponse=ICORUtil.Response()
      asrctable.DumpAsXML(aresponse,{'_MAX_TABLE_RECUR':3})
      axml=aresponse.AsText(aashtmlstring=0)
      afield=awwweditor.Fields('XMLSource')
      afield.FieldValue=axml
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   pobj=aobj.Dotyczy.Projekt
   acrmpath=pobj.AppPath+'/'

   d={'text':XMLUtil.GetAsXMLStringNoPL('Obsługa XML'),
      'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
      'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
   }
   xmlfile.TagOpen('tree',d)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Jako wyszukiwarka'),
      'action':acrmpath+'xmldata_BZR_%d_sv.asp'%(aobj.OID,)
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   #d={'text':XMLUtil.GetAsXMLStringNoPL('Jako Pivot'),
   #   'action':acrmpath+'xmldata_BZR_%d.asp'%(aobj.OID,)
   #}
   #xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Jako edytor'),
      'action':acrmpath+'xmldata_BZR_%d_au.asp'%(aobj.OID,)
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   xmlfile.TagClose('tree')

