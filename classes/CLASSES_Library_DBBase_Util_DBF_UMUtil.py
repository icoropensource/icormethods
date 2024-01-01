# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_DBBase_Util_CSVImport import CSVExport
from CLASSES_Library_DBBase_Util_DBFImport import DBFImport
import string,sys,time,os
import bsddb3
import md5

FILE_PESEL='pesel.db'
FILE_SIGID_PODATNICY_GLOWNI='sigid_pg.db'
FILE_ULICE='ulice.db'

class SampleDBF(DBFImport): # zbior NF_GL.DBF
   def CheckDeleted(self,afname):
      self.Open(afname)
      dcnt=0
      while self.cnt<99999999999L:
         if not self.cnt%100:
            print '\r%d/%d'%(dcnt,self.cnt),
         self.Next()
         if not self.Record:
            break
         if self.IsDeleted:
            dcnt=dcnt+1
            self.DumpRecord()
      print
   def UniqueTest(self,afname,afield):
      self.Open(afname)
      audbname='_uniquetest1.db'
      if os.path.exists(audbname):
         os.unlink(audbname)
      f=bsddb3.hashopen(audbname)
      dcnt=0
      while self.cnt<99999999999L:
         if not self.cnt%100:
            print '\r%d/%d'%(dcnt,self.cnt),
         self.Next()
         if not self.Record:
            break
         if not self.IsDeleted:
            if f.has_key(self.Record[afield]):
               dcnt=dcnt+1
               self.DumpRecord()
            else:
               f[self.Record[afield]]='1'
      f.close()
      os.unlink(audbname)
      print

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

class PodatnicyGlowni(DBFImport): # zbior NF_GL.DBF
   def OutputOpen(self,bfname):
      afname,afext=os.path.splitext(bfname)
      aheader=['Ident','WlascicielNazwisko','WlascicielImie','Pesel','WlascicielUlica','WlascicielNIP']
      self.ifile=CSVExport()
      self.ifile.Header=aheader[:]
      self.ifile.Open(afname+'_IMPORT'+afext)
      self.ufile=CSVExport()
      self.ufile.Header=aheader[:]
      self.ufile.Open(afname+'_UPDATE'+afext)
      self.dfile=CSVExport()
      self.dfile.Header=aheader[:]
      self.dfile.Open(afname+'_DIFF'+afext)
      self.dufile=CSVExport()
      self.dufile.Header=aheader[:]
      self.dufile.Open(afname+'_DIFF_ULICE'+afext)
      self.dnfile=CSVExport()
      self.dnfile.Header=aheader[:]
      self.dnfile.Open(afname+'_DIFF_NIP'+afext)
   def Process(self,afname):
      f=bsddb3.hashopen(FILE_SIGID_PODATNICY_GLOWNI)
      fp=bsddb3.hashopen(FILE_PESEL)
      fu=bsddb3.hashopen(FILE_ULICE)
      try:
         self.Open(afname)
         acnt,abadpeselnip=0,0
         while acnt<99999999999L:
            if not acnt%1000:
               print '\r%d/%d'%(acnt,self.nrecs),
            self.Next()
            if not self.Record:
               break
            if not self.IsDeleted:
               apesel=self.Record['PESEL']
               aident=self.Record['IDENT']
               aulica=self.Record['WADR_U']
               anip=self.Record['WNIP']
               if not fu.has_key(aulica):
                  o2file=self.dufile
               else:
                  o2file=None
               if GetNIP(anip):
                  o3file=None
               else:
                  o3file=self.dnfile
               amd5=md5.new(apesel+'_'+self.Record['WLASC_N']+'_'+self.Record['WLASC_I'])
               ahex=amd5.hexdigest()
               if fp.has_key(apesel):
                  if f.has_key(aident):
                     if f[aident]==ahex:
                        ofile=None
                     else:
                        ofile=self.ufile
                        f[aident]=ahex
                  else:
                     ofile=self.ifile
                     f[aident]=ahex
               else:
                  ofile=self.dfile
               if ofile:
                  ofile['Ident']=aident
                  ofile['WlascicielNazwisko']=self.Record['WLASC_N']
                  ofile['WlascicielImie']=self.Record['WLASC_I']
                  ofile['Pesel']=apesel
                  ofile['WlascicielNIP']=anip
                  ofile['WlascicielUlica']=aulica
                  ofile.Next()
               if o2file:
                  o2file['Ident']=aident
                  o2file['WlascicielNazwisko']=self.Record['WLASC_N']
                  o2file['WlascicielImie']=self.Record['WLASC_I']
                  o2file['Pesel']=apesel
                  o2file['WlascicielUlica']=aulica
                  o2file['WlascicielNIP']=anip
                  o2file.Next()
               if o3file:
                  o3file['Ident']=aident
                  o3file['WlascicielNazwisko']=self.Record['WLASC_N']
                  o3file['WlascicielImie']=self.Record['WLASC_I']
                  o3file['Pesel']=apesel
                  o3file['WlascicielUlica']=aulica
                  o3file['WlascicielNIP']=anip
                  o3file.Next()
               if ofile and o3file:
                  abadpeselnip=abadpeselnip+1
            acnt=acnt+1
      finally:
         f.close()
         fp.close()
         fu.close()
      print
      print 'Bad PESEL and NIP:',abadpeselnip
   def OutputClose(self):
      self.ifile.Close()
      self.ufile.Close()
      self.dfile.Close()
      self.dufile.Close()
      self.dnfile.Close()

