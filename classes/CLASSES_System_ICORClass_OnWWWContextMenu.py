# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_WWW_Server_ICORWWWLib as ICORWWWLib

DCMENU=[
   {'text':'Wszystkie obiekty'},
   {'text':'Dodaj menu dla edycji obiektów'},
   {'text':'Dodaj menu dla kasowania obiektów'},
   {'text':'Dodaj menu dla uruchamiania metod'},
   {'text':'Właściwości pól'},
]

#   d={'text':XMLUtil.GetAsXMLString(CAPTION),'id':str(ID)}
#   ret.append(d)
def OnWWWContextMenu(aclass,afieldname,aoid,UID,brcid=-1,broid=-1):
   ret=ICORWWWLib.GetClassContextMenu(aclass,aoid,UID,brcid,broid)
   aid=len(ret)+1
   for d1 in DCMENU:
      d2={}
      d2.update(d1)
      d2['id']=str(aid)
      ret.append(d2)
      aid=aid+1
   return ret

#   d={'action':'redirect','value':'LINK','text':XMLUtil.GetAsXMLString(CAPTION)}
#   ret.append(d)
def OnWWWContextMenuSubmit(aclass,afieldname,aoid,aid,UID,brcid=-1,broid=-1):
   ret=ICORWWWLib.GetClassContextMenuSubmit(aclass,aoid,aid,UID,brcid,broid)
   return ret

