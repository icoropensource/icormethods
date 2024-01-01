# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   adt=CLASSES_Library_ICORBase_Interface_ICORUtil.tdatetime()
   aclass.DataModyfikacji.SetValuesAsDateTime(OID,adt)
   return



