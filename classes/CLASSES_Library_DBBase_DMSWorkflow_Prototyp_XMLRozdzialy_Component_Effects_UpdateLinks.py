# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ReplaceLinks(s):
   sl=string.split(s,'\n')
   s3=''
   for ss in sl:
      s2=string.replace(ss,'lib/','/icorlib/')
      s3=s3+s2+'\n'
   return s3

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      aobj.URLScripts=ReplaceLinks(aobj.URLScripts)
      aobj.URLCSSFiles=ReplaceLinks(aobj.URLCSSFiles)
      aobj.Next()
   return
