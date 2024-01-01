# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   return

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   return

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
   return

def OnWWWGetFieldAutoCompleteValues(aobj,afield):
   if afield.Name in ['XXX']:
      return aobj._backreffield._referencedfield
   return

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
#   print 'T:',aobj.Class.CID,aobj.Class.NameOfClass,'o:',aobj.OID,'u:',UID
   pobj=aobj.Projekt
   acrmpath=pobj.AppPath+'/'

   d={'text':XMLUtil.GetAsXMLStringNoPL('Obsługa strony'),
      'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
      'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
   }
   xmlfile.TagOpen('tree',d)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Strona'),
      'action':acrmpath+'page_%d.asp'%(aobj.OID,)
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   xmlfile.TagClose('tree')

