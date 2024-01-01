# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aupdate='2009_12_17 TableLinkName'
   if not UpdateManager.CheckUpdate(aupdate):
      return

   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_TableLink']
   aobj=aclass.GetFirstObject()
   while aobj:
      if not aobj.LinkName and aobj.DestinationTable:
         aobj.LinkName=aobj.DestinationTable.Nazwa
      aobj.Next()
   return

