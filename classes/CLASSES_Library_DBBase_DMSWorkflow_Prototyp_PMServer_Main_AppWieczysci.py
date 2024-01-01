# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserPaczki as XMLParserPaczki
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppUtil as AppUtil
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import appplatform.startutil as startutil
import appplatform.startutil as startutil

class PMPlatnoscWGmina(XMLParserPaczki.PMPlatnosc):
   def __init__(self,*args):
      apply(XMLParserPaczki.PMPlatnosc.__init__,(self,)+args)
      self.DigestFields=['Kwota','DataWymagalnosci','IDPlatnika','IDTytulu','Tytulem','Platnik'] # 'TrescPrzelewu'
      self.IDDigestFields=['IDPlatnika','Platnik','PlatnikAdresMiejscowosc','PlatnikAdresUlica','PlatnikAdresNrPosesji','PlatnikAdresNrLokalu']

"""
OID paczki|OID paczki|OID

Kwota|Kwota|Pieni�dze
Data wymagalno�ci|Data wymagalno�ci|Data
ID p�atnika|ID p�atnika|Ci�g znak�w - 1 linia
ID tytu�u|ID tytu�u|Ci�g znak�w - 1 linia
Tytu�em|Tytu�em|Ci�g znak�w - 1 linia
P�atnik|P�atnik|Ci�g znak�w - 1 linia
Tre�� decyzji|Tre�� decyzji|Opis
Tre�� przelewu|Tre�� przelewu|Opis
Tre�� zwrotki|Tre�� zwrotki|Opis

PM kwota zap�aty|PM kwota zap�aty|Pieni�dze
PM data zap�aty|PM data zap�aty|Data
PM bank|PM bank|Ci�g znak�w - 1 linia
PM kasa|PM kasa|Ci�g znak�w - 1 linia
PM kasjer|PM kasjer|Ci�g znak�w - 1 linia
PM data wp�ywu|PM data wp�ywu|Data i czas
PM status p�atno�ci|PM status p�atno�ci|Ci�g znak�w - 1 linia

Czy anulowano|Czy anulowano|Liczba ca�kowita
Czy ju� zap�acono|Czy ju� zap�acono|Liczba ca�kowita
Czy bez kwoty|Czy bez kwoty|Liczba ca�kowita
Czy g��wna p�atno�� grupy|Czy g��wna p�atno�� grupy|Liczba ca�kowita

Data akceptacji|Data akceptacji|Data
OID p�atno�ci g��wnej|OID p�atno�ci g��wnej|OID

Klucz g��wny|Klucz g��wny|Kod, Identyfikator
Suma kontrolna|Suma kontrolna|Kod, Identyfikator

Zwrotka grupa|Zwrotka grupa|Ci�g znak�w - 1 linia

P�atnik Adres|P�atnik Adres|Opis
P�atnik Adres Ulica|P�atnik Adres Ulica|Ci�g znak�w - 1 linia
P�atnik Adres Nr posesji|P�atnik Adres Nr posesji|Ci�g znak�w - 1 linia
P�atnik Adres Nr lokalu|P�atnik Adres Nr lokalu|Ci�g znak�w - 1 linia
P�atnik Adres Kod pocztowy|P�atnik Adres Kod pocztowy|Ci�g znak�w - 1 linia
P�atnik Adres Miejscowo��|P�atnik Adres Miejscowo��|Ci�g znak�w - 1 linia
P�atnik Adres Gmina|P�atnik Adres Gmina|Ci�g znak�w - 1 linia
P�atnik Adres Powiat|P�atnik Adres Powiat|Ci�g znak�w - 1 linia
P�atnik Adres Wojew�dztwo|P�atnik Adres Wojew�dztwo|Ci�g znak�w - 1 linia
P�atnik Adres Pa�stwo|P�atnik Adres Pa�stwo|Ci�g znak�w - 1 linia
P�atnik Adres Inne informacje|P�atnik Adres Inne informacje|Ci�g znak�w - 1 linia

PM Data odbioru decyzji|PM Data odbioru decyzji|Data
"""

