# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      OID=aICORDBEngine.SystemOwnerUserID
   uname=aclass.UserName[OID]
   aICORDBEngine.Variables._LoginUser=uname
   aICORDBEngine.Variables._LoginPassword=''
   InputPassword('Wprowadź stare hasło dla użytkownika:')
   unname=aICORDBEngine.Variables._LoginUser
   if unname!=uname:
      MessageDialog('Niepoprawna nazwa użytkownika.',mtError,mbOK)
      return
   aopass=aICORDBEngine.Variables._LoginPassword
   aopass=aICORDBEngine.HashString(aopass+'_'+str(OID))
   if aopass!=aclass.Password[OID]:
      MessageDialog('Niepoprawne hasło.',mtError,mbOK)
      return
   aICORDBEngine.Variables._LoginUser=uname
   aICORDBEngine.Variables._LoginPassword=''
   InputPassword('Wprowadź nowe hasło dla użytkownika:')
   aICORDBEngine.Variables._LoginUser
   if unname!=uname:
      MessageDialog('Niepoprawna nazwa użytkownika.',mtError,mbOK)
      return
   anew1=aICORDBEngine.Variables._LoginPassword
   aICORDBEngine.Variables._LoginUser=uname
   aICORDBEngine.Variables._LoginPassword=''
   InputPassword('Wprowadź nowe hasło dla użytkownika:')
   unname=aICORDBEngine.Variables._LoginUser
   if unname!=uname:
      MessageDialog('Niepoprawna nazwa użytkownika.',mtError,mbOK)
      return
   anew2=aICORDBEngine.Variables._LoginPassword
   if anew1!=anew2:
      MessageDialog('Pomyłka podczas wprowadzania hasła.',mtError,mbOK)
      return
   aclass.Password[OID]=anew1
   MessageDialog('Hasło zostało zmienione.',mtInformation,mbOK)
   return


