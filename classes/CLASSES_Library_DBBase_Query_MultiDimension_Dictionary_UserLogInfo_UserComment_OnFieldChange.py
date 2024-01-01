# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['Comment',]:
      aclass.UserName[OID]=aICORDBEngine.User.UserName[UID]
      aclass.Date.SetValuesAsDateTime(OID,ICORUtil.tdatetime())
   return



