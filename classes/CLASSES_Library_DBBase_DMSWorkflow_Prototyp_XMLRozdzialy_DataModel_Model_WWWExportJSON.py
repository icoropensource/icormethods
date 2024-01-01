# -*- coding: windows-1250 -*-
# saved: 2023/04/07 22:15:03

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

import icorupgrade.exportimportjson as exportimportjson

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('indent',adisplayed='Czy formatować dane',atype=mt_Bool,avalue='1')
   awwweditor.RegisterField('backref',adisplayed='Czy eksportować obiekty BackRef',atype=mt_Bool,avalue='')
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
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
   aindent=ICORUtil.str2bool(awwweditor['indent'])
   abackref=ICORUtil.str2bool(awwweditor['backref'])
   exportimportjson.ExportJSON(aobj=aobj,UID=amenu.uid,aindent=aindent,abackref=abackref,file=file)

