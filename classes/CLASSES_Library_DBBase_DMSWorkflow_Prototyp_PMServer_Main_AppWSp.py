# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserPaczki as XMLParserPaczki
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppUtil as AppUtil
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import appplatform.startutil as startutil

class PMPlatnoscWSp(XMLParserPaczki.PMPlatnosc):
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

class PaymentsManagerWSp(AppUtil.PaymentsManager):
   def __init__(self,*args):
      apply(AppUtil.PaymentsManager.__init__,(self,)+args)
      self.AccountBank='12401864'
      self.AccountAcc1='5111'
      self.AccountAcc2='00133'
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
   def GenerateXMLPrintPackageWSp(self,aapplication,afname,alocalcity=0):
      amaxcnt=0
      self.OpenConnection()
      try:
         if aapplication=='WSP':
            if alocalcity>0:
               sp=" AND PlatnikAdresMiejscowosc='%s'"%startutil.appconfig.IParams['pm_miasto']
            elif alocalcity==-1:
               sp=""
            else:
               sp=" AND PlatnikAdresMiejscowosc<>'%s'"%startutil.appconfig.IParams['pm_miasto']
#               asql="SELECT IDPlatnika,IDTytulu,Platnik,Kwota,DataWymagalnosci,Tytulem,PlatnikAdres,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu,PlatnikAdresKodPocztowy,PlatnikAdresMiejscowosc,PlatnikAdresGmina,PlatnikAdresPowiat,PlatnikAdresWojewodztwo,PlatnikAdresPanstwo,PlatnikAdresInneInformacje,CAST(TrescPrzelewu AS Varchar(8000)) AS TrescPrzelewu FROM %s WHERE IDTytulu='%s' AND czyjuzzaplacono=0 %s ORDER BY PlatnikAdresMiejscowosc,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu"%(self.stn_buforpreprocesora,aapplication,sp)
#            asql="SELECT IDPlatnika,IDTytulu,Platnik,Kwota,DataWymagalnosci,Tytulem,PlatnikAdres,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu,PlatnikAdresKodPocztowy,PlatnikAdresMiejscowosc,PlatnikAdresGmina,PlatnikAdresPowiat,PlatnikAdresWojewodztwo,PlatnikAdresPanstwo,PlatnikAdresInneInformacje,TrescDecyzji FROM %s WHERE IDTytulu like 'RA%%' AND czyjuzzaplacono=0 %s ORDER BY PlatnikAdresMiejscowosc,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu"%(self.stn_buforpreprocesora,sp)
            asql1="""
SELECT
count(%s._OID) as Ilosc 
FROM
%s
LEFT JOIN
%s
ON
%s._OID = %s.OidPaczki
WHERE 
CzyJuzZaplacono='0' and Aplikacja='WSP'
and (Kwota-PMKwotaZaplaty)>0.0
and PMStatusPlatnosci='I1'
--and Kwota<1.4
%s
"""%(self.stn_buforpreprocesora,self.stn_buforpreprocesora,self.stn_rejestrpaczek,self.stn_rejestrpaczek,self.stn_buforpreprocesora,sp) #'E3'
            atop=''
            if amaxcnt:
               atop='top '+str(amaxcnt)
            sorder2=''
