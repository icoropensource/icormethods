# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      file.write('<h1>Zestawienie:</h1>')
      file.write('<h3><i>%s</i></h3>'%aobj.Title)
      file.write('<h3><i>%s</i></h3>'%aobj.Name)
      file.write('<h3><i>%s</i></h3>'%aobj.SubTitle)
      awwweditor.Write(acaption='Nagraj na dysk',amimesave='zestawienie.xls')
   return 0

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      auid=GetUID()
      if auid>=0:
         uclass=aobj.Class.UserLogInfo.ClassOfType
         uoid=uclass.AddObject()
         uclass.UserName[uoid]=aICORDBEngine.User.UserName[auid]
         uclass.Date.SetValuesAsDateTime(uoid,ICORUtil.tdatetime())
         aobj.Class.UserLogInfo.AddRefs(aobj.OID,[uoid,uclass.CID])
      file.write(aobj.SourceData)



