# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import CLASSES_Library_NetBase_Utils_JSONUtil as JSONUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   sret=''
   if OID<0:
      OID=10
   if UID>=0:
      arefs=aICORDBEngine.User.WWWLoginLog.GetRefList(UID)
      lret=[]
      jret=[]
      if arefs:
         i=OID
         while arefs and i:
            l=[]
            d={}
            l.append(arefs.EventDateTime[arefs.OID])
            d['eventDateTime']=arefs.EventDateTime[arefs.OID]
            l.append(arefs.LoginUser[arefs.OID])
            d['loginUser']=arefs.LoginUser[arefs.OID]
            if arefs.Logged.ValuesAsInt(arefs.OID):
               l.append('Zalogowany')
               d['loggedText']='Zalogowany'
               d['logged']='1'
            else:
               l.append('Błędne hasło')
               d['loggedText']='Błędne hasło'
               d['logged']='0'
            l.append(arefs.RemoteAddr[arefs.OID])
            d['remoteAddr']=arefs.RemoteAddr[arefs.OID]
            l.append(arefs.HttpUserAgent[arefs.OID])
            d['httpUserAgent']=arefs.HttpUserAgent[arefs.OID]
            lret.append(l)
            jret.append(d)
            arefs.Next()
            i=i-1
      if not Value:
         lret2=[]                    
         for l in lret:
            s=ServerUtil.SPLIT_CHAR_VALUE.join(l)
            lret2.append(s)
         sret=ServerUtil.SPLIT_CHAR_PARAM.join(lret2)
      if Value=='JSON':
         d={
            'count':len(jret),
            'items':jret
         }
         sret=JSONUtil.write(d)
   return sret

