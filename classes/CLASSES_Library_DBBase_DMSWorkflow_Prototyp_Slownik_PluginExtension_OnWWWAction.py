# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import icordbmain.adoutil as ADOLibInit
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
#   print 'obj - c:',aobj.Class.CID,aobj.Class.NameOfClass,'o:',aobj.OID,'u:',UID
   lparms=[
      [aobj.URLDocumentation,'Dokumentacja','/icormanager/images/icons/silk/icons/folder_page_white.png','/icormanager/images/icons/silk/icons/link_go.png'],
      [aobj.URLExamples,'Przykłady','/icormanager/images/icons/silk/icons/folder_picture.png','/icormanager/images/icons/silk/icons/link_go.png'],
      [aobj.URLHomePage,'Strona główna','/icormanager/images/icons/silk/icons/folder_home.png','/icormanager/images/icons/silk/icons/link_go.png'],
   ]
   for aurls,ainfo,afoldericon,aicon in lparms:
      durls=ICORUtil.ParseVars(aurls,{})
      w=0
      for atext,aurl in durls.items():
         if not w:
            d={'text':XMLUtil.GetAsXMLStringNoPL(ainfo)}
            d['icon']=afoldericon
            d['openIcon']=d['icon']
            xmlfile.TagOpen('tree',d)
            w=1
         d={'text':XMLUtil.GetAsXMLStringNoPL(atext),'action':aurl}
         d['icon']=aicon
         d['openIcon']=d['icon']
         d['action']=aurl
         xmlfile.TagOpen('tree',d,aclosetag=1)
      if w:
         xmlfile.TagClose('tree')