class PaymentsManagerWGmina(AppUtil.PaymentsManager):
   def __init__(self,*args):
      apply(AppUtil.PaymentsManager.__init__,(self,)+args)
      self.AccountBank=startutil.appconfig.IParams['pm_AccountBankWie']
      self.AccountAcc1=startutil.appconfig.IParams['pm_AccountAcc1Wie']
      self.AccountAcc2=startutil.appconfig.IParams['pm_AccountAcc2Wie']
   def OnNowaPozycja(self,rs,aplatnosc):
      rs.Fields.Item("Kwota").Value=aplatnosc.Pola['Kwota']
      rs.Fields.Item("DataWymagalnosci").Value=ICORUtil.tdatetime2fmtstr(aplatnosc.Pola['DataWymagalnosci'],adelimiter='-')
      rs.Fields.Item("IDPlatnika").Value=aplatnosc.Pola['IDPlatnika']
      rs.Fields.Item("IDTytulu").Value=aplatnosc.Pola['IDTytulu']
      rs.Fields.Item("Tytulem").Value=aplatnosc.Pola['Tytulem']
      rs.Fields.Item("Platnik").Value=aplatnosc.Pola['Platnik']
      rs.Fields.Item("PlatnikAdres").Value=XMLUtil.GetAsXMLStringNoPL(aplatnosc.Pola.get('PlatnikAdres',''))
      rs.Fields.Item("PlatnikAdresUlica").Value=aplatnosc.Pola.get('PlatnikAdresUlica','')
      rs.Fields.Item("PlatnikAdresNrPosesji").Value=aplatnosc.Pola.get('PlatnikAdresNrPosesji','')
      rs.Fields.Item("PlatnikAdresNrLokalu").Value=aplatnosc.Pola.get('PlatnikAdresNrLokalu','')
      rs.Fields.Item("PlatnikAdresKodPocztowy").Value=aplatnosc.Pola.get('PlatnikAdresKodPocztowy','')
      rs.Fields.Item("PlatnikAdresMiejscowosc").Value=aplatnosc.Pola.get('PlatnikAdresMiejscowosc','')
      rs.Fields.Item("PlatnikAdresGmina").Value=aplatnosc.Pola.get('PlatnikAdresGmina','')
      rs.Fields.Item("PlatnikAdresPowiat").Value=aplatnosc.Pola.get('PlatnikAdresPowiat','')
      rs.Fields.Item("PlatnikAdresWojewodztwo").Value=aplatnosc.Pola.get('PlatnikAdresWojewodztwo','')
      rs.Fields.Item("PlatnikAdresPanstwo").Value=aplatnosc.Pola.get('PlatnikAdresPanstwo','')
      rs.Fields.Item("PlatnikAdresInneInformacje").Value=aplatnosc.Pola.get('PlatnikAdresInneInformacje','')
      rs.Fields.Item("TrescPrzelewu").Value=XMLUtil.GetAsXMLStringNoPL(aplatnosc.Pola.get('TrescPrzelewu',''))
      return 1

class MassPaymentsServer:
   def GenerateXMLPrintPackageWGmina(self,aapplication,afname,alocalcity=0):
      self.OpenConnection()
      try:
         if aapplication=='WGMINA':
            if alocalcity>0:
               sp=" AND PlatnikAdresMiejscowosc='%s'"%startutil.appconfig.IParams['pm_miasto']
            elif alocalcity==-1:
               sp=""
            else:
               sp=" AND PlatnikAdresMiejscowosc<>'%s'"%startutil.appconfig.IParams['pm_miasto']
#               asql="SELECT IDPlatnika,IDTytulu,Platnik,Kwota,DataWymagalnosci,Tytulem,PlatnikAdres,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu,PlatnikAdresKodPocztowy,PlatnikAdresMiejscowosc,PlatnikAdresGmina,PlatnikAdresPowiat,PlatnikAdresWojewodztwo,PlatnikAdresPanstwo,PlatnikAdresInneInformacje,CAST(TrescPrzelewu AS Varchar(8000)) AS TrescPrzelewu FROM %s WHERE IDTytulu='%s' AND czyjuzzaplacono=0 %s ORDER BY PlatnikAdresMiejscowosc,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu"%(self.stn_buforpreprocesora,aapplication,sp)
            asql="SELECT IDPlatnika,IDTytulu,Platnik,Kwota,DataWymagalnosci,Tytulem,PlatnikAdres,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu,PlatnikAdresKodPocztowy,PlatnikAdresMiejscowosc,PlatnikAdresGmina,PlatnikAdresPowiat,PlatnikAdresWojewodztwo,PlatnikAdresPanstwo,PlatnikAdresInneInformacje,TrescPrzelewu FROM %s WHERE IDTytulu='%s' AND czyjuzzaplacono=0 %s ORDER BY PlatnikAdresMiejscowosc,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu"%(self.stn_buforpreprocesora,aapplication,sp)
