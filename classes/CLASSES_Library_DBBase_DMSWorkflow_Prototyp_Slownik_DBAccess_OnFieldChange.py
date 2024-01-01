# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if FieldName in ['SGIsInactive',]:
      aclass.InactiveCounter[OID]='0'
   if FieldName in ['XXConnectionString',]:
      sconnection=aclass.ConnectionString[OID]
      dp=ICORUtil.ParseVars(sconnection,asplit1=';',asplit2='=',areplace1='',alowerkey=1)
      aclass.DataBaseHost[OID]=dp.get('server','')
      aclass.DataBaseName[OID]=dp.get('database','')
      aclass.DataBaseOwner[OID]=dp.get('owner','')
      aclass.DataBaseUser[OID]=dp.get('uid','')
      aclass.DataBasePassword[OID]=dp.get('pwd','')
      s=aclass.DataBaseRelease[OID]
      if not s:
         aclass.DataBaseRelease[OID]='4:'+str(aclass.DataBaseRelease.ClassOfType.CID)+':' # ms sql 2016
      aprovider=dp.get('provider','')
      toid=aclass.DBProvider.ClassOfType.Nazwa.Identifiers(aprovider)
      if toid<0:
         toid=1
      aclass.DBProvider[OID]='%d:%d:'%(toid,aclass.DBProvider.ClassOfType.CID)
      adriver=dp.get('driver','')
      toid=aclass.DBDriver.ClassOfType.Nazwa.Identifiers(adriver)
      if toid<0:
         toid=1
      aclass.DBDriver[OID]='%d:%d:'%(toid,aclass.DBDriver.ClassOfType.CID)
   return

