# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aoidfrom=20000
   aoidto=20007

   aoidfrom=25002
   aoidto=26005

   lo=0
   hi=aclass.ObjectsCount()
   if not hi:
      return []
   while lo<hi:
      mid=(lo+hi)/2
      aoid=aclass.GetObjectIDByPosition(mid)
      if aoid<aoidfrom:
         lo=mid+1
      else:
         hi=mid
   aoid=aclass.GetObjectIDByPosition(lo)
   l=[]
   while aoid>=0 and aoid>=aoidfrom and aoid<aoidto:
      l.append(aoid)
      aoid=aclass.NextObject(aoid)
   return l



