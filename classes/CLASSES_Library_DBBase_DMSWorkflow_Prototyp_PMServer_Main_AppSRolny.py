# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserPaczki as XMLParserPaczki
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppUtil as AppUtil
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_DBBase_Util_CSVImport as CSVImport
import icordbmain.adoutil as ADOLibInit
import appplatform.startutil as startutil

class PMPlatnoscSRolny(XMLParserPaczki.PMPlatnosc):
   def __init__(self,*args):
      apply(XMLParserPaczki.PMPlatnosc.__init__,(self,)+args)
      self.DigestFields=['Kwota','DataWymagalnosci','IDPlatnika','IDTytulu','Tytulem','Platnik'] # 'TrescPrzelewu'
      self.IDDigestFields=['IDPlatnika','Platnik','PlatnikAdresMiejscowosc','PlatnikAdresUlica','PlatnikAdresNrPosesji','PlatnikAdresNrLokalu']

"""
-OID paczki|OID paczki|OID
                            
-Kwota|Kwota|Pieni�dze
-*Data wymagalno�ci|Data wymagalno�ci|Data
-ID p�atnika|ID p�atnika|Ci�g znak�w - 1 linia
-ID tytu�u|ID tytu�u|Ci�g znak�w - 1 linia
-Tytu�em|Tytu�em|Ci�g znak�w - 1 linia
-P�atnik|P�atnik|Ci�g znak�w - 1 linia
-Tre�� decyzji|Tre�� decyzji|Opis
#Tre�� przelewu|Tre�� przelewu|Opis
#Tre�� zwrotki|Tre�� zwrotki|Opis

PM kwota zap�aty|PM kwota zap�aty|Pieni�dze
*PM data zap�aty|PM data zap�aty|Data
PM bank|PM bank|Ci�g znak�w - 1 linia
PM kasa|PM kasa|Ci�g znak�w - 1 linia
PM kasjer|PM kasjer|Ci�g znak�w - 1 linia
*PM data wp�ywu|PM data wp�ywu|Data i czas
-PM status p�atno�ci|PM status p�atno�ci|Ci�g znak�w - 1 linia

-Czy anulowano|Czy anulowano|Liczba ca�kowita
-Czy ju� zap�acono|Czy ju� zap�acono|Liczba ca�kowita
-Czy bez kwoty|Czy bez kwoty|Liczba ca�kowita
-Czy g��wna p�atno�� grupy|Czy g��wna p�atno�� grupy|Liczba ca�kowita

-*Data akceptacji|Data akceptacji|Data
-OID p�atno�ci g��wnej|OID p�atno�ci g��wnej|OID

-Klucz g��wny|Klucz g��wny|Kod, Identyfikator
-Suma kontrolna|Suma kontrolna|Kod, Identyfikator

-Zwrotka grupa|Zwrotka grupa|Ci�g znak�w - 1 linia

-P�atnik Adres|P�atnik Adres|Opis
-P�atnik Adres Ulica|P�atnik Adres Ulica|Ci�g znak�w - 1 linia
-P�atnik Adres Nr posesji|P�atnik Adres Nr posesji|Ci�g znak�w - 1 linia
-P�atnik Adres Nr lokalu|P�atnik Adres Nr lokalu|Ci�g znak�w - 1 linia
-P�atnik Adres Kod pocztowy|P�atnik Adres Kod pocztowy|Ci�g znak�w - 1 linia
-P�atnik Adres Miejscowo��|P�atnik Adres Miejscowo��|Ci�g znak�w - 1 linia
#P�atnik Adres Gmina|P�atnik Adres Gmina|Ci�g znak�w - 1 linia
#P�atnik Adres Powiat|P�atnik Adres Powiat|Ci�g znak�w - 1 linia
#P�atnik Adres Wojew�dztwo|P�atnik Adres Wojew�dztwo|Ci�g znak�w - 1 linia
#P�atnik Adres Pa�stwo|P�atnik Adres Pa�stwo|Ci�g znak�w - 1 linia
-P�atnik Adres Inne informacje|P�atnik Adres Inne informacje|Ci�g znak�w - 1 linia

*PM Data odbioru decyzji|PM Data odbioru decyzji|Data
"""
############
"""
    <POLEWZORCOWE nazwa="Kwota" typ="Liczba" czyzwrotne="1"/>
    <POLEWZORCOWE nazwa="DataWymagalnosci" typ="Data" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="IDPlatnika" typ="Ci�g znak�w - 1 linia" czyzwrotne="1"/>
    <POLEWZORCOWE nazwa="IDTytulu" typ="Ci�g znak�w - 1 linia" czyzwrotne="1"/>
    <POLEWZORCOWE nazwa="Tytulem" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="Platnik" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="PlatnikAdres" typ="Opis" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="PlatnikAdresUlica" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="PlatnikAdresNrPosesji" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="PlatnikAdresNrLokalu" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="PlatnikAdresMiejscowosc" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="PlatnikAdresKodPocztowy" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="PlatnikAdresInneInformacje" typ="Ci�g znak�w - 1 linia" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="TrescDecyzji" typ="Opis" czyzwrotne="0"/>
    <POLEWZORCOWE nazwa="ZwrotkaGrupa" typ="Ci�g znak�w - 1 linia" czyzwrotne="1"/>

    <POLEINFORMACYJNE nazwa="PESEL" typ="PESEL" czyzwrotne="0"/>
"""

