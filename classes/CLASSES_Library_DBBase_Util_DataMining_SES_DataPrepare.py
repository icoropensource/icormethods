# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_DBBase_Util_CSVImport import CSVExport,CSVImport,DictFromCSV
import xmllib
import string
import struct
import types
import time
import sys
import os
import re

DAYS=['pon','wto','sro','czw','pia','sob','nie']
SECS_IN_DAY=86400.0

def DateDiff(ad1,ad2):
   dd=(0,0,0,-1,-1,-1)
   try:
      d1=time.mktime(ad1+dd)
   except:
      print 'Bad date:',ad1
      raise
   try:
      d2=time.mktime(ad2+dd)
   except:
      print 'Bad date:',ad2
      raise
   t1=time.localtime(d1)
   t2=time.localtime(d2)
   return int(round((d1-d2)/SECS_IN_DAY)),DAYS[t1[6]],t1[7],DAYS[t2[6]],t2[7] #datediff,weekday 1, day count 1, weekday 2, day count 2

def DateInfo(d1):
   dd=(0,0,0,-1,-1,-1)
   d1=time.mktime(d1+dd)
   t1=time.localtime(d1)
   return DAYS[t1[6]],t1[7] #weekday,day count

def WriteDMCols(cfile,ccols,rcols):
   w=0
   for acol in cfile.Header:
      if w:
         cfile.fout.write(chr(9))
      w=1
      if acol in ccols:
         cfile.fout.write('c')
      else:
         cfile.fout.write('d')
   cfile.fout.write('\n')
   w=0
   for acol in cfile.Header:
      if w:
         cfile.fout.write(chr(9))
      w=1
      if acol in rcols:
         cfile.fout.write('class')
   cfile.fout.write('\n')

def RejHZaplaty(arejhfile,aoutfile):
   cfile=CSVExport(adelimiter=chr(9),atextQualifier='',acleandata=1)
   cfile.Header=[
   #'KodMagazynu',
     'WarunekDostawy',
      'SposobZaplaty','WartoscFaktury','KodAkwizytora','FiliaOddzial',
#      'DataWystawienia',
#      'DataWystawieniaDzienTygodnia',
      #'DataWystawieniaNrDnia',
#      'TerminZaplaty',
#      'TerminZaplatyDzienTygodnia',
      #'TerminZaplatyNrDnia',
#      'DataZaplaty','DataZaplatyDzienTygodnia','DataZaplatyNrDnia',
#      'TerminZaplatyWDniach',
#      'OpoznienieZaplatyWDniach',
#      'KwotaZaplaty',
      'ZaplataWTerminie',]
   ccols=['KwotaZaplaty','TerminZaplatyWDniach','OpoznienieZaplatyWDniach','DataWystawieniaNrDnia','TerminZaplatyNrDnia','DataZaplatyNrDnia',]
   rcols=['ZaplataWTerminie',]
   cfile.Open(aoutfile)
   WriteDMCols(cfile,ccols,rcols)
   acsv=CSVImport()
   acsv.Open(arejhfile)
   acnt=0
   while not acsv.EOF:
      acnt=acnt+1
      if not acnt%100:
         print '\r%d'%acnt,
      if (acsv['Anulacja']=='Nie Anulowano VAT') and (acsv['FakturaRachunek']=='Faktura VAT'):
         adatawystawienia=acsv['DataWystawienia',mt_DateTime]
         aterminzaplaty=acsv['TerminZaplaty',mt_DateTime]
         adatazaplaty=acsv['DataZaplaty',mt_DateTime]
         d1,aterminzaplatyweekday,aterminzaplatydaycount,adatawystawieniaweekday,adatawystawieniadaycount=DateDiff(aterminzaplaty,adatawystawienia)
         if adatazaplaty<aterminzaplaty:
            d2,adatazaplatyweekday,adatazaplatydaycount,aterminzaplatyweekday,aterminzaplatydaycount=DateDiff(time.localtime()[:3],aterminzaplaty)
         else:
            d2,adatazaplatyweekday,adatazaplatydaycount,aterminzaplatyweekday,aterminzaplatydaycount=DateDiff(adatazaplaty,aterminzaplaty)
         if d2<0:
            d2=0
         akwotazaplaty=acsv['KwotaZaplaty',mt_Double]
         awartoscfaktury=acsv['WartoscFaktury',mt_Double]
