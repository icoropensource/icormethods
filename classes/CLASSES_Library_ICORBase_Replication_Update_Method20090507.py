# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   aupdate='2009_04_17 Addins'
#   if not UpdateManager.CheckUpdate(aupdate):
#      return
   #***************************************************************************
   lp=['Biblioteka standardowa','Moduł bezpieczeństwa','Wyszukiwarka','CSS Sprites','Narzędzia SEO']
   dp={}
   tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Component_Template']
   for spname in lp:
      toid=tclass.Nazwa.Identifiers(spname)
      if toid<0:
         print 'Brak szablonu wtyczki!',spname
      else:
         dp[spname]=toid
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   pclass=aclass.Plugins.ClassOfType
   aobj=aclass.GetFirstObject()
   while aobj:
      arefs=aobj.Class.Plugins.GetRefList(aobj.OID)
      for spname in lp:
         toid=dp.get(spname,-1)
         if toid<0:
            continue
         apos,afind=arefs.FindRefByValue(arefs.Nazwa,spname)
         if apos<0:
            boid=pclass.AddObject(arefobject=aobj,arangeobject=aobj)
            print 'PLUGIN:',aobj.Nazwa,spname,boid
            pclass.Nazwa[boid]=spname
            pclass.Template[boid]=[toid,tclass.CID]
            pclass.AccessLevelView[boid]=aobj.Class.AccessLevelView[aobj.OID]
            aclass.Plugins.AddRefs(aobj.OID,[boid,pclass.CID])
      aobj.Next()
   return
