# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      s=aobj.ASPSourceOnDelete
      if s:
         print '*************************************************************************'
         l=string.split(s,'\n')
         for s in l:
            print s
      aobj.Next()
   
   return


