# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_NetBase_WWW_Server_DoObjectEdit import ProcessObjectEdit
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Name',aoid=aoid)
   awwweditor.RegisterField('FromAccount',aoid=aoid)
   awwweditor.RegisterField('ToAccount',aoid=aoid)
   awwweditor.RegisterField('AccountMask',aoid=aoid)
   awwweditor.RegisterField('AccountInheritedMask',aoid=aoid)
   return awwweditor

def OnWWWAction(aclass,amenu,file):
   if amenu.Action=='ObjectEdit':
      pcid,poid,pfieldname=amenu.WWWParam
      awwweditor=RegisterFields(aclass,amenu,file,poid,None)
      awwweditor.Write(arefCID=pcid,arefOID=poid,arefField=pfieldname)

def OnWWWActionSubmit(aclass,amenu,areport,file):
   if amenu.Action in ['ObjectAdd','ObjectEdit']:
      awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
      aoid=awwweditor['refOID']
      w=1
      if aoid<0:
         aoid=aclass.AddObject()
         isnew=1
      else:
         isnew=0
      aobj=aclass[aoid]
      aobj.Name=awwweditor['Name']
      aobj.FromAccount=awwweditor['FromAccount']
      aobj.ToAccount=awwweditor['ToAccount']
      aobj.AccountMask=awwweditor['AccountMask']
      aobj.AccountInheritedMask=awwweditor['AccountInheritedMask']
      ProcessObjectEdit(file,aclass,aoid,amenu.uid)
   else:
      file.write('<h1>Nierozpoznana akcja</h1>')



