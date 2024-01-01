# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_Win32_OLE_ICORExcel import *
from CLASSES_Library_DBBase_GDVR_Main_ICORGDVRMain import aICORGDVR
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_WWW_Server_ICORWWWInterfaceUtil as ICORWWWInterfaceUtil
import string
import re
import cStringIO
import cPickle

ExceptionIgnore = 'ExceptionIgnore'

class StatusInfo:
   def __init__(self,atype,adescription,acell='',acellref='',alinkref='',adata=''):
      self.Type=atype # Error, Warning, Info, Debug
      self.Description=adescription
      if type(acell)==type(''):
         self.Cell=acell
      else:
         acol,arow=acell
         self.Cell=GetCellAddressAsExcelCellAddress(acol,arow)
      if type(acellref)==type(''):
         self.CellRef=acellref
      else:
         acol,arow=acellref
         self.CellRef=GetCellAddressAsExcelCellAddress(acol,arow)
      self.LinkRef=alinkref
      self.Data=adata
   def AsString(self):
      s='%s: %s; %s'%(self.Cell,self.Type,self.Description)
      if self.LinkRef:
         s=s+' : ['+str(self.LinkRef)+']'
      if self.Data:
         s=s+': <'+str(self.Data)+'>'
      return s

class ICORWorksheetCell:
   def __init__(self,acolumn,aoid):
      self.Column=acolumn
      self.OID=aoid                        
      self.ClassItem=self.Column.CellsClass
      self._CellRow,self._Formula,self._Value,self._ValueType,self._ValueAsComp,self._Coords,self._CellID=None,None,None,None,None,None,None
      self._IsBold,self._IsItalic,self._IsUnderline,_CellAlign,self._IsHeader,self._IsFooter,self._IsPercent,self._NumFormat,self._FontSize,self._FontColor,self._BackgroundColor,self._ColumnJoin,self._RowJoin=None,None,None,None,None,None,None,None,None,None,None,None,None
   def __getattr__(self,name):
      if name=='Coords':
         if self._Coords is None:
            self._Coords=self.Column.ColumnID,self.CellRow
         return self._Coords
      if name=='CellID':
         if self._CellID is None:
            self._CellID=self.Column.Query.TableID+'!'+GetCellAddressAsExcelCellAddress(self.Column.ColumnID,self.CellRow)
         return self._CellID
      if name=='CellRow':
         if self._CellRow is None:
            self._CellRow=self.ClassItem.CellRow.ValuesAsInt(self.OID)
         return self._CellRow
      if name=='Formula':
         if self._Formula is None:
            self._Formula=self.ClassItem.Formula[self.OID]
         return self._Formula
      if name=='ColumnJoin':
         if self._ColumnJoin is None:
            self._ColumnJoin=self.ClassItem.ColumnJoin[self.OID]
         return self._ColumnJoin
      if name=='RowJoin':
         if self._RowJoin is None:
            self._RowJoin=self.ClassItem.RowJoin[self.OID]
         return self._RowJoin
      if name=='ValueType':
         if self._ValueType is None:
            self._ValueType=self.ClassItem.CellType.ValuesAsInt(self.OID)
         return self._ValueType
      if name=='Value':
         if self._Value is None:
            self._Value=self.ClassItem.CellValue[self.OID]
         return self._Value
      if name=='ValueAsComp':
         if self._ValueAsComp is None:
            atype=self.ValueType
            if atype==mt_Double:
               self._ValueAsComp=float(self.Value)
            else:
               self._ValueAsComp=self.Value
         return self._ValueAsComp
      if name=='IsBold':
         if self._IsBold is None:
            self._IsBold=self.ClassItem.IsBold.ValuesAsInt(self.OID)
         return self._IsBold
      if name=='IsItalic':
         if self._IsItalic is None:
            self._IsItalic=self.ClassItem.IsItalic.ValuesAsInt(self.OID)
         return self._IsItalic
      if name=='IsUnderline':
         if self._IsUnderline is None:
            self._IsUnderline=self.ClassItem.IsUnderline.ValuesAsInt(self.OID)
         return self._IsUnderline
      if name=='IsHeader':
         if self._IsHeader is None:
            self._IsHeader=self.ClassItem.IsHeader.ValuesAsInt(self.OID)
         return self._IsHeader
      if name=='IsFooter':
         if self._IsFooter is None:
            self._IsFooter=self.ClassItem.IsFooter.ValuesAsInt(self.OID)
         return self._IsFooter
      if name=='IsPercent':
         if self._IsPercent is None:
            self._IsPercent=self.ClassItem.IsPercent.ValuesAsInt(self.OID)
         return self._IsPercent
      if name=='NumFormat':
         if self._NumFormat is None:
            self._NumFormat=self.ClassItem.CellNumFormat[self.OID]
         return self._NumFormat
      if name=='FontSize':
         if self._FontSize is None:
            self._FontSize=self.ClassItem.FontSize[self.OID]
         return self._FontSize
      if name=='FontColor':
         if self._FontColor is None:
            self._FontColor=self.ClassItem.FontColor[self.OID]
         return self._FontColor
      if name=='BackgroundColor':
         if self._BackgroundColor is None:
            self._BackgroundColor=self.ClassItem.BackgroundColor[self.OID]
         return self._BackgroundColor
      if name=='CellAlign':
         if self._CellAlign is None:
            self._CellAlign=self.ClassItem.CellAlign[self.OID]
         return self._CellAlign
   def SetFormula(self,avalue):
      self.ClassItem.Formula[self.OID]=avalue
      self._Formula=avalue
   def SetValueType(self,atype):
      self.ClassItem.CellType[self.OID]=str(atype)
      self._ValueType=atype
   def SetValue(self,avalue):
      self.ClassItem.CellValue[self.OID]=avalue
      self._Value=avalue
      try:
         bvalue=float(avalue)
         atype=mt_Double
      except ValueError:
         bvalue=avalue
         atype=mt_String
      self.SetValueType(atype)
      self._ValueAsComp=bvalue
   def SetIsBold(self,avalue):
      self.ClassItem.IsBold[self.OID]=str(avalue)
      self._IsBold=avalue
   def SetIsItalic(self,avalue):
      self.ClassItem.IsItalic[self.OID]=str(avalue)
      self._IsItalic=avalue
   def SetIsUnderline(self,avalue):
      self.ClassItem.IsUnderline[self.OID]=str(avalue)
      self._IsUnderline=avalue
   def SetIsHeader(self,avalue):
      self.ClassItem.IsHeader[self.OID]=str(avalue)
      self._IsHeader=avalue
   def SetIsFooter(self,avalue):
      self.ClassItem.IsFooter[self.OID]=str(avalue)
      self._IsFooter=avalue
   def SetIsPercent(self,avalue):
      self.ClassItem.IsPercent[self.OID]=str(avalue)
      self._IsPercent=avalue
   def SetCellAlign(self,avalue):
      self.ClassItem.CellAlign[self.OID]=avalue
      self._CellAlign=avalue
   def SetColumnJoin(self,avalue):
      self.ClassItem.ColumnJoin[self.OID]=avalue
      self._ColumnJoin=avalue
   def SetRowJoin(self,avalue):
      self.ClassItem.RowJoin[self.OID]=avalue
      self._RowJoin=avalue
   def SetNumFormat(self,avalue):
      self.ClassItem.CellNumFormat[self.OID]=avalue
      self._NumFormat=avalue
   def SetFontSize(self,avalue):
      self.ClassItem.FontSize[self.OID]=avalue
      self._FontSize=avalue
   def SetFontColor(self,avalue):
      self.ClassItem.FontColor[self.OID]=avalue
      self._FontColor=avalue
   def SetBackgroundColor(self,avalue):
      self.ClassItem.BackgroundColor[self.OID]=avalue
      self._BackgroundColor=avalue
   def cmd_TABLEID(self,avalue):
      self.Column.Query.SetID(avalue)
   def cmd_TABLETITLE(self,avalue):
      self.Column.Query.SetTitle(avalue)
   def cmd_TABLEDESCRIPTION(self,avalue):
      self.Column.Query.SetDescription(avalue)
   def cmd_TABLEAUTHOR(self,avalue):
      self.Column.Query.SetAuthor(avalue)
   def cmd_CELLNAME(self,avalue): # do zrobienia
      return 1
   def cmd_CELLHEADER(self):
      self.SetIsHeader(1)
   def cmd_CELLFOOTER(self):
      self.SetIsFooter(1)
   def cmd_CELLBOLD(self):
      self.SetIsBold(1)
   def cmd_CELLITALIC(self):
      self.SetIsItalic(1)
   def cmd_CELLUNDERLINE(self):
      self.SetIsUnderline(1)
   def cmd_CELLALIGNLEFT(self):
      self.SetCellAlign('left')
   def cmd_CELLALIGNRIGHT(self):
      self.SetCellAlign('right')
   def cmd_CELLALIGNCENTER(self):
      self.SetCellAlign('center')
   def cmd_CELLNUMFORMAT(self,avalue):
      if avalue==r'%':
         self.SetIsPercent(1)
      else:
         self.SetNumFormat(avalue)
   def cmd_COLUMNJOIN(self,avalue):
      self.SetColumnJoin(avalue)
   def cmd_ROWJOIN(self,avalue):
      self.SetRowJoin(avalue)
   def cmd_CELLFONTSIZE(self,avalue):
      self.SetFontSize(avalue)
   def cmd_CELLFONTCOLOR(self,avalue):
      self.SetFontColor(avalue)
   def cmd_CELLBACKGROUNDCOLOR(self,avalue):
      self.SetBackgroundColor(avalue)
   def cmd_CELLDEFAULTVALUE(self,avalue): # do zrobienia
      return 1
   def cmd_CELLDISABLEFORMULA(self): # do zrobienia
      return 1
   def cmd_ROWHEADER(self):
      acol,arow=self.Coords
      acol=1
      while acol<=self.Column.Query.MaxCol:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetIsHeader(1)
         acol=acol+1
   def cmd_ROWFOOTER(self):
      acol,arow=self.Coords
      acol=1
      while acol<=self.Column.Query.MaxCol:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetIsFooter(1)
         acol=acol+1   
   def cmd_ROWBOLD(self):
      acol,arow=self.Coords
      acol=1
      while acol<=self.Column.Query.MaxCol:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetIsBold(1)
         acol=acol+1
   def cmd_ROWITALIC(self):
      acol,arow=self.Coords
      acol=1
      while acol<=self.Column.Query.MaxCol:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetIsItalic(1)
         acol=acol+1
   def cmd_ROWUNDERLINE(self):
      acol,arow=self.Coords
      acol=1
      while acol<=self.Column.Query.MaxCol:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetIsUnderline(1)
         acol=acol+1
   def cmd_ROWNUMFORMAT(self,avalue):
      acol,arow=self.Coords
      acol=1
      while acol<=self.Column.Query.MaxCol:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.cmd_CELLNUMFORMAT(avalue)
         acol=acol+1
   def cmd_COLUMNBOLD(self):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetIsBold(1)
         arow=arow+1
   def cmd_COLUMNITALIC(self):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.cmd_CELLITALIC()
         arow=arow+1
   def cmd_COLUMNUNDERLINE(self):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.cmd_CELLUNDERLINE()
         arow=arow+1
   def cmd_COLUMNALIGNLEFT(self):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetCellAlign('left')
         arow=arow+1
   def cmd_COLUMNALIGNRIGHT(self):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetCellAlign('right')
         arow=arow+1
   def cmd_COLUMNALIGNCENTER(self):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.SetCellAlign('center')
         arow=arow+1
   def cmd_COLUMNFONTSIZE(self,avalue):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.cmd_CELLFONTSIZE(avalue)
         arow=arow+1
   def cmd_COLUMNNUMFORMAT(self,avalue):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.cmd_CELLNUMFORMAT(avalue)
         arow=arow+1
   def cmd_COLUMNFONTCOLOR(self,avalue):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.cmd_CELLFONTCOLOR(avalue)
         arow=arow+1
   def cmd_COLUMNBACKGROUNDCOLOR(self,avalue):
      acol,arow=self.Coords
      arow=arow+1
      while arow<=self.Column.Query.MaxRow:
         acell=self.Column.Query.GetCell(acol,arow)
         acell.cmd_CELLBACKGROUNDCOLOR(avalue)
         arow=arow+1
   def GetProperNumLine(self,aline):
      patt='([\(\,])0(\d)'
      def f(amatch):
         return amatch.group(1)+amatch.group(2)
      return re.sub(patt,f,aline)
   def EvalCommand(self,aline):
      gdict={
         'TABLEID':self.cmd_TABLEID,
         'TABLETITLE':self.cmd_TABLETITLE,
         'TABLEDESCRIPTION':self.cmd_TABLEDESCRIPTION,
         'TABLEAUTHOR':self.cmd_TABLEAUTHOR,
         'CELLNAME':self.cmd_CELLNAME,
         'CELLHEADER':self.cmd_CELLHEADER,
         'CELLFOOTER':self.cmd_CELLFOOTER,
         'CELLBOLD':self.cmd_CELLBOLD,
         'CELLITALIC':self.cmd_CELLITALIC,
         'CELLUNDERLINE':self.cmd_CELLUNDERLINE,
         'CELLALIGNLEFT':self.cmd_CELLALIGNLEFT,
         'CELLALIGNRIGHT':self.cmd_CELLALIGNRIGHT,
         'CELLALIGNCENTER':self.cmd_CELLALIGNCENTER,
         'CELLFONTSIZE':self.cmd_CELLFONTSIZE,
         'CELLNUMFORMAT':self.cmd_CELLNUMFORMAT,
         'CELLFONTCOLOR':self.cmd_CELLFONTCOLOR,
         'CELLBACKGROUNDCOLOR':self.cmd_CELLBACKGROUNDCOLOR,
         'CELLDEFAULTVALUE':self.cmd_CELLDEFAULTVALUE,
         'CELLDISABLEFORMULA':self.cmd_CELLDISABLEFORMULA,
         'ROWBOLD':self.cmd_ROWBOLD,
         'ROWITALIC':self.cmd_ROWITALIC,
         'ROWUNDERLINE':self.cmd_ROWUNDERLINE,
         'ROWHEADER':self.cmd_ROWHEADER,
         'ROWFOOTER':self.cmd_ROWFOOTER,
         'ROWNUMFORMAT':self.cmd_ROWNUMFORMAT,
         'COLUMNBOLD':self.cmd_COLUMNBOLD,
         'COLUMNITALIC':self.cmd_COLUMNITALIC,
         'COLUMNUNDERLINE':self.cmd_COLUMNUNDERLINE,
         'COLUMNALIGNLEFT':self.cmd_COLUMNALIGNLEFT,
         'COLUMNALIGNRIGHT':self.cmd_COLUMNALIGNRIGHT,
         'COLUMNALIGNCENTER':self.cmd_COLUMNALIGNCENTER,
         'COLUMNFONTSIZE':self.cmd_COLUMNFONTSIZE,
         'COLUMNNUMFORMAT':self.cmd_COLUMNNUMFORMAT,
         'COLUMNFONTCOLOR':self.cmd_COLUMNFONTCOLOR,
         'COLUMNBACKGROUNDCOLOR':self.cmd_COLUMNBACKGROUNDCOLOR,
         'COLUMNJOIN':self.cmd_COLUMNJOIN,
         'ROWJOIN':self.cmd_ROWJOIN,
      }
      try:
         aline=self.GetProperNumLine(aline)
         res=eval(aline,gdict)
         if res is not None:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','nieznana komenda w komórce',acell=(acol,arow),acellref='',alinkref='',adata=aline)
      except:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','błędna zawartość',acell=(acol,arow),acellref='',alinkref='',adata=aline)
   def stm_IIF(self,w,t,f):
      if w:
         return t
      return f
   def stm_CELL(self,arange):
      if string.find(arange,'!')>=0:
         sl=string.split(arange,'!')
         if len(sl)!=2:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','nieprawidłowe odniesienie do innego arkusza',acell=(acol,arow),acellref='',alinkref='',adata=arange)
            return 0.0
         aworksheet=aWorksheetQueries[(self.Column.Query.StructName,sl[0])]
         if aworksheet is None:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','odniesienie do nieistniejącego arkusza',acell=(acol,arow),acellref='',alinkref='',adata=sl[0])
            return 0.0
         arange=sl[1]
      else:
         aworksheet=self.Column.Query
      if string.find(arange,':')>=0:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','nieprawidłowe odniesienie do zakresu',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return 0.0
      acol1,arow1=GetExcelCellAddressAsCellAddress(arange)
      sum=0.0
      if acol1>aworksheet.MaxCol or arow1>aworksheet.MaxRow:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','odniesienie do komórki poza zakresem',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return sum
      acell=aworksheet[acol1,arow1]
      if acell is not None:
         if not acell.IsCalculated:
            acell.Calculate()
         elif acell.CellID in aWorksheetQueries._CalculateRecurList:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','referencja do tej samej komórki',acell=(acol,arow),acellref='',alinkref='',adata=string.join(aWorksheetQueries._CalculateRecurList,', '))
            return 0.0
         sum=acell.ValueAsComp
         if type(sum)!=type(0.0):
            acol1,arow1=self.Coords
            acol2,arow2=acell.Coords
            sv=acell.Formula
            s='komórka %s [%d,%d] odwołuje się do komórki %s [%d,%d], która nie posiada wartości numerycznej: %s'%(GetCellAddressAsExcelCellAddress(acol1,arow1),acol1,arow1,GetCellAddressAsExcelCellAddress(acol2,arow2),acol2,arow2,sv)
            aWorksheetQueries.AddStatusInfo('Warning','odwołanie do komórki, która nie posiada wartości numerycznej',acell=(acol1,arow1),acellref=(acol2,arow2),alinkref='',adata=sv)
            raise ExceptionIgnore
      return sum
   def stm_SUM(self,arange):
      if string.find(arange,'!')>=0:
         sl=string.split(arange,'!')
         if len(sl)!=2:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','nieprawidłowe odniesienie do innego arkusza',acell=(acol,arow),acellref='',alinkref='',adata=arange)
            return 0.0
         aworksheet=aWorksheetQueries[(self.Column.Query.StructName,sl[0])]
         if aworksheet is None:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','odniesienie do nieistniejącego arkusza',acell=(acol,arow),acellref='',alinkref='',adata=sl[0])
            return 0.0
         arange=sl[1]
      else:
         aworksheet=self.Column.Query
      sl=string.split(arange,':')
      if not len(sl) or len(sl)>2:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','nieprawidłowy zakres',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return 0.0
      if len(sl)==1:
         sl.append(sl[0])
      acol1,arow1=GetExcelCellAddressAsCellAddress(sl[0])
      acol2,arow2=GetExcelCellAddressAsCellAddress(sl[1])
      sum=0.0
      w=0
      while arow1<=arow2:
         bcol=acol1
         while bcol<=acol2:
            if bcol>aworksheet.MaxCol or arow1>aworksheet.MaxRow:
               acol,arow=self.Coords
               aWorksheetQueries.AddStatusInfo('Error','odniesienie do komórki poza zakresem',acell=(acol,arow),acellref='',alinkref='',adata=arange)
               w=1
               break
            acell=aworksheet[bcol,arow1]
            if acell is not None:
               if not acell.IsCalculated:
                  acell.Calculate()
               elif acell.CellID in aWorksheetQueries._CalculateRecurList:
                  acol,arow=self.Coords
                  aWorksheetQueries.AddStatusInfo('Error','referencja do tej samej komórki',acell=(acol,arow),acellref='',alinkref='',adata=string.join(aWorksheetQueries._CalculateRecurList,', '))
                  return sum 
               try:
                  avc=acell.ValueAsComp
                  if avc:
                     sum=sum+avc
               except:
                  acol1,arow1=self.Coords
                  acol2,arow2=acell.Coords
                  sv=acell.Formula
                  if sv:
                     aWorksheetQueries.AddStatusInfo('Error','odwołanie do komórki, która posiada błędną wartość',acell=(acol1,arow1),acellref=(acol2,arow2),alinkref='',adata=sv)
                  else:
                     aWorksheetQueries.AddStatusInfo('Error','odwołanie do komórki, która nie posiada wartości',acell=(acol1,arow1),acellref=(acol2,arow2),alinkref='',adata='')
