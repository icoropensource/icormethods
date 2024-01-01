# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSummary as ICORSummary
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import *
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_NetBase_WWW_HTML_Office_OWC_ChartTypes_Util as OWCChartUtil
import random
import string

TRANS_FIELD={}
for i in range(0,256):
   TRANS_FIELD[chr(i)]=' '
for i in range(ord('a'),ord('z')+1):
   TRANS_FIELD[chr(i)]=chr(i)
for i in range(ord('A'),ord('Z')+1):
   TRANS_FIELD[chr(i)]=chr(i)
for i in range(ord('0'),ord('9')+1):
   TRANS_FIELD[chr(i)]=chr(i)
for c in 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ':
   TRANS_FIELD[c]=c

def GetOWCField(s):
   res=''
   for c in s:
      res=res+TRANS_FIELD[c]
   return res

class Summary2XMLData(ICORMDSpaceTableIterator):
   def __init__(self,asummary,aspace,file,ashowchart=1):
      ICORMDSpaceTableIterator.__init__(self,aspace)
      self.summary=asummary
      self.space=aspace
      self.file=file
      self._Fields=[]
   def FuncField(self,afield):
      acaption=ICORUtil.GetUniqueStringInContainer(GetOWCField(self.summary.ColumnsID[afield.Col-2].Caption),self._Fields,22,aadd=1)
      self.Fields.append([afield.Col,afield,afield.Field,self.summary.ColumnsID[afield.Col-2],acaption])
   def OnData(self,arow,acol):
      if (self.Value is None) or (acol<2) or (acol>(self.space.MaxCol-2)):
         return
      afield=self.Fields[acol-2][2]
      acolumn=self.Fields[acol-2][3]
      acaption=self.Fields[acol-2][4]
      self.fxml[acaption]=self.Value.DataValue
   def OnEndRow(self,arow):
      self.fxml.AddData()
   def GenerateAsXMLData(self,acnt):
      self.Fields=[]
      self.summary.Tree.ForEachField(self.FuncField)
      self.Fields.sort()
      self.Cols=[]
      self.fxml=XMLUtil.MXMLRecordset(self.file)
      try:
         self.fxml.Header()
         for acol,asummfield,afield,acolumn,acaption in self.Fields:
            self.Cols.append(acol)
            self.fxml.AddRow(aname=acaption,arsname=acaption,atype=afield.FieldTID)
         if acnt:
            self.ForEachNotEmptyRow()
      finally:
         pass
      self.fxml.close()
      return
   def GenerateAsOWCPivot(self,ashowchart=1):
      if 0:
         self.file.write('<a href="icormain.asp?jobtype=summaryexecute&OID=%d&XMLData=1">link do xmldata</a>'%(self.summary.summoid,))
      self.Fields=[]
      ashowchart=ashowchart and self.summary.ChartType>=0
      self.summary.Tree.ForEachField(self.FuncField)
      self.Fields.sort()
#      self.file.write('<hr>')
      srowfield=self.Fields[self.summary.PivotRowCol][4]
      scolumnfield=self.Fields[self.summary.PivotColumnCol][4]
      sdatafield=self.Fields[self.summary.PivotDataCol][4]
      sdataaxistotalfunction=ICORSummary.pes_fieldgroup[self.Fields[self.summary.PivotDataCol][3].PivotFieldGroupType]
      if not sdataaxistotalfunction:
         sdataaxistotalfunction='sum'
