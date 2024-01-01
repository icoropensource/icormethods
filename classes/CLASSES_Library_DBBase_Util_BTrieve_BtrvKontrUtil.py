# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_DBBase_Util_CSVImport import CSVImport,CSVExport
import string
import sys
import re

def JoinFields(s1,s2):
   l=[string.strip(s1),string.strip(s2)]
   return string.strip(string.join(l,' '))

def GetKonto(s,alen=12):
   while len(s)<alen:
      s=s+'0'
   return s

def GetUlicaKodMiejscowosc(s1,s2,s3):
   s1,s2,s3=string.strip(s1),string.strip(s2),string.strip(s3)
   ulica,kod,miejscowosc='','',''
   p1=re.compile('\d\d\ {0,2}\- {0,2}\d\d\d')
   p2=re.compile('ul\W|al\W|aleja|pl\W|plac|os\W|osiedle|\/| m |m\d|\d',re.I)
   p3=re.compile('warsz|pu.tusk|gdynia|konin|zielonka|piaseczno|rado..|o.wiecim|my.lenice|jas.o|krak.w|olsztyn|ustanow|swider|zielona g.ra|izbica|gm\.|o.ar.w|henryk.w|j.zefos.aw|stara|bydgoszcz|gda.sk|z.bki|pozna.|komor.w|komornica|j.zef.w|za.ubice',re.I)
   l1=p1.findall(s1)
   l2=p1.findall(s2)
   l3=p1.findall(s3)
   if l1:
      kod=l1[0]
      miejscowosc=string.replace(s1,kod,'')
      ulica=JoinFields(s2,s3)
   elif l2:
      kod=l2[0]
      miejscowosc=string.replace(s2,kod,'')
      ulica=JoinFields(s1,s3)
   elif l3:
      kod=l3[0]
      miejscowosc=string.replace(s3,kod,'')
      ulica=JoinFields(s1,s2)
   else:
      if p3.search(s1):
         amiejscowosc=s1
         ulica=JoinFields(s2,s3)
      elif p3.search(s2):
         amiejscowosc=s2
         ulica=JoinFields(s1,s3)
      elif p3.search(s3):
         amiejscowosc=s3
         ulica=JoinFields(s1,s2)
      else:
         m1=p2.search(s1)
         m2=p2.search(s2)
         m3=p2.search(s3)
         if m1:
            ulica=s1
            miejscowosc=JoinFields(s2,s3)
         elif m2:
            ulica=s2
            miejscowosc=JoinFields(s1,s3)
         elif m3:
            ulica=s3
            miejscowosc=JoinFields(s1,s2)
         elif s1 or s2 or s3:
            print 'bad',s1,s2,s3
            ulica=JoinFields(s1,s2)
            ulica=JoinFields(ulica,s3)
   kod=string.replace(kod,' ','')
   return string.strip(ulica),string.strip(kod),string.strip(miejscowosc)

def GetNIP(s):
   wagi=[6,5,7,2,3,4,5,6,7]
   i,sum=0,0
   ret=''
   for c in s:
      if c>='0' and c<='9':
         if i<len(wagi):
            sum=sum+int(c)*wagi[i]
            ret=ret+c
            i=i+1
         elif i==len(wagi):
            if int(c)!=(sum%11):
               ret=''
            else:
               ret=ret+c
            i=i+1
   if len(ret)!=10:
      ret=''
   return ret

def ProcessKontr(fname1,fname2):
   acsv=CSVImport()
   bcsv=CSVExport(adelimiter=';',aemptyvalues=0)
   acsv.Open(fname1)
   bcsv.Header=[
'NazwaNazwiskoIImie',
'Ulica',
'KodPocztowy',
'Miejscowosc',
'Telefon',
'TelefonKomorkowy',
'ReprezentowanyPrzez',
'AdresKorespondencyjny',
'Nip',
'Pesel',
'NumerKontrahentaWSes',
'Uwagi',
]
   bcsv.Open(fname2)
   try:
      cnt=0
      while not acsv.EOF:
         if not cnt%20:
            print cnt,'\r',
