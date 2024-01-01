# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_IBAN as IBAN
import appplatform.startutil as startutil
import random
import string
import time
import sha
import os

def GetPackageFileInfo(afname,anohash=0):
   asize=0
   amsize=os.path.getsize(afname)
   if anohash:
      asize=amsize
   ahash=''
   alastline=0
   fin=open(afname,'rb')
   try:
      if not anohash:
         asha=sha.new()
         while 1:
            abuff=fin.read(65536)
            if not abuff:
               break
            asha.update(abuff)
            asize=asize+len(abuff)
            InfoStatus('Hash left: '+str(amsize-asize))
         ahash=asha.hexdigest()
         InfoStatus('')
      if asize>100:
         fin.seek(-100,2)
         atext=fin.read(100)
         l=string.split(atext,'\n')
         l.reverse()
         for s in l:
            if string.find(s,'</PMPACZKA>')>=0:
               alastline=1
               break
      if not alastline:
         ahash=''
   finally:
      fin.close()
   return ahash,asize,alastline

def GetZaplatyFileInfo(afname):
   asize=os.path.getsize(afname)
   alastline=0
   fin=open(afname,'rb')
   try:
      if asize>100:
         fin.seek(-100,2)
         atext=fin.read(100)
         l=string.split(atext,'\n')
         l.reverse()
         for s in l:
            if string.find(s,'</DANE>')>=0:
               alastline=1
               break
   finally:
      fin.close()
   return asize,alastline

class PaymentsManager:
   def __init__(self,aparser,aapplication):
      self.PaymentsParser=aparser
      self.PaymentsProcessor=aparser.PaymentsProcessor
      self.Aplikacja=aapplication
      self.adolib=self.PaymentsProcessor.adolib
      self.adoconst=self.PaymentsProcessor.adoconst
      self.AccountBank=''
      self.AccountAcc1=''
      self.AccountAcc2=''
      self._TransID=[]
   def GetTransID(self):
      if self._TransID:
         return self._TransID.pop()[:-5] #[:-len(self.AccountAcc2)]
      rs=self.adolib.Recordset()
      acnt=100
      while acnt>0:
         self._TransID=[]
         for i in range(4):
            n1=random.randrange(0,10000000)
            self._TransID.append('%07d%s'%(n1,self.AccountAcc2))
         asql="select top 1 IDTransakcji from %s where IDTransakcji in (%s)"%(self.PaymentsProcessor.stn_buforpreprocesora,str(self._TransID)[1:-1])
         rs.Open(asql,self.PaymentsProcessor.connection,self.adoconst.adOpenKeyset,self.adoconst.adLockOptimistic)
         if rs.EOF or rs.BOF:
            if rs.State<>self.adoconst.adStateClosed:
               rs.Close()
            return self._TransID.pop()[:-5] #[:-len(self.AccountAcc2)]
         if rs.State<>self.adoconst.adStateClosed:
            rs.Close()
         acnt=acnt-1
      return ''
   def GetAccountInfo(self,atransid):
      ret=''
      try:
         ret=IBAN.create_iban('PL',self.AccountBank,self.AccountAcc1+atransid+self.AccountAcc2)
      except IBAN.IBANError,err:
         self.PaymentsProcessor.ImportStatus.append('  IBAN Error: '+self.AccountBank+' '+self.AccountAcc1+' '+atransid+' '+self.AccountAcc2)
         print err
      return ret[2:4],ret[4:12],ret[12:]
   def StorePlatnosc(self,aplatnosc):
      asql="SELECT * FROM %s WHERE SumaKontrolna='%s'"%(self.PaymentsProcessor.stn_buforpreprocesora,aplatnosc.Digest)
      rs=self.PaymentsProcessor.GetRS(asql)
      if rs.State!=self.adoconst.adStateClosed:
         w,wnowe=0,0
         if rs.EOF or rs.BOF:
            rs.AddNew()
            wnowe=1
            InfoStatus('%s: %d %s %s %s'%(self.PaymentsProcessor.BaseName,self.PaymentsParser.MaxPayments-self.PaymentsParser.PaymentsCnt,self.PaymentsParser.Elapsed,self.PaymentsParser.Estimated,self.PaymentsParser.Remaining))
            rs.Fields.Item('OIDPaczki').Value=self.PaymentsProcessor.OIDPaczki
            rs.Fields.Item('PMStatusPlatnosci').Value='I1'
            rs.Fields.Item('PMStatusAkceptacji').Value='A1'
            rs.Fields.Item('SumaKontrolna').Value=aplatnosc.Digest
            rs.Fields.Item('SumaKontrolnaPlatnika').Value=aplatnosc.DigestID
            for apname in ['DataWymagalnosci','PMDataWplywu','PMDataOdbioruDecyzji','DataAkceptacji','PMDataZaplaty']:
               rs.Fields.Item(apname).Value='1900-01-01'
            w1=self.OnNowaPozycja(rs,aplatnosc)
            w=w or w1
            atransid,anrb,abank,aaccount=self.OnTransID(rs,aplatnosc)
         else:
            pass
            self.PaymentsParser.PaymentsExisting=1+self.PaymentsParser.PaymentsExisting
            self.PaymentsProcessor.ImportStatus.append('  Platnosc juz istnieje: '+aplatnosc.Digest+' - '+str(aplatnosc))
         if aplatnosc.CzyJuzZaplacono:
            w1=self.OnCzyJuzZaplacono(rs,aplatnosc)
            if w1:
               rs.Fields.Item('PMStatusPlatnosci').Value='K3'
            w=w or w1
         if aplatnosc.CzyAnulowano:
            w1=self.OnCzyAnulowano(rs,aplatnosc)
            if w1:
               rs.Fields.Item('PMStatusPlatnosci').Value='99'
            w=w or w1
         if aplatnosc.DataAkceptacji!=(0,0,0):
            w1=self.OnDataAkceptacji(rs,aplatnosc)
            if w1:
               rs.Fields.Item('PMStatusAkceptacji').Value='A3'
            w=w or w1
         if aplatnosc.CzyAktualizacjaTresci:
            w1=self.OnAktualizacjaTresci(rs,aplatnosc)
            w=w or w1
         if aplatnosc.CzyBezKwoty:
            w1=self.OnCzyBezKwoty(rs,aplatnosc)
            w=w or w1
         if not aplatnosc.NadPlatnosc is None: #raty
            w1=self.OnNadPlatnosc(rs,aplatnosc)
            w=w or w1
         if aplatnosc.CzyPlatnoscGrupowa:
            w1=self.OnPlatnoscGrupowa(rs,aplatnosc)
            w=w or w1
         if w:
            acnt=7
            while acnt>0:
               try:
                  rs.Update()
                  break
               except:
                  acnt=acnt-1
                  if not acnt:
                     raise
                  print 'waiting for update',aplatnosc.Digest,acnt
                  time.sleep(7)
         aoid=rs.Fields.Item('_OID').Value
         aplatnosc.OID=aoid.encode('cp1250')
         if wnowe and self.PaymentsParser.IsPolaInformacyjne:
            self.OnPolaInformacyjne(rs,aplatnosc)
      if rs.State<>self.adoconst.adStateClosed:
         rs.Close()
      rs=None