#      self.file.write('<h1>Row: %s</h1>'%(srowfield,))
#      self.file.write('<h1>Column: %s</h1>'%(scolumnfield,))
#      self.file.write('<h1>Data: %s</h1>'%(sdatafield,))
      d={
         'pivotid':random.randint(0,1000000),
         'datasource':'icormain.asp?jobtype=summaryexecute&OID=%d&XMLData=1&rv=%d'%(self.summary.summoid,random.randint(0,1000000)),
         'pivotcaption':self.summary.Name,
         'rowaxis':srowfield,
         'columnaxis':scolumnfield,
         'dataaxisfieldset':sdatafield,
         'dataaxis':sdatafield+' Total',
         'dataaxistotalfunction':sdataaxistotalfunction,
         'dataaxisnumberformat':'#',
         'charttitle':self.summary.Name,
         'charttype':self.summary.ChartType,
      }
      self.file.write("""
<BR>
<TABLE><CAPTION class='objectsviewcaption'>%(pivotcaption)s</CAPTION><TR><TD>
<object style="display:none" classid=CLSID:0002E530-0000-0000-C000-000000000046 id=MSODSC%(pivotid)s></object>
<object classid=clsid:0002E520-0000-0000-C000-000000000046 id="PTable%(pivotid)s"></object>
</TD></TR>
"""%d)
      if ashowchart:
         self.file.write("""
<TR><TD>
<HR>
<OBJECT CLASSID="clsid:0002E500-0000-0000-C000-000000000046" id="ChartSpace%(pivotid)s"></OBJECT>
</TD></TR>
<TR><TD>
<SELECT id=lstChartType%(pivotid)s>
"""%d)
         for aid,acharttype in OWCChartUtil.ChartTypes:
            if aid==self.summary.ChartType:
               ss='SELECTED '
            else:
               ss=''
            self.file.write('<OPTION %svalue=%d>%s</OPTION>'%(ss,aid,acharttype))
         self.file.write("""
</SELECT>
</TD></TR>
"""%d)
      self.file.write("""
</TABLE>

<SCRIPT LANGUAGE=VBScript>
'MSODSC%(pivotid)s.RecordsetDefs.AddNew "%(datasource)s", MSODSC%(pivotid)s.Constants.dscCommandFile
'Set Ptable%(pivotid)s.DataSource=MSODSC%(pivotid)s
'Ptable%(pivotid)s.DataMember=MSODSC%(pivotid)s.RecordsetDefs(0).Name
'Ptable%(pivotid)s.ActiveView.AutoLayout

PTable%(pivotid)s.ConnectionString = "provider=mspersist"
Ptable%(pivotid)s.CommandText = "%(datasource)s"

Ptable%(pivotid)s.BackColor="Ivory"
With Ptable%(pivotid)s.ActiveView
   .ColumnAxis.InsertFieldSet .FieldSets("%(columnaxis)s")
   .RowAxis.InsertFieldSet .FieldSets("%(rowaxis)s")
   aplfunction=Ptable%(pivotid)s.Constants.plFunctionSum
   if "%(dataaxistotalfunction)s"="sum" then
      aplfunction=Ptable%(pivotid)s.Constants.plFunctionSum
   elseif "%(dataaxistotalfunction)s"="count" then
      aplfunction=Ptable%(pivotid)s.Constants.plFunctionCount
   elseif "%(dataaxistotalfunction)s"="max" then
      aplfunction=Ptable%(pivotid)s.Constants.plFunctionMax
   elseif "%(dataaxistotalfunction)s"="min" then
      aplfunction=Ptable%(pivotid)s.Constants.plFunctionMin
   end if
   .DataAxis.InsertTotal .AddTotal("%(dataaxis)s", _
      .FieldSets("%(dataaxisfieldset)s").Fields(0), aplfunction)
   .Totals("%(dataaxis)s").NumberFormat = "%(dataaxisnumberformat)s"
   Ptable%(pivotid)s.AllowDetails = False
   '.Fieldsets("Rodzaj").Fields(0).SubTotals(1) = True
   .FilterAxis.Label.Visible = False
   Ptable%(pivotid)s.DisplayToolbar = True
   Ptable%(pivotid)s.AllowPropertyToolbox = True
   .TitleBar.Visible = False
   .TotalBackColor = "Ivory"
   .FieldLabelBackColor = "DarkBlue"
   .FieldLabelFont.Color = "White"
   .ColumnAxis.Fieldsets(0).Fields(0).SubTotalBackColor = "LightSteelBlue"
   .RowAxis.Fieldsets(0).Fields(0).SubTotalBackColor = "LightSteelBlue"
   .MemberBackColor = "Lavender"
End With
"""%d)
      if ashowchart:
         self.file.write("""
set c = ChartSpace%(pivotid)s.Constants
ChartSpace%(pivotid)s.Clear 

Set oChart = ChartSpace%(pivotid)s.Charts.Add
oChart.type = %(charttype)d 'c.chChartTypeColumnClustered
oChart.Interior.Color="Ivory"
oChart.HasLegend = true
oChart.Legend.Position = c.chLegendPositionRight
oChart.HasTitle = True
oChart.Title.Font.Bold = True
oChart.Title.Caption="%(charttitle)s"
Set ChartSpace%(pivotid)s.DataSource = PTable%(pivotid)s
oChart.SetData c.chDimSeriesNames, 0, c.chPivotColumns
oChart.SetData c.chDimCategories, 0, c.chPivotRows
oChart.SetData c.chDimValues, 0, 0

Sub lstChartType%(pivotid)s_onChange()
    Dim oChart
    Dim c
    Dim nChartType
    set c = ChartSpace%(pivotid)s.Constants
    Set oChart = ChartSpace%(pivotid)s.Charts(0)
    nChartType = CLng(lstChartType%(pivotid)s.value)
    oChart.Type = nChartType
End Sub
"""%d)
      self.file.write("""
</SCRIPT>
""")
      return

def GenerateAsXMLData(asummary,aspace,file,acnt):
   if not acnt:
      print 'empty data:',asummary.Name
   asummaryxml=Summary2XMLData(asummary,aspace,file)
   asummaryxml.GenerateAsXMLData(acnt)

def GenerateAsOWCPivot(asummary,aspace,file):
   asummaryxml=Summary2XMLData(asummary,aspace,file)
   asummaryxml.GenerateAsOWCPivot(ashowchart=1)