#"KodKontr";"Nazwa1";"Nazwa2";"Adres1";"Adres2";"Adres3";"Nip";"Bank";"Konto";"Tel";"Fax"
         bcsv['NumerKontrahentaWSes']=GetKonto(acsv['KodKontr'])
         bcsv['NazwaNazwiskoIImie']=JoinFields(acsv['Nazwa1'],acsv['Nazwa2'])
         ulica,kod,miejscowosc=GetUlicaKodMiejscowosc(acsv['Adres1'],acsv['Adres2'],acsv['Adres3'])
         bcsv['Ulica']=ulica
         bcsv['KodPocztowy']=kod
         bcsv['Miejscowosc']=miejscowosc
         anip=acsv['Nip']
         bnip=GetNIP(anip)
         luwagi=[]
         if bnip:
            bcsv['Nip']=bnip
         elif anip:
            luwagi.append('Zly numer NIP: '+anip)
         abank=acsv['Bank']
         if abank:
            luwagi.append('Bank: '+abank)
         akonto=acsv['Konto']
         if akonto:
            luwagi.append('Konto bankowe: '+akonto)
         bcsv['Telefon']=JoinFields(acsv['Tel'],acsv['Fax'])
         bcsv['Uwagi']=string.join(luwagi,', ')
         bcsv['TelefonKomorkowy']=''
         bcsv['ReprezentowanyPrzez']=''
         bcsv['AdresKorespondencyjny']=''
         bcsv['Pesel']=''
         bcsv.Next()
         acsv.Next()
         cnt=cnt+1
      print
   finally:
      acsv.Close()
      bcsv.Close()

def ProcessKontrNIP(fname1,fname1b,fname2):
   acsv=CSVImport()
   bcsv=CSVExport(adelimiter=';',aemptyvalues=0)
   dnip={}
   acsv.Open(fname1b)
   while not acsv.EOF:
      dnip[GetKonto(acsv['NrKonta'])]=acsv['NIP']
      acsv.Next()
   print
   acsv.Close()

   acsv=CSVImport()
   acsv.Open(fname1)
   bcsv.Header=[
   'NazwaNazwiskoIImie',
   'Ulica',
   'KodPocztowy',
   'Miejscowosc',
   'Telefon',
   'Nip',
   'NumerKontrahentaFK',
   'Bank',
   'KontoWBanku',
   'Uwagi',
]
   bcsv.Open(fname2)
   try:
      cnt=0
      while not acsv.EOF:
         if not cnt%20:
            print cnt,'\r',
         bcsv['NumerKontrahentaFK']=GetKonto(acsv['NrKonta'])
         bcsv['NazwaNazwiskoIImie']=JoinFields(JoinFields(acsv['Nazwa1'],acsv['Nazwa2']),acsv['Nazwa3'])
         bcsv['Ulica']=acsv['Ulica']
         bcsv['KodPocztowy']=acsv['KodPocztowy']
         bcsv['Miejscowosc']=acsv['Miasto']
         anip=dnip.get(GetKonto(acsv['NrKonta']),'')
         bnip=GetNIP(anip)
         luwagi=[]
         if bnip:
            bcsv['Nip']=bnip
         elif anip:
            luwagi.append('Zly numer NIP: '+anip)
         bcsv['Bank']=acsv['Bank']
         bcsv['KontoWBanku']=acsv['KontoB']
         bcsv['Telefon']=JoinFields(acsv['Tel'],acsv['Fax'])
         luwagi.append(acsv['Wolne'])
         bcsv['Uwagi']=string.join(luwagi,', ')
         bcsv.Next()
         acsv.Next()
         cnt=cnt+1
      print
   finally:
      acsv.Close()
      bcsv.Close()

def Usage():
   print 'usage:'
   print '   python kontr2gk.py mode infile [infile2] outfile'
   print 'where:'
   print '   mode:'
   print '      -kontr - process KONTR.CSV from SES'
   print '      -kontrnip - process KONTR.CSV and KONTRNIP.CSV from FK'
   print '   infile: csv input file (KONTR)'
   print '   infile2: csv input file (KONTRNIP)'
   print '   outfile: .csv output file'

def Main():
   if len(sys.argv)==1:
      Usage()
      return
   if sys.argv[1]=='-kontr':
      ProcessKontr(sys.argv[2],sys.argv[3])
   elif sys.argv[1]=='-kontrnip':
      ProcessKontrNIP(sys.argv[2],sys.argv[3],sys.argv[4])
   else:
      Usage()
      return

