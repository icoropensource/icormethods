# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   l=[6558,6557,6556,6555,6554,6553,6552,6551,6550,6549]
   UID=18500
   OID=10
   if UID>=0:
      arefs=aICORDBEngine.User.WWWLoginLog.GetRefList(UID)
      lret=[]
      if arefs:
         i=OID
         while arefs and i:
            l=[]
            print arefs.OID,arefs.LoginUser[arefs.OID],arefs.EventDateTime[arefs.OID],'|',aclass.EventDateTime[arefs.OID]
            l.append(arefs.EventDateTime[arefs.OID])
            l.append(arefs.LoginUser[arefs.OID])
            if arefs.Logged.ValuesAsInt(arefs.OID):
               l.append('Zalogowany')
            else:
               l.append('Błędne hasło')
            l.append(arefs.RemoteAddr[arefs.OID])
            l.append(arefs.HttpUserAgent[arefs.OID])
            lret.append(l)
            arefs.Next()
            i=i-1
      if not Value:
         lret2=[]
         for l in lret:
            s=ServerUtil.SPLIT_CHAR_VALUE.join(l)
            lret2.append(s)
         sret=ServerUtil.SPLIT_CHAR_PARAM.join(lret2)
      if Value=='JSON':
         sret=JSONUtil.write(lret)
   return
