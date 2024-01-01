# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass=aICORDBEngine.Classes[CID]
   aupdate='2009_04_20 Aktualnosci'
   if not UpdateManager.CheckUpdate(aupdate):
      return

   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
   aobj=aclass.GetFirstObject()
   while aobj:
      if aobj.Naglowek=='Aktualności':
         print aobj.OID
         aobj.IsAutoGenerate=0
         aobj.IsCustomXSL=1
         aobj.IsCustomXSLSO=1
         aobj.XSLData='<!--\n'+aobj.XSLData+'\n-->\n'
         aobj.XSLDataSO='<!--\n'+aobj.XSLDataSO+'\n-->\n'
      aobj.Next()
   return


