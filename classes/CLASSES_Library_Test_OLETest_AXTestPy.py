# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   start=time.clock()
   s=aclass.AXTest.Execute()
   finish=time.clock()
   print 'py:',s,finish-start
   start=time.clock()
   s=aclass.AXTestPy1.Execute()
   finish=time.clock()
   print 'py:',s,finish-start
   return


