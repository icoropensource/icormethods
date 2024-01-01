# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Name',aoid=aoid)
   awwweditor.RegisterField('LogBaseDirPath',aoid=aoid)
   awwweditor.RegisterField('LogFileMask',aoid=aoid)
   return awwweditor

def OnWWWAction(aclass,amenu,file):
   if amenu.Action=='ObjectAdd':
      awwweditor=RegisterFields(aclass,amenu,file)
      awwweditor.Write(arefCID=aclass.CID)
   if amenu.Action=='ObjectEdit':
      pcid,poid,pfieldname=amenu.WWWParam
      awwweditor=RegisterFields(aclass,amenu,file,poid,None)
      awwweditor.Write(arefCID=pcid,arefOID=poid,arefField=pfieldname)
   if amenu.Action=='ObjectDelete':
      pcid,poid,pfieldname=amenu.WWWParam
      aclass=aICORDBEngine.Classes[pcid]
#      gclass=aclass.Gmina.ClassOfType
#      gclass.JednostkiOrganizacyjne.DeleteRefs(gclass.FirstObject(),[[poid,pcid],])
      aclass.DeleteObject(poid)
      file.write('<h2>Obiekt został skasowany</h2>')
#      import CLASSES_Library_NetBase_WWW_Server_DoObjectEdit
#      CLASSES_Library_NetBase_WWW_Server_DoObjectEdit.ProcessObjectEdit(file,gclass,gclass.FirstObject(),amenu.uid)
   
def OnWWWActionSubmit(aclass,amenu,areport,file):
   if amenu.Action in ['ObjectAdd','ObjectEdit']:
      awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
      aoid=awwweditor['refOID']
      w=1
      w=w and awwweditor.CheckField('Name',file)
      w=w and awwweditor.CheckField('LogBaseDirPath',file)
      if not w:
         file.write('<font color="red"><h2><u>Popraw dane i spróbuj jeszcze raz.</u></h2><hr></font>\n')
      else:
         if aoid<0:
            aoid=aclass.AddObject()
            isnew=1
         else:
            isnew=0
         file.write('<a class="fg-button-single ui-state-default ui-corner-all uihover" href="icormain.asp?jobtype=objectedit&CID=%d&OID=%d">Ostatnio zapamiętany obiekt</a><hr>'%(aclass.CID,aoid))
         aobj=aclass[aoid]
         aobj.Name=awwweditor['Name']
         aobj.LogBaseDirPath=awwweditor['LogBaseDirPath']
         aobj.LogFileMask=awwweditor['LogFileMask']
      awwweditor.Write()