#                  import traceback
#                  traceback.print_exc()
#                  print s
                  raise ExceptionIgnore
            bcol=bcol+1
         if w:
            break
         arow1=arow1+1
      return sum
   def stm_GETVALUE(self,adict,aitem,ayear,amonth,aday,afield):
      adate=(ayear,amonth,aday)
      agvrdict=aICORGDVR[self.Column.Query.StructName,adict]
      try:
         bitem=agvrdict[aitem]
      except:
         acol,arow=self.Coords
         sv='#!getvalue("%s","%s",%d,%d,%d,"%s")'%(adict,aitem,ayear,amonth,aday,afield)
         aWorksheetQueries.AddStatusInfo('Error','odwołanie do nieistniejącej pozycji',acell=(acol,arow),acellref='',alinkref='',adata=sv)
         return 0.0
#         raise ExceptionIgnore
      try:
         bfield=bitem.ValueFields[afield]
      except:
         acol,arow=self.Coords
         sv='#!getvalue("%s","%s",%d,%d,%d,"%s")'%(adict,aitem,ayear,amonth,aday,afield)
         aWorksheetQueries.AddStatusInfo('Error','odwołanie do nieistniejącego pola',acell=(acol,arow),acellref='',alinkref='',adata=sv)
         return 0.0
#         raise ExceptionIgnore
      res=bfield[adate]
      if res==0.0:
         acol,arow=self.Coords
         sv='#!getvalue("%s","%s",%d,%d,%d,"%s")'%(adict,aitem,ayear,amonth,aday,afield)
         aWorksheetQueries.AddStatusInfo('Warning','funkcja zwróciła wartość 0.00',acell=(acol,arow),acellref='',alinkref='',adata=sv)
      return res
   def EvalFormula(self,aline):
      gdict={
         'iif':self.stm_IIF,
         'cell':self.stm_CELL,
         'sum':self.stm_SUM,
         'getvalue':self.stm_GETVALUE,
      }
      try:
         aline=self.GetProperNumLine(aline)
         acol,arow=self.Coords
         try:
            res=eval(aline,gdict)
         except ZeroDivisionError:
            res=0.0
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Warning','dzielenie przez zero',acell=(acol,arow),acellref='',alinkref='',adata=aline)
         if res is None:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','nieznana formuła',acell=(acol,arow),acellref='',alinkref='',adata=aline)
         else:
            if type(res)!=type(''):
               res=str(res)
            self.SetValue(res)
      except ExceptionIgnore:
         pass
      except SyntaxError:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','błąd składni (sprawdź nawiasy i cudzysłowy)',acell=(acol,arow),acellref='',alinkref='',adata=aline)
      except NameError,e:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','nieznany identyfikator',acell=(acol,arow),acellref='',alinkref='',adata='['+e.args[0]+'] '+aline)
      except:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','błędna formuła',acell=(acol,arow),acellref='',alinkref='',adata=aline)
