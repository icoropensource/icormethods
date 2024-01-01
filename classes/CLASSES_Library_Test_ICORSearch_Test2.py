# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   fin=open('c:/icor/data.out','w')
   aoid=aclass.Kontr.GetFirstValueID()
   while aoid>=0:
      fin.write(aclass.Kontr[aoid]+'\n')
      aoid=aclass.Kontr.GetNextValueID(aoid)
   fin.close()
   return



