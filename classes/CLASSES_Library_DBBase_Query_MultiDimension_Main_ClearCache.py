# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   basename=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath)+'RS_428_36_mdqueryExcel_'
   aoid=aclass.FirstObject()
   while aoid>=0:
      aclass.OutputFileSize[aoid]='0'
      aclass.LastGenerated[aoid]=''
      fname=basename+str(aoid)+'.html'
      try:
         if os.path.exists(fname):
            os.unlink(fname)
      except:
         print 'blad dostępu do:',fname
      aoid=aclass.NextObject(aoid)
   return



