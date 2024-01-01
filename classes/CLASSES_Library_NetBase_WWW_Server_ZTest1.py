# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   UID=18500
   print aclass.GetUserByUID()
   print aclass.GetUserByUID(Value='VCFFirstName')
   print aclass.GetUserByUID(Value='VCFLastName')
   print aclass.GetUserByUID(Value='VCFEMail')
   return

   x=1/0
   print 'Hello from ZTEST!'
   ret="ICOR OK działa super 333!"
   return ret



