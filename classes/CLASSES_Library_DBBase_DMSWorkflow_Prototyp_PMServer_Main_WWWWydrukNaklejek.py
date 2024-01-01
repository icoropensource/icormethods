# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSync as ICORSync
import appplatform.startutil as startutil
import os
import time

from sokutil import etykiety

import pythoncom

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   tstart=time.time()
   pythoncom.CoInitialize()
   sok='OK'
   smessage='Identyfikatory zosta�y wygenerowane do pliku .pdf'
   aclass=aICORDBEngine.Classes[CID]
   apreprocessor=MassPaymentsServer(startutil.appconfig.IParams['pm_projekt'])
   apreprocessor.OpenConnection()
   try:
      ailoscstron=OID
      apath=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+apreprocessor.ProjectAppPath+'/wydruki/'
      try:
         os.makedirs(apath)
      except:
         pass
      afname=ICORUtil.GetRandomFileName(apath[-1:],'sokw_','.pdf')
      l=string.split(Value,chr(255))
      aprid=l[0]
      astateid=int(l[1])
      aFormatWydruku=l[2]
      aMarginesLewy=float(l[3])
      aMarginesGorny=float(l[4])
      aSzerokoscEtykiety=float(l[5])
      aWysokoscEtykiety=float(l[6])
      aIloscEtykietWWierszu=float(l[7])
      aIloscEtykietWKolumnie=float(l[8])
      aOdstepPoziomyMiedzyEtykietami=float(l[9])
      aOdstepPionowyMiedzyEtykietami=float(l[10])
      aWydrukPodwojny=int(l[11])
      apreprocessor.ConnectionExecute("""
update TMP_BZR_36005
set Status='C01'
where _OID='%s'
"""%(aprid,))
      apreprocessor.connection.BeginTrans()
      try:
         amax=ailoscstron*int(aIloscEtykietWWierszu*aIloscEtykietWKolumnie)
         if aWydrukPodwojny:
            amax=amax>>1
         lkody=apreprocessor.GetKID(amax,aprid)
         etykiety.TworzWydruk(apath+afname,lkody,aWydrukPodwojny,aMarginesLewy,aMarginesGorny,aSzerokoscEtykiety,aWysokoscEtykiety,aIloscEtykietWKolumnie,aIloscEtykietWWierszu,aOdstepPoziomyMiedzyEtykietami,aOdstepPionowyMiedzyEtykietami)
         i=0
         while i<len(lkody):
            s=string.join(lkody[i:i+20],"','")
            apreprocessor.ConnectionExecute("""
update TMP_BZR_36006
set Status='D2',Pula='%s'
where KodPrzesylki in ('%s')
"""%(aprid,s))
            i=i+20
         fout=open(apath+afname[:-4]+'.txt','w')
         try:
            fout.write(string.join(lkody,'\n'))
         finally:
            fout.close()
         apreprocessor.ConnectionExecute("""
update TMP_BZR_36005
set Status='E01',DataWydruku=getdate(),Wydruk='%s'
where _OID='%s'
"""%(afname,aprid))
         apreprocessor.connection.CommitTrans()
         tfinish=time.time()
         smessage=smessage+' Czas generowania: '+str(int(tfinish-tstart))+' sek.'
      except:
         apreprocessor.connection.RollbackTrans()
         apreprocessor.ConnectionExecute("""
update TMP_BZR_36005
set Status='A01'
where _OID='%s'
"""%(aprid,))
         sok='BAD'
         smessage='Wyst�pi� b��d podczas tworzenia wydruku etykiet.'
         raise
   finally:
      bstate=ICORSync.ICORState(astateid)
      bstate.Name=smessage
      bstate.Value=sok
      apreprocessor.CloseConnection()
      pythoncom.CoUninitialize()
   return ''




