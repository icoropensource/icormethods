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
   InputPassword('Wprowad� stare has�o dla u�ytkownika:')
   unname=aICORDBEngine.Variables._LoginUser
   if unname!=uname:
      MessageDialog('Niepoprawna nazwa u�ytkownika.',mtError,mbOK)
      return
   aopass=aICORDBEngine.Variables._LoginPassword
   aopass=aICORDBEngine.HashString(aopass+'_'+str(OID))
   if aopass!=aclass.Password[OID]:
      MessageDialog('Niepoprawne has�o.',mtError,mbOK)
      return
   aICORDBEngine.Variables._LoginUser=uname
   aICORDBEngine.Variables._LoginPassword=''
   InputPassword('Wprowad� nowe has�o dla u�ytkownika:')
   aICORDBEngine.Variables._LoginUser
   if unname!=uname:
      MessageDialog('Niepoprawna nazwa u�ytkownika.',mtError,mbOK)
      return
   anew1=aICORDBEngine.Variables._LoginPassword
   aICORDBEngine.Variables._LoginUser=uname
   aICORDBEngine.Variables._LoginPassword=''
   InputPassword('Wprowad� nowe has�o dla u�ytkownika:')
   unname=aICORDBEngine.Variables._LoginUser
   if unname!=uname:
      MessageDialog('Niepoprawna nazwa u�ytkownika.',mtError,mbOK)
      return
   anew2=aICORDBEngine.Variables._LoginPassword
   if anew1!=anew2:
      MessageDialog('Pomy�ka podczas wprowadzania has�a.',mtError,mbOK)
      return
   aclass.Password[OID]=anew1
   MessageDialog('Has�o zosta�o zmienione.',mtInformation,mbOK)
   return


