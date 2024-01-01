# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   return
   aclass=aICORDBEngine.Classes[CID]
   def fieldfunc(aclass,afield):
      aclass.CopyField(aclass.CID,afield.Name,0,-1,'a'+afield.Name)
   aclass.ForEachField(fieldfunc)
   return
