# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *
import appplatform.startutil as startutil

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if Value=='SIGID':
      apreprocessor=MassPaymentsServer(startutil.appconfig.IParams['pm_projekt'])
      apreprocessor.GenerateCSVPackageSigidDatyOdbioruDecyzji('SIGID')
   return



