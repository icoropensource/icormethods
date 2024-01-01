# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def MarkQuery(qobj):
   qobj.Status='q'
   sobj=qobj.SubQuery
   while sobj:
      MarkQuery(sobj)
      sobj.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      qobj=aobj.Query
      while qobj:
         MarkQuery(qobj)
         qobj.Next()
      aobj.Next()
   return



