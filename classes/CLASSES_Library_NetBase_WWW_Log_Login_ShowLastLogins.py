# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   afield=aclass.EventDateTime
   aoid=afield.GetLastValueID()
   acnt=20
   while aoid>=0 and acnt:
      print aclass.EventDateTime[aoid],aclass.LoginUser[aoid],aclass.RemoteHost[aoid]
      aoid=afield.GetPrevValueID(aoid)
      acnt=acnt-1
   return