class PaymentsManagerSRolny(AppUtil.PaymentsManager):
   def __init__(self,*args):
      apply(AppUtil.PaymentsManager.__init__,(self,)+args)
      self.AccountBank=startutil.appconfig.IParams['pm_AccountBank']
      self.AccountAcc1=startutil.appconfig.IParams['pm_AccountAcc1']
      self.AccountAcc2=startutil.appconfig.IParams['pm_AccountAcc2']
   def OnNowaPozycja(self,rs,aplatnosc):
      rs.Fields.Item("Kwota").Value=aplatnosc.Pola['Kwota']
      rs.Fields.Item("DataWymagalnosci").Value=ICORUtil.tdatetime2fmtstr(aplatnosc.Pola['DataWymagalnosci'],adelimiter='-')
      rs.Fields.Item("IDPlatnika").Value=aplatnosc.Pola['IDPlatnika']
      rs.Fields.Item("IDTytulu").Value=aplatnosc.Pola['IDTytulu']
      rs.Fields.Item("Tytulem").Value=aplatnosc.Pola['Tytulem']
      rs.Fields.Item("Platnik").Value=aplatnosc.Pola['Platnik']
      aPlatnikAdresUlica=aplatnosc.Pola['PlatnikAdresUlica']
      aPlatnikAdresNrPosesji=aplatnosc.Pola['PlatnikAdresNrPosesji']
      aPlatnikAdresNrLokalu=aplatnosc.Pola['PlatnikAdresNrLokalu']
      aPlatnikAdresMiejscowosc=aplatnosc.Pola['PlatnikAdresMiejscowosc']
      aPlatnikAdresKodPocztowy=aplatnosc.Pola['PlatnikAdresKodPocztowy']
      aPlatnikAdresPanstwo=aplatnosc.Pola.get('PlatnikAdresPanstwo','')
      aPlatnikAdresInneInformacje=aplatnosc.Pola['PlatnikAdresInneInformacje']
      aPlatnikAdres=XMLUtil.GetAsXMLStringNoPL(aplatnosc.Pola['PlatnikAdres'])
      if aPlatnikAdresKodPocztowy=='-':
         aPlatnikAdresKodPocztowy=''
      rs.Fields.Item("PlatnikAdresUlica").Value=aPlatnikAdresUlica
      rs.Fields.Item("PlatnikAdresNrPosesji").Value=aPlatnikAdresNrPosesji
      rs.Fields.Item("PlatnikAdresNrLokalu").Value=aPlatnikAdresNrLokalu
      rs.Fields.Item("PlatnikAdresMiejscowosc").Value=aPlatnikAdresMiejscowosc
      rs.Fields.Item("PlatnikAdresKodPocztowy").Value=aPlatnikAdresKodPocztowy
      rs.Fields.Item("PlatnikAdresPanstwo").Value=aPlatnikAdresPanstwo
      rs.Fields.Item("PlatnikAdresInneInformacje").Value=aPlatnikAdresInneInformacje
      rs.Fields.Item("ZwrotkaGrupa").Value=aplatnosc.Pola['ZwrotkaGrupa']
      rs.Fields.Item("PlatnikAdres").Value=aPlatnikAdres
      rs.Fields.Item("TrescDecyzji").Value=XMLUtil.GetAsXMLStringNoPL(aplatnosc.Pola.get('TrescDecyzji',''))
      #2008<
      aPlatnikAdresCzyKraj=aplatnosc.Pola['PlatnikAdresCzyKraj']
      rs.Fields.Item("PlatnikAdresCzyKraj").Value=aPlatnikAdresCzyKraj
      rs.Fields.Item("PlatnikAdresNieruchomosciUlica").Value=aplatnosc.Pola['PlatnikAdresNieruchomosciUlica']
      rs.Fields.Item("PlatnikAdresNieruchomosciNrPosesji").Value=aplatnosc.Pola['PlatnikAdresNieruchomosciNrPosesji']
      rs.Fields.Item("PlatnikAdresNieruchomosciNrLokalu").Value=aplatnosc.Pola['PlatnikAdresNieruchomosciNrLokalu']
      aPlatnikAdresKorespondencjiKodPocztowy=aplatnosc.Pola.get('PlatnikAdresKorespondencjiKodPocztowy','')
      if aPlatnikAdresKorespondencjiKodPocztowy=='-':
         aPlatnikAdresKorespondencjiKodPocztowy=''
      aPlatnikAdresKorespondencjiMiejscowosc=aplatnosc.Pola.get('PlatnikAdresKorespondencjiMiejscowosc','')
      if not aPlatnikAdresKorespondencjiMiejscowosc:
         aPlatnikAdresKorespondencjiMiejscowosc=aplatnosc.Pola.get('PlatnikAdresKorespondencjiMiasto','')
      aPlatnikAdresKorespondencjiUlica=aplatnosc.Pola.get('PlatnikAdresKorespondencjiUlica','')
      aPlatnikAdresKorespondencjiNrPosesji=aplatnosc.Pola.get('PlatnikAdresKorespondencjiNrPosesji','')
      aPlatnikAdresKorespondencjiNrLokalu=aplatnosc.Pola.get('PlatnikAdresKorespondencjiNrLokalu','')
      aPlatnikAdresKorespondencjiCzyKraj=aplatnosc.Pola.get('PlatnikAdresKorespondencjiCzyKraj','')
      aPlatnikAdresKorespondencjiPanstwo=aplatnosc.Pola.get('PlatnikAdresKorespondencjiPanstwo','')
      aPlatnikAdresKorespondencjiInneInformacje=aplatnosc.Pola.get('PlatnikAdresKorespondencjiInneInformacje','')
      if not aPlatnikAdresKorespondencjiUlica:
         aPlatnikAdresKorespondencjiKodPocztowy=aPlatnikAdresKodPocztowy
         aPlatnikAdresKorespondencjiMiejscowosc=aPlatnikAdresMiejscowosc
         aPlatnikAdresKorespondencjiUlica=aPlatnikAdresUlica
         aPlatnikAdresKorespondencjiNrPosesji=aPlatnikAdresNrPosesji
         aPlatnikAdresKorespondencjiNrLokalu=aPlatnikAdresNrLokalu
         aPlatnikAdresKorespondencjiCzyKraj=aPlatnikAdresCzyKraj
         aPlatnikAdresKorespondencjiPanstwo=aPlatnikAdresPanstwo
         aPlatnikAdresKorespondencjiInneInformacje=aPlatnikAdresInneInformacje
      rs.Fields.Item("PlatnikAdresKorespondencjiKodPocztowy").Value=aPlatnikAdresKorespondencjiKodPocztowy
      rs.Fields.Item("PlatnikAdresKorespondencjiMiejscowosc").Value=aPlatnikAdresKorespondencjiMiejscowosc
      rs.Fields.Item("PlatnikAdresKorespondencjiUlica").Value=aPlatnikAdresKorespondencjiUlica
      rs.Fields.Item("PlatnikAdresKorespondencjiNrPosesji").Value=aPlatnikAdresKorespondencjiNrPosesji
      rs.Fields.Item("PlatnikAdresKorespondencjiNrLokalu").Value=aPlatnikAdresKorespondencjiNrLokalu
      rs.Fields.Item("PlatnikAdresKorespondencjiCzyKraj").Value=aPlatnikAdresKorespondencjiCzyKraj
      rs.Fields.Item("PlatnikAdresKorespondencjiPanstwo").Value=aPlatnikAdresKorespondencjiPanstwo
      rs.Fields.Item("PlatnikAdresKorespondencjiInneInformacje").Value=aPlatnikAdresKorespondencjiInneInformacje
      rs.Fields.Item("PlatnikAdresKorespondencjiUlicaNrPosesji").Value=aPlatnikAdresKorespondencjiUlica+' '+aPlatnikAdresKorespondencjiNrPosesji
      #2008>
      return 1
   def OnPolaInformacyjne(self,rs,aplatnosc):
      if aplatnosc.Pola.get('PESEL',''):
         rs1=self.adolib.Recordset()
         asql="select _OID,OIDPozycji,PESEL from %s where _OID='-1'"%(self.PaymentsProcessor.stn_poladodatkoweSIGID,)
         rs1.Open(asql,self.PaymentsProcessor.connection,self.adoconst.adOpenKeyset,self.adoconst.adLockOptimistic)
         if rs1.EOF or rs1.BOF:
            rs1.AddNew()
            rs1.Fields.Item('OIDPozycji').Value=aplatnosc.OID
            rs1.Fields.Item('PESEL').Value=aplatnosc.Pola['PESEL']
            rs1.Update()
         if rs1.State<>self.adoconst.adStateClosed:
            rs1.Close()
      return 1

