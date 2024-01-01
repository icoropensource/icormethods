# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import ICORSecurityUser

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID>=0:
      auser=ICORSecurityUser(OID)
   else:
      auser=ICORSecurityUser(UID)
   if Value=='VCFFirstName':
      return auser.VCFFirstName
   elif Value=='VCFLastName':
      return auser.VCFLastName
   elif Value=='VCFEMail':
      return auser.VCFEMail
   elif Value=='VCFPhone':
      return auser.VCFPhone
   return auser.UserName



