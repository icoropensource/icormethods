# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icordbmain.adoutil as ADOLibInit
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import os
import re
import sys
import string
import cStringIO
import sha

class ICORSOKPrzesylkiParser(XMLUtil.ICORBaseXMLParser):
   def ParseFile(self,aprocessor,afpath,ret=None,acompressed=0,adomyslnystatusprzesylki='K',adomyslnystatuslisty='K',adomyslnytrybdoreczenia='Ordynacja Podatkowa',anolist=0,anadawca='',awydzialmerytoryczny='',alistafilterfunc=None,aprzesylkafilterfunc=None):
      self.PaymentsCnt=0
      self.PaymentsExisting=0
      self.PaymentsProcessor=aprocessor
      self.adolib=self.PaymentsProcessor.adolib
      self.adoconst=self.PaymentsProcessor.adoconst
      self.Wersja=''
      self.IsGood=1
      self.Aplikacja=''
      self.DataUtworzeniaWydruku=''
      self.CzasUtworzeniaWydruku=''
      self.Nadawca=anadawca
      self.WydzialMerytoryczny=awydzialmerytoryczny
      self.IDWydruku=''
      self.AutorWydruku=''
      self.ListaOID=''
      self.DomyslnyStatusPrzesylki=adomyslnystatusprzesylki # 'K' - przesylka wydrukowana, gotowa do przekazania do goncow; 'P' - przesylka nadana przez nadawce (sortownik drukuje zwrotki)
      self.DomyslnyStatusListy=adomyslnystatuslisty # 'K' - lista wydrukowana, gotowa do przekazania i polaczona z przesylkami; '' - puste, jesli statusem przesylki jest 'P' (bo nie ma jeszcze list)
      self.DomyslnyTrybDoreczenia=adomyslnytrybdoreczenia
      self.ListaFilterFunc=alistafilterfunc
      self.PrzesylkaFilterFunc=aprzesylkafilterfunc
      self.NoList=anolist
      if self.DomyslnyStatusPrzesylki=='P':
         self.NoList=1
      self.reset()
      if acompressed:
         bfname=aprocessor.ArchiveDir+'/'+rs.Fields.Item("_OID").Value+'.gz'
#         print 'bfname:',bfname
         afarchive=ICORTextFile.TextFile(bfname,'w')
      amsize=os.path.getsize(afpath)
      self.ProgressEstimator=ICORUtil.TimeProgressEstimator(amsize)
      aasize=0
      fout=open(afpath,'rb')
      try:
         while 1:
            v=fout.read(8192)
            aasize=aasize+len(v)
            SetProgress(aasize,amsize)
            self.Elapsed,self.Estimated,self.Remaining=self.ProgressEstimator.SetProgress(aasize)
            InfoStatus('%s %d %s %s %s'%(afpath[-20:],amsize-aasize,self.Elapsed,self.Estimated,self.Remaining))
            if len(v)<=0:
               break
            if acompressed:
               afarchive.write(v)
            self.feed(v)
      finally:
         if acompressed:
            afarchive.close()
         fout.close()
      InfoStatus('')
      SetProgress(0,0)
   def GetNrPierwszejPosesji(self,s):
      m=re.search('^([\da-zA-Z]+)',string.strip(s))
      if m:
         return m.group(1)
      return s
   def start_SOKWYDRUK(self,attrs):