class MassPaymentsServer:
   def GenerateCSVPackageSRolny(self,aapplication):
      afname=self.GetRandomFileName(aapplication,'sz')
      self.OpenConnection()
      try:
         asql="""
SELECT
IDPaczki,AutorPaczki, Kwota,IDPlatnika,IDTytulu,ZwrotkaGrupa, PMKwotaZaplaty,PMDataZaplaty,PMDataOdbioruDecyzji,PMDataWplywu,PMStatusPlatnosci
FROM
%s
LEFT JOIN
%s
ON
%s._OID = %s.OidPaczki
WHERE PMStatusPlatnosci='K1' and %s.Aplikacja in ('SROLNY','SIGID_R')
"""%(self.stn_buforpreprocesora,self.stn_rejestrpaczek,self.stn_rejestrpaczek,self.stn_buforpreprocesora,self.stn_rejestrpaczek)
         asql="""
SELECT
%s.Kwota AS Kwota1, DataWaluty,DataKsiegowania,DataWyciagu,%s.Status,%s.IDTransakcji,
IDPaczki,AutorPaczki, %s.Kwota AS Kwota2, IDPlatnika,IDTytulu,ZwrotkaGrupa, PMKwotaZaplaty,PMDataZaplaty,PMDataOdbioruDecyzji,PMDataWplywu,PMStatusPlatnosci
FROM
%s
LEFT JOIN
%s
ON
%s.IDTransakcji=%s.IDTransakcji
LEFT JOIN
%s
ON
%s._OID = %s.OidPaczki
WHERE %s.Status='I1' and %s.Aplikacja in ('SROLNY','SIGID_R')
"""%(self.stn_pozycjewyciagu,self.stn_pozycjewyciagu,self.stn_pozycjewyciagu,self.stn_buforpreprocesora,self.stn_pozycjewyciagu,self.stn_buforpreprocesora,self.stn_pozycjewyciagu,self.stn_buforpreprocesora,self.stn_rejestrpaczek,self.stn_rejestrpaczek,self.stn_buforpreprocesora,self.stn_pozycjewyciagu,self.stn_rejestrpaczek,)
         rs=self.GetRS(asql)
         if rs.State!=self.adoconst.adStateClosed:
            afout=CSVImport.CSVExport(adelimiter=';',atextQualifier='"') #"
            afout.Header=["IDPaczki","AutorPaczki", "Kwota","IDPlatnika","IDTytulu","ZwrotkaGrupa", "PMKwotaZaplaty","PMDataZaplaty","PMDataOdbioruDecyzji","PMDataWplywu"]
            afout.Open(afname)
            try:
               cnt=1
               while not rs.EOF and not rs.BOF:
                  afout["IDPaczki"]=ADOLibInit.GetRSValueAsStr(rs,'IDPaczki')
                  afout["AutorPaczki"]=ADOLibInit.GetRSValueAsStr(rs,'AutorPaczki')
                  afout["Kwota"]=ADOLibInit.GetRSValueAsStr(rs,'Kwota2',astype=1)
                  afout["IDPlatnika"]=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
                  afout["IDTytulu"]=ADOLibInit.GetRSValueAsStr(rs,'IDTytulu')
                  afout["ZwrotkaGrupa"]=ADOLibInit.GetRSValueAsStr(rs,'ZwrotkaGrupa')
                  afout["PMKwotaZaplaty"]=ADOLibInit.GetRSValueAsStr(rs,'Kwota1',astype=1)
                  afout["PMDataZaplaty"]=ADOLibInit.GetRSValueAsStr(rs,'DataWaluty',astype=1)
