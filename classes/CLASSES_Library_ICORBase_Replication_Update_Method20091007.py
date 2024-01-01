# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass=aICORDBEngine.Classes[CID]
   aupdate='2009_10_07 GrupyPol'
   if not UpdateManager.CheckUpdate(aupdate):
      return

   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_OpisPolaDotyczy']
   aobj=aclass.GetFirstObject()
   while aobj:
      if aobj.Nazwa in ['_ChapterID','_OIDDictRef','Informacja data wytworzenia','Informacja opis czynności','Informacja osoba odpowiedzialna','Informacja podmiot udostępniający']:
         aobj.Grupa='Sygnatura'
      aobj.Next()
   return

