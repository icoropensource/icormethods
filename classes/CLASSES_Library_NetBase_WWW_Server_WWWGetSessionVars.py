# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import CLASSES_Library_NetBase_WWW_Server_ICORWWWInterfaceUtil as ICORWWWInterfaceUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   areport=ServerUtil.ICORReport()
   areport['UI_SKIN']=ICORWWWInterfaceUtil.DEFAULTS['UI_SKIN']
   aprofile=ICORSecurity.ICORSecurityProfile()
   aprofile.SetByUser(UID)
   dd=aprofile.GetParams()
   auser=ICORSecurity.ICORSecurityUser(UID)
   dd2=auser.GetParams()
   dd.update(dd2)
   for aparam in ['UI_SKIN','FRAME_BGCOLOR','FRAME_TOC_BGCOLOR','FRAME_TEXT_BGCOLOR']:
      if dd.has_key(aparam):
         areport[aparam]=dd[aparam]
   return areport.AsString()

