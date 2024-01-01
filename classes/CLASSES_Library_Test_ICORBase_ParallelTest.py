# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import time
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   PPID=str(os.getpid())
   print 'method: CLASSES_Library_Test_ICORBase_ParallelTest, PID: %s, START'%(PPID,)
   aclass=aICORDBEngine.Classes[CID]
   time.sleep(5)
   print 'method: CLASSES_Library_Test_ICORBase_ParallelTest, PID: %s, END'%(PPID,)
   return 'OK'