#         cfile['DataWystawienia']=adatawystawienia
#         cfile['KodMagazynu']=acsv['KodMagazynu']
#         cfile['TerminZaplaty']=aterminzaplaty
         cfile['WarunekDostawy']=acsv['WarunekDostawy']
         cfile['SposobZaplaty']=acsv['SposobZaplaty']
         if awartoscfaktury<=200:
            swartoscfaktury='do 200 PLN'
         elif awartoscfaktury<=1000:
            swartoscfaktury='do 1000 PLN'
         elif awartoscfaktury<=10000:
            swartoscfaktury='do 10000 PLN'
         else:
            swartoscfaktury='powyzej 10000 PLN'
         cfile['WartoscFaktury']=swartoscfaktury
         cfile['KodAkwizytora']=acsv['KodAkwizytora']
         cfile['FiliaOddzial']=acsv['FiliaOddzial']
#         cfile['DataZaplaty']=adatazaplaty
#         cfile['KwotaZaplaty']=akwotazaplaty

#         cfile['DataWystawieniaDzienTygodnia']=adatawystawieniaweekday
#         cfile['DataWystawieniaNrDnia']=adatawystawieniadaycount
#         cfile['TerminZaplatyDzienTygodnia']=aterminzaplatyweekday
#         cfile['TerminZaplatyNrDnia']=aterminzaplatydaycount
#         cfile['DataZaplatyDzienTygodnia']=adatazaplatyweekday
#         cfile['DataZaplatyNrDnia']=adatazaplatydaycount
#         cfile['TerminZaplatyWDniach']=d1
#         cfile['OpoznienieZaplatyWDniach']=d2

         if 0:
            if d2==0:
               cfile['ZaplataWTerminie']='0 - w terminie'
            elif d2<=7:
               cfile['ZaplataWTerminie']='1 - do 7 dni'
            elif d2<=14:
               cfile['ZaplataWTerminie']='2 - do 14 dni'
            elif d2<=21:
               cfile['ZaplataWTerminie']='3 - do 21 dni'
            elif d2<=30:
               cfile['ZaplataWTerminie']='4 - do 30 dni'
            elif d2<=60:
               cfile['ZaplataWTerminie']='5 - do 60 dni'
            elif akwotazaplaty==0.0:
               cfile['ZaplataWTerminie']='8 - brak zaplaty'
            else:
               cfile['ZaplataWTerminie']='7 - powyzej 60 dni'
         if 0:
            if d2<=7:
               cfile['ZaplataWTerminie']='0 - w terminie lub do 7 dni'
            else:
               cfile['ZaplataWTerminie']='1 - powyzej 7 dni lub brak'
         if 1:
            if d2==0:
               cfile['ZaplataWTerminie']='w terminie'
            elif d2<=14:
               cfile['ZaplataWTerminie']='do 14 dni opoznienia'
            elif d2<=30:
               cfile['ZaplataWTerminie']='do 30 dni opoznienia'
            elif akwotazaplaty==0.0:
               cfile['ZaplataWTerminie']='brak zaplaty'
            else:
               cfile['ZaplataWTerminie']='powyzej 60 dni opoznienia'

         cfile.Next()
      acsv.Next()
   acsv.Close()
   cfile.Close()

def RejPMat(arejpfile,arejhfile,amatfile,aoutfile):
   cfile=CSVExport(adelimiter=chr(9),atextQualifier='',acleandata=1)
   cfile.Header=['FakturaRachunek','NrFaktury','Lp','LiczbaPorzadkowa','KodMagazynu',
      'TypPozycji','KodTowaruUslugi','KodStawki','Ilosc','Cena','Rabat','WartoscBezVAT',
      'StawkaVAT','WartoscVAT','WartoscLp','IloscWydana','KodOperatora',
      'KodMagazynowyZlecenia','LpWzorca','FiliaOddzial','GrupaTowarowa','ImportKraj',
      'PodgrupaTowarowa','TowarSerwis']