#               asql="SELECT * FROM %s WHERE IDTytulu='%s' AND czyjuzzaplacono=0 %s ORDER BY PlatnikAdresMiejscowosc,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu"%(self.stn_buforpreprocesora,aapplication,sp)
         else:
            asql=''
         rs=self.GetRS(asql)
         if rs.State!=self.adoconst.adStateClosed:
            fout=XMLUtil.MXMLFile(afname,anopl=1)
            fout.Header()
            fout.TagOpen('PMWYDRUKI',{'wersja':'1.0.0'})
            fout.TagOpen('NAGLOWEK')
            fout.TagOpen('DANE',{'nazwa':'DataUtworzenia','wartosc':ICORUtil.tdatetime2fmtstr(ICORUtil.tdate(),adelimiter='-')},aclosetag=1)
            fout.TagOpen('DANE',{'nazwa':'Autor','wartosc':'PMAdminSK'},aclosetag=1)
            fout.TagClose()
            fout.TagOpen('PAKIETY')
            try:
               while not rs.EOF and not rs.BOF:
                  fout.TagOpen('PAKIET')
                  fout.TagOpen('FORMULARZ',{'idformularza':'WI-P-1'})
                  fout.TagOpen('POLE',{'nazwa':'IDPlatnika','wartosc':ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'IDTytulu','wartosc':ADOLibInit.GetRSValueAsStr(rs,'IDTytulu')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'Platnik','wartosc':ADOLibInit.GetRSValueAsStr(rs,'Platnik')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'Kwota','wartosc':ADOLibInit.GetRSValueAsStr(rs,'Kwota')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'DataWymagalnosci','wartosc':ADOLibInit.GetRSValueAsStr(rs,'DataWymagalnosci')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'Tytulem','wartosc':ADOLibInit.GetRSValueAsStr(rs,'Tytulem')},aclosetag=1)
                  atransid=self.GetTransID(achecksum=0)
                  fout.TagOpen('POLE',{'nazwa':'NrRachunkuBankowego','wartosc':'22-88888888-4444-'+atransid+'-55555'},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'IdTransakcji','wartosc':'55555'+atransid+str(self.GetCheckSum('55555'+atransid))},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdres','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdres')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresUlica','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresUlica')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresNrPosesji','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrPosesji')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresNrLokalu','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrLokalu')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresKodPocztowy','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresKodPocztowy')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresMiejscowosc','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresMiejscowosc')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresGmina','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresGmina')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresPowiat','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresPowiat')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresWojewodztwo','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresWojewodztwo')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresPanstwo','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresPanstwo')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresInneInformacje','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresInneInformacje')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'TrescPrzelewu','wartosc':ADOLibInit.GetRSValueAsStr(rs,'TrescPrzelewu')},aclosetag=1)
                  fout.TagClose()
                  fout.TagClose()
                  print '.',
                  rs.MoveNext()
            finally:
               fout.TagClose()
               fout.TagClose()
      finally:
         self.CloseConnection()
   def GenerateCSVPackageWGmina(self,aapplication,afname):
      self.OpenConnection()
      try:
         asql="""
SELECT
IDPaczki, Kwota,IDPlatnika,PMKwotaZaplaty,PMDataZaplaty,PMDataWplywu, PMStatusPlatnosci
FROM
%s
LEFT JOIN
%s
ON
%s._OID = %s.OidPaczki
WHERE PMStatusPlatnosci='K1' and %s.Aplikacja='%s'
"""%(self.stn_buforpreprocesora,self.stn_rejestrpaczek,self.stn_rejestrpaczek,self.stn_buforpreprocesora,self.stn_rejestrpaczek,aapplication)
         rs=self.GetRS(asql)
         if rs.State!=self.adoconst.adStateClosed:
            afout=CSVImport.CSVExport(adelimiter=';',atextQualifier='"') #"
            afout.Header=["IDPaczki","Kwota","IDPlatnika","PMKwotaZaplaty","PMDataZaplaty","PMDataWplywu"]
            afout.Open(afname)
            try:
               cnt=1
               while not rs.EOF and not rs.BOF:
                  afout["IDPaczki"]=ADOLibInit.GetRSValueAsStr(rs,'IDPaczki')
                  afout["Kwota"]=ADOLibInit.GetRSValueAsStr(rs,'Kwota',astype=1)
                  afout["IDPlatnika"]=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
                  afout["PMKwotaZaplaty"]=ADOLibInit.GetRSValueAsStr(rs,'PMKwotaZaplaty',astype=1)
                  afout["PMDataZaplaty"]=ADOLibInit.GetRSValueAsStr(rs,'PMDataZaplaty',astype=1)
                  afout["PMDataWplywu"]=ADOLibInit.GetRSValueAsStr(rs,'PMDataWplywu',astype=1)
                  afout.Next()
                  rs.MoveNext()
                  cnt=cnt+1
            finally:
               afout.Close()
      finally:
         self.CloseConnection()

