# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import time
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if FieldName=='Password':
      if aICORDBEngine.UserVars['PasswordChange']==1:
         return
      aICORDBEngine.UserVars['PasswordChange']=1
      aclass=aICORDBEngine.Classes[CID]
      s=aclass.Password[OID]
      p=aICORDBEngine.HashString(s+'_'+str(OID))
      aclass.Password[OID]=p
      aICORDBEngine.UserVars['PasswordChange']=0
      l=string.split(p+chr(10)+aclass.PasswordHistory[OID],chr(10))
      aclass.PasswordHistory[OID]=string.join(l[:100],chr(10))
      x=time.localtime(time.time())
      aclass.PasswordLastChanged.SetValuesAsDate(OID,(x[0],x[1],x[2]))
      aclass.PasswordMustChange[OID]='0'
   elif FieldName in ['Groups',]:
      aclass=aICORDBEngine.Classes[CID]
      afield=aclass.FieldsByName(FieldName)
      afield.UpdateReferencedObjects(OID,aupdaterefs=1)
      s='Zmiana uprawnien dla uzytkownika: '+str(OID)+' przez uzytkownika '+str(UID)+' na: '+afield[OID]
      aConnection=ICORUtil.GetCONNECTION()
      if aConnection:
         s=s+' IP: '+aConnection['REMOTE_ADDR']+' Cookie: '+aConnection['HTTP_COOKIE']+' Browser: '+aConnection['HTTP_USER_AGENT']
      MLog.Log(s,fname=FilePathAsSystemPath('%ICOR%/log/userACLchangelog.txt'),aconsole=0)
   return

