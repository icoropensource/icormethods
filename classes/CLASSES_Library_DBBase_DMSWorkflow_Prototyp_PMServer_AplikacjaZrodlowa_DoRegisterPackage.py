# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *
import CLASSES_Library_ICORBase_External_MLog as MLog

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   mobj=aobj.PMServer
   afname=aobj.SciezkaDanych+'/'+Value+'.xml'
   saveout=MLog.MemorySysOutWrapper()
   ret=''
   try:
      try:
         apreprocessor=MassPaymentsServer(mobj.Nazwa)
         ret=apreprocessor.ProcessPackage(afname,aobj)
      except:
         import traceback
         traceback.print_exc()
         import win32api
         try:
            for i in range(100):
               win32api.Beep(500-i*2,2)
         except:
            pass
   finally:
      aobj.StatusRejestracji=aobj.StatusRejestracji+'\n'+ret+'\n'+saveout.read()
      saveout.Restore()
   return



