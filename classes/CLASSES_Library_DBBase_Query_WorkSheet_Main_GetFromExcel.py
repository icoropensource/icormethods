# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_Win32_OLE_ICORExcel import *
from CLASSES_Library_DBBase_Query_WorkSheet_Main_ICORWorksheetQuery import aWorksheetQueries
import string

def UpdateFromExcel(aclass,astructname,adictname):
   excel=ICORExcel(0)
   if not adictname:
      adictname=excel.GetSheetName()
   aworksheet=aWorksheetQueries[astructname,adictname]
   if aworksheet is None:
      aworksheet=aWorksheetQueries.NewWorksheet(astructname,adictname)
   aworksheet.Clear()
   arow,acol,maxcol=1,1,1
   while 1:
      s=excel[maxcol,arow]
      if s=='#!TABLECOLUMNEND':
         break
      if maxcol>=250:
         print 'Tabela nie posiada ostatniej kolumny (#!TABLECOLUMNEND).'
         return
      maxcol=maxcol+1
   while 1:
      InfoStatus('Wiersz: '+str(arow))
      if excel[1,arow]=='#!TABLEEND':
         break
      if arow>2499:
         print 'tabela posiada ponad 2500 wierszy!'
         break
      for i in range(maxcol-1):
         s=excel[i+1,arow]
         if s:
            acell=aworksheet.GetCell(i+1,arow)
            acell.SetFormula(s)
      arow=arow+1
   InfoStatus('')

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      astruct='???'
      atable=''
   else:
      aobj=aclass[OID]
      astruct=aobj.QueryStruct.StructName
      atable=aobj.TableID
   UpdateFromExcel(aclass,astruct,atable)
   return



