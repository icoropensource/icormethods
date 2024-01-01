# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORChart import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import SimpleLinksHTMLTree

def OnBeforeSheetOutput(aclass,aoid,asheetid,file):
   pass

def OnBeforeFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   if afield.Name in ['Kreatory','Procedury']:
      return 0

def OnAfterFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   pass

def DoReportDrzewoKreatorow(aclass,aoid,file):
   atree=SimpleLinksHTMLTree('Kreatory')
   dobj=aclass[aoid]
   aobj=dobj.Kreatory
   while aobj:
      anode=atree.RootNode.AddNode(aobj.Nazwa,'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(aobj.CID,aobj.OID))
      pobj=aobj.Etapy
      while pobj:
         cnode=anode.AddNode(pobj.Nazwa,'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(pobj.CID,pobj.OID))
         pobj.Next()
      aobj.Next()
   atree.Write(file)

def DoReportDrzewoProcedur(aclass,aoid,file):
   atree=SimpleLinksHTMLTree('Lista procedur')
   aobj=aclass[aoid]
   pobj=aobj.Procedury
   while pobj:
      jobj=pobj.JednostkaOrganizacyjna
      if jobj:
         s=': '+jobj.Nazwa
      else:
         s=''
      bnode=atree.RootNode.AddNode(pobj.Symbol+s,'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(pobj.Class.CID,pobj.OID),aexpanded=1)
      cobj=pobj.Czynnosci
      while cobj:
         cnode=bnode.AddNode(cobj.Nazwa,'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(cobj.Class.CID,cobj.OID),aexpanded=1)
         cobj.Next()
      pobj.Next()
   atree.Write(file)

def OnAfterSheetOutput(aclass,aoid,asheetid,file,afields):
   if 'FieldName' in afields: #enter value here
      achart=ICORHTMLChartMSControl20(aclass,asheetid)
      achart.Title='' #enter value here
      achart.ChartType=VtChChartType2dBar
      achart.Stacked=0
      achart.Chart3D=1
      achart.AddColumn('Column1') #enter value here
      achart.AddColumn('Column2') #enter value here
      arow=1
      aobj=aclass[aoid]
      bobj=aobj.FieldName  #enter value here
      l=len(bobj)
      while bobj:
         achart.AddRow(bobj.FieldNameOfAxisValue)  #enter value here
         achart[arow,1]=str(bobj.Class.FieldNameValue1.ValuesAsFloat(bobj.OID)) #enter value here
         achart[arow,2]=str(bobj.Class.FieldNameValue2.ValuesAsFloat(bobj.OID)) #enter value here
         arow=arow+1
         bobj.Next()
      if l>0:
         achart.WriteToFile(file)
      return
   elif 'Kreatory' in afields:
      DoReportDrzewoKreatorow(aclass,aoid,file)
   elif 'Procedury' in afields:
      DoReportDrzewoProcedur(aclass,aoid,file)