#      print '#',
      if aplatnosc.Raty:
#$$ zrobic obsluge rat
         self.PaymentsProcessor.ImportStatus.append('  RATY: '+aplatnosc.Digest)
         for arata in aplatnosc.Raty:
            self.StorePlatnosc(arata)
   def OnTransID(self,rs,aplatnosc):
      atransid=self.GetTransID()
      if atransid:
         anrb,abank,aaccount=self.GetAccountInfo(atransid)
         rs.Fields.Item('IDTransakcji').Value=atransid+self.AccountAcc2
         rs.Fields.Item('KontoNRB').Value=anrb
         rs.Fields.Item('KontoBank').Value=self.AccountBank
#$$ UWAGA! Nie wstawia prawidlowo parametrow z aplikacji w danym roku!!!
         rs.Fields.Item('KontoBankNr').Value=self.AccountAcc1
         rs.Fields.Item('KontoTransakcja').Value=atransid
         rs.Fields.Item('KontoRachunek').Value=self.AccountAcc2
      else:
         anrb,abank,aaccount='','',''
         self.PaymentsProcessor.ImportStatus.append('  Nie mozna utworzyc ID Transakcji dla platnosci: '+str(aplatnosc))
      return atransid,anrb,abank,aaccount
   def OnCzyJuzZaplacono(self,rs,aplatnosc):
      rs.Fields.Item('CzyJuzZaplacono').Value=aplatnosc.CzyJuzZaplacono
      akwota=aplatnosc.Pola.get('PMKwotaZaplaty',0.0)
      if akwota>0.0:
         rs.Fields.Item("PMKwotaZaplaty").Value=akwota
      else:
         rs.Fields.Item("PMKwotaZaplaty").Value=aplatnosc.Pola['Kwota']
      adata=aplatnosc.Pola.get('PMDataZaplaty',None)
      if not adata is None:       
         rs.Fields.Item('PMDataZaplaty').Value=ICORUtil.tdatetime2fmtstr(aplatnosc.Pola['PMDataZaplaty'],adelimiter='-')
      return 1
   def OnCzyAnulowano(self,rs,aplatnosc):
