# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import time

def TestDates(aclass):
   aoid=aclass.FirstObject()
   while aoid>=0:
      print 'PoleS['+str(aoid)+'] '+str(aclass.PoleS.GetValueLastModified(aoid))
      print 'PoleI['+str(aoid)+'] '+str(aclass.PoleI.GetValueLastModified(aoid))
      print 'PoleB['+str(aoid)+'] '+str(aclass.PoleB.GetValueLastModified(aoid))
      print 'PoleM['+str(aoid)+'] '+str(aclass.PoleM.GetValueLastModified(aoid)),aclass.PoleM[aoid]
      aoid=aclass.NextObject(aoid)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   for i in range(10):
      print i,
#      time.sleep(1)
#      DoEvents()
#   aclass=aICORDBEngine.Classes[CID]
#   TestDates(aclass)
   return