class PeselImionaDrugie(DBFImport): # zbior I2.DBF
   def OutputOpen(self,bfname):
      self.bfile=CSVExport()
      self.bfile.Header=['ImieDrugie','Pesel']
      self.bfile.Open(bfname)
   def Process(self,afname):
      f=bsddb3.hashopen(FILE_PESEL)
      try:
         self.Open(afname)
         while self.cnt<99999999999L:
            if not self.cnt%1000:
               print '\r%d/%d'%(self.cnt,self.nrecs),
            self.Next()
            if not self.Record:
               break
            f[self.Record['P']]=self.Record['I2']
            self.bfile['ImieDrugie']=self.Record['I2']
            self.bfile['Pesel']=self.Record['P']
            self.bfile.Next()
      finally:
         f.close()
      print
   def OutputClose(self):
      self.bfile.Close()

class Pesel(DBFImport): # zbior DP.DBF
   def OutputOpen(self,bfname):
      self.bfile=CSVExport()
      self.bfile.Header=['Nazwisko','Imie','Pesel']
      self.bfile.Open(bfname)
   def Process(self,afname):
      f=bsddb3.hashopen(FILE_PESEL)
      try:
         self.Open(afname)
         while self.cnt<99999999999L:
            if not self.cnt%1000:
               print '\r%d/%d'%(self.cnt,self.nrecs),
            self.Next()
            if not self.Record:
               break
            if not self.IsDeleted:
               f[self.Record['P']]='1'
               self.bfile['Nazwisko']=self.Record['N1']
               self.bfile['Imie']=self.Record['I1']
               self.bfile['Pesel']=self.Record['P']
               self.bfile.Next()
      finally:
         f.close()
      print
   def OutputClose(self):
      self.bfile.Close()

class Ulice(DBFImport): # zbior ULICE.DBF
   def OutputOpen(self,bfname):
      self.bfile=CSVExport()
      self.bfile.Header=['Ulica','Uwagi']
      self.bfile.Open(bfname)
   def Process(self,afname):
      f=bsddb3.hashopen(FILE_ULICE)
      try:
         self.Open(afname)
         while self.cnt<99999999999L:
            if not self.cnt%1000:
               print '\r%d/%d'%(self.cnt,self.nrecs),
            self.Next()
            if not self.Record:
               break
            if not self.IsDeleted:
               f[self.Record['ULICA']]='1'
               self.bfile['Ulica']=self.Record['ULICA']
               self.bfile['Uwagi']=self.Record['UWAGI']
               self.bfile.Next()
      finally:
         f.close()
      print
   def OutputClose(self):
      self.bfile.Close()

def Usage():
   print 'usage:'
   print '   python umicorimport.py mode infile [infile2,infile3,...] outfile'
   print 'where:'
   print '   mode:'
   print '      -tpmain - process NF_GL file from SIGID'
   print '      -pesel - process DP file from Ewidencja Ludnosci'
   print '      -peselimiona2 - process I2 file from Ewidencja Ludnosci'
   print '      -ulice - process ULICE file from Ewidencja Ludnosci'
   print '      -checkdeleted - check for deleted records in infile.DBF'
   print '      -uniquetest - check for unique field values in specified INFILE2 field'
   print '   infile: DBF input file'
   print '   infile2,...: other DBF files'
   print '   outfile: .csv output file'

def Main():
   if len(sys.argv)==1:
      Usage()
      return
   if sys.argv[1]=='-tpmain':
      afile=PodatnicyGlowni()
      afile.OutputOpen(sys.argv[3])
      afile.Process(sys.argv[2])
      afile.OutputClose()
   elif sys.argv[1]=='-pesel':
      afile=Pesel()
      afile.OutputOpen(sys.argv[3])
      afile.Process(sys.argv[2])
      afile.OutputClose()
   elif sys.argv[1]=='-ulice':
      afile=Ulice()
      afile.OutputOpen(sys.argv[3])
      afile.Process(sys.argv[2])
      afile.OutputClose()
   elif sys.argv[1]=='-peselimiona2':
      afile=PeselImionaDrugie()
      afile.OutputOpen(sys.argv[3])
      afile.Process(sys.argv[2])
      afile.OutputClose()
   elif sys.argv[1]=='-checkdeleted':
      afile=SampleDBF()
      afile.CheckDeleted(sys.argv[2])
   elif sys.argv[1]=='-uniquetest':
      afile=SampleDBF()
      afile.UniqueTest(sys.argv[2],sys.argv[3])
   else:
      Usage()
      return



