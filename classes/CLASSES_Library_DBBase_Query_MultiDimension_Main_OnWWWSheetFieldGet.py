# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORChart import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def OnBeforeSheetOutput(aclass,aoid,asheetid,file):
   pass

def OnBeforeFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   if afield.Name in ['UserLogInfo','UserComments',]:
      return 0

def OnAfterFieldOutput(aclass,afield,aoid,asheetid,file,afields):
   pass

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
   if 'SourceData' in afields:
      auid=GetUID()
      if auid<0:
         return
      uclass=aclass.UserLogInfo.ClassOfType
      uoid=uclass.AddObject()
      uclass.UserName[uoid]=aICORDBEngine.User.UserName[auid]
      uclass.Date.SetValuesAsDateTime(uoid,ICORUtil.tdatetime())
      aclass.UserLogInfo.AddRefs(aoid,[uoid,uclass.CID])
   if 'UserLogInfo' in afields:
      aobj=aclass[aoid]
      uobj=aobj.UserLogInfo
      uobj.Last()
      cnt=1
      while uobj and cnt<=100:
         adt=uobj.Class.Date.ValuesAsDateTime(uobj.OID)
         sc=string.replace('%3d'%cnt,' ','&nbsp;')
         file.write('<div class=commentheader>%s.&nbsp;&nbsp;%s&nbsp;%s&nbsp;-&nbsp;<font color="green">%s</font></div>'%(sc,ICORUtil.tdate2fmtstr(adt,longfmt=1),ICORUtil.ttime2fmtstr(adt,longfmt=1),uobj.UserName,))
         uobj.Prev()
         cnt=cnt+1
   if 'UserComments' in afields:
      aobj=aclass[aoid]
      cobj=aobj.UserComments
      cnt=1
      while cobj:
         adt=cobj.Class.Date.ValuesAsDateTime(cobj.OID)
         file.write('<div class=commentheader>%d.&nbsp;&nbsp;%s&nbsp;%s&nbsp;,&nbsp;%s&nbsp;&nbsp;-&nbsp;<font color="green"><i>%s</i></font></div>'%(cnt,ICORUtil.tdate2fmtstr(adt,longfmt=1),ICORUtil.ttime2fmtstr(adt,longfmt=1),cobj.UserName,cobj.Temat))
         file.write('<div class=commentbody>%s</div>'%(cobj.Comment,))
         cobj.Next()
         cnt=cnt+1



