# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   fout=open(FilePathAsSystemPath('%ICOR%/tmp/passwords.txt'),'w')
   try:
      aobj=aclass.GetFirstObject()
      while aobj.Exists():
         fout.write('%d,%s,%s\n'%(aobj.OID,aobj.UserName,aobj.Password))
         aobj.Next()
   finally:
      fout.close()
   return



