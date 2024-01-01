# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   aoidranges=aobj.GetOIDRanges()
   if aoidranges:
      for aidmin,aidmax in aoidranges:
         aoid=aclass.GetNextFreeObjectID(aidmin,aidmax)
         if aoid>=0:
            return str(aoid)
   aprofile=ICORSecurity.ICORSecurityProfile()
   aprofile.SetByUser(UID)
   ret=aprofile.GetNextFreeOID(aclass,OID)
#   print aclass.NameOfClass,ret,UID
   return str(ret)


