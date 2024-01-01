# -*- coding: windows-1250 -*-
# saved: 2023/11/18 00:40:53

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def PrintClass(aclass):
   print aclass.CID,aclass.NameOfClass
   lfields=aclass.GetFieldsList()
   for afieldname in lfields:
      afield=aclass.FieldsByName(afieldname)
      print '  ',afield.FOID,afield.Name

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   PrintClass(aclass)
   aclass=aICORDBEngine.Classes['CLASSES_Library_Test_NetBase_Input_Test2']
   PrintClass(aclass)


