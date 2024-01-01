# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   #print 'OnObjectAdd CID: %d, Class: %s, OID: %d, UID: %d'%(CID,aclass.NameOfClass,OID,UID)
   aprofile=ICORSecurity.ICORSecurityProfile()
   aprofile.SetByUser(UID)
   ret=aprofile.GetNextFreeOID(aclass,OID,auseronly=1)
   #print '   ret 1: %d'%(ret,)
   if ret>=0 or Value=='internal':
      return str(ret)
   if OID>=0:
      aobj=aclass[OID]
      aoidranges=aobj.GetOIDRanges()
      if aoidranges:
         for aidmin,aidmax in aoidranges:
            aoid=aclass.GetNextFreeObjectID(aidmin,aidmax)
            if aoid>=0:
               #print '   ret 2: %d'%(aoid,)
               return str(aoid)
   ret=aprofile.GetNextFreeOID(aclass,OID)
   #print '   ret 3: %d'%(ret,)
   return str(ret)

