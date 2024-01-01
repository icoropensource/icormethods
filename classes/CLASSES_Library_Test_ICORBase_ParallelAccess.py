# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_Miasto_JednostkaOrganizacyjna']
#   aoid=aclass.FirstObject()
#   while aoid>=0:
#      print aoid
#      aoid=aclass.NextObject(aoid)
#   return
#   print 'Jestem uruchomiony'
   for i in range(16):
      print 'ala '+str(OID)+' '+str(i)
      time.sleep(1)
#   return 'xfiles'



