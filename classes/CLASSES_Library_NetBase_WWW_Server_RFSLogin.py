# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSecurity import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_NetBase_WWW_Server_ServerUtil import ICORReport
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
import string
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   areport=ICORReport(Value)
   aclass=aICORDBEngine.Classes[CID]
   uid=GetUIDByUserPassword(areport.LOGIN_USER,areport.LOGIN_PASSWORD,awwwuser=0)
   arfsitem=aICORWWWServerInterface.GetUserDefaultRFSItem(UID)
   if arfsitem is not None:
      apath='/'#arfsitem.Name
      aroid=arfsitem.oid
   else:
      apath=''
      uid=-1
      aroid=-1
   areport.SetValue('UID',str(uid))
   areport.SetValue('ROOT_PATH',apath)
   areport.SetValue('ROOT_OID',str(aroid))
   return areport.AsString()



