# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0 or not aclass.ObjectExists(OID):
      return 'DEL'+ServerUtil.SPLIT_CHAR_PARAM+'DEL'
   astate=ICORSync.ICORState(OID)
   return astate.Name+ServerUtil.SPLIT_CHAR_PARAM+astate.Value

