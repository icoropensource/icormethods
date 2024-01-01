# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:14:00

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icorlib.projekt.msqlsecurity as MSQLSecurity
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   sl=string.split(Value,':')
   if len(sl)!=2:
      return '0'
   amode,achapterid=sl[0],int(sl[1])
   pobj=aclass[OID]
   if not pobj:
      return '0'
   abvector=ICORUtil.BitVector('0x'+FieldName)
   auserbvector=None
   if abvector:
      auserbvector=MSQLSecurity.GetUserACL(pobj,UID,asbitvector=1)
      v=abvector&auserbvector
      if not abvector&auserbvector:
         return '0'
   if amode=='Read':
      pass
   elif amode=='Edit':
      pass
   elif amode=='Delete':
      pass
   return '1'



