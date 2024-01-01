# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSearch import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   def afunc(afield,aposition,avalue):
      print 'afunc:',aposition,avalue
   aclass.Kontr.ForEachValueByPattern(afunc,'888-101-49-33','^888-101')
#   siter=ICORRepositorySearch(aclass.Kontr)
#   siter.FirstPattern('888-101-49-33','^888-101')
#   print 'res:',siter.Position,siter.Value
   return