#                  afout["PMDataOdbioruDecyzji"]=ADOLibInit.GetRSValueAsStr(rs,'PMDataOdbioruDecyzji',astype=1)
                  afout["PMDataWplywu"]=ADOLibInit.GetRSValueAsStr(rs,'DataWyciagu',astype=1) #2007 - bylo DataKsiegowania
                  aidtransakcji=ADOLibInit.GetRSValueAsStr(rs,'IDTransakcji')
                  rs.Fields.Item('Status').Value='K1'
                  rs.Update()

                  bsql="""
update %s
set PMStatusPlatnosci='K3'
where IDTransakcji='%s'
"""%(self.stn_buforpreprocesora,aidtransakcji)
                  rs1,status=self.connection.Execute(bsql)
                  if rs1.State<>self.adoconst.adStateClosed:
                     rs1.Close()                           
                  rs1=None

                  afout.Next()
                  rs.MoveNext()
                  cnt=cnt+1
            finally:
               afout.Close()
      finally:
         self.CloseConnection()
   def GenerateCSVPackageSRolnyDatyOdbioruDecyzji(self,aapplication):
      afname=self.GetRandomFileName(aapplication,'sp')
      self.OpenConnection()
      try:
         asql="""
update tmp_bzr_18000
set tmp_bzr_18000.PMDataOdbioruDecyzji=TMP_BZR_36000.DataDoreczenia,tmp_bzr_18000.PMStatusAkceptacji='A2'
from tmp_bzr_18000
inner join TMP_BZR_36000 on TMP_BZR_36000.IdTransakcji=tmp_bzr_18000.IdTransakcji
where TMP_BZR_36000.DataDoreczenia>'2000-01-01' and TMP_BZR_36000.status in('d1','d2') and tmp_bzr_18000.PMStatusAkceptacji='A1'
and datediff(day,TMP_BZR_36000.DataDoreczenia,getdate())>7
"""
         rs=self.GetRS(asql)
         asql="""
SELECT
IDPaczki,AutorPaczki, Kwota,IDPlatnika,IDTytulu,ZwrotkaGrupa, PMKwotaZaplaty,PMDataZaplaty,PMDataOdbioruDecyzji,PMDataWplywu,PMStatusPlatnosci,PMStatusAkceptacji
FROM
%s
LEFT JOIN
%s
ON
%s._OID = %s.OidPaczki
WHERE PMStatusAkceptacji='A2' and %s.Aplikacja='%s'
"""%(self.stn_buforpreprocesora,self.stn_rejestrpaczek,self.stn_rejestrpaczek,self.stn_buforpreprocesora,self.stn_rejestrpaczek,aapplication)
         rs=self.GetRS(asql)
         if rs.State!=self.adoconst.adStateClosed:
            afout=CSVImport.CSVExport(adelimiter=';',atextQualifier='"') #"
            afout.Header=["IDPaczki","AutorPaczki", "Kwota","IDPlatnika","IDTytulu","ZwrotkaGrupa", "PMKwotaZaplaty","PMDataZaplaty","PMDataOdbioruDecyzji","PMDataWplywu"]
            afout.Open(afname)
            try:
               cnt=1
               while not rs.EOF and not rs.BOF:
                  afout["IDPaczki"]=ADOLibInit.GetRSValueAsStr(rs,'IDPaczki')
                  afout["AutorPaczki"]=ADOLibInit.GetRSValueAsStr(rs,'AutorPaczki')
                  afout["Kwota"]=ADOLibInit.GetRSValueAsStr(rs,'Kwota',astype=1)
                  afout["IDPlatnika"]=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
                  afout["IDTytulu"]=ADOLibInit.GetRSValueAsStr(rs,'IDTytulu')
                  afout["ZwrotkaGrupa"]=ADOLibInit.GetRSValueAsStr(rs,'ZwrotkaGrupa')
                  afout["PMKwotaZaplaty"]=ADOLibInit.GetRSValueAsStr(rs,'PMKwotaZaplaty',astype=1)
