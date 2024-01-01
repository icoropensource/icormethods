# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   l=[]
   aobj=aclass.GetFirstObject()
   while aobj:
      if aobj.Category=='ICOR':
         l.append(aobj.Name)
      aobj.Next()
   l.sort()
   for s in l:
      print s
   return
   afield=aclass.Name
   aoid=afield.GetFirstValueID()
   l=[]
   while aoid>=0:
      if not aclass.ObjectExists(aoid):
         print aoid,afield[aoid]
         l.append(aoid)
      aoid=afield.GetNextValueID(aoid)
   for aoid in l:
      aclass.DeleteObject(aoid)
   return            
