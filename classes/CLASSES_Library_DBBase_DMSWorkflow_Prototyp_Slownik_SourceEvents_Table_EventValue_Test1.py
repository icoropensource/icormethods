# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      s=aobj.EventSource
      if string.find(s,'extrule_')>=0:
         print '===================================================================='
         print '******************',aobj.EventKind.EventName,'******************'
         sl=string.split(s,'\n')
         for s1 in sl:
            print s1
         print
      aobj.Next()
   return