#   ccols=['KwotaZaplaty','TerminZaplatyWDniach','OpoznienieZaplatyWDniach','DataWystawieniaNrDnia','TerminZaplatyNrDnia','DataZaplatyNrDnia',]
#   rcols=['ZaplataWTerminie',]
#   cfile.Open(aoutfile)
#   WriteDMCols(cfile,ccols,rcols)

#   drejh=DictFromCSV(arejhfile,['FakturaRachunek','NrFaktury','FiliaOddzial','KodMagazynu'])
#   dmat=DictFromCSV(amatfile,['KodTowaruUslugi','FiliaOddzial'])
   dmat=DictFromCSV(amatfile,['KodTowaruUslugi'])

   da_fakt={}

   acsv=CSVImport(acleandata=1)
   acsv.Open(arejpfile)
   acnt=0
   while not acsv.EOF:
      acnt=acnt+1
      if not acnt%100:
         print '\r%d'%acnt,
      akey=string.join([acsv['FakturaRachunek'],acsv['NrFaktury'],acsv['FiliaOddzial'],acsv['KodMagazynu']],'_')
      lpos=da_fakt.get(akey,[])
      atowar=acsv['KodTowaruUslugi']
      if not atowar in lpos:
         lpos.append(atowar)
      da_fakt[akey]=lpos
#      adatawystawienia=acsv['DataWystawienia',mt_DateTime]
#      akwotazaplaty=acsv['KwotaZaplaty',mt_Double]
#      cfile.Next()
      acsv.Next()
   acsv.Close()
   lkeys=da_fakt.keys()
   lkeys.sort()
   fout=open(aoutfile+'1.txt','w')
   for akey in lkeys:
      fout.write('"%s" - %s\n'%(akey,str(da_fakt[akey])))
   fout.close()
   da_towary={}
   for akey,altowary in da_fakt.items():
      for atowar in altowary:
         d=da_towary.get(atowar,{})
         for btowar in altowary:
            d[btowar]=d.get(btowar,0)+1
         da_towary[atowar]=d
   fout=open(aoutfile+'2.txt','w')
   fout2=open(aoutfile+'3.txt','w')
   for atowar,asums in da_towary.items():
      lsums=[]
      acnt=0
      for btowar,bsum in asums.items():
         if btowar==atowar:
            acnt=bsum
         else:
            lsums.append([bsum,btowar])
      lsums.sort()
      lsums.reverse()
      if acnt>=5:
         anazwatowaru=dmat[atowar,'NazwaMaterialu']
         fout2.write('%s\n'%(string.join([atowar,str(acnt),anazwatowaru],chr(9))))
         for asum,btowar in lsums:
            aratio=asum*1.0/acnt
            if aratio>=0.25:
               l=[atowar,str(acnt),anazwatowaru,str(aratio),btowar,str(asum),dmat[btowar,'NazwaMaterialu']]
               fout.write('%s\n'%(string.join(l,chr(9))))
   fout2.close()
   fout.close()

#   cfile.Close()

class Faktura:
   def __init__(self,adatawystawienia,aterminzaplaty,adatazaplaty):
      self.DataWystawienia=adatawystawienia
      self.TerminZaplaty=aterminzaplaty
      self.DataZaplaty=adatazaplaty

