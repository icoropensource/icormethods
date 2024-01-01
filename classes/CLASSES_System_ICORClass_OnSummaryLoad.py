# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
from CLASSES_Library_ICORBase_Interface_ICORSummary import DoSummaryLoad,DoSummarySave
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   afile=InputFile()
   if afile=='':
      return
   afile=FilePathAsSystemPath(afile)
   fout=TextFile(afile,'r')
   s=''
   try:
      l=fout.readline()
      while l:
         s=s+l
         l=fout.readline()
   finally:
      fout.close()
   DoSummaryLoad(s,OID=OID)
   return

