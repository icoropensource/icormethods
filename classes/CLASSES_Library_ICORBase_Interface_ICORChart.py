# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import *
import random
import types

################################################################
# MSChart Control v2.0 - HTML Version
################################################################

VtChChartType3dBar,VtChChartType2dBar,VtChChartType3dLine=0,1,2
VtChChartType2dLine,VtChChartType3dArea,VtChChartType2dArea=3,4,5
VtChChartType3dStep,VtChChartType2dStep,VtChChartType3dCombination=6,7,8
VtChChartType2dCombination,VtChChartType2dPie,VtChChartType2dXY=9,14,16

VtChSeriesTypeVaries,VtChSeriesTypeDefault=-2,-1
VtChSeriesType3dBar,VtChSeriesType2dBar,VtChSeriesType3dLine=0,1,5
VtChSeriesType2dLine,VtChSeriesType3dArea,VtChSeriesType3dStep=6,7,9
VtChSeriesType2dStep,VtChSeriesType2dXY,VtChSeriesType2dPie=10,11,24

# MSChart20Lib.MSChart.2
# clsid:3A2B370C-BA0A-11D1-B137-0000F8753F5D

class ICORHTMLChartMSControl20:
   def __init__(self,aclass=None,achartid=-1):
      self.ClassItem=aclass
      if achartid<0:
         achartid=random.randint(0,10000000)
      self.ChartID='Chart'+str(achartid)
      self.ChartType=VtChChartType2dBar
      self.Stacked=0
      self.Chart3D=0
      self.ShowLegend=1
      self.Title=''
      self.FootnoteText=''
      self.Columns={}
      self.ColumnsByName={}
      self.ColumnCount=0
      self.Rows={}
      self.RowsByName={}
      self.RowCount=0
      self.Data={}
      self.FrameStyle=0
      self.AsSinglePage=0
      self.DisableAxisGrid=0
   def __setitem__(self,key,value):
      arow,acol=key
      if isinstance(arow,types.StringTypes):
         rname=arow
         arow=self.RowsByName.get(rname,-1)
         if arow<0:
            arow=self.AddRow(rname)
      if arow>self.RowCount:
         self.RowCount=arow
      if isinstance(acol,types.StringTypes):
         rname=acol
         acol=self.ColumnsByName.get(rname,-1)
         if acol<0:
            acol=self.AddColumn(rname)
      if acol>self.ColumnCount:
         self.ColumnCount=acol
      adata=self.Data.get(acol,{})
      adata[arow]=value
      self.Data[acol]=adata
   def AddColumn(self,aname):
      self.ColumnCount=self.ColumnCount+1
      self.Columns[self.ColumnCount]=aname
      self.ColumnsByName[aname]=self.ColumnCount
      return self.ColumnCount
   def AddRow(self,aname):
      self.RowCount=self.RowCount+1
      self.Rows[self.RowCount]=aname
      self.RowsByName[aname]=self.RowCount
      return self.RowCount
   def WriteToFile(self,file):
      self.WriteObject(file)
      self.WriteInit(file)
   def WriteObject(self,file):
      s="""
<table>
<tr>
   <td></td>
   <td><img style="cursor:pointer" onclick="javascript:if(%(ChartID)s.height<200){%(ChartID)s.height=200;}else{%(ChartID)s.height=%(ChartID)s.height-25;}" src="images/arrow4_up.gif" alt="zwiększ rozmiar pionowo"></td>
   <td></td>
</tr>
<tr>
   <td><img style="cursor:pointer" onclick="javascript:if(%(ChartID)s.width<320){%(ChartID)s.width=300;}else{%(ChartID)s.width=%(ChartID)s.width-50}" src="images/arrow4_left.gif" alt="zmniejsz rozmiar poziomo"></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.width=document.body.clientWidth-90;%(ChartID)s.height=document.body.clientHeight-160;" src="images/arrow4_circle.gif" alt="przywróć początkowe rozmiary"></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.width=1*%(ChartID)s.width+50;" src="images/arrow4_right.gif" alt="zwiększ rozmiar poziomo"></td>
   <td></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.EditCopy();" src="images/icon_copy.gif" alt="Kopiuj wykres do schowka. Skopiowany wykres możesz wkleić np. do MS Excel jako tabelkę z danymi, obrazek, bądź też obrazek wektorowy. Aby tego dokonać należy wybrać pozycję 'Wklej specjalnie' z menu 'Edycja'."></td>
   <td><img style="cursor:pointer" onclick="javascript:var m=%(ChartID)s.ChartType;var i;i=m;if(m==0)i=1;if(m==1)i=0;if(m==2)i=3;if(m==3)i=2;if(m==4)i=5;if(m==5)i=4;if(m==6)i=7;if(m==7)i=6;if(m==8)i=9;if(m==9)i=8;%(ChartID)s.ChartType=i;" src="images/icon_3DOffOn.gif" alt="Przełącz tryb wyświetlania z 3D na 2D i odwrotnie. Ustawiając kursor myszki w obszarze wykresu, równocześnie w wciśniętym klawiszem Ctrl, możesz zmieniać sposób wyświetlania wykresu w widoku 3D"></td>
   <td><input type="hidden" id="stacking%(ChartID)s" value="0"><img style="cursor:pointer" onclick="javascript:if (document.all.stacking%(ChartID)s.value=='0') {%(ChartID)s.Stacking=1;document.all.stacking%(ChartID)s.value='1'; } else {%(ChartID)s.Stacking=0;document.all.stacking%(ChartID)s.value='0';}" src="images/icon_ChartingStacked.gif" alt="Grupuj dane w wierszu."></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.ShowLegend=1-%(ChartID)s.ShowLegend;" src="images/icon_ChartingLegend.gif" alt="Pokaż/schowaj legendę."></td>

   <td colspan=5>&nbsp;</td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.ChartType=1;" src="images/icon_ColumnChart.gif" alt="Wykres słupkowy."></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.ChartType=3;" src="images/icon_LineChart.gif" alt="Wykres liniowy."></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.ChartType=5;" src="images/icon_AreaChart.gif" alt="Wykres powierzchniowy."></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.ChartType=7;" src="images/icon_StepChart.gif" alt="Wykres narastająco."></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.ChartType=14;" src="images/icon_PieChart.gif" alt="Wykres kołowy. Uwaga: dla tego wykresu widok 3D oraz tryb grupowania jest niedostępny."></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.ChartType=16;" src="images/icon_XYChart.gif" alt="Wykres XY. Uwaga: dla tego wykresu widok 3D oraz tryb grupowania jest niedostępny."></td>
</tr>
<tr>
   <td></td>
   <td><img style="cursor:pointer" onclick="javascript:%(ChartID)s.height=1*%(ChartID)s.height+25;" src="images/arrow4_down.gif" alt="zmniejsz rozmiar pionowo"></td>
   <td></td>
</tr>
</table>
"""%(self.__dict__)
      file.write(s)
   def WriteInit(self,file):
      s="""
<script language="VBScript" EVENT="OnReadyStateChange" FOR=\"%(ChartID)s\">
'sub %(ChartID)sOnReadyStateChange()
   %(ChartID)s.width=680 '480 'window.parent.document.all(window.name).width-120
   %(ChartID)s.height=520 '320 'window.parent.document.all(window.name).height-160
   %(ChartID)s.ColumnCount = 0
   %(ChartID)s.RowCount = 0
   %(ChartID)s.RandomFill=False
'   %(ChartID)s.ScrollLeft = 0
'   %(ChartID)s.ScrollTop = 0
   %(ChartID)s.AllowDithering = False
   %(ChartID)s.AllowDynamicRotation = True
   %(ChartID)s.AllowSelections = True
   %(ChartID)s.AllowSeriesSelection = True
   %(ChartID)s.DoSetCursor = True
   %(ChartID)s.OLEDragMode = 1
   %(ChartID)s.OLEDropMode = 2
   %(ChartID)s.Style.backgroundColor = "ivory"
"""%(self.__dict__)
      file.write(s)
      s="""
   %(ChartID)s.Backdrop.Frame.Style = %(FrameStyle)d
   %(ChartID)s.ChartType = %(ChartType)d
   %(ChartID)s.object.Title.Text = "%(Title)s"
   %(ChartID)s.object.Title.VtFont.Name="ARIAL CE"
   %(ChartID)s.object.Legend.VtFont.Name="ARIAL CE"
   %(ChartID)s.ShowLegend = %(ShowLegend)d
   %(ChartID)s.FootnoteText = "%(FootnoteText)s"
   %(ChartID)s.ColumnCount = %(ColumnCount)d
   %(ChartID)s.RowCount = %(RowCount)d
""" % (self.__dict__)
      file.write(s)
      if self.Columns!={}:
         file.write('%s.object.ColumnLabelCount = %d\n'%(self.ChartID,self.ColumnCount))
         for acol,aname in self.Columns.items():
            file.write('%s.object.Column = %d\n'%(self.ChartID,acol))
            file.write('%s.object.ColumnLabel = "%s"\n'%(self.ChartID,aname))
      if self.Rows!={}:
         file.write('%s.object.RowLabelCount = %d\n'%(self.ChartID,self.RowCount))
         for arow,aname in self.Rows.items():
            file.write('%s.object.Row = %d\n'%(self.ChartID,arow))
            file.write('%s.object.RowLabel = "%s"\n'%(self.ChartID,aname))
      acols=self.Data.keys()
      acols.sort()
      for acol in acols:
         arows=self.Data[acol].keys()
         arows.sort()
         file.write('%s.object.Column = %d\n'%(self.ChartID,acol))
         for arow in arows:
            file.write('%s.object.Row = %d\n'%(self.ChartID,arow))
            file.write('%s.object.Data = %s\n'%(self.ChartID,self.Data[acol][arow])) #UWAGA! bylo: object.Data = "liczba"
      s="""
      for aid=0 to 3
         set axis=%(ChartID)s.object.Plot.Axis(aid)
         axis.AxisTitle.VtFont.Name="ARIAL CE"
         for each label in axis.Labels
            label.VtFont.Name="ARIAL CE"
            label.VtFont.Size=6
            next
""" % (self.__dict__)
      file.write(s)
      if self.DisableAxisGrid:
         file.write("""
            axis.AxisGrid.MajorPen.Style = 0
            axis.AxisGrid.MinorPen.Style = 0
""")
      s="""
         next
   %(ChartID)s.Stacking = %(Stacked)d
   For axisID = 1 To 3
      set axis=%(ChartID)s.Plot.Axis(axisID,1)
      For alabelid = 1 To axis.Labels.Count
         axis.Labels(alabelid).Format = "# ## ##0"
      Next
   Next

'end sub
</script>

<OBJECT classid=\"clsid:3A2B370C-BA0A-11D1-B137-0000F8753F5D\" id=%(ChartID)s width=600 height=300 
""" % (self.__dict__)
      file.write(s) #onreadystatechange=\"%(ChartID)sOnReadyStateChange\"
      if not self.AsSinglePage:
         s=""" CODEBASE=\"/icormanager/ole/mschrt20/mschrt20.cab#version=6,0,84,18\"><PARAM NAME=\"LPKPath\" VALUE=\"/icormanager/ole/mschrt20/mschrt20.lpk\"></OBJECT>"""
      else:
         s='></OBJECT>'
      file.write(s) 



