# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   acclevel=aclass.AccessLevel.ValuesAsInt(OID)
   if acclevel<0:
      acclevel=0
   if acclevel>8:
      acclevel=8
   aclass.AccessLevel[OID]=str(acclevel)
   return



