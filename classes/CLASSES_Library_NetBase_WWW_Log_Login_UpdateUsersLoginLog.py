# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   dusers={}
   aobj=aclass.GetFirstObject()
   while aobj:
      aname=aobj.LoginUser.lower()
      lname=string.split(aname,'#')
      aname=lname[0]
      dusers[aname]=str(aobj.OID)+':'+str(aobj.CID)+':'+dusers.get(aname,'')
      aobj.Next()
   for auser,srefs in dusers.items():
      auid=aICORDBEngine.User.UserName.Identifiers(auser)
      if auid>=0:
         aICORDBEngine.User.WWWLoginLog[auid]=srefs
   return

