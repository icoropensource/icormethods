# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import CLASSES_Library_DBBase_Util_CSVImport as CSVImport
import string
import sys
import os
import re

def SortObrotyWgKonta(afname1,afname2):
   import bsddb3
   fin=CSVImport.CSVImport()
   fin.Open(afname1)
   if os.path.exists(afname2+'.bt'):
      os.unlink(afname2+'.bt')
   bfout=bsddb3.btopen(afname2+'.bt','w')
   cnt=0
   while not fin.EOF:
      cnt=cnt+1
      if not cnt%500:
         print '\r p1:',cnt,
      sn=fin['NrKonta']
      sd=map(int,string.split(fin['DataDok'],'-'))
      sr=int(fin['NrDok'])
      sp=int(fin['PozDok'])
      s='%s %04d %02d %02d %014d %014d %s %s %s %s %s %d'%(sn,sd[0],sd[1],sd[2],sr,sp,fin['SymbolDok'],fin['KodOperatora'],fin['StronaKonta'],fin['Kwota'],fin['Opis'],cnt)
      bfout[s]=fin.line
      fin.Next()
   print '\rtotal:',cnt
   fout=open(afname2,'w')
   try:
      fout.write(fin.headerline)
      cnt=0
      r=bfout.first()
      while r:
         cnt=cnt+1
         if not cnt%100:
            print '\r p2:',cnt,
         fout.write(r[1])
         r=bfout.next()
   except bsddb3._db.DBNotFoundError:
      pass
   print '\rtotal:',cnt
   bfout.close()
   os.unlink(afname2+'.bt')

def SortObrotyWgSumNaKonto(afname1,afname2,abymonth=1):
   fin=CSVImport.CSVImport()
   fin.Open(afname1)
   d={}
   cnt=0
   while not fin.EOF:
      cnt=cnt+1
      if not cnt%100:
         print '\r p1:',cnt,' , ',len(d.keys()),
      snumer=fin['NrKonta']
      sdata=map(int,string.split(fin['DataDok'],'-'))
      ssymbol=fin['SymbolDok']
      sstrona=fin['StronaKonta']
      dkwota=float(fin['Kwota'])
      if abymonth:
         skod='%s %d %02d'%(snumer,sdata[0],sdata[1]) # w rozbiciu na miesiace
      else:
         skod='%s %d %02d'%(snumer,sdata[0],1) # w rozbiciu na miesiace
      dv=d.get(skod,[0.0,0.0,0.0,0.0])
      if ssymbol=='99':
         if sstrona=='W':
            apos=0
         else:
            apos=1
      else:
         if sstrona=='W':
            apos=2
         else:
            apos=3
      dv[apos]=dv[apos]+dkwota
      d[skod]=dv
      fin.Next()
   print '\rtotal:',cnt
   fout=open(afname2,'w')
   try:
      fout.write('"Konto";"Data";"BOWn";"BOMa";"Wn";"Ma"\n')
      cnt=0
      lk=d.keys()
      lk.sort()
      for akey in lk:
         cnt=cnt+1
         if not cnt%100:
            print '\r p2:',cnt,
         ld=d[akey]
         sl=string.split(akey)
         fout.write('"%s";%s-%s-1;%0.2f;%0.2f;%0.2f;%0.2f\n'%(sl[0],sl[1],sl[2],ld[0],ld[1],ld[2],ld[3]))
      print '\rtotal:',cnt
      del lk
   finally:
      fout.close()
   del d

def SortObrotyWgMiesiecy(afname1,afname2,abyrodzaj=0):
   fin=CSVImport.CSVImport()
   fin.Open(afname1)
   d={}
   cnt=0
   while not fin.EOF:
      cnt=cnt+1
      if not cnt%100:
         print '\r p1:',cnt,' , ',len(d.keys()),
      snumer=fin['NrKonta']
      sdata=map(int,string.split(fin['DataDok'],'-'))
      ssymbol=fin['SymbolDok']
      sstrona=fin['StronaKonta']
      dkwota=float(fin['Kwota'])
      if abyrodzaj:
         skod='%s %d %02d'%(ssymbol,sdata[0],sdata[1])
      else:
         skod='%d %02d'%(sdata[0],sdata[1])
      dv=d.get(skod,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0])
      if ssymbol=='99':
         if sstrona=='W':
            apos=0
         else:
            apos=1
      else:
         if sstrona=='W':
            apos=2
         else:
            apos=3
      if snumer[1:2]=='9':
         apos=apos+4
      dv[apos]=dv[apos]+dkwota
      dv[8]=dv[8]+1
      d[skod]=dv
      fin.Next()
   print '\rtotal:',cnt
   fout=open(afname2,'w')
   try:
      if abyrodzaj:
         fout.write('"Data";"Rodzaj";"Ilosc","BOWn";"BOMa";"Wn";"Ma";"BOWnPB";"BOMaPB";"WnPB";"MaPB"\n')
      else:
         fout.write('"Data";"Ilosc","BOWn";"BOMa";"Wn";"Ma";"BOWnPB";"BOMaPB";"WnPB";"MaPB"\n')
      cnt=0
      lk=d.keys()
      lk.sort()
      for akey in lk:
         cnt=cnt+1
         if not cnt%100:
            print '\r p2:',cnt,
         ld=d[akey]
         sl=string.split(akey)
         if abyrodzaj:
            fout.write('%s-%s-1;"%s";%d;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f\n'%(sl[1],sl[2],sl[0],ld[8],ld[0],ld[1],ld[2],ld[3],ld[4],ld[5],ld[6],ld[7]))
         else:
            fout.write('%s-%s-1;%d;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f;%0.2f\n'%(sl[0],sl[1],ld[8],ld[0],ld[1],ld[2],ld[3],ld[4],ld[5],ld[6],ld[7]))
      print '\rtotal:',cnt
      del lk
   finally:
      fout.close()
   del d

