# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def SecuritySave(afile):
   asecprofile=ICORSecurity.ICORSecurityProfile()
   asecprofile.SetByAll()
   asecprofile.DumpXML(afile,auidranges=1,ausers=1,aoidranges=1)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   SecuritySave('d:/icor/security.xml')
   return



