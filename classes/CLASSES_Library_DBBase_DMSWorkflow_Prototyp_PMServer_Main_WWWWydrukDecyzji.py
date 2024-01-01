# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppGlobal as AppGlobal
import appplatform.startutil as startutil
from spmutil import pmwydruki
from spmutil import pmwydruksigid

import pythoncom

LOG_DATA=0

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   pythoncom.CoInitialize()
   try:
      aclass=aICORDBEngine.Classes[CID]
      apreprocessor=MassPaymentsServer(AppGlobal.MAIN_APP_NAME)
      arok=-1
      apretextcode=''
      if AppGlobal.MAIN_APP_NAME==startutil.appconfig.IParams['pm_projekt']:
         if FieldName[0]=='R':
            if FieldName[1]=='A':
               arok=2000+int(FieldName[2])
            elif FieldName[1]=='B':
               arok=2010+int(FieldName[2])
            else:
               arok=1900+int(FieldName[1:3])
      elif AppGlobal.MAIN_APP_NAME==startutil.appconfig.IParams['pm_projekt2']:
         apretextcode=chr(27)+'&k4S'
         arok=int(FieldName[1:5]) #$$
         arok=2009
      if arok>1900:
         apath=FilePathAsSystemPath(aICORWWWServerInterface.AppOutputPath)
         lp=[]
         if AppGlobal.MAIN_APP_NAME==startutil.appconfig.IParams['pm_projekt']:
            lp=apreprocessor.GeneratePDFPrintDataSigid(arok,Value)
            aodbiorca=startutil.appconfig.IParams['pm_adres']
         elif AppGlobal.MAIN_APP_NAME==startutil.appconfig.IParams['pm_projekt2']:
            lp=apreprocessor.GeneratePDFPrintDataRadix(arok,Value)
            aodbiorca=startutil.appconfig.IParams['pm_adres2']
         if lp:
            afname=ICORUtil.GetRandomFileName(apath[-1:],'spmw_','.pdf')
         #   fout=open(apath+afname+'.txt','w')
         #   fout.write(lp[0][0]['TrescDecyzji'])
         #   fout.close()
            mywydruk1=pmwydruki.Wydruk(apath+afname)
            if LOG_DATA:
               import cPickle
               fout=open('c:/icor/tmp/wydruk1.dat','wb')
               fout.write(cPickle.dumps(lp,1))
               fout.close()
            for d1,ld2 in lp:
               if len(d1['TrescDecyzji'])>100:
                  if apretextcode:
                     d1['TrescDecyzji']=apretextcode+d1['TrescDecyzji']
                     if 0:
                        l=[chr(13)+chr(10),]
                        for i in range(32,256):
                           l.append('%03d %s '%(i,chr(i)))
                           if not i%10:
                              l.append(chr(13)+chr(10))
                        d1['TrescDecyzji']=d1['TrescDecyzji']+string.join(l,'')
                  bformularz=pmwydruksigid.F_SIGID_Decyzja(d1)
                  mywydruk1.DodajFormularz(bformularz)
               for d2 in ld2:
                  bformularz=pmwydruksigid.F_SIGID_Nr1(d2,aodbiorca=aodbiorca)
                  mywydruk1.DodajFormularz(bformularz)
            mywydruk1.Rysuj()
            ret="""
         <script language='javascript'>
         window.location='/icormanager/output/%s';
         </script>
         """%(afname,)
         else:
            ret="""
   <h1>Brak danych do wydruku</h1>
"""
      else:
         ret="""
   <h1>B��dny nr identyfikacyjny dla p�atno�ci: %s</h1>
"""%(FieldName,)
   finally:
      pythoncom.CoUninitialize()
   return ret