#         raise
   def Calculate(self):
      self.IsCalculated=1
      acol,arow=self.Coords
      if self.CellID in aWorksheetQueries._CalculateRecurList:
         aWorksheetQueries.AddStatusInfo('Error','odniesienie do tej samej komórki',acell=(acol,arow),acellref='',alinkref='',adata=string.join(aWorksheetQueries._CalculateRecurList,', '))
         return
      aWorksheetQueries._CalculateRecurList.append(self.CellID)
      aformula=self.Formula
      if string.find(aformula,'#!')>=0:
         sl=string.split(aformula,'#!')
         for aline in sl:
            if not aline:
               continue
            if aline[:1]=='@':
               self.SetValue(aline[1:])
            elif aline[:1]=='=':
               self.EvalFormula(aline[1:])
            else:
               if aline[-1:]!=')':
                  aline=aline+'()'
               self.EvalCommand(aline)
      else:
         self.SetValue(aformula)
      aWorksheetQueries._CalculateRecurList.pop()
      return
   def DumpHTML(self,file):
      valueasis=0
      res=['    <TD']
      sclass='objectsviewdata'
      if self.IsHeader:
         sclass='objectsviewheader'
         valueasis=1
      if self.IsFooter:
         sclass='objectsviewfooter'
      if sclass:
         res.append(' class="%s"'%sclass)
      if self.CellAlign:
         res.append(' align="%s"'%self.CellAlign)
      if self.BackgroundColor:
         res.append(' bgcolor="%s"'%self.BackgroundColor)
      res.append('>')
      if self.IsBold:
         res.append('<B>')
      if self.IsItalic:
         res.append('<I>')
      if self.IsUnderline:
         res.append('<U>')
      sf=''
      if self.FontSize:
         sf=' size="%s"'%(self.FontSize,)
      if self.FontColor:
         sf=sf+' color="%s"'%(self.FontColor,)
      if sf:
         res.append('<FONT')
         res.append(sf)
         res.append('>')

      s=self.Value
      if not s:
         s='&nbsp;'
      elif valueasis:
         pass
      elif self.ValueType==mt_Double:
         nv=self.ValueAsComp
         nv1=nv
         nf='%14.0n'
         if self.NumFormat=='0.0':
            nf='%14.0n'
         elif self.NumFormat=='0.2':
            nf='%14.2n'
         elif self.NumFormat[:1]=='/':
            nd=float(self.NumFormat[1:])
            nv=1.0*nv/nd
         if self.ValueAsComp==0.0:
            s='&nbsp;-&nbsp;'
         else:
            s=ICORUtil.FormatFNumHTML(nv,nf)
            if self.IsPercent:
               s=s+r'%'
            s=string.replace(s,' ','&nbsp;')
      res.append(s)
      if sf:
         res.append('</FONT>')
      if self.IsUnderline:
         res.append('</U>')
      if self.IsItalic:
         res.append('</I>')
      if self.IsBold:
         res.append('</B>')
      res.append('</TD>\n')
      file.write(string.join(res,''))