#      self.PaymentsProcessor.ImportStatus.append('  CzyAnulowano: '+aplatnosc.Digest)
      rs.Fields.Item('CzyAnulowano').Value=aplatnosc.CzyAnulowano
      return 1
   def OnDataAkceptacji(self,rs,aplatnosc):
#      self.PaymentsProcessor.ImportStatus.append('  DataAkceptacji: '+aplatnosc.Digest)
      rs.Fields.Item('DataAkceptacji').Value=ICORUtil.tdatetime2fmtstr(aplatnosc.DataAkceptacji,adelimiter='-')
      return 1
   def OnCzyBezKwoty(self,rs,aplatnosc):
#      self.PaymentsProcessor.ImportStatus.append('  CzyBezKwoty: '+aplatnosc.Digest)
      rs.Fields.Item('CzyBezKwoty').Value=aplatnosc.CzyBezKwoty
      return 1
   def OnAktualizacjaTresci(self,rs,aplatnosc):
#      self.PaymentsProcessor.ImportStatus.append('  AktualizacjaTresci: '+aplatnosc.Digest)
      rs.Fields.Item("TrescDecyzji").Value=XMLUtil.GetAsXMLStringNoPL(aplatnosc.Pola.get('TrescDecyzji',''))
      return 1
   def OnNadPlatnosc(self,rs,aplatnosc):
#      self.PaymentsProcessor.ImportStatus.append('  NadPlatnosc: '+aplatnosc.Digest)
      rs.Fields.Item('OIDPlatnosciGlownej').Value=aplatnosc.NadPlatnosc.OID
      return 1
   def OnPlatnoscGrupowa(self,rs,aplatnosc):
#      self.PaymentsProcessor.ImportStatus.append('  PlatnoscGrupowa: '+aplatnosc.Digest)
      rs.Fields.Item('CzyGlownaPlatnoscGrupy').Value=aplatnosc.CzyPlatnoscGrupowa
      rs.Fields.Item('KluczGlowny').Value=aplatnosc.Digest
      return 1
   def OnNowaPozycja(self,rs,aplatnosc):
#      self.PaymentsProcessor.ImportStatus.append('  NowaPozycja: '+aplatnosc.Digest)
      return 1
   def OnPolaInformacyjne(self,rs,aplatnosc):
      return 1

class Other:
   def GenerateXMLPrintPackage(self,aapplication,afname,alocalcity=0):
      self.connection=self.adolib.Connection()
      self.connection.Open(self.ConnectionString)
      self.connection.CursorLocation=self.adoconst.adUseClient #adUseServer
      self.connection.CommandTimeout=0
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
         rs,status=self.connection.Execute(asql)
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
         self.connection.Close()
   def GetCheckSum(self,s1):
      awagi=[1,3,1,3,1,3,1,3,1,3,1,3]
      sum=0
      for i in range(len(s1)):
         sum=sum+awagi[i]*int(s1[i:i+1])
      sum=(10-sum%10)%10
      return sum
   def CheckTransID(self,s1):
      sum=self.GetCheckSum(s1[:-1])
      if sum!=int(s1[-1:]):
         return 0
      return 1
   def GetTransID(self,achecksum=1):
      while 1:
         n1=random.randrange(1,10)
         n2=random.randrange(0,1000000)
#         print 'n1:',n1
#         print 'n2:',n2
         ret='%d%06d'%(n1,n2)
#         print 'ret:',ret
         if not TRANS_ID_DICT.has_key(ret):
            TRANS_ID_DICT[ret]=1
            if achecksum:
               sum=self.GetCheckSum(ret)
#               print 'sum:',sum
               ret=ret+str(sum)
#               print 'ret:',ret
#            print ret
            return ret
         self.Hits+=1
      return ret



