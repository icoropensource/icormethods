# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

#from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_Test_OLETest_OLEPythonTest2

xx=11

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   aclass=aICORDBEngine.Classes[CID]
   global xx
   print 'OLEPython Test #1 - start'
   print 'T1: xx0=',xx
   xx=12
   for i in range(1500000):
      x=123/124.0
   print 'OLEPython Test #1 - finish'
   print 'T1: xx1=',xx
   xx=13
   print 'T1: xx2=',xx
   return 'asdfghijk'



