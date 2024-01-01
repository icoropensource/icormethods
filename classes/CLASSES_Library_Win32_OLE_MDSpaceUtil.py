# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import *
from CLASSES_Library_Win32_OLE_ICORExcel import *

class ICORMDSpace2Excel(ICORMDSpaceTableIterator):
   def __init__(self,aspace):
      ICORMDSpaceTableIterator.__init__(self,aspace)
   def __del__(self):
      pass
   def OnStart(self,acaption=''):
      self.caption=acaption
      self.excel=ICORExcel(0)
      self.excel.ClearSheet()
   def OnEnd(self):
      self.excel.AutoFit()
      if self.caption!='':
         self.excel[1,1]=self.caption
      self.excel[1,self.RowCount+3]='Koniec zestawienia'
   def OnHeader(self,acol,avalue):
      self.excel[acol+2,2]=avalue
   def OnStartRow(self,arow):
      pass
   def OnEndRow(self,arow):
      pass
   def OnStartCol(self,arow,acol):
      pass
   def OnEndCol(self,arow,acol):
      pass
   def OnData(self,arow,acol):
      self.excel[acol+1,arow+2]=str(self.Value)

class SummarySpace2Excel(ICORMDSpace2Excel):
   def OnData(self,arow,acol):
      if self.Value is None:
         return
      s=self.Value.StringValue
      self.excel[acol+1,arow+2]=s