#            if aonlydecisions:
#               sorder2='Platnik, '
            asql2="""
SELECT
--count(TMP_BZR_18000._OID)
%s
--*
Kwota,(Kwota-PMKwotaZaplaty) as CalcDoZaplaty,
IDPlatnika,IDTransakcji,IDTytulu,Platnik,Tytulem,DataWymagalnosci,
PlatnikAdres,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu,PlatnikAdresKodPocztowy,PlatnikAdresMiejscowosc,PlatnikAdresInneInformacje,
TrescPrzelewu,
KontoNRB,KontoBank,KontoBankNr,KontoTransakcja,KontoRachunek
FROM
%s
LEFT JOIN
%s
ON
%s._OID = %s.OidPaczki
WHERE 
CzyJuzZaplacono='0' and Aplikacja='WSP'
and (Kwota-PMKwotaZaplaty)>0.0
and PMStatusPlatnosci='I1'
--and Kwota<1.4
%s
ORDER BY 
%s
PlatnikAdresMiejscowosc, PlatnikAdresUlica, PlatnikAdresNrPosesji, PlatnikAdresNrLokalu, IDPlatnika, IDTytulu
"""%(atop,self.stn_buforpreprocesora,self.stn_rejestrpaczek,self.stn_rejestrpaczek,self.stn_buforpreprocesora,sp,sorder2) #'E3'
#               asql="SELECT * FROM %s WHERE IDTytulu='%s' AND czyjuzzaplacono=0 %s ORDER BY PlatnikAdresMiejscowosc,PlatnikAdresUlica,PlatnikAdresNrPosesji,PlatnikAdresNrLokalu"%(self.stn_buforpreprocesora,aapplication,sp)
         else:
            asql=''
#         atrescpieczatki=''
         if not amaxcnt:
            rs1=self.GetRS(asql1)
            amaxcnt=rs1.Fields.Item('Ilosc').Value
            if rs1.State!=self.adoconst.adStateClosed:
               rs1.Close()
            rs1=None
         print 'MaxCnt:',amaxcnt
         rs=self.GetRS(asql2)
#         if not aonlydecisions:
#            apieczatkapos,apieczatkacnt=0,0
#            apieczatkatresc,apieczatkamax=lpieczatki[apieczatkapos]
         adecyzjecnt=0
         if rs.State!=self.adoconst.adStateClosed:
            fout=XMLUtil.MXMLFile(afname,anopl=1)
            fout.Header()
            fout.TagOpen('PMWYDRUKI',{'wersja':'1.0.1'})
            fout.TagOpen('NAGLOWEK')
            fout.TagOpen('DANE',{'nazwa':'DataUtworzenia','wartosc':ICORUtil.tdatetime2fmtstr(ICORUtil.tdate(),adelimiter='-')},aclosetag=1)
            fout.TagOpen('DANE',{'nazwa':'Autor','wartosc':'PMAdminRS'},aclosetag=1)
            fout.TagClose()
            fout.TagOpen('PAKIETY')
            try:
               acnt=0
               while not rs.EOF and not rs.BOF:
                  lidplatnika=aidplatnika=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
                  aidtransakcji=self.GetCheckSum(ADOLibInit.GetRSValueAsStr(rs,'IDTransakcji'))
#                  if aonlydecisions:
#                     apieczatkatresc=ADOLibInit.GetRSValueAsStr(rs,'TrescPieczatki')
#                  akwota=ADOLibInit.GetRSValueAsStr(rs,'Kwota')
#                  if akwota=='0.00':
#                     print 'kwota == 0.00 dla platnika:',aidplatnika
#                     acnt=acnt+1
#                     rs.MoveNext()
#                     continue
                  fout.TagOpen('PAKIET')
                  fout.TagOpen('FORMULARZ',{'idformularza':'um-przelew-1'})
                  fout.TagOpen('POLE',{'nazwa':'IDPlatnika','wartosc':aidplatnika},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'Platnik','wartosc':ADOLibInit.GetRSValueAsStr(rs,'Platnik')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'Tytulem','wartosc':ADOLibInit.GetRSValueAsStr(rs,'Tytulem')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'IDTransakcji','wartosc':aidtransakcji},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdres','wartosc':XMLUtil.GetXMLStringAsString(ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdres'))},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresUlica','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresUlica')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresNrPosesji','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrPosesji')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresNrLokalu','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrLokalu')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresKodPocztowy','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresKodPocztowy')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresMiejscowosc','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresMiejscowosc')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresInneInformacje','wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresInneInformacje')},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'TrescPieczatki','wartosc':XMLUtil.GetXMLStringAsString(apieczatkatresc)},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'TrescPrzelewu','wartosc':XMLUtil.GetXMLStringAsString(ADOLibInit.GetRSValueAsStr(rs,'TrescPrzelewu'))},aclosetag=1)
