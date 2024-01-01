# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_NetBase_WWW_Server_DoObjectEdit import ProcessObjectEdit
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Name',aoid=aoid)
   awwweditor.RegisterField('FromDate',aoid=aoid)
   awwweditor.RegisterField('ToDate',aoid=aoid)
   awwweditor.RegisterField('MultiplyBy',aoid=aoid,aempty='0.0')
   awwweditor.RegisterField('ShowWn',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowMa',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowBOWn',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowBOMa',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowObrotyWn',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowObrotyMa',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowSaldoWn',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowSaldoMa',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowSaldoObrotyWn',aoid=aoid,asubfields=['Name'])
   awwweditor.RegisterField('ShowSaldoObrotyMa',aoid=aoid,asubfields=['Name'])
   return awwweditor

def OnWWWAction(aclass,amenu,file):
   if amenu.Action=='ObjectEdit':
      pcid,poid,pfieldname=amenu.WWWParam
      awwweditor=RegisterFields(aclass,amenu,file,poid,None)
      awwweditor.Write(arefCID=pcid,arefOID=poid,arefField=pfieldname)

def OnWWWActionSubmit(aclass,amenu,areport,file):
   if amenu.Action in ['ObjectEdit']:
      awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
      aoid=awwweditor['refOID']
      w=1
      w=w and awwweditor.CheckField('FromDate',file)
      w=w and awwweditor.CheckField('ToDate',file)
      w=w and awwweditor.CheckField('MultiplyBy',file)
      if not w:
         file.write('<font color="red"><h2><u>Popraw dane i spróbuj jeszcze raz.</u></h2><hr></font>\n')
         file.write('<a class=reflistoutnavy href="icormain.asp?jobtype=objectedit&CID=%d&OID=%d">Ostatnio edytowany obiekt</a><hr>'%(aclass.CID,aoid))
      else:
         aobj=aclass[aoid]
         aobj.Name=awwweditor['Name']

         aobj.FromDate=awwweditor['FromDate']
         aobj.ToDate=awwweditor['ToDate']
         aobj.MultiplyBy=awwweditor['MultiplyBy']

         aobj.ShowWn=awwweditor['ShowWn']
         aobj.ShowMa=awwweditor['ShowMa']
         aobj.ShowBOWn=awwweditor['ShowBOWn']
         aobj.ShowBOMa=awwweditor['ShowBOMa']
         aobj.ShowObrotyWn=awwweditor['ShowObrotyWn']
         aobj.ShowObrotyMa=awwweditor['ShowObrotyMa']
         aobj.ShowSaldoWn=awwweditor['ShowSaldoWn']
         aobj.ShowSaldoMa=awwweditor['ShowSaldoMa']
         aobj.ShowSaldoObrotyWn=awwweditor['ShowSaldoObrotyWn']
         aobj.ShowSaldoObrotyMa=awwweditor['ShowSaldoObrotyMa']
         ProcessObjectEdit(file,aclass,aoid,amenu.uid)



