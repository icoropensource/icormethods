# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:13:10

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.projekt.msqlworksheet as MSQLWorksheet
import CLASSES_Library_ICORBase_External_MLog as MLog
import pythoncom

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   aexception=0
   pobj=pclass.GetFirstObject()
   while pobj:
      if pobj['SGIsDisabled']:
         pobj.Next()
         continue
      aicorvar='SQLSheetsCalculate_%s'%pobj.Nazwa
      if aICORDBEngine.Variables[aicorvar]=='1' or aICORDBEngine.Variables[aicorvar]=='':
         aICORDBEngine.Variables[aicorvar]='2'
         saveout=MLog.MemorySysOutWrapper()
         try:
            pythoncom.CoInitialize()
            try:
               aWorksheetQueries=MSQLWorksheet.ICORWorksheetQueries(pobj)
               aWorksheetQueries.Calculate()
               aWorksheetQueries.CloseConnection()
               aWorksheetQueries=None
            finally:
               pythoncom.CoUninitialize()
         except:
            saveout.LogException()
            aexception=1
         pobj.SheetStatus=saveout.read()
         pclass.SheetDataOstatniegoGenerowania.SetValuesAsDateTime(pobj.OID,ICORUtil.tdatetime())
         saveout.Restore()
         aICORDBEngine.Variables[aicorvar]='3'
      pobj.Next()
   if aexception:
      import win32api
      try:
         for i in range(100):
            win32api.Beep(500-i*2,2)
      except:
         pass
   else:
      import win32api
      try:
         win32api.Beep(5000,100)
         win32api.Beep(3000,150)
      except:
         pass
   return



