# -*- coding: windows-1250 -*-
# saved: 2023/03/04 14:55:47

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_External_MLog as MLog

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Rozdzialy','UserTSQL','UserCode','RozdzialyUsuniete','GrupyRozdzialow','RSSInfo','Plugins','MapServices','Alerty','UserXML','UserXSL','UserXSD','APILibraries','PageTemplate',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName=='Rozdzialy':
      aobj=aclass[OID]
      robj=aobj.Rozdzialy
      atabid=10
      while robj:
         robj.SGTabID=atabid
         atabid=atabid+10
         robj.Next()
   if FieldName=='Plugins':
      aobj=aclass[OID]
      robj=aobj.Plugins
      atabid=10
      while robj:
         robj.SGTabID=atabid
         atabid=atabid+10
         robj.Next()
   if FieldName=='Status':
      alogfname=MLog.GetLogTempFileName('status_wwwmenustruct')
      fout=open(alogfname,'w')
      fout.write(aclass.Status[OID])
      fout.close()
   return

