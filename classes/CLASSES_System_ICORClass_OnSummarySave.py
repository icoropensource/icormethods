# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
from CLASSES_Library_ICORBase_Interface_ICORSummary import DoSummaryLoad,DoSummarySave
import string
import os

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   sclass=aICORDBEngine.Classes['CLASSES_System_SummaryItem']
   afile=InputFile(afilename=sclass.Name[OID])
   if afile=='':
      return
   afile=FilePathAsSystemPath(afile)
   if os.path.splitext(afile)[1]!='.gz':
      afile=afile+'.gz'
   fout=TextFile(afile,'w')
   try:
      atext=DoSummarySave(OID)
      fout.write(atext)
   finally:
      fout.close()
   return

