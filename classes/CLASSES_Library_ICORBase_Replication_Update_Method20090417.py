# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   aupdate='2009_04_17 Addins'
#   if not UpdateManager.CheckUpdate(aupdate):
#      return
   #***************************************************************************
   tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_AddIns_AddInTemplate']
   toid=tclass.Nazwa.Identifiers('Biblioteka standardowa')
   if toid<0:
      print 'Brak szablonu addins!'
      return
   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   aobj=aclass.GetFirstObject()
   while aobj:
      bobj=aobj.AddIns
      if not bobj:
         if not bobj.Class.ObjectExists(aobj.OID):
            boid=bobj.Class.CreateObjectByID(aobj.OID)
            bobj.Class.Nazwa[boid]='Biblioteka standardowa'
            bobj.Class.AddInTemplate[boid]=[toid,tclass.CID]
            bobj.Class.AccessLevelView[boid]=aobj.Class.AccessLevelView[aobj.OID]
            aobj.Class.AddIns.AddRefs(aobj.OID,[boid,bobj.CID])
            print aobj.Nazwa
         else:
            print 'Projekt ',aobj.Nazwa,' nie posiada addins, ale jest zajete miejsce na nie'
      aobj.Next()
   return
