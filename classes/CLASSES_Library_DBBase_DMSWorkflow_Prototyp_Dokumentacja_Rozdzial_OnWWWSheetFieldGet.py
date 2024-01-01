# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORChart import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import SimpleLinksHTMLTree

def OnBeforeSheetOutput(aclass,aoid,asheetid,file):
   pass

def OnBeforeFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   if afield.Name in ['NadRozdzial','PodRozdzialy','Publikacja']:
      return 0

def OnFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   if afield.Name=='Tresc':
      file.write('</table><table width="100%%"><tr><td class=objectseditdatafieldvalue>%s</td></tr></table><table>'%(afield[aoid]))
      return 0
   if afield.Name=='Tytul':
      file.write('</table><table width="100%%"><tr><td class=objectseditdatafieldvalue><h1>%s</h1><hr></td></tr></table><table>'%(afield[aoid]))
      return 0

def OnAfterFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   pass

def DoTreeReport(aclass,aoid,file):
   atree=SimpleLinksHTMLTree('MAIN_FIELD') #enter value here
   dobj=aclass[aoid]
   aobj=dobj.RECUR_FIELD_1 #enter value here
   while aobj:
      anode=atree.RootNode.AddNode(aobj.NAME_FIELD_1,'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(aobj.CID,aobj.OID)) #enter value here
      pobj=aobj.RECUR_FIELD_2 #enter value here
      while pobj:
         cnode=anode.AddNode(pobj.NAME_FIELD_2,'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(pobj.CID,pobj.OID)) #enter value here
         pobj.Next()
      aobj.Next()
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
   elif 'FIELD_TREE' in afields:
      DoTreeReport(aclass,aoid,file)
