# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:14:19

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icorlib.projekt.msqlsecurity as MSQLSecurity
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      return ''
   aclass=aICORDBEngine.Classes[CID]
   pobj=aclass[OID]
   if not pobj:
      return ''
   tobj=pobj.BazyZrodlowe
   tobj.SetByOID(int(FieldName))
   if not tobj:
      return ''

   lp=Value.split(ServerUtil.SPLIT_CHAR_SEPTR)
   l1=[y for y in [map(int,filter(None,x.split(ServerUtil.SPLIT_CHAR_VALUE))) for x in lp[0].split(ServerUtil.SPLIT_CHAR_PARAM)]]
   l2=lp[1].split(ServerUtil.SPLIT_CHAR_PARAM)
   baclread,bacledit,bacldelete=MSQLSecurity.GetTableACLs(pobj,tobj,UID,l1,l2)
   return baclread.AsString()+ServerUtil.SPLIT_CHAR_PARAM+bacledit.AsString()+ServerUtil.SPLIT_CHAR_PARAM+bacldelete.AsString()+ServerUtil.SPLIT_CHAR_PARAM



