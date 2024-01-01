# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   moid,mid,mstep=54,54000,1000
   for i in range(944):
      aclass.IDMin[moid]=str(mid)
      aclass.IDMax[moid]=str(mid+mstep-1)
      mid=mid+mstep
      moid=moid+1
   return