#                  afout["PMDataZaplaty"]=ADOLibInit.GetRSValueAsStr(rs,'PMDataZaplaty',astype=1)
                  afout["PMDataOdbioruDecyzji"]=ADOLibInit.GetRSValueAsStr(rs,'PMDataOdbioruDecyzji',astype=1)
#                  afout["PMDataWplywu"]=ADOLibInit.GetRSValueAsStr(rs,'PMDataWplywu',astype=1)
                  afout.Next()
                  rs.Fields.Item('PMStatusAkceptacji').Value='A3'
                  rs.Update()
                  rs.MoveNext()
                  cnt=cnt+1
            finally:
               afout.Close()
      finally:
         self.CloseConnection()
   def GeneratePDFPrintDataSRolny(self,arok,aplatnikid):
      arok='A'+str(arok)[-1:]
      ret=[]
      amaxcnt=0
      self.OpenConnection()
      try:
         tt1=time.time()
         asql="select * from %s where idtytulu in ('R%s01000','R%s02000','R%s03000','R%s04000') and idplatnika='%s' order by PlatnikAdresMiejscowosc, PlatnikAdresUlica, PlatnikAdresNrPosesji, PlatnikAdresNrLokalu, IDPlatnika, IDTytulu"%(self.stn_buforpreprocesora,arok,arok,arok,arok,aplatnikid)
         rs=self.GetRS(asql)
         tt2=time.time()