class ICORWorksheetColumn:
   def __init__(self,aquery,aoid):
      self.Query=aquery
      self.ClassItem=self.Query.ColumnsClass
      self.CellsClass=self.ClassItem.Cells.ClassOfType
      self.OID=aoid
      self._Cells=None
      self._ColumnID=None
   def __getattr__(self,name):
      if name=='Cells':
         if self._Cells is None:
            self._Cells={}
            arefs=self.ClassItem.Cells.GetRefList(self.OID)
            while arefs:
               acell=ICORWorksheetCell(self,arefs.OID)
               self._Cells[acell.CellRow]=acell
               arefs.Next()
         return self._Cells
      if name=='ColumnID':
         if self._ColumnID is None:
            self._ColumnID=self.ClassItem.ColumnID.ValuesAsInt(self.OID)
         return self._ColumnID
   def __getitem__(self,arow):
      acell=self.Cells.get(arow,None)
      if acell is None:
         return None
      return acell
   def AddCell(self,arow):
      if self.Cells.has_key(arow):
         return self.Cells[arow]
      coid=self.CellsClass.AddObject()
      self.CellsClass.CellRow[coid]=str(arow)
      self.ClassItem.Cells.AddRefs(self.OID,[coid,self.CellsClass.CID],asortedreffield=self.CellsClass.CellRow)
      acell=ICORWorksheetCell(self,coid)
      self._Cells[arow]=acell
      self.Query.SetMaxRow(arow)
      return acell

