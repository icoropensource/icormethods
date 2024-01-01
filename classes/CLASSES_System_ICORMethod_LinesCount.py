# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   cntlines,cntsize,cntmethods=0,0,0
   aobj=aclass.GetFirstObject()
   while aobj.Exists():
      atext=aobj.aMethodText
      cntlines=cntlines+string.count(atext,'\n')
      cntsize=cntsize+len(atext)
      cntmethods=cntmethods+1
      aobj.Next()
   print 'total methods count:',cntmethods
   print 'total size:',cntsize
   print 'total lines count:',cntlines
   return

