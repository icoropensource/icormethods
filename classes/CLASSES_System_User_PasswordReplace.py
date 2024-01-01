# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   InputPassword('Wprowadź nowe hasło dla użytkownika:')
   aoid=aclass.UserName.Identifiers(aICORDBEngine.Variables._LoginUser)
   if aoid<0:
      MessageDialog('Użytkownik o takiej nazwie nie istnieje.',mtError,mbOK)
      return
   aclass.Password[aoid]=aICORDBEngine.Variables._LoginPassword
   MessageDialog('Hasło zostało zmienione.',mtInformation,mbOK)
   return



