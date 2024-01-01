# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import appplatform.startutil as startutil
import os
import random

from sokutil import etykiety

import pythoncom

LOG_DATA=0

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   pythoncom.CoInitialize()
   try:
      apodwojne=0
      if OID==1:
         apodwojne=1
      aclass=aICORDBEngine.Classes[CID]
      apreprocessor=MassPaymentsServer(startutil.appconfig.IParams['pm_projekt'])
      apath=FilePathAsSystemPath(aICORWWWServerInterface.AppOutputPath)
      afname=ICORUtil.GetRandomFileName(apath[-1:],'sokw_','.pdf')

      l=string.split(Value,chr(255))
      aprid=l[0]
      aFormatWydruku=l[1]
      aMarginesLewy=float(l[2])
      aMarginesGorny=float(l[3])
      aSzerokoscEtykiety=float(l[4])
      aWysokoscEtykiety=float(l[5])
      aIloscEtykietWWierszu=float(l[6])
      aIloscEtykietWKolumnie=float(l[7])
      aOdstepPoziomyMiedzyEtykietami=float(l[8])
      aOdstepPionowyMiedzyEtykietami=float(l[9])
      if 1:
#         X0=9     # Margines lewy
#         Y0=10    # Margines g�rny
#        Ny=11     # Ilo�� wierszy
#         Nx=4     # Ilo�� kolumn
#         dx=0.2     # Odst�p poziomy mi�dzy etykietami
#         dy=0.2     # Odst�p pionowy mi�dzy etykietami
#         We=48.1    # Szeroko�� etykiety
#         He=25.1  # Wysoko�� etykiety
         lkody=[]
         amax=int(aIloscEtykietWWierszu*aIloscEtykietWKolumnie)
         if apodwojne:
            amax=amax>>1
         for i in range(amax):
            akod=apreprocessor.GetCheckSum('1%06d%06d'%(random.randrange(0,1000000),random.randrange(0,1000000)))
            lkody.append(akod)
         etykiety.TworzWydruk(apath+afname,lkody,apodwojne,aMarginesLewy,aMarginesGorny,aSzerokoscEtykiety,aWysokoscEtykiety,aIloscEtykietWKolumnie,aIloscEtykietWWierszu,aOdstepPoziomyMiedzyEtykietami,aOdstepPionowyMiedzyEtykietami)
         ret="""
         <script language='javascript'>
         window.location='/icormanager/output/%s';
         </script>
         """%(afname,)
   finally:
      pythoncom.CoUninitialize()
   return ret



