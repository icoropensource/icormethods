# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   print int(0==1)
   print int(1==1)
   x=1==0
   amethod=aclass.Test1
   print amethod.IsParallel
   return
   l=['WWWBackRefField',
'WWWDefaultCheck',
'WWWDefaultValue',
'WWWFilter',
'WWWLowercase',
'WWWMask',
'WWWMaxValue',
'WWWMinValue',
'WWWNoSpace',
'WWWRegex',
'WWWUnsigned',
'WWWUpdateRefs',
'WWWUppercase',]
   for aatr in l:
      print "bfield.%s=attrs.get('%s','')"%(aatr,aatr)
   return