class Kontrahent:
   def __init__(self,akodplatnika):
      self.KodPlatnika=akodplatnika
      self.Faktury={}
      self.WarunkiDostawy={}
      self.SposobyZaplaty={}
      self.KodyAkwizytorow={}
      self.FilieOddzialy={}
      self.WartoscFaktury=0.0
      self.WartoscVAT=0.0
      self.KwotaZaplat=0.0
      self.TerminyZaplatWDniach=0
      self.OpoznieniaZaplatWDniach=0
      self.WartoscOpoznienZaplat=0
   def RegisterPosition(self,akey,adatawystawienia,aterminzaplaty,awarunekdostawy,asposobzaplaty,awartoscfaktury,awartoscvat,akodakwizytora,afiliaoddzial,adatazaplaty,akwotazaplaty):
      if awartoscfaktury<0.0:
         return
      if not self.Faktury.has_key(akey):
         self.Faktury[akey]=Faktura(adatawystawienia,aterminzaplaty,adatazaplaty)
         self.WarunkiDostawy[awarunekdostawy]=1+self.WarunkiDostawy.get(awarunekdostawy,0)
         self.SposobyZaplaty[asposobzaplaty]=1+self.SposobyZaplaty.get(asposobzaplaty,0)
         self.KodyAkwizytorow[akodakwizytora]=1+self.KodyAkwizytorow.get(akodakwizytora,0)
         self.FilieOddzialy[afiliaoddzial]=1+self.FilieOddzialy.get(afiliaoddzial,0)
         self.WartoscFaktury=self.WartoscFaktury+awartoscfaktury
         self.WartoscVAT=self.WartoscVAT+awartoscvat
         self.KwotaZaplat=self.KwotaZaplat+akwotazaplaty
         d1,aterminzaplatyweekday,aterminzaplatydaycount,adatawystawieniaweekday,adatawystawieniadaycount=DateDiff(aterminzaplaty,adatawystawienia)
         if adatazaplaty<aterminzaplaty:
            d2,adatazaplatyweekday,adatazaplatydaycount,aterminzaplatyweekday,aterminzaplatydaycount=DateDiff(time.localtime()[:3],aterminzaplaty)
         else:
            d2,adatazaplatyweekday,adatazaplatydaycount,aterminzaplatyweekday,aterminzaplatydaycount=DateDiff(adatazaplaty,aterminzaplaty)
         if d2<0:
            d2=0
         self.TerminyZaplatWDniach=d1+self.TerminyZaplatWDniach
         self.OpoznieniaZaplatWDniach=d2+self.OpoznieniaZaplatWDniach
         self.WartoscOpoznienZaplat=(d2*self.WartoscFaktury)+self.WartoscOpoznienZaplat
   def ReCalc(self):
      self.IloscFaktur=len(self.Faktury.keys())
      self.SredniaWartoscFaktury=0.0
      self.SredniaWartoscZaplat=0.0
      self.SrednieTerminyZaplatWDniach=0.0
      self.SrednieOpoznieniaZaplatWDniach=0.0
      self.SredniaWartoscOpoznienZaplatNaFakture=0.0
      self.SredniaWartoscOpoznienZaplatNaDzien=0.0
      try:
         self.SredniaWartoscFaktury=self.WartoscFaktury/self.IloscFaktur
         self.SredniaWartoscZaplat=self.KwotaZaplat/self.IloscFaktur
         self.SrednieTerminyZaplatWDniach=self.TerminyZaplatWDniach*1.0/self.IloscFaktur
         self.SrednieOpoznieniaZaplatWDniach=self.OpoznieniaZaplatWDniach*1.0/self.IloscFaktur
         self.SredniaWartoscOpoznienZaplatNaFakture=self.WartoscOpoznienZaplat/self.IloscFaktur
      except ZeroDivisionError:
         pass
      try:
         self.SredniaWartoscOpoznienZaplatNaDzien=self.WartoscOpoznienZaplat/self.OpoznieniaZaplatWDniach
      except ZeroDivisionError:
         pass

   def Dump(self,fout):
      self.ReCalc()

      fout.write('%s\n'%self.KodPlatnika)
      fout.write('   Ilosc faktur: %d\n'%(self.IloscFaktur))
      fout.write('   Warunki dostawy: %s\n'%(str(self.WarunkiDostawy)))
      fout.write('   Sposoby zaplaty: %s\n'%(str(self.SposobyZaplaty)))
      fout.write('   Kody akwizytorow: %s\n'%(str(self.KodyAkwizytorow)))
      fout.write('   Filie oddzialy: %s\n'%(str(self.FilieOddzialy)))
      fout.write('   Wartosc faktur: %0.2f\n'%(self.WartoscFaktury))
      fout.write('   Wartosc VAT: %0.2f\n'%(self.WartoscVAT))
      fout.write('   Kwota zaplat: %0.2f\n'%(self.KwotaZaplat))

      fout.write('   Srednia wartosc faktury: %0.2f\n'%(self.SredniaWartoscFaktury))
      fout.write('   Srednia kwota zaplat: %0.2f\n'%(self.SredniaWartoscZaplat))

      fout.write('   Terminy zaplat w dniach: %d\n'%(self.TerminyZaplatWDniach))
      fout.write('   Opoznienia zaplat w dniach: %d\n'%(self.OpoznieniaZaplatWDniach))
      fout.write('   Wartosc opoznien zaplat: %0.2f\n'%(self.WartoscOpoznienZaplat))

      fout.write('   Srednie terminy zaplat w dniach: %d\n'%(self.SrednieTerminyZaplatWDniach))
      fout.write('   Srednie opoznienia zaplat w dniach: %d\n'%(self.SrednieOpoznieniaZaplatWDniach))
      fout.write('   Srednia wartosc opoznien zaplat na fakture: %0.2f\n'%(self.SredniaWartoscOpoznienZaplatNaFakture))
      fout.write('   Srednia wartosc opoznien zaplat na dzien: %0.2f\n'%(self.SredniaWartoscOpoznienZaplatNaDzien))

      fout.write('\n')