def MergeCSV(afname,aflist):
   print 'Merge into file:',afname
   fout=open(afname,'w')
   w=1
   for bfname in aflist:
      fin=open(bfname,'r')
      print '  Add:',bfname
      l=fin.readline()
      if w:
         fout.write(l)
         w=0
      while 1:
         l=fin.readline()
         if not l:
            break
         fout.write(l)
      fin.close()
   fout.close()

def OverwriteCSV(afname,aflist):
   for bfname in aflist:
      fout=open(afname,'w')
      fin=open(bfname,'r')
      while 1:
         l=fin.readline()
         if not l:
            break
         fout.write(l)
      fin.close()
      fout.close()

def CheckCSVForBadCharacters(afname1,afname2):
   apatt=re.compile('[^ -~ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]')
   fin=CSVImport.CSVImport()
   fin.Open(afname1)
   fout=open(afname2,'w')
   cnt=0
   while not fin.EOF:
      cnt=cnt+1
      if not cnt%100:
         print '\r',cnt,
      for acol in fin.Header:
         s=fin[acol]
         if apatt.search(s):
            fout.write('%d,%s,"%s"\n'%(cnt,acol,s))
      fin.Next()

def Usage():
   print 'sposob uruchomienia:'
   print '   python csvsort.py parametr plik_we.csv plik_wy.csv'
   print 'gdzie:'
   print '   mode:'
   print '      -obrotywk - plik WE to obroty z FK, plik WY - dane posortowane w/g konta'
   print '      -obrotywskm - plik WE to obroty z FK, plik WY - dane posortowane w/g konta - zsumowane miesiecznie'
   print '      -obrotywsk - plik WE to obroty z FK, plik WY - dane posortowane w/g konta - zsumowane od poczatku roku'
   print '      -obrotywdm - plik WE to obroty z FK, plik WY - dane posortowane i zsumowane w/g miesiecy'
   print '      -obrotywdmd - plik WE to obroty z FK, plik WY - dane posortowane i zsumowane w/g miesiecy oraz rodzaju dokumentu'
   print '      -merge <plik_WY> <plik_WE_1> <plik_WE_2> .... <plik_WE_N> - laczy podane pliki CSV w jeden'
   print '      -overwrite <plik_WY> <plik_WE_1> <plik_WE_2> .... <plik_WE_N> - laczy podane pliki CSV w jeden (zachowuje tylko ostatni)'
   print '      -checkcharacters <plik_WE> <plik_WY> - sprawdza plik CSV pod katem poprawnosci znakow'
   print '   plik_we.csv: dane WE w postaci CSV'
   print '   plik_wy.csv: plik wynikowy w postaci CSV'

def Main():
   if len(sys.argv)<4:
      Usage()
      return
   if sys.argv[1]=='-obrotywk':
      SortObrotyWgKonta(sys.argv[2],sys.argv[3])
   elif sys.argv[1]=='-obrotywskm':
      SortObrotyWgSumNaKonto(sys.argv[2],sys.argv[3])
   elif sys.argv[1]=='-obrotywsk':
      SortObrotyWgSumNaKonto(sys.argv[2],sys.argv[3],abymonth=0)
   elif sys.argv[1]=='-obrotywdm':
      SortObrotyWgMiesiecy(sys.argv[2],sys.argv[3])
   elif sys.argv[1]=='-obrotywdmd':
      SortObrotyWgMiesiecy(sys.argv[2],sys.argv[3],abyrodzaj=1)
   elif sys.argv[1]=='-merge':
      MergeCSV(sys.argv[2],sys.argv[3:])
   elif sys.argv[1]=='-overwrite':
      OverwriteCSV(sys.argv[2],sys.argv[3:])
   elif sys.argv[1]=='-checkcharacters':
      CheckCSVForBadCharacters(sys.argv[2],sys.argv[3])
   else:
      Usage()
      return



