# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   apath=aICORDBEngine.Variables['_DEFAULT_PROCESS_EXECUTOR']
   ExecuteShellCommand(apath,'Process')#,'ProcessNoWindow'
   return



