# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aupdate='2011_06_24 FieldFormat'
   if not UpdateManager.CheckUpdate(aupdate):
      return

   aclass=aICORDBEngine.Classes['CLASSES_System_ICORField']
   aobj=aclass.GetFirstObject()
   while aobj:
      fmt=aobj.aFieldFormat
      if fmt:
         ofmt=fmt  
         fmt=fmt.replace('0n','0f')
         fmt=fmt.replace('1n','1f')
         fmt=fmt.replace('2n','2f')
         fmt=fmt.replace('%n','%f')
         fmt=fmt.replace('%t','')
         aobj.aFieldFormat=fmt
      aobj.Next()
   return
