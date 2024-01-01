# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_Win32_OLE_ICORExcel import *
from CLASSES_Library_DBBase_Util_CSVImport import CSVExport

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   excel=ICORExcel(0)
   bcsv=CSVExport()
   ahl=[]
   for i in range(70):
      ahl.append(excel[i+1,1])
   bcsv.Header=ahl
   bcsv.Open('c:/icor/sql/obiektyf.csv')
   arow=2
   while 1:
      InfoStatus(str(arow))
      for i in range(70):
         s=excel[i+1,arow]
         bcsv[bcsv.Header[i]]=s
      bcsv.Next()  
      arow=arow+1
   bcsv.Close()
   InfoStatus('')
   return



