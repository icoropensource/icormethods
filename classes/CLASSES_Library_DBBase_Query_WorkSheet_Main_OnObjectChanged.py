# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_DBBase_Query_WorkSheet_Main_ICORWorksheetQuery import aWorksheetQueries

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if Value in ['ObjectAdd','ObjectEdit']:
      aobj=aclass[OID]
      if aobj.CalculationMethod.Nazwa=='Automatyczny':
         aworksheet=aWorksheetQueries[OID]
         aworksheet.Calculate()
   return



