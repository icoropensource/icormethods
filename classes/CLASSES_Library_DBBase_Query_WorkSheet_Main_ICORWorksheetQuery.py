# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_Win32_OLE_ICORExcel import *
from CLASSES_Library_DBBase_GDVR_Main_ICORGDVRMain import aICORGDVR
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_DBBase_Util_Excel_HTMLXLSTable as HTMLXLSTable
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
   def __init__(self,aquery,acolumnid,acellrow,axlscell):
      self.Query=aquery
      self.ColumnID=acolumnid
      self.CellRow=acellrow
      self.Coords=self.ColumnID,self.CellRow
      self.Cell=axlscell
      self.CellID=self.Query.TableID+'!'+GetCellAddressAsExcelCellAddress(self.ColumnID,self.CellRow)
      self.IsCalculated=0
   def __getattr__(self,name):
      if name=='Formula':
         s=self.Cell.Value
         if type(s)!=type(''):
            return str(s)
         return s
      if name=='ValueType':
         if type(self.Cell.Value)==type(0.0):
            return mt_Double
         else:
            return mt_String
      if name=='Value':
         return self.Cell.Value
      if name=='ValueAsComp':
         return self.Cell.Value
      if name=='ValueAsString':
         return self.Cell.ValueAsString
   def cmd_CELLNAME(self,avalue): # do zrobienia
      return 1
   def GetProperNumLine(self,aline):  
      patt='([\(\,])0(\d)'
      def f(amatch):
         return amatch.group(1)+amatch.group(2)
      return re.sub(patt,f,aline)
   def EvalCommand(self,aline):
      gdict={
         'CELLNAME':self.cmd_CELLNAME,
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
         aworksheet=aWorksheetQueries[(self.Query.StructName,sl[0])]
         if aworksheet is None:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','odniesienie do nieistniejącego arkusza',acell=(acol,arow),acellref='',alinkref='',adata=sl[0])
            return 0.0
         arange=sl[1]
      else:
         aworksheet=self.Query
      if string.find(arange,':')>=0:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','nieprawidłowe odniesienie do zakresu',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return 0.0
      acol1,arow1=GetExcelCellAddressAsCellAddress(arange)
      if acol1<0 or arow1<0 or acol1>256 or arow1>65536:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','Odniesienie do komórki poza zakresem',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return 0.0
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
         aworksheet=aWorksheetQueries[(self.Query.StructName,sl[0])]
         if aworksheet is None:
            acol,arow=self.Coords
            aWorksheetQueries.AddStatusInfo('Error','odniesienie do nieistniejącego arkusza',acell=(acol,arow),acellref='',alinkref='',adata=sl[0])
            return 0.0
         arange=sl[1]
      else:
         aworksheet=self.Query
      sl=string.split(arange,':')
      if not len(sl) or len(sl)>2:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','nieprawidłowy zakres',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return 0.0
      if len(sl)==1:
         sl.append(sl[0])
      acol1,arow1=GetExcelCellAddressAsCellAddress(sl[0])
      if acol1<0 or arow1<0 or acol1>256 or arow1>65536:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','Odniesienie do komórki poza zakresem',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return 0.0
      acol2,arow2=GetExcelCellAddressAsCellAddress(sl[1])
      if acol2<0 or arow2<0 or acol2>256 or arow2>65536:
         acol,arow=self.Coords
         aWorksheetQueries.AddStatusInfo('Error','Odniesienie do komórki poza zakresem',acell=(acol,arow),acellref='',alinkref='',adata=arange)
         return 0.0
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
      agvrdict=aICORGDVR[self.Query.StructName,adict]
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
            self.Cell.SetValue(res)
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
               self.Cell.SetValue(aline[1:])
            elif aline[:1]=='=':
               self.EvalFormula(aline[1:])
            else:
               if aline[-1:]!=')':
                  aline=aline+'()'
               self.EvalCommand(aline)
      else:
         self.Cell.SetValue(aformula)
      aWorksheetQueries._CalculateRecurList.pop()
      return
   def DumpHTML(self,file):
      valueasis=0
      res=['    <TD']
      sclass='objectsviewdata'
      res.append(' class="%s"'%sclass)
      res.append('>')
      sf=''
      s=self.ValueAsString
      if not s:
         s='&nbsp;'
      res.append(s)
      res.append('</TD>\n')
      file.write(string.join(res,''))

class ICORWorksheetQuery:
   def __init__(self,aoid,astructname=''):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_WorkSheet_Main']
      self.OID=aoid
      self.StructName=astructname
      self.InitVariables()
   def InitVariables(self):
      self._TableTitle,self._TableID,self._TableDescription,self._TableAuthor=None,None,None,None
      self._StatusCalculate=None
      self._MaxCol,self._MaxRow=None,None
      self._LastCalculation=None
      self._XLSTable=None
      self._Cells={}
   def __getattr__(self,name):
      if name=='TableTitle':
         if self._TableTitle is None:
            self._TableTitle=self.ClassItem.TableTitle[self.OID]
         return self._TableTitle
      if name=='TableID':
         if self._TableID is None:
            self._TableID=self.ClassItem.TableID[self.OID]
         return self._TableID
      if name=='XLSTable':
         if self._XLSTable is None:
            amhtmltableparser=HTMLXLSTable.MHTMLXLSTableParser()
            amhtmltableparser.Process(self.ClassItem.SourceData[self.OID])
            self._XLSTable=amhtmltableparser.Table
         return self._XLSTable
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
            self._MaxCol=self.XLSTable.MaxCol
         return self._MaxCol
      if name=='MaxRow':
         if self._MaxRow is None:
            self._MaxRow=self.XLSTable.MaxRow
         return self._MaxRow
      if name=='LastCalculation':
         if self._LastCalculation is None:
            self._LastCalculation=self.ClassItem.LastCalculation.ValuesAsDateTime(self.OID)
         return self._LastCalculation
      if name=='LastModification':
         arefs=self.ClassItem.SheetItems.GetRefList(self.OID)
         if arefs:
            return arefs.LastModification.ValuesAsDateTime(arefs.OID)
         else:
            return ICORUtil.ZERO_DATE
   def __getitem__(self,akey):
      acol,arow=akey
      if self._Cells.has_key(akey):
         acell=self._Cells[akey]
      else:
         acell=ICORWorksheetCell(self,acol,arow,self.XLSTable[acol,arow])
         self._Cells[akey]=acell
      return acell
   def Clear(self):
      self.ClassItem.StatusCalculate[self.OID]=''
      self.InitVariables()
   def SetStatusCalculate(self,avalue):
      if type(avalue)==type([]):
         avalue.sort()
         self.ClassItem.StatusCalculate[self.OID]=cPickle.dumps(avalue)
      else:
         self.ClassItem.StatusCalculate[self.OID]=avalue
      self._StatusCalculate=avalue
   def StatusCalculateAsString(self):
      ret=[]
      if self.StatusCalculate is None:
         return ''
      if type(self.StatusCalculate)!=type([]):
         return self.StatusCalculate
      for sdata,asi in self.StatusCalculate:
         ret.append(asi.AsString())
      return string.join(ret,'\n')
   def Calculate(self,asettext=1):
      if self.LastCalculation>self.LastModification:
         print 'nic do przeliczenia!'
         return
      self.InitVariables()
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
               if not acell is None:
                  if not acell.IsCalculated:
                     acell.Calculate()
            SetProgress((arow+1)*self.MaxCol,max)
      finally:
         SetProgress(0,0)
      self.SetStatusCalculate(aWorksheetQueries._CalculateInfo)
      self.ClassItem.LastCalculation.SetValuesAsDateTime(self.OID,ICORUtil.tdatetime())
      if asettext:
         self.SetTextAsHTML()
   def SetTextAsHTML(self):
      f=cStringIO.StringIO()
      self.XLSTable.DumpAsHTML(f,aasvisible=1)
#      self.DumpHTML(f)
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



