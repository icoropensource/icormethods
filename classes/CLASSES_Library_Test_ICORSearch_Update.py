# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   fin=open('c:/icor/data.txt','r')
   l=fin.readline()
   while l:
      aoid=aclass.AddObject()
      aclass.Kontr[aoid]=l[:-1]
      l=fin.readline()
   fin.close()
   return



