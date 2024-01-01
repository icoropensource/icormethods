# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_WWW_Server_ICORWWWLib as ICORWWWLib

#   d={'text':XMLUtil.GetAsXMLString(CAPTION),'id':str(ID)}
#   ret.append(d)
def OnWWWContextMenu(aclass,afieldname,aoid,UID,brcid=-1,broid=-1):
   ret=ICORWWWLib.GetClassContextMenu(aclass,aoid,UID,brcid,broid)
   return ret

#   d={'action':'redirect','value':'LINK','text':XMLUtil.GetAsXMLString(CAPTION)}
#   ret.append(d)
def OnWWWContextMenuSubmit(aclass,afieldname,aoid,aid,UID,brcid=-1,broid=-1):
   ret=ICORWWWLib.GetClassContextMenuSubmit(aclass,aoid,aid,UID,brcid,broid)
   return ret
