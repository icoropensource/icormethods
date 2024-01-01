# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def CheckUpdate(aupdate):
   aclass=aICORDBEngine.Classes['CLASSES_Library_ICORBase_Replication_Update']
   aoid=aclass.Nazwa.Identifiers(aupdate)
   if aoid>=0:
      print 'Update:',aupdate,'has already been processed on',aclass.DataUruchomienia[aoid]
      return 0
   print 'Processing update:',aupdate
   aoid=aclass.AddObject()
   aclass.Nazwa[aoid]=aupdate
   aclass.DataUruchomienia.SetValuesAsDateTime(aoid,ICORUtil.tdatetime())
   return 1

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return
