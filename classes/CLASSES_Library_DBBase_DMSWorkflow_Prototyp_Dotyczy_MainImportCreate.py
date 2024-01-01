# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:12:37

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
import icorlib.projekt.sqlimportlib as SQLImportLib

import CLASSES_Library_ICORBase_Interface_ICORUtil

def MainI(aproject,atableoid,acreatetables=0):
   pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   poid=pclass.Nazwa.Identifiers(aproject)
   if poid<0:
      return
   if pclass.SGIsDisabled.ValuesAsInt(poid):
      return
   pobj=pclass[poid]
   acrm=mcrmbase.MCRM(aproject,acreatetables=acreatetables,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   acrm.PreProcess(pobj,adir)
   asrctable=acrm.sourcetables[atableoid]
   SQLImportLib.DoSQLCreate(aproject,asrctable.SQLTable.GetDropSQL()+asrctable.SQLTable.GetCreateTableSQL())
   pclass.BazyZrodlowe.ClassOfType.DataOstatniegoGenerowania.SetValuesAsDateTime(atableoid,CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime())
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if not Value:
      return
   if FieldName=='CREATE':
      MainI(Value,OID)
   print 'Koniec'
   return



