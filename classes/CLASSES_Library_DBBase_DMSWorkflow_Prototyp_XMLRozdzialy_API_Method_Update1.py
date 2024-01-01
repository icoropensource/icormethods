# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]

   if 1:
      pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_API_Parameter']
      for i in range(200000,200200):
         print i,pclass.Nazwa[i]
         #s=pclass.Dokumentacja[i]
         #pclass.Dokumentacja[i]='x'
         #pclass.Dokumentacja[i]=s

   if 0:
      pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_API_Parameter']
      dp={}
      pobj=pclass.GetFirstObject()
      while pobj:
         pname=pobj.Nazwa
         poid=dp.get(pname,999999999)
         if pobj.OID<poid:
            dp[pname]=pobj.OID
         pobj.Next()
      print dp

      ld=[]
      aobj=aclass.GetFirstObject()
      while aobj:
         pobj=aobj.Parameters
         lp=[]
         while pobj:
            pname=pobj.Nazwa
            poid=dp[pname]
            if poid!=pobj.OID:
               ld.append(pobj.OID)
            lp.append([poid,pobj,CID])
            pobj.Next()
         print lp
         #aobj.Parameters=lp
         aobj.Next()
      print ld
      #pclass.DeleteObject(ld)
   return
