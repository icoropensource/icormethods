# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]

   for i in range(10):
      aclass.ParallelTest()
      for i in range(5):
         aclass.ParallelTest('F_%d'%i,i,'V_%d'%i)
   return
