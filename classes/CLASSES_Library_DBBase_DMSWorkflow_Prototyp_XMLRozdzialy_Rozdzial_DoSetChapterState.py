# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      return ''
   aclass=aICORDBEngine.Classes[CID]
   if not aclass.ObjectExists(OID):
      return ''
   achaptertitle=aclass.Naglowek[OID]
   apriority='N03'
   prefs=aclass.Priorytet.GetRefList(OID)
   if prefs:
      apriority=prefs.Nazwa[prefs.OID]
   sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   soid=int(FieldName)
   sname=''
   if soid>=0:
      sname=sclass.Nazwa[soid]
   uclass=aICORDBEngine.Classes['CLASSES_System_User']
   username=''
   if UID>=0:
      username=uclass.UserName[UID]
   ret=aICORDBEngine.SysBase.SetCMSChapterState(acmsid=soid,acmsname=sname,achapterid=OID,achaptertitle=achaptertitle,apriority=apriority,auid=UID,ausername=username,aoperationtype='generate',aitemoid=Value,astatus='N')
   cnt=aICORDBEngine.SysBase.GetCMSChapterGenerateCount()
   for i in range(cnt):
      sclass.MainChapterByPriority(apriority=apriority)
   return ret