#                  fout.TagClose()
#                  if not aonlydecisions:
#                     apieczatkacnt=apieczatkacnt+1
#                     if apieczatkacnt>=apieczatkamax:
#                        apieczatkapos=apieczatkapos+1
#                        apieczatkacnt=0
#                        apieczatkatresc,apieczatkamax=lpieczatki[apieczatkapos]
#                  aformid,aprzelewycnt=0,0
#                  while not rs.EOF and not rs.BOF:
#                     aidplatnika=ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')
#                     if lidplatnika!=aidplatnika:
#                        break
#                     if not aonlydecisions:
                  akwota=ADOLibInit.GetRSValueAsStr(rs,'CalcDoZaplaty')
#                        if akwota!='0.00':
#                           if not aformid:
#                              fout.TagOpen('FORMULARZ',{'idformularza':'um-przelew-2'})
#                              aformid=aformid+1
                  akwotaslownie=ICORUtil.KwotaSlownie(float(akwota))
                  anrb=ADOLibInit.GetRSValueAsStr(rs,'KontoNRB')
                  abank=ADOLibInit.GetRSValueAsStr(rs,'KontoBank')
                  arachunek=ADOLibInit.GetRSValueAsStr(rs,'KontoBankNr')+ADOLibInit.GetRSValueAsStr(rs,'KontoTransakcja')+ADOLibInit.GetRSValueAsStr(rs,'KontoRachunek')
                  aidtransakcji=self.GetCheckSum(ADOLibInit.GetRSValueAsStr(rs,'IDTransakcji'))
                  aidtytulu=ADOLibInit.GetRSValueAsStr(rs,'IDTytulu')
#                  fout.TagOpen('POLE',{'nazwa':'IDPlatnika_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'IDPlatnika')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'IDTytulu','wartosc':aidtytulu},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'Platnik_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'Platnik')},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'Kwota','wartosc':akwota},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'KwotaSlownie','wartosc':akwotaslownie},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'DataWymagalnosci','wartosc':ADOLibInit.GetRSValueAsStr(rs,'DataWymagalnosci')},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'Tytulem_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'Tytulem')+': rata '+aidtytulu[4:5]},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'IDTransakcji_%d'%aformid,'wartosc':aidtransakcji},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'KontoOdbiorcy','wartosc':anrb+'-'+abank+'-'+arachunek},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'KontoLiczbaKontrolna','wartosc':anrb},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'KontoBank','wartosc':abank},aclosetag=1)
                  fout.TagOpen('POLE',{'nazwa':'KontoRachunek','wartosc':arachunek},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdres_%d'%aformid,'wartosc':XMLUtil.GetXMLStringAsString(ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdres'))},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresUlica_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresUlica')},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresNrPosesji_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrPosesji')},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresNrLokalu_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresNrLokalu')},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresKodPocztowy_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresKodPocztowy')},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresMiejscowosc_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresMiejscowosc')},aclosetag=1)
#                  fout.TagOpen('POLE',{'nazwa':'PlatnikAdresInneInformacje_%d'%aformid,'wartosc':ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdresInneInformacje')},aclosetag=1)
#                           aformid=aformid+1
#                           if aformid>2:
#                              aformid=0
#                              fout.TagClose()
#                        aprzelewycnt=aprzelewycnt+1
#                     else:
#                        pass
#                        print 'kwota == 0.00 dla platnika:',aidplatnika
#                     acnt=acnt+1
#                     if not aonlydecisions:
#                        rs.Fields.Item('TrescPieczatki').Value=apieczatkatresc
#                        rs.Update()
                  rs.MoveNext()
                  adecyzjecnt=adecyzjecnt+1
#                  if not aonlydecisions:
#                     if aformid:
                  fout.TagClose()
#                     if aprzelewycnt!=4:
#                        print 'platnik z %d ratami: %s'%(aprzelewycnt,lidplatnika)
                  fout.TagClose()
                  print amaxcnt-acnt,'\r',
            finally:
               fout.TagClose()
               fout.TagClose()
         print 'Ilosc decyzji:',adecyzjecnt
      finally:
         self.CloseConnection()

