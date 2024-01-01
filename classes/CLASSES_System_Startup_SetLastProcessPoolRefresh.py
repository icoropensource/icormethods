# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aoid=aclass.FirstObject()
   anow=ICORUtil.tdatetime()
   aclass.LastProcessPoolRefresh.SetValuesAsDateTime(aoid,anow)
   return 'OK'

