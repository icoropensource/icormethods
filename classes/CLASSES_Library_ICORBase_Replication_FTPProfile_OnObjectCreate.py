# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass.FTPUser[OID]='anonymous'
   aclass.FTPPassword[OID]='anonymous@'
   aclass.FTPBaseDir[OID]='ICOR'
   aclass.FTPLocalDir[OID]='%ICOR%/TMP'
   aclass.FTPArchiveDir[OID]='archive'
   aclass.FTPPort[OID]='21'
   return


