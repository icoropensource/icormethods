# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   alastmodfield='OstatnieZmiany'
   lfields=aclass.GetFieldsList()
   aobj=aclass.GetFirstObject()
   while aobj:
      adate=None
      for afieldname in lfields:
         if afieldname==alastmodfield:
            continue
         afield=aclass.FieldsByName(afieldname)
         bdate=afield.GetValueLastModified(aobj.OID)
         if bdate>adate:
            adate=bdate
      if adate:
         aclass.FieldsByName(alastmodfield)[aobj.OID]=adate
      aobj.Next()
   return