class ICORWorksheetQuery:
   def __init__(self,aoid,astructname=''):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_WorkSheet_Main']
      self.ColumnsClass=self.ClassItem.Columns.ClassOfType
      self.OID=aoid
      self.StructName=astructname
      self.InitVariables()
   def InitVariables(self):
      self._TableTitle,self._TableID,self._TableDescription,self._TableAuthor=None,None,None,None
      self._StatusCalculate=None
      self._Columns=None
      self._MaxCol,self._MaxRow=None,None
      self._LastCalculation=None
   def __getattr__(self,name):
      if name=='TableTitle':
         if self._TableTitle is None:
            self._TableTitle=self.ClassItem.TableTitle[self.OID]
         return self._TableTitle
      if name=='TableID':
         if self._TableID is None:
            self._TableID=self.ClassItem.TableID[self.OID]
         return self._TableID
      if name=='TableDescription':
         if self._TableDescription is None:
            self._TableDescription=self.ClassItem.TableDescription[self.OID]
         return self._TableDescription
      if name=='TableAuthor':
         if self._TableAuthor is None:
            self._TableAuthor=self.ClassItem.TableAuthor[self.OID]
         return self._TableAuthor
      if name=='StatusCalculate':
         if self._StatusCalculate is None:
            try:
               self._StatusCalculate=cPickle.loads(self.ClassItem.StatusCalculate[self.OID])
            except:
               self._StatusCalculate=self.ClassItem.StatusCalculate[self.OID]
         return self._StatusCalculate
      if name=='MaxCol':
         if self._MaxCol is None:
            self._MaxCol=self.ClassItem.MaxCol.ValuesAsInt(self.OID)
         return self._MaxCol
      if name=='MaxRow':
         if self._MaxRow is None:
            self._MaxRow=self.ClassItem.MaxRow.ValuesAsInt(self.OID)
         return self._MaxRow
      if name=='Columns':
         if self._Columns is None:
            self._Columns={}
            arefs=self.ClassItem.Columns.GetRefList(self.OID)
            while arefs:
               acolumn=ICORWorksheetColumn(self,arefs.OID)
               self._Columns[acolumn.ColumnID]=acolumn
               arefs.Next()
         return self._Columns
      if name=='LastCalculation':
         if self._LastCalculation is None:
            self._LastCalculation=self.ClassItem.LastCalculation.ValuesAsDateTime(self.OID)
         return self._LastCalculation
   def __getitem__(self,akey):
      acol,arow=akey
      acolumn=self.Columns.get(acol,None)
      if acolumn is None:
         return None
      return acolumn[arow]
   def Clear(self):
      self.ClassItem.Columns.DeleteReferencedObjects(self.OID)
      self.ClassItem.Columns[self.OID]=''
      self.ClassItem.MaxCol[self.OID]='-1'
      self.ClassItem.MaxRow[self.OID]='-1'
      self.ClassItem.StatusCalculate[self.OID]=''
      self.InitVariables()
   def SetTitle(self,avalue):
      self.ClassItem.TableTitle[self.OID]=avalue
      self._TableTitle=avalue
   def SetID(self,avalue):
      self.ClassItem.TableID[self.OID]=avalue
      self._TableID=avalue
   def SetDescription(self,avalue):
      self.ClassItem.TableDescription[self.OID]=avalue
      self._TableDescription=avalue
   def SetAuthor(self,avalue):
      self.ClassItem.TableAuthor[self.OID]=avalue
      self._TableAuthor=avalue
   def SetStatusCalculate(self,avalue):
      if type(avalue)==type([]):
         avalue.sort()
         self.ClassItem.StatusCalculate[self.OID]=cPickle.dumps(avalue)
      else:
         self.ClassItem.StatusCalculate[self.OID]=avalue
      self._StatusCalculate=avalue
   def SetMaxCol(self,acol):
      if acol>self.MaxCol:
         self.ClassItem.MaxCol[self.OID]=str(acol)
         self._MaxCol=acol
   def SetMaxRow(self,arow):
      if arow>self.MaxRow:
         self.ClassItem.MaxRow[self.OID]=str(arow)
         self._MaxRow=arow
   def StatusCalculateAsString(self):
      ret=[]
      if self.StatusCalculate is None:
         return ''
      if type(self.StatusCalculate)!=type([]):
         return self.StatusCalculate
      for sdata,asi in self.StatusCalculate:
         ret.append(asi.AsString())
      return string.join(ret,'\n')
   def AddColumn(self,acolid):
      if self.Columns.has_key(acolid):
         return self.Columns[acolid]
      coid=self.ColumnsClass.AddObject()
      self.ColumnsClass.ColumnID[coid]=str(acolid)
      self.ClassItem.Columns.AddRefs(self.OID,[coid,self.ColumnsClass.CID],asortedreffield=self.ColumnsClass.ColumnID)
      acolumn=ICORWorksheetColumn(self,coid)
      self._Columns[acolid]=acolumn
      self.SetMaxCol(acolid)
      return acolumn
   def GetCell(self,acol,arow):
      acolumn=self.AddColumn(acol)
      return acolumn.AddCell(arow)
   def Calculate(self,asettext=1):
      aWorksheetQueries._CalculateRecurList=[]
      aWorksheetQueries._CalculateInfo=[]
      for arow in range(self.MaxRow):
         for acol in range(self.MaxCol):
            acell=self[acol+1,arow+1]
            if acell is not None:
               acell.IsCalculated=0
      max=self.MaxRow*self.MaxCol
      try:
         for arow in range(self.MaxRow):
            for acol in range(self.MaxCol):
               acell=self[acol+1,arow+1]
               if (acell is not None) and not acell.IsCalculated:
                  acell.Calculate()
            SetProgress((arow+1)*self.MaxCol,max)
      finally:
         SetProgress(0,0)
      self.SetStatusCalculate(aWorksheetQueries._CalculateInfo)
      self.ClassItem.LastCalculation.SetValuesAsDateTime(self.OID,ICORUtil.tdatetime())
      if asettext:
         self.SetTextAsHTML()
   def CalculateCell(self,acol,arow):
      aWorksheetQueries._CalculateRecurList=[]
      acell=self[acol,arow]
      if acell is not None:
         acell.Calculate()
   def SetTextAsHTML(self):
      f=cStringIO.StringIO()
      self.DumpHTML(f)
      self.ClassItem.TextAsHTML[self.OID]=f.getvalue()
   def DumpHTML(self,afile,aspage=0,ashowerrors=0):
      if type(afile)==type(''):
         file=open(afile,'w')
         fclosed=1
      else:
         file=afile
         fclosed=0
      try:
         if aspage:
            file.write('<HTML>\n')
            file.write('<HEAD>\n')
            file.write(ICORWWWInterfaceUtil.GetScriptCSS())
            file.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=windows-1250">\n')
            file.write('<TITLE>Tabela</TITLE>\n')
            file.write('</HEAD><BODY>\n\n')
         file.write('<TABLE class="objectsviewtable">\n')
         if self.TableTitle:
            file.write('  <CAPTION class="objectsviewcaption">%s</CAPTION>\n'%(self.TableTitle,))
         for arow in range(self.MaxRow):
            file.write('  <TR>\n')
            for acol in range(self.MaxCol):
               acell=self[acol+1,arow+1]
               if acell is not None:
                  acell.DumpHTML(file)
               else:
                  file.write('    <TD class="objectsviewdata">&nbsp;</TD>\n')
            file.write('  </TR>\n')
         file.write('</TABLE>')
         if ashowerrors:
            file.write('<PRE>%s</PRE>'%self.StatusCalculateAsString())
         if aspage:
            file.write('</BODY></HTML>\n')
      finally:
         if fclosed:
            file.close()

