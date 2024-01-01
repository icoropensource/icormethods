# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import spread

def Test1():
   m=spread.connect('4803@195.117.158.5','',0,0)
   m.join('a')
   m.multicast(spread.FIFO_MESS,'a','ICOR')
   m.leave('a')
   while not m.poll():
      DoEvents()
   m.disconnect()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   Test1()
   return