#         print 't1:',tt2-tt1
         if rs.State!=self.adoconst.adStateClosed:
            acnt=0
            while not rs.EOF and not rs.BOF:
               asumakwota=0.0
               d1,ld2,d2={},[],{}
               lidplatnika=aidplatnika=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
               aidtransakcji=self.GetCheckSum(ADOLibInit.GetRSValueAsStr(rs,'IDTransakcji'))
               d1["TrescPieczatki"]=ADOLibInit.GetRSValueAsStr(rs,'TrescPieczatki')
               d1["TrescDecyzji"]=XMLUtil.GetXMLStringAsString(ADOLibInit.GetRSValueAsStr(rs,'TrescDecyzji'))
               aformid,aprzelewycnt=0,0
               while not rs.EOF and not rs.BOF:
                  aidplatnika=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
                  if lidplatnika!=aidplatnika:
                     break
                  akwota=ADOLibInit.GetRSValueAsStr(rs,'Kwota')
                  if akwota!='0.00':
                     if not aformid:
                        aformid=aformid+1
                     asumakwota=asumakwota+float(akwota)
                     akwotaslownie=ICORUtil.KwotaSlownie(float(akwota))
                     anrb=ADOLibInit.GetRSValueAsStr(rs,'KontoNRB')
                     abank=ADOLibInit.GetRSValueAsStr(rs,'KontoBank')
                     arachunek=ADOLibInit.GetRSValueAsStr(rs,'KontoBankNr')+ADOLibInit.GetRSValueAsStr(rs,'KontoTransakcja')+ADOLibInit.GetRSValueAsStr(rs,'KontoRachunek')
                     aidtransakcji=self.GetCheckSum(ADOLibInit.GetRSValueAsStr(rs,'IDTransakcji'))
                     aidtytulu=ADOLibInit.GetRSValueAsStr(rs,'IDTytulu')
                     d2["IDPlatnika_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
                     d2["IDTytulu_%d"%aformid]=aidtytulu
                     d2["Platnik_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'Platnik')
                     d2["Kwota_%d"%aformid]=akwota
                     d2["KwotaSlownie_%d"%aformid]=akwotaslownie
                     d2["DataWymagalnosci_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'DataWymagalnosci')
                     d2["Tytulem_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'Tytulem')+': rata '+aidtytulu[4:5]
                     d2["IDTransakcji_%d"%aformid]=aidtransakcji
                     d2["KontoOdbiorcy_%d"%aformid]=anrb+'-'+abank+'-'+arachunek
                     d2["KontoLiczbaKontrolna_%d"%aformid]=anrb
                     d2["KontoBank_%d"%aformid]=abank
                     d2["KontoRachunek_%d"%aformid]=arachunek
                     d2["PlatnikAdres_%d"%aformid]=XMLUtil.GetXMLStringAsString(ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdres'))
                     d2["PlatnikAdresUlica_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresUlica')
                     d2["PlatnikAdresNrPosesji_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrPosesji')
                     d2["PlatnikAdresNrLokalu_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrLokalu')
                     d2["PlatnikAdresKodPocztowy_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresKodPocztowy')
                     d2["PlatnikAdresMiejscowosc_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresMiejscowosc')
                     d2["PlatnikAdresInneInformacje_%d"%aformid]=ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresInneInformacje')
                     aformid=aformid+1
                     if aformid>2:
                        ld2.append(d2)
                        d2={}
                        aformid=0
                     aprzelewycnt=aprzelewycnt+1
                  else:
                     pass
                  acnt=acnt+1
                  rs.MoveNext()
               if aformid:
                  ld2.append(d2)
               if ld2:
                  dd={}
                  dd.update(ld2[0])
                  asumakwotaslownie=ICORUtil.KwotaSlownie(asumakwota)
                  dd["Kwota_1"]='%0.2f'%asumakwota
                  dd["KwotaSlownie_1"]=asumakwotaslownie
                  for akey in dd.keys():
                     if akey[-2:]=='_1':
                        dd[akey[:-1]+'2']=dd[akey]
                  dd["Kwota_2"]=''
                  dd["KwotaSlownie_2"]=''
                  ld2.append(dd)
               ret.append([d1,ld2])
         tt3=time.time()
#         print 't2:',tt3-tt2
      finally:
         self.CloseConnection()
      return ret