def RejPKontr(arejpfile,arejhfile,amatfile,aoutfile):
   drejh=DictFromCSV(arejhfile,['FakturaRachunek','NrFaktury','FiliaOddzial','KodMagazynu'])
#   dmat=DictFromCSV(amatfile,['KodTowaruUslugi','FiliaOddzial'])
#   dmat=DictFromCSV(amatfile,['KodTowaruUslugi'])
   da_kontr={}
   acsv=CSVImport(acleandata=1)
   acsv.Open(arejpfile)
   acnt=0
   while not acsv.EOF:
      acnt=acnt+1
      if not acnt%100:
         print '\r%d'%acnt,
      akey=string.join([acsv['FakturaRachunek'],acsv['NrFaktury'],acsv['FiliaOddzial'],acsv['KodMagazynu']],'_')
      akodplatnika=drejh[akey,'KodPlatnika']
      akontrahent=da_kontr.get(akodplatnika,None)
      if akontrahent is None:
         akontrahent=Kontrahent(akodplatnika)
      akontrahent.RegisterPosition(akey,
         drejh[akey,("DataWystawienia",mt_DateTime)],
         drejh[akey,("TerminZaplaty",mt_DateTime)],
         drejh[akey,"WarunekDostawy"],
         drejh[akey,"SposobZaplaty"],
         drejh[akey,("WartoscFaktury",mt_Double)],
         drejh[akey,("WartoscVAT",mt_Double)],
         drejh[akey,"KodAkwizytora"],
         drejh[akey,"FiliaOddzial"],
         drejh[akey,("DataZaplaty",mt_DateTime)],
         drejh[akey,("KwotaZaplaty",mt_Double)]
      )
      da_kontr[akodplatnika]=akontrahent
      acsv.Next()
   acsv.Close()
   lkontr=da_kontr.keys()
   lkontr.sort()
   fout=open(aoutfile+'1.txt','w')
   fout.write('\n')
   try:
      for akey in lkontr:
         akontrahent=da_kontr[akey]
         akontrahent.Dump(fout)
   finally:
      fout.close()

#   cfile.Close()

def Usage():
   print 'usage:'
   print '   python dataprepare.py mode infile [infile2] outfile'
   print 'where:'
   print '   mode:'
   print '      -rejhzaplaty - process REJH file from SES'
   print '      -rejpmatkontr - process REJP file from SES'

def Main():
   if len(sys.argv)==1:
      Usage()
      return
   if sys.argv[1]=='-rejhzaplaty':
      RejHZaplaty(sys.argv[2],sys.argv[3])
   elif sys.argv[1]=='-rejpmat':
      RejPMat(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
   elif sys.argv[1]=='-rejpkontr':
      RejPKontr(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
   else:
      Usage()
      return



