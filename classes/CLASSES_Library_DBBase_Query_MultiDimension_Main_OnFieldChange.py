# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['UserComments',]:
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID)
   if FieldName in ['QueryStruct',]:
      aobj=aclass[OID]
      bobj=aobj.SubQuery
      while bobj:
         bobj.Class.QueryStruct[bobj.OID]=aclass.QueryStruct[OID]
         bobj.Next()
   return



