# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes['CLASSES_DataBase_Miasto_JednostkaOrganizacyjna']
   arefs=aclass.SelectObjectsFromDictionary()
   while arefs:
      print arefs.Nazwa[arefs.OID]
      arefs.Next()
   return



