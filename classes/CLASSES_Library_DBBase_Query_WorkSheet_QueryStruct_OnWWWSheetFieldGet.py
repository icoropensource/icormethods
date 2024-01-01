# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORChart import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import SimpleLinksHTMLTree

def OnBeforeSheetOutput(aclass,aoid,asheetid,file):
   pass

def OnBeforeFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   if afield.Name in ['Query',]:
      return 0

def OnAfterFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   pass

def DoSubQueryAdd(anode,aobj):
   while aobj:
      s=aobj.TableID
      if s:
         s='<font color="green">'+s+'</font> '
      s=s+aobj.TableTitle
      bnode=anode.AddNode(s,'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(aobj.CID,aobj.OID),asorted=1) #enter value here
      pobj=aobj.SubQuery
      if pobj:
         DoSubQueryAdd(bnode,pobj)
      aobj.Next()

def DoTreeReport(aclass,aoid,file):
   atree=SimpleLinksHTMLTree('Podzestawienia') #enter value here
   dobj=aclass[aoid]
   aobj=dobj.Query #enter value here
   if aobj:
      DoSubQueryAdd(atree.RootNode,aobj)
      atree.Write(file)

def OnAfterSheetOutput(aclass,aoid,asheetid,file,afields):
   if 'FIELD_CHART' in afields: #enter value here
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
   elif 'Query' in afields:
      DoTreeReport(aclass,aoid,file)



