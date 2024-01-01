# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   afile=InputFile()
   afile='c:/icor/tmp/update'
   if afile=='':
      return
   ClearStdOut()
   afile=FilePathAsSystemPath(afile)
   atext=aclass.MethodRep.MethodText
   file=TextFile(afile+'.gz','w')
   try:
      file.write(atext)
   finally:
      file.close()
   return


