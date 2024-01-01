# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_External_MProfile as MProfile
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   MProfile.Start()
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   aobj=aclass.GetFirstObject()
   l=[]
   while aobj:
      robj=aobj.Rozdzialy
      while robj:
         acaption=robj.Naglowek
         l.append(acaption)
         robj.Next()
      aobj.Next()
   adir='d:\\icor\\log'
   afname=ICORUtil.GetRandomFileName(adir,'mprofile','.py')
   MProfile.Stop(adir+'\\'+afname)
   print afname
   return
