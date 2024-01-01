# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      return
   fname='c:/temp/_pagehtml.html'
   fout=open(fname,'w')
   try:
      fout.write(aclass.TextValue[OID])
   finally:
      fout.close()
   ExecuteShellCommand(fname)
   return