#    wersja='1.0.1'>
      l=self.CheckAttrs(attrs,['wersja'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <SOKWYDRUK>: %s'%str(l)
      self.Wersja=attrs.get('wersja','')
   def end_SOKWYDRUK(self):
      pass
   def start_DANEWYDRUKU(self,attrs):
      pass
   def end_DANEWYDRUKU(self):
      pass
   def start_DANE(self,attrs):
      l=self.CheckAttrs(attrs,['nazwa','wartosc'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <DANE>: %s'%str(l)
      anazwa=attrs.get('nazwa','')
      awartosc=attrs.get('wartosc','')
      if anazwa=='Aplikacja':
         self.Aplikacja=awartosc
      elif anazwa=='DataUtworzeniaWydruku':
         self.DataUtworzeniaWydruku=awartosc
      elif anazwa=='CzasUtworzeniaWydruku':
         self.CzasUtworzeniaWydruku=awartosc
      elif anazwa=='IDWydruku':
         self.IDWydruku=awartosc
      elif anazwa=='AutorWydruku':
         self.AutorWydruku=awartosc
   def end_DANE(self):
      pass
   def start_PRZESYLKI(self,attrs):
      pass
   def end_PRZESYLKI(self):
      pass
   def start_LISTA(self,attrs):
      if self.NoList:
         return
      l=self.CheckAttrs(attrs,['Tytul','Rok','Ulica','KodTerytorialny','IDListy','NrKolejny','NrKolejnyOsiedle','IDTytulu','Status',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <LISTA>: %s'%str(l)
         return

      self.ListaOID=''
      if not self.ListaFilterFunc is None:
         w=self.ListaFilterFunc(attrs)
         if not w:
            return

      asql="SELECT * FROM %s WHERE IDListy='%s'"%(self.PaymentsProcessor.stn_listy,attrs.get('IDListy',''))
      rs=self.PaymentsProcessor.GetRS(asql)
      if rs.State!=self.adoconst.adStateClosed:
         if rs.EOF or rs.BOF:
            rs.AddNew()
            rs.Fields.Item('IDListy').Value=attrs.get('IDListy','')
            rs.Fields.Item('IDTytulu').Value=attrs.get('IDTytulu','')
            rs.Fields.Item('NrStrony').Value=attrs.get('NrKolejny','')
            rs.Fields.Item('NrKolejnyUlica').Value=attrs.get('NrKolejnyOsiedle','') #NrKolejny
            rs.Fields.Item('Rok').Value=attrs.get('Rok','')
            rs.Fields.Item('Tytul').Value=attrs.get('Tytul','')
            rs.Fields.Item('Ulica').Value=attrs.get('Ulica','')
            rs.Fields.Item('KodTerytorialny').Value=attrs.get('KodTerytorialny','')
            rs.Fields.Item('Status').Value=attrs.get('Status',self.DomyslnyStatusListy)
#            for apname in ['DataWymagalnosci','PMDataWplywu','PMDataOdbioruDecyzji','DataAkceptacji','PMDataZaplaty']:
#               rs.Fields.Item(apname).Value='1900-01-01'
            self.PaymentsProcessor.UpdateRS(rs)
         aoid=rs.Fields.Item('_OID').Value
         self.ListaOID=aoid.encode('cp1250')
      if rs.State<>self.adoconst.adStateClosed:
         rs.Close()                              
      rs=None
   def end_LISTA(self):
      if self.NoList:
         return
   def start_PRZESYLKA(self,attrs):
      if attrs.get('AdresatadresX',''):
         attrs['AdresatAdresX']=attrs.get('AdresatadresX','')
      if attrs.get('AdresatadresY',''):
         attrs['AdresatAdresY']=attrs.get('AdresatadresY','')
#      attrs['TrybDoreczenia']='Ordynacja Podatkowa'
      l=self.CheckAttrs(attrs,['IDPrzesylki', 'IDAdresata', 'IDTytulu', 'Tytulem', 'Adresat',
'AdresatAdres','AdresatAdresUlicaNrPosesji', 'AdresatAdresUlica', 'AdresatAdresNrPosesji',
'AdresatAdresNrLokalu', 'AdresatAdresMiejscowosc', 'AdresatAdresKodPocztowy','AdresatAdresPelnyNrPosesji',
'AdresatAdresKodTerytorialny', 'AdresatAdresInneInformacje', 'IDTransakcji',
'PESEL', 'NIP', 'REGON', 'DataPisma', 'AdresOID', 'AdresatAdresEwidencyjnyNrPosesji','AdresatAdresCzyKraj',
'ZnakSprawy', 'UNP', 'Dotyczy', 'RodzajKorespondencji',
'Priorytet', 'Status', 'Nadawca', 'WydzialMerytoryczny', 'DataNadania',
'DataRejestracjiUSortownika', 'Sortownik', 'DoRakWlasnychAdresata',
'CzyDoreczac', 'DataDoreczenia',
'AdresatadresX', 'AdresatadresY','AdresatAdresX', 'AdresatAdresY', #UWAGA!
'NrKolejny','TrybDoreczenia','CzyBezKontroliDatyPrzesylki',
'DataWymagalnosci','ZwrotkaGrupa',
])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <PRZESYLKA>: %s'%str(l)
         return
      aidprzesylki=attrs.get('IDPrzesylki','')
      if not self.PaymentsProcessor.CheckTransID(aidprzesylki):
         self.IsGood=0
         print 'bledny id przesylki w tagu <PRZESYLKA>: %s'%str(aidprzesylki)
         return

      if attrs.get('AdresOID',''):
         asql="SELECT * FROM %s WHERE _OID='%s'"%(self.PaymentsProcessor.stn_adresy,attrs.get('AdresOID',''))
         rs=self.PaymentsProcessor.GetRS(asql)
         if rs.State!=self.adoconst.adStateClosed:
            if not (rs.EOF or rs.BOF):
# tabela_przesylek.AdresatAdres=tabela_adresow.KodPocztowy+' '+tabela_przesylek.AdresatAdresMiejscowosc+' '+tabela_adresow.AdresEwidencyjny+' '+tabela_przesylek.AdresatAdresNrLokalu
#               if not attrs.get('AdresatAdres',''):
               attrs['AdresatAdres']=ADOLibInit.GetRSValueAsStr(rs,'KodPocztowy')+' '+attrs.get('AdresatAdresMiejscowosc','')+' '+ADOLibInit.GetRSValueAsStr(rs,'AdresEwidencyjny')+' '+attrs.get('AdresatAdresNrLokalu','')
# tabela_przesylek.AdresatAdresKodTerytorialny=tabela_adresow.Osiedle,
#               if not attrs.get('AdresatAdresKodTerytorialny',''):
               attrs['AdresatAdresKodTerytorialny']=ADOLibInit.GetRSValueAsStr(rs,'Osiedle')
# tabela_przesylek.AdresatAdresUlicaNrPosesji=tabela_adresow.AdresEwidencyjny,
#               if not attrs.get('AdresatAdresUlicaNrPosesji',''):
               attrs['AdresatAdresUlicaNrPosesji']=ADOLibInit.GetRSValueAsStr(rs,'AdresEwidencyjny')
# tabela_przesylek.AdresatAdresUlica=tabela_adresow.UlicaEwidencyjna,
#               if not attrs.get('AdresatAdresUlica',''):
               attrs['AdresatAdresUlica']=ADOLibInit.GetRSValueAsStr(rs,'UlicaEwidencyjna')
# tabela_przesylek.AdresatAdresEwidencyjnyNrPosesji=tabela_adresow.PrefiksEwidencyjny+tabela_adresow.NumerEwidencyjny+tabela_adresow.SufiksEwidencyjny,
#               if not attrs.get('AdresatAdresEwidencyjnyNrPosesji',''):
               attrs['AdresatAdresEwidencyjnyNrPosesji']=ADOLibInit.GetRSValueAsStr(rs,'PrefiksEwidencyjny')+ADOLibInit.GetRSValueAsStr(rs,'NumerEwidencyjny')+ADOLibInit.GetRSValueAsStr(rs,'SufiksEwidencyjny')
# tabela_przesylek.AdresatAdresKodPocztowy=tabela_adresow.KodPocztowy,
#               if not attrs.get('AdresatAdresKodPocztowy',''):
               attrs['AdresatAdresKodPocztowy']=ADOLibInit.GetRSValueAsStr(rs,'KodPocztowy')
# tabela_przesylek.AdresatAdresX=tabela_adresow.X,
#               if not attrs.get('AdresatAdresX',''):
               attrs['AdresatAdresX']=ADOLibInit.GetRSValueAsStr(rs,'X')
# tabela_przesylek.AdresatAdresX=tabela_adresow.Y,
#               if not attrs.get('AdresatAdresY',''):
               attrs['AdresatAdresY']=ADOLibInit.GetRSValueAsStr(rs,'Y')
# tabela_przesylek.CzyDoreczac=tabela_adresow.CzyDoreczac
#               if not attrs.get('CzyDoreczac',''):
               attrs['CzyDoreczac']=ADOLibInit.GetRSValueAsStr(rs,'CzyDoreczac')
         if rs.State<>self.adoconst.adStateClosed:
            rs.Close()
         rs=None
         attrs['CzyBezKontroliDatyPrzesylki']='0'
      else:
         attrs['CzyDoreczac']='0'
         attrs['CzyBezKontroliDatyPrzesylki']='1'

      if not self.PrzesylkaFilterFunc is None:
         w=self.PrzesylkaFilterFunc(attrs)
         if not w:
            return

      asql="SELECT * FROM %s WHERE IDPrzesylki='%s' and IDTransakcji='%s'"%(self.PaymentsProcessor.stn_przesylki,attrs.get('IDPrzesylki',''),attrs.get('IDTransakcji',''))
      rs=self.PaymentsProcessor.GetRS(asql)
      if rs.State!=self.adoconst.adStateClosed:
         if rs.EOF or rs.BOF:
            rs.AddNew()
         if not self.NoList:
            rs.Fields.Item('Lista').Value=self.ListaOID
         rs.Fields.Item('IDPrzesylki').Value=attrs.get('IDPrzesylki','')
         rs.Fields.Item('IDTransakcji').Value=attrs.get('IDTransakcji','')
         rs.Fields.Item('IDAdresata').Value=attrs.get('IDAdresata','')
         rs.Fields.Item('IDTytulu').Value=attrs.get('IDTytulu','')
         rs.Fields.Item('Tytulem').Value=attrs.get('Tytulem','')
         rs.Fields.Item('DataPisma').Value=attrs.get('DataPisma','1900-01-01')
         rs.Fields.Item('Adresat').Value=attrs.get('Adresat','')
         rs.Fields.Item('AdresOID').Value=attrs.get('AdresOID','')
         rs.Fields.Item('AdresatAdres').Value=attrs.get('AdresatAdres','')
         rs.Fields.Item('AdresatAdresUlicaNrPosesji').Value=attrs.get('AdresatAdresUlicaNrPosesji','')
         rs.Fields.Item('AdresatAdresUlica').Value=attrs.get('AdresatAdresUlica','')
         anrposesji=attrs.get('AdresatAdresNrPosesji','')
         if not anrposesji:
            anrposesji=attrs.get('AdresatAdresPelnyNrPosesji','')
         rs.Fields.Item('AdresatAdresNrPosesji').Value=anrposesji
         rs.Fields.Item('AdresatAdresEwidencyjnyNrPosesji').Value=attrs.get('AdresatAdresEwidencyjnyNrPosesji','')
         rs.Fields.Item('AdresatAdresNrLokalu').Value=attrs.get('AdresatAdresNrLokalu','')
         rs.Fields.Item('AdresatAdresMiejscowosc').Value=attrs.get('AdresatAdresMiejscowosc','')
         rs.Fields.Item('AdresatAdresKodPocztowy').Value=attrs.get('AdresatAdresKodPocztowy','')
         rs.Fields.Item('AdresatAdresKodTerytorialny').Value=attrs.get('AdresatAdresKodTerytorialny','')
         rs.Fields.Item('AdresatAdresInneInformacje').Value=attrs.get('AdresatAdresInneInformacje','')
         rs.Fields.Item('AdresatadresX').Value=attrs.get('AdresatAdresX','0.0')
         rs.Fields.Item('AdresatadresY').Value=attrs.get('AdresatAdresY','0.0')
         rs.Fields.Item('ZnakSprawy').Value=attrs.get('ZnakSprawy','')
         rs.Fields.Item('UNP').Value=attrs.get('UNP','')
         rs.Fields.Item('Dotyczy').Value=attrs.get('Dotyczy','')
         rs.Fields.Item('RodzajKorespondencji').Value=attrs.get('RodzajKorespondencji','ZPO')
         rs.Fields.Item('Priorytet').Value=attrs.get('Priorytet','0')
         rs.Fields.Item('PESEL').Value=attrs.get('PESEL','')
         rs.Fields.Item('NIP').Value=attrs.get('NIP','')
         rs.Fields.Item('REGON').Value=attrs.get('REGON','')
         rs.Fields.Item('Status').Value=attrs.get('Status',self.DomyslnyStatusPrzesylki)
         rs.Fields.Item('DataDoreczenia').Value=attrs.get('DataDoreczenia','1900-01-01')
         if self.NoList:
            rs.Fields.Item('NrKolejnyNaLiscie').Value='0'
         else:
            rs.Fields.Item('NrKolejnyNaLiscie').Value=attrs.get('NrKolejny','0') #NrKolejny
         rs.Fields.Item('Nadawca').Value=attrs.get('Nadawca',self.Nadawca)
         rs.Fields.Item('WydzialMerytoryczny').Value=attrs.get('WydzialMerytoryczny',self.WydzialMerytoryczny)
         rs.Fields.Item('DataNadania').Value=attrs.get('DataNadania','1900-01-01')
         rs.Fields.Item('DataRejestracjiUSortownika').Value=attrs.get('DataRejestracjiUSortownika','1900-01-01')
         rs.Fields.Item('Sortownik').Value=attrs.get('Sortownik','')
         rs.Fields.Item('DoRakWlasnychAdresata').Value=attrs.get('DoRakWlasnychAdresata','0')
         rs.Fields.Item('CzyDoreczac').Value=attrs.get('CzyDoreczac','1')
         if attrs.get('AdresatAdresCzyKraj','1')=='0':
            rs.Fields.Item('CzyZagraniczna').Value='1'
         else:
            rs.Fields.Item('CzyZagraniczna').Value='0'
         rs.Fields.Item('TrybDoreczenia').Value=attrs.get('TrybDoreczenia',self.DomyslnyTrybDoreczenia)
         rs.Fields.Item('CzyBezKontroliDatyPrzesylki').Value=attrs['CzyBezKontroliDatyPrzesylki']


         rs.Fields.Item('_UserName').Value=self.AutorWydruku
#            rs.Fields.Item('DataWymagalnosci').Value=attrs.get('DataWymagalnosci','')
#            rs.Fields.Item('ZwrotkaGrupa').Value=attrs.get('ZwrotkaGrupa','')
#         for apname in ['DataDoreczenia',]:
#            rs.Fields.Item(apname).Value='1900-01-01'
         self.PaymentsProcessor.UpdateRS(rs)
      if rs.State<>self.adoconst.adStateClosed:
         rs.Close()
      rs=None
   def end_PRZESYLKA(self):
      pass

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return


