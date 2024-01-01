# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_External_MLog as MLog

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName=='Status':
      alogfname=MLog.GetLogTempFileName('status_szablongenerowania')
      fout=open(alogfname,'w')
      fout.write(aclass.Status[OID])
      fout.close()
   return

