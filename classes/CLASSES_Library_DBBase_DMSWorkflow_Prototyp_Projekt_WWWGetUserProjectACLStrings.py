# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:14:25

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icorlib.projekt.msqlsecurity as MSQLSecurity
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
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
   slv=string.split(Value,':')
   if len(slv)!=3:
      return ''
   Value=slv[0]
   try:
      achapterid=int(slv[2])
   except:
      achapterid=-1
   ret=luacl=MSQLSecurity.GetUserACLStrings(pobj,UID,slv[1])
   if Value=='Read':
      sobj=tobj.AccessLevelView
   elif Value=='Edit':
      sobj=tobj.AccessLevelEdit
   elif Value=='Delete':
      sobj=tobj.AccessLevelDelete
   if sobj:
      d={}
      ret=[]
      while sobj:
         d[sobj.Name]=1
         sobj.Next()
      for s,aoid,achecked in luacl:
         if d.has_key(s):
            ret.append([s,aoid,achecked])
   crefs=None
   if achapterid>=0:
      cclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
      cobj=cclass[achapterid]
      if Value=='Read':
         crefs=ICORSecurity.GetRecursiveAccessLevelRefs(cobj,'AccessLevelView')
      elif Value=='Edit':
         crefs=ICORSecurity.GetRecursiveAccessLevelRefs(cobj,'AccessLevelTableEdit')
      elif Value=='Delete':
         crefs=ICORSecurity.GetRecursiveAccessLevelRefs(cobj,'AccessLevelTableEdit')
      if crefs:
         crefs=MSQLSecurity.GetItemACLAsUserACL(crefs)
   l=[]
   for sname,aoid,achecked in ret:
      if crefs:
         if aoid in crefs:
            l.append(sname+ServerUtil.SPLIT_CHAR_VALUE+str(aoid)+ServerUtil.SPLIT_CHAR_VALUE+str(achecked))
      elif not crefs is None and crefs.RefExists(aoid):
         l.append(sname+ServerUtil.SPLIT_CHAR_VALUE+str(aoid)+ServerUtil.SPLIT_CHAR_VALUE+str(achecked))
      else:
         l.append(sname+ServerUtil.SPLIT_CHAR_VALUE+str(aoid)+ServerUtil.SPLIT_CHAR_VALUE+str(achecked))
   return string.join(l,ServerUtil.SPLIT_CHAR_PARAM)