class ICORWorksheetQueries:
   def __init__(self):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_WorkSheet_QueryStruct']
      self.QueryClass=self.ClassItem.Query.ClassOfType
      self.Refresh()
   def InitWorksheet(self,aobj,qobj):
      aitem=ICORWorksheetQuery(qobj.OID,aobj.StructName)
      self.Dicts[(aobj.StructName,aitem.TableID)]=aitem
      self.DictsOID[qobj.OID]=aitem
      sobj=qobj.SubQuery
      while sobj:
         self.InitWorksheet(aobj,sobj)
         sobj.Next()
   def Refresh(self):
      self.Dicts={}
      self.DictsOID={}
      aobj=self.ClassItem.GetFirstObject()
      while aobj.Exists():
         qobj=aobj.Query
         while qobj:
            self.InitWorksheet(aobj,qobj)
            qobj.Next()
         aobj.Next()
      self._CalculateRecurList=[]
      self._CalculateInfo=[]
   def __getitem__(self,key):
      if type(key)==type(1):
         return self.DictsOID.get(key,None)
      return self.Dicts.get(key,None)
   def AddStatusInfo(self,atype='',adescription='',acell='',acellref='',alinkref='',adata=''):
      asi=StatusInfo(atype,adescription,acell=acell,acellref=acellref,alinkref=alinkref,adata=adata)
#      print asi.AsString()
      self._CalculateInfo.append([(atype,adescription),asi])
   def NewWorksheet(self,adictname,aworksheetname):
      if type(adictname)==type(1):
         soid=adictname
         adictname=self.ClassItem.StructName[soid]
      else:
         soid=self.ClassItem.StructName.Identifiers(adictname)
         if soid<0:
            soid=self.ClassItem.AddObject()
            self.ClassItem.StructName[soid]=adictname
      aquery=self.Dicts.get((adictname,aworksheetname),None)
      if not aquery is None:
         aquery.Clear()
         return aquery
      qoid=self.QueryClass.AddObject()
      self.QueryClass.TableID[qoid]=aworksheetname
      self.ClassItem.Query.AddRefs(soid,[qoid,self.QueryClass.CID],asortedreffield=self.QueryClass.TableID)
      aquery=ICORWorksheetQuery(qoid,adictname)
      self.Dicts[(adictname,aworksheetname)]=aquery
      self.DictsOID[qoid]=aquery
      return aquery

aWorksheetQueries = ICORWorksheetQueries()



