# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import tdatetime
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
import os
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   basename=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath)+'RS_428_36_mdqueryExcel_'
   aoid=aclass.FirstObject()
   while aoid>=0:
      fname=basename+str(aoid)+'.html'
      try:
         w=0
         if os.path.exists(fname):
            fsize=os.path.getsize(fname)
            if fsize>0:
               aclass.OutputFileSize[aoid]=str(fsize)
               aclass.LastGenerated.SetValuesAsDateTime(aoid,tdatetime(os.path.getmtime(fname)))
               w=1
         if not w
            aclass.OutputFileSize[aoid]='0'
            aclass.LastGenerated[aoid]=''
      except:
         print 'blad dostępu do:',fname
         aclass.OutputFileSize[aoid]='0'
         aclass.LastGenerated[aoid]=''
      aoid=aclass.NextObject(aoid)
   return



