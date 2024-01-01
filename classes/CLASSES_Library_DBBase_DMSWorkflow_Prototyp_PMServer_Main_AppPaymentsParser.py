# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserPaczki as XMLParserPaczki
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppSigid as AppSigid
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppWieczysci as AppWieczysci
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppWSp as AppWSp
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppUtil as AppUtil
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppSRolny as AppSRolny
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppRadix as AppRadix
import CLASSES_Library_ICORBase_Interface_ICORTextFile as ICORTextFile
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import os

class PaymentsParser(XMLParserPaczki.ICORPMPackageParser):
   def ParseRS(self,aprocessor,rs,acheckonly=0):
      self.PaymentsCnt=0
      self.PaymentsExisting=0
      arsfield=rs.Fields.Item("TrescPaczki")
      self.PaymentsProcessor=aprocessor
      self.CheckOnly=acheckonly
      self.Initialize()
      self.reset()
      asize=arsfield.ActualSize
      fout=open(aprocessor.TEMP_DIR+aprocessor.OIDPaczki+'.xml','wb')
      try:
         while asize>0:
            v=arsfield.GetChunk(1000)
            v=v.encode('cp1250')
            fout.write(v)
            self.feed(v)
            asize=asize-1000
      finally:
         fout.close()

      if self.IsGood:
         print 'Ilosc pozycji:',self.PaymentsCnt
         rs.Fields.Item("IloscPozycji").Value=self.PaymentsCnt

         rs.Fields.Item("Aplikacja").Value=self.Aplikacja
         rs.Fields.Item("DataUtworzeniaPaczki").Value=self.DataUtworzeniaPaczki
         rs.Fields.Item("IDPaczki").Value=self.IDPaczki
         rs.Fields.Item("AutorPaczki").Value=self.AutorPaczki
         rs.Fields.Item("CSVSeparator").Value=self.CSVSeparator
         rs.Fields.Item("CSVOgranicznikTekstu").Value=self.CSVOgranicznikTekstu
         rs.Fields.Item("CSVFormatDaty").Value=self.CSVFormatDaty
         rs.Fields.Item("CSVSeparatorNaKoncuLinii").Value=self.CSVSeparatorNaKoncuLinii
         rs.Fields.Item("CSVZnakNowejLinii").Value=self.CSVZnakNowejLinii

#$$ uaktualniac maszyne stanow
#         rs.Fields.Item('Status').Value=5
      else:
         rs.Fields.Item("StatusTresc").Value=string.join(self.status,'<br>\n')
#$$ uaktualniac maszyne stanow 
#         rs.Fields.Item('Status').Value=4
         rs.Update()
   def ParseFile(self,aprocessor,afpath,rs,acheckonly=0,ret=None,acompressed=0):
      self.PaymentsCnt=0
      self.PaymentsExisting=0
      self.PaymentsProcessor=aprocessor
      self.CheckOnly=acheckonly
      self.Initialize()
      self.reset()
      if acompressed:
         bfname=aprocessor.ArchiveDir+'/'+rs.Fields.Item("_OID").Value+'.gz'
#         print 'bfname:',bfname
         afarchive=ICORTextFile.TextFile(bfname,'w')
      amsize=os.path.getsize(afpath)
      self.ProgressEstimator=ICORUtil.TimeProgressEstimator(amsize)
      aasize=0
      fout=open(afpath,'r')
      try:
         c1=''
         c1=fout.read(1)
         if c1==chr(10) or c1==chr(13):
            c1=fout.read(1)
            if c1==chr(10) or c1==chr(13):
               c1=''
         while 1:
            v=c1+fout.readline()
            aasize=aasize+len(v)
            SetProgress(aasize,amsize)
            self.Elapsed,self.Estimated,self.Remaining=self.ProgressEstimator.SetProgress(aasize)
            if len(v)<=0:
               break
            if v!='\n' and not v[-2:-1] in ['"','>']:
               v=v[:-1]+'&#13;&#10;'
            if acompressed:
               afarchive.write(v)
            self.feed(v)
            c1=''
      finally:
         if acompressed:
            afarchive.close()
         fout.close()
      SetProgress(0,0)
      if self.CheckOnly:
         if self.IsGood:
            if not ret is None:
               ret.append('  Ilosc pozycji: '+str(self.PaymentsCnt))
               ret.append('  Paczka poprawna')
            rs.Fields.Item("IloscPozycji").Value=self.PaymentsCnt
            rs.Fields.Item("Aplikacja").Value=self.Aplikacja
            rs.Fields.Item("DataUtworzeniaPaczki").Value=self.DataUtworzeniaPaczki
            rs.Fields.Item("IDPaczki").Value=self.IDPaczki
            rs.Fields.Item("AutorPaczki").Value=self.AutorPaczki
            rs.Fields.Item("CSVSeparator").Value=self.CSVSeparator
            rs.Fields.Item("CSVOgranicznikTekstu").Value=self.CSVOgranicznikTekstu
            rs.Fields.Item("CSVFormatDaty").Value=self.CSVFormatDaty
            rs.Fields.Item("CSVSeparatorNaKoncuLinii").Value=self.CSVSeparatorNaKoncuLinii
            rs.Fields.Item("CSVZnakNowejLinii").Value=self.CSVZnakNowejLinii
            astatus=3
         else:
            astatus=2
            if not ret is None:
               ret.append('  Paczka błędna - lista błędów:')
               ret.extend(self.status)
         rs.Fields.Item("StatusTresc").Value=string.join(self.status,'<br>\n')
         rs.Fields.Item('Status').Value=astatus
   def OnPaymentAdd(self,aplatnosc):
      if not self.CheckOnly:
         self.paymentsmanager.StorePlatnosc(aplatnosc)
      self.PaymentsCnt=self.PaymentsCnt+1
#      self.Platnosci.append(aplatnosc)
   def OnStartPlatnosci(self):
      if self.CheckOnly:
         return
      if self.Aplikacja=='WGMINA':
         self.paymentsmanager=AppWieczysci.PaymentsManagerWGmina(self,self.Aplikacja)
      elif self.Aplikacja in ['SIGID','SIGID_N']:
         self.paymentsmanager=AppSigid.PaymentsManagerSigid(self,self.Aplikacja)
      elif self.Aplikacja=='WSP':
         self.paymentsmanager=AppWSp.PaymentsManagerWSp(self,self.Aplikacja)
      elif self.Aplikacja in ['SROLNY','SIGID_R']:
         self.paymentsmanager=AppSRolny.PaymentsManagerSRolny(self,self.Aplikacja)
      elif self.Aplikacja=='RADIX_POGRUN':
         self.paymentsmanager=AppRadix.PaymentsManagerRadixPoGrun(self,self.Aplikacja)
      else:
         print '*** Nieznana aplikacja:',self.Aplikacja
         self.paymentsmanager=None
   def OnEndPlatnosci(self):
      print 'koniec'
   def OnGetPlatnoscClass(self):
      if self.Aplikacja=='WGMINA':
         return AppWieczysci.PMPlatnoscWGmina
      elif self.Aplikacja=='WSP':
         return AppWSp.PMPlatnoscWSp
      elif self.Aplikacja in ['SIGID','SIGID_N']:
         return AppSigid.PMPlatnoscSigid
      elif self.Aplikacja in ['SROLNY','SIGID_R']:
         return AppSRolny.PMPlatnoscSRolny
      elif self.Aplikacja=='RADIX_POGRUN':
         return AppRadix.PMPlatnoscRadixPoGrun
      else:
         print '*** Nieznana aplikacja:',self.Aplikacja
      return AppUtil.PMPlatnosc



