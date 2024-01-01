# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   aclass=aICORDBEngine.Classes[CID]
   aclass.Values.ClearAllValues()
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_Dictionary_DimensionValues']
   aclass.ClearAllObjects()
   return




