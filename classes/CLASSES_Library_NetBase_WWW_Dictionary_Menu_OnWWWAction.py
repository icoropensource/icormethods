# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

"""
def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
#   awwweditor.RegisterFieldsDefault(aoid)
   if 1:
      awwweditor.RegisterField('Caption',aoid=aoid)
      awwweditor.RegisterField('AsPageCaption',aoid=aoid)
      awwweditor.RegisterField('AsPageSubCaption',aoid=aoid)
#      awwweditor.RegisterField('AsPageDescription',aoid=aoid)
      awwweditor.RegisterField('PageHTML',aoid=aoid,acols=80,arows=20)
#      awwweditor.RegisterField('PageHTMLInfo',aoid=aoid,acols=80,arows=20)
#   awwweditor.RegisterField('DateField',aoid=aoid)
#   awwweditor.RegisterField('ClassField',aoid=aoid,asubfields=['Nazwa'])
   return awwweditor

def OnWWWAction(aclass,amenu,file):
   if amenu.Action=='ObjectAdd':
      awwweditor=RegisterFields(aclass,amenu,file)
      awwweditor.Write(arefCID=aclass.CID)
   if amenu.Action=='ObjectEdit':
      pcid,poid,pfieldname=amenu.WWWParam
      print amenu.Action,pcid,poid,pfieldname
      awwweditor=RegisterFields(aclass,amenu,file,poid,None)
      awwweditor.Write(arefCID=pcid,arefOID=poid,arefField=pfieldname)
   if amenu.Action=='ObjectDelete':
      import CLASSES_Library_NetBase_WWW_Server_DoObjectEdit
      pcid,poid,pfieldname=amenu.WWWParam
      aclass=aICORDBEngine.Classes[pcid]
      gclass=aclass.MainRefField.ClassOfType #here: class reference from field
      joid=aclass[poid].MainRefField.OID #here object reference from field
      gclass.RefClassRefField.DeleteRefs(joid,[[poid,pcid],]) #here main class ref field delete object reference from objects list
      aclass.DeleteObject(poid)
      CLASSES_Library_NetBase_WWW_Server_DoObjectEdit.ProcessObjectEdit(file,gclass,joid,amenu.uid)

def OnWWWActionSubmit(aclass,amenu,areport,file):
   if amenu.Action in ['ObjectAdd','ObjectEdit']:
      awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
      aoid=awwweditor['refOID']
      w=1
#      w=w and awwweditor.CheckField('Caption',file)
#      w=w and awwweditor.CheckField('NumField',file)
#      w=w and awwweditor.CheckField('DateField',file)
#      w=w and awwweditor.CheckField('ClassField',file)
      if not w:
         file.write('<font color="red"><h2><u>Popraw dane i spróbuj jeszcze raz.</u></h2><hr></font>\n')
      else:
         if aoid<0:
            aoid=aclass.AddObject()
            isnew=1
         else:
            isnew=0
#         file.write('<a class=reflistoutnavy href="icormain.asp?jobtype=objectedit&CID=%d&OID=%d">Ostatnio zapamiętany obiekt</a><hr>'%(aclass.CID,aoid))
         aobj=aclass[aoid]
#         aclass.DateField.SetValuesAsDate(aoid,CLASSES_Library_ICORBase_Interface_ICORUtil.getStrAsDate(awwweditor['DateField']))


         aobj.Caption=awwweditor['Caption']
         aobj.AsPageCaption=awwweditor['AsPageCaption']
         aobj.AsPageSubCaption=awwweditor['AsPageSubCaption']
#         aobj.AsPageDescription=awwweditor['AsPageDescription']
         aobj.PageHTML=awwweditor['PageHTML']
#         aobj.PageHTMLInfo=awwweditor['PageHTMLInfo']

#         aobj.NumField=awwweditor['NumField']
#         aobj.StringField=awwweditor['StringField']
#         aobj.ClassField=awwweditor['ClassField']
#         jobj=aobj.ClassRefField #here field with backward class reference
#         jobj.Class.RefClassRefField.AddRefs(jobj.OID,[[aoid,aclass.CID],],jobj.Class.RefClassRefField.ClassOfType.ClassSortField,aremoveexisting=1) # here RefClassRefField and ClassSortField insert into ref objects list sorted by class sort field
#         aclass.OnObjectChanged('',aoid,'') # if needed
      file.write(aobj.PageHTML)
#      awwweditor.Write()

"""
