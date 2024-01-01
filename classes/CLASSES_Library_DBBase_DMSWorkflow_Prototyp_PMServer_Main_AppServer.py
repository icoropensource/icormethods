# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserPaczki as XMLParserPaczki
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserWydruku as XMLParserWydruku
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserZaplat as XMLParserZaplat
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppPaymentsParser as AppPaymentsParser
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppUtil as AppUtil
import CLASSES_Library_NetBase_Utils_SMTPUtil as SMTPUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import icordbmain.adoutil as ADOLibInit
import CLASSES_Library_DBBase_Util_CSVImport as CSVImport
import pythoncom
import string
import random
import time
import sha
import os
import re

import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppSigid as AppSigid
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppWieczysci as AppWieczysci
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppWSp as AppWSp
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppSRolny as AppSRolny
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppRadix as AppRadix

import icordbmain.dbaccess as dbaccess
import appplatform.startutil as startutil

TEMP_DIR='c:/icor/util/pmserver/packages/'

"select TransactionID from Trans where TransactionID in ('123123','124123','133124','133123')"

TRANS_ID_DICT={}

class SPMError(Exception):
   def __init__(self,errmsg=''):
      Exception.__init__(self,errmsg)

class MassPaymentsServer:
   def __init__(self,aproject):
      self.adolib,self.adoconst,amajor,aminor=ADOLibInit.ADOInitialize()
      self.TEMP_DIR=TEMP_DIR
      pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
      poid=pclass.Nazwa.Identifiers(startutil.appconfig.IParams['pm_projekt'])
      if poid<0:
         return
      pobj=pclass[poid]
      self.stn_rejestrpaczek,self.stn_buforpreprocesora,self.stn_poladodatkoweSIGID,self.stn_pozycjewyciagu='','','',''
      self.stn_przesylki,self.stn_listy,self.stn_rejestrrachunkowbankowych='','',''
      self.stn_kodyprzesylek,self.stn_formatywydrukupulikodow='',''
      self.stn_adresy=''
      dobj=pobj.BazyZrodlowe
      while dobj:
         if dobj.Nazwa=='Rejestr paczek':
            self.stn_rejestrpaczek='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Bufor Preprocesora':
            self.stn_buforpreprocesora='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Pola dodatkowe SIGID':
            self.stn_poladodatkoweSIGID='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Pola dodatkowe':
            self.stn_poladodatkoweSIGID='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Pozycje Wyci�gu':
            self.stn_pozycjewyciagu='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Przesy�ki':
            self.stn_przesylki='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Listy':
            self.stn_listy='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Kody przesy�ek':
            self.stn_kodyprzesylek='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Pula Kod�w Przesy�ek':
            self.stn_pulakodowprzesylek='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Formaty wydruku puli kod�w':
            self.stn_formatywydrukupulikodow='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Rejestr rachunk�w bankowych':
            self.stn_rejestrrachunkowbankowych='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         elif dobj.Nazwa=='Adresy':
            self.stn_adresy='%sBZR_%d'%(pobj.BaseNameModifier,dobj.OID)
         dobj.Next()
      self.ConnectionString=dbaccess.GetConnectionString(pobj.DBAccess)
      self.ProjectAppPath=pobj.AppPath
      self.ProjectWWWDataPath=FilePathAsSystemPath(pobj.WWWDataPath)
      self.connection=None
      self.Hits=0
      mclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main']
      self.PMOID=mclass.Nazwa.Identifiers(aproject)
      self.Rachunki2IDTransakcji={}
      self.Aplikacje2SciezkaArchiwum={}
      self.Aplikacje2SciezkaDanych={}
      if self.PMOID>=0:
         mobj=mclass[self.PMOID]
         self.RokObliczeniowy=mobj['RokObliczeniowy']
         aobj=mobj.AplikacjeZrodlowe
         while aobj:
            self.Rachunki2IDTransakcji[aobj.RachunekPomocniczy[2:]]=aobj.AccountAcc2
            self.Aplikacje2SciezkaArchiwum[(aobj.Aplikacja,aobj['RokObliczeniowy'])]=FilePathAsSystemPath(aobj.SciezkaArchiwum)
            self.Aplikacje2SciezkaDanych[(aobj.Aplikacja,aobj['RokObliczeniowy'])]=FilePathAsSystemPath(aobj.SciezkaDanych)
            aobj.Next()
         self.SciezkaWyciagow=mobj.SciezkaWyciagow
         self.SMTPServer=mobj.SMTPServer
         self.SMTPUser=mobj.SMTPUser
         self.SMTPPassword=mobj.SMTPPassword
         self.SMTPFrom=mobj.SMTPFrom
         self.SMTPTo=string.split(mobj.SMTPTo,',')
   def SendMail(self,asubject,atext):
      if not self.SMTPServer:
         return          
      if type(atext)==type([]):
         atext=string.join(atext,'\n')
      asmtp=SMTPUtil.AuthSMTP(self.SMTPServer)
      if self.SMTPUser!='' and self.SMTPPassword!='':
         asmtp.login(self.SMTPUser,self.SMTPPassword)
      for ato in self.SMTPTo:
         asmtp.sendmail(string.strip(self.SMTPFrom),string.strip(ato),'Subject: [SPM] %s\n\n'%asubject+atext)
      asmtp.quit()
   def GetRandomFileName(self,aaplikacja,aprefix):
      acnt=0
      arok=int(self.RokObliczeniowy)
      adir=''
      while not adir and acnt<10:
         adir=self.Aplikacje2SciezkaDanych.get((aaplikacja,arok-acnt),'')
         acnt=acnt+1
      if not adir:
         raise SPMError('Brak danych o roku obliczeniowym dla aplikacji: '+aaplikacja)
      afname=ICORUtil.GetRandomFileName([adir,adir+'/archiwum'],aprefix,'.csv')
      return adir+'/'+afname
   def OpenConnection(self,aservercursor=1):
      try:
         self.connection=self.adolib.Connection()
      except:
         import win32api
         print 'USER:',win32api.GetUserName()
         raise
      self.connection.Open(self.ConnectionString)
      if aservercursor:
         alocation=self.adoconst.adUseServer
      else:
         alocation=self.adoconst.adUseClient
      self.connection.CursorLocation=alocation
      self.connection.CommandTimeout=0
   def CloseConnection(self):
      if not self.connection is None:
         self.connection.Close()
         self.connection=None
   def GetRS(self,asql,aclient=0):
      rs=self.adolib.Recordset()
      if aclient:
         rs.Open(asql,self.connection,self.adoconst.adUseClient,self.adoconst.adLockOptimistic) #
      else:
         rs.Open(asql,self.connection,self.adoconst.adOpenKeyset,self.adoconst.adLockOptimistic) #
      return rs
   def UpdateRS(self,rs,acnt=7):
      while acnt:
         try:
            rs.Update()
            break
         except:
            acnt=acnt-1
            if not acnt:
               raise
            time.sleep(7)
   def ConnectionExecute(self,asql):
      rs1,status=self.connection.Execute(asql)
      if rs1.State<>self.adoconst.adStateClosed:
         rs1.Close()
      rs1=None
      return status
   def ProcessPackage(self,afpath,aobj):
      self.ImportStatus=[]
      adir,afname=os.path.split(afpath)
      afbasename,afext=os.path.splitext(afname)
      self.BaseName=afbasename
      self.ArchiveDir=FilePathAsSystemPath(aobj.SciezkaArchiwum)
      ahash,asize,alastline=AppUtil.GetPackageFileInfo(afpath)
      self.RokObliczeniowyPaczki=aobj['RokObliczeniowy']
      self.ImportStatus.append('***********************************************************')
      self.ImportStatus.append('Import paczki dla aplikacji: '+aobj.Aplikacja+' / '+aobj.RokObliczeniowy)
      self.ImportStatus.append('  Plik: '+afname+' Rozmiar: '+str(asize)+' Suma kontrolna: '+ahash)
      if not alastline or ahash=='':
         self.ImportStatus.append('  Plik jest uszkodzony, b�d� nie zamkni�ty')
         try:
            self.SendMail('process package',self.ImportStatus)
         except:
            self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
         return string.join(self.ImportStatus,'\n')
      self.OpenConnection()
      try:
         asql="select * from %s where SumaKontrolna='%s'"%(self.stn_rejestrpaczek,ahash)
         wexists=0
         rs=self.GetRS(asql)
         if rs.State!=self.adoconst.adStateClosed:
            if not rs.EOF and not rs.BOF:
               wexists=1
               self.ImportStatus.append('  Paczka zosta�a ju� wcze�niej zarejestrowana.')
         if not wexists:
            rs.AddNew()
            rs.Fields.Item('Status').Value=1
            rs.Fields.Item('NazwaPaczki').Value=afbasename
            rs.Fields.Item('SumaKontrolna').Value=ahash
            rs.Fields.Item('RozmiarPliku').Value=asize
            self.ImportStatus.append('  Pocz�tek rejestracji paczki: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
            t1=time.time()
            aparser=AppPaymentsParser.PaymentsParser()
            aerror=0
            try:
               aparser.ParseFile(self,afpath,rs,acheckonly=1,ret=self.ImportStatus)
               self.ImportStatus.append('  Paczka sprawdzona, pocz�tek importu: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
               rs.Update()
               self.OIDPaczki=ADOLibInit.GetRSValueAsStr(rs,"_OID")
               rs.Close()
               asql="select * from %s where _OID='%s'"%(self.stn_rejestrpaczek,self.OIDPaczki)
               rs=self.GetRS(asql)
            except:
               aparser.IsGood=0
               aerror=1
               self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
            if aparser.IsGood:
               self.ImportStatus.append('  pocz�tek dodawania: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
               amaxpayments=aparser.PaymentsCnt
               aparser=AppPaymentsParser.PaymentsParser()
               aparser.MaxPayments=amaxpayments
               try:
                  aparser.ParseFile(self,afpath,rs,acheckonly=0,ret=self.ImportStatus,acompressed=1)
               except:
                  aerror=1
                  self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
               if aerror:
                  self.ImportStatus.append('  Zaimportowano cz�� p�atno�ci: '+str(aparser.PaymentsCnt))
               else:
                  self.ImportStatus.append('  Zaimportowano p�atno�ci: '+str(aparser.PaymentsCnt))
               if aparser.PaymentsExisting:
                  self.ImportStatus.append('  Ilo�� ju� istniej�cych p�atno�ci: '+str(aparser.PaymentsExisting))
            t2=time.time()
            if not aerror:
               os.rename(afpath,adir+'/archiwum/'+afname)
               try:
                  rs.Fields.Item('CzasImportu').Value=int(t2-t1)
                  if not aerror:
                     rs.Fields.Item('Status').Value=5 # OK
                  else:
                     rs.Fields.Item('Status').Value=4 # Error
                  rs.Update()
                  rs.Close()
               except:
                  self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
            self.ImportStatus.append('  Koniec rejestracji paczki: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
      finally:
         try:
            self.CloseConnection()
         except:
            self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
      try:
         self.SendMail('process package',self.ImportStatus)
      except:
         self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
      InfoStatus('')
      import win32api
      try:
         win32api.Beep(4000,150)
         win32api.Beep(2000,100)
      except:
         pass
      return string.join(self.ImportStatus,'\n')
   def Process(self):
      if self.stn_rejestrpaczek=='' or self.stn_buforpreprocesora=='' or self.stn_poladodatkoweSIGID=='':
         print 'brak tabel systemowych dla serwera PM'
         return
      self.OpenConnection()
      try:
         asql="DELETE %s WHERE _OID<>'44'"%self.stn_buforpreprocesora
         rs,status=self.connection.Execute(asql)
         asql='select * from %s where Status=3'%self.stn_rejestrpaczek
         rs=self.GetRS(asql)
         if rs.State!=self.adoconst.adStateClosed:
            while not rs.EOF and not rs.BOF:
               anazwa=ADOLibInit.GetRSValueAsStr(rs,"NazwaPaczki")
               self.OIDPaczki=ADOLibInit.GetRSValueAsStr(rs,"_OID")
               aparser=AppPaymentsParser.PaymentsParser()
               aparser.ParseRS(self,rs,acheckonly=1)
               if aparser.IsGood:
                  aparser=AppPaymentsParser.PaymentsParser()
                  aparser.ParseFile(self,rs)
               rs.MoveNext()
      finally:
         self.CloseConnection()
   def ProcessBankImport2005(self,afname):
#            
#         print acsv.Header
#      return 'OK!!! '+afname
      self.ImportStatus=['',]
      asize,alastline=AppUtil.GetZaplatyFileInfo(afname)
      self.ImportStatus.append('***********************************************************')
      self.ImportStatus.append('Import zaplat')
      self.ImportStatus.append('  Plik: '+afname+' Rozmiar: '+str(asize))
      if not alastline or asize<100:
         self.ImportStatus.append('  Plik jest uszkodzony, b�d� nie zamkni�ty')
         try:
            self.SendMail('process payments',self.ImportStatus)
         except:
            self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
         return string.join(self.ImportStatus,'\n')
      self.OpenConnection()
      aparser=XMLParserZaplat.ICORProfficeParser()
      try:
         aparser.ParseFile(self,afname)
      finally:
         self.CloseConnection()
      return string.join(self.ImportStatus,'\n')
   def ProcessBankImport(self,afname):
#            
#         print acsv.Header
#      return 'OK!!! '+afname
      self.ImportStatus=['',]
      self.OpenConnection()
      try:
         dwyciagi={}
         acsv=CSVImport.CSVImport(adelimiter=',',atextQualifier='"')
         acsv.Open(afname)
         try:
            while not acsv.EOF:
               self.ImportStatus.append(acsv['Id. rachunku']+' '+acsv['Kwota']+' '+acsv['Referencje klienta']+' '+acsv['Wyci�g'])
               anrpozycji=dwyciagi.get(acsv['Wyci�g'],0)
               anrpozycji=1+anrpozycji
               dwyciagi[acsv['Wyci�g']]=anrpozycji
               asha=sha.new()
               for s in [acsv['Bank'],acsv['Id. rachunku'],acsv['Wyci�g'],'20'+acsv['Data waluty'],acsv['Tre�� operacji'],acsv['Kod operacji'],acsv['Referencje klienta'],acsv['Kwota'],'20'+acsv['Data ksi�g.'],acsv['Kontrahent'],acsv['Kontrahent 2'],acsv['Kod stat.'],acsv['Id. rachunku dla dyspozycji'],acsv['Nazwa rachunku'],acsv['Szczeg�y p�atno�ci']]: #str(anrpozycji),
                  asha.update(s)
               adigest=asha.hexdigest()
               
               asql="SELECT * FROM %s WHERE SumaKontrolna='%s'"%(self.stn_pozycjewyciagu,adigest)
               rs=self.GetRS(asql,aclient=1)
               astatus='I1'
               if rs.State!=self.adoconst.adStateClosed:
                  if rs.EOF or rs.BOF:
                     rs.AddNew()
                     aacc2=self.Rachunki2IDTransakcji.get(acsv['Bank']+acsv['Id. rachunku'],'')
                     if aacc2=='':
                        astatus='E1'
                     areferencje=acsv['Referencje klienta']
                     aidtransakcji=''
                     if areferencje=='NONREF':
                        astatus='I2'
                     elif areferencje=='':
                        astatus='I3'
                     else:
                        aidtransakcji=areferencje+aacc2
                        rs.Fields.Item('IDTransakcji').Value=aidtransakcji
                     rs.Fields.Item('PozycjaNaWyciagu').Value=anrpozycji
                     rs.Fields.Item('SumaKontrolna').Value=adigest
                     rs.Fields.Item('Bank').Value=acsv['Bank']
                     rs.Fields.Item('IdRachunku').Value=acsv['Id. rachunku']
                     rs.Fields.Item('Wyciag').Value=acsv['Wyci�g']
                     rs.Fields.Item('DataWaluty').Value='20'+acsv['Data waluty']
                     rs.Fields.Item('SzczegolyPlatnosci').Value=acsv['Szczeg�y p�atno�ci'][:199]
                     rs.Fields.Item('TrescOperacji').Value=acsv['Tre�� operacji'][:199]
                     rs.Fields.Item('KodOperacji').Value=acsv['Kod operacji']
                     rs.Fields.Item('ReferencjeKlienta').Value=acsv['Referencje klienta']
                     rs.Fields.Item('Kwota').Value=acsv['Kwota']
                     rs.Fields.Item('DataKsiegowania').Value='20'+acsv['Data ksi�g.']
                     rs.Fields.Item('Kontrahent').Value=acsv['Kontrahent']+acsv['Kontrahent 2']
                     rs.Fields.Item('KodStatystyczny').Value=acsv['Kod stat.']
                     rs.Fields.Item('Storno').Value=acsv['Storno']
                     rs.Fields.Item('Aktualizacja').Value='20'+acsv['Aktualizacja']
                     rs.Fields.Item('DataWyciagu').Value='20'+acsv['Data  wyci�gu']
                     rs.Fields.Item('IdRachunkuDlaDyspozycji').Value=acsv['Id. rachunku dla dyspozycji']
                     rs.Fields.Item('IdRachunkuDlaFk').Value=acsv['Id. rachunku dla FK']
                     rs.Fields.Item('KlasaRachunku').Value=acsv['Klasa rachunku']
                     rs.Fields.Item('KodOperacji2').Value=acsv['Kod operacji 2']
                     rs.Fields.Item('KwotaOperacji').Value=acsv['Kwota operacji']
                     rs.Fields.Item('NazwaRachunku').Value=acsv['Nazwa rachunku']
                     rs.Fields.Item('Prowizje').Value=acsv['Prowizje']
                     rs.Fields.Item('SaldoKoncowe').Value=acsv['Saldo ko�cowe']
                     rs.Fields.Item('SaldoPoczatkowe').Value=acsv['Saldo pocz�tkowe']
                     rs.Fields.Item('Wplywy').Value=acsv['Wp�ywy']
                     rs.Fields.Item('Wyplywy').Value=acsv['Wyp�ywy']

                     if aidtransakcji:
                        awartoscwplaty=acsv['Kwota',mt_Double]
                        if awartoscwplaty>0.0:
                           asql="SELECT _OID,Kwota,PMKwotaZaplaty,PMDataZaplaty,PMBank,PMDataWplywu,PMStatusPlatnosci,IDTransakcji FROM %s WHERE IDTransakcji='%s'"%(self.stn_buforpreprocesora,aidtransakcji)
                           rs1=self.GetRS(asql)
                           if rs1.State!=self.adoconst.adStateClosed and not rs1.EOF and not rs1.BOF:
                              akwotazaplaty=float(ADOLibInit.GetRSValueAsStr(rs1,'PMKwotaZaplaty'))
                              rs1.Fields.Item('PMKwotaZaplaty').Value=akwotazaplaty+awartoscwplaty
                              rs1.Fields.Item('PMDataZaplaty').Value='20'+acsv['Data waluty']
                              rs1.Fields.Item('PMBank').Value=acsv['Bank']
                              rs1.Fields.Item('PMDataWplywu').Value='20'+acsv['Data ksi�g.']
                              rs1.Fields.Item('PMStatusPlatnosci').Value='K1'
                              rs1.Update()
                           else:
                              astatus='E2'
                           if rs1.State<>self.adoconst.adStateClosed:
                              rs1.Close()
                           rs1=None
                     rs.Fields.Item('Status').Value=astatus
                     rs.Update()
#                     aoid=rs.Fields.Item('_OID').Value
#                     aoid=aoid.encode('cp1250')
                  else:
                     self.ImportStatus.append('Powtorzona platnosc: '+acsv['Id. rachunku']+' '+acsv['Kwota']+' '+acsv['Referencje klienta']+' '+acsv['Wyci�g'])
                  if rs.State<>self.adoconst.adStateClosed:
                     rs.Close()
                  rs=None
               acsv.Next()
         finally:
            acsv.Close()
      finally:
         self.CloseConnection()
      return string.join(self.ImportStatus,'\n')
   def ProcessBankImportOstrow2006(self,afname):
#            
#         print acsv.Header
#      return 'OK!!! '+afname
      self.ImportStatus=['',]
      self.OpenConnection()
      try:
#         dwyciagi={}
         acsv=CSVImport.CSVImport(adelimiter=',',atextQualifier='"',ahasheader=0,aheaderline='"ID1","DataOperacji","Kwota","BANK1","BANK2","RachunekDocelowy","RachunekZrodlowy","Nadawca1","Nadawca2","ID3","Bank3","Tytulem1","Tytulem2","Tytulem3","Tytulem4","IDPozycji"\n')
         acsv.Open(afname)
         anrpozycji=1
         adatawyciagu='20'+afname[-10:-4]
         adatawyciagu=adatawyciagu[:4]+'-'+adatawyciagu[4:6]+'-'+adatawyciagu[-2:]
         adataksiegowania='20'+afname[-10:-4]
         adataksiegowania=adataksiegowania[:4]+'-'+adataksiegowania[4:6]+'-'+adataksiegowania[-2:]
         try:
            while not acsv.EOF:
               aRachunekDocelowy=string.replace(acsv['RachunekDocelowy'],' ','')
               self.ImportStatus.append(aRachunekDocelowy+' '+acsv['Kwota']+' '+acsv['RachunekZrodlowy']+' '+acsv['ID1'])
#               anrpozycji=dwyciagi.get(acsv['Wyci�g'],0)
#               anrpozycji=1+anrpozycji
#               dwyciagi[acsv['Wyci�g']]=anrpozycji
               asha=sha.new()
               for s in [acsv['ID1'],acsv['DataOperacji'],acsv['Kwota'],aRachunekDocelowy,acsv['RachunekZrodlowy'],acsv['Nadawca1'],acsv['Nadawca2'],acsv['Tytulem1'],acsv['Tytulem2'],acsv['Tytulem3'],acsv['Tytulem4'],acsv['IDPozycji']]: #str(anrpozycji),
                  asha.update(s)
               adigest=asha.hexdigest()
               asql="SELECT * FROM %s WHERE SumaKontrolna='%s'"%(self.stn_pozycjewyciagu,adigest)
               rs=self.GetRS(asql,aclient=1)
               astatus='I1'
               if rs.State!=self.adoconst.adStateClosed:
                  if rs.EOF or rs.BOF:
                     rs.AddNew()
#                     aRachunekDocelowy=acsv['RachunekDocelowy']
                     aidtransakcji=aRachunekDocelowy[11:14]+aRachunekDocelowy[-4:]
                     akwota=acsv['Kwota'][:-2]+'.'+acsv['Kwota'][-2:]
                     adataoperacji=acsv["DataOperacji"]
                     adataoperacji=adataoperacji[:4]+'-'+adataoperacji[4:6]+'-'+adataoperacji[-2:]
                     rs.Fields.Item('IDTransakcji').Value=aidtransakcji
                     rs.Fields.Item('PozycjaNaWyciagu').Value=anrpozycji
                     rs.Fields.Item('SumaKontrolna').Value=adigest
                     rs.Fields.Item('Bank').Value=aRachunekDocelowy
                     rs.Fields.Item('IdRachunku').Value=acsv["RachunekZrodlowy"]
                     rs.Fields.Item('Wyciag').Value=acsv["ID1"]
                     rs.Fields.Item('DataWaluty').Value=adataoperacji
                     rs.Fields.Item('DataKsiegowania').Value=adataksiegowania
                     rs.Fields.Item('Kwota').Value=akwota
                     s=acsv['Nadawca1']+acsv['Nadawca2']
                     rs.Fields.Item('Kontrahent').Value=s[:199]
                     atytulem=acsv["Tytulem1"]+acsv["Tytulem2"]+acsv["Tytulem3"]+acsv["Tytulem4"]
                     rs.Fields.Item('SzczegolyPlatnosci').Value=atytulem[:199]
                     rs.Fields.Item('IdRachunkuDlaDyspozycji').Value=acsv['IDPozycji']
#                     rs.Fields.Item('TrescOperacji').Value=acsv['Tre�� operacji'][:199]
#                     rs.Fields.Item('KodOperacji').Value=acsv['Kod operacji']
#                     rs.Fields.Item('ReferencjeKlienta').Value=acsv['Referencje klienta']
#                     rs.Fields.Item('KodStatystyczny').Value=acsv['Kod stat.']
#                     rs.Fields.Item('Storno').Value=acsv['Storno']
#                     rs.Fields.Item('Aktualizacja').Value='20'+acsv['Aktualizacja']
#                     rs.Fields.Item('DataWyciagu').Value='20'+acsv['Data  wyci�gu']
#                     rs.Fields.Item('IdRachunkuDlaFk').Value=acsv['Id. rachunku dla FK']
#                     rs.Fields.Item('KlasaRachunku').Value=acsv['Klasa rachunku']
#                     rs.Fields.Item('KodOperacji2').Value=acsv['Kod operacji 2']
#                     rs.Fields.Item('KwotaOperacji').Value=acsv['Kwota operacji']
#                     rs.Fields.Item('NazwaRachunku').Value=acsv['Nazwa rachunku']
#                     rs.Fields.Item('Prowizje').Value=acsv['Prowizje']
#                     rs.Fields.Item('SaldoKoncowe').Value=acsv['Saldo ko�cowe']
#                     rs.Fields.Item('SaldoPoczatkowe').Value=acsv['Saldo pocz�tkowe']
#                     rs.Fields.Item('Wplywy').Value=acsv['Wp�ywy']
#                     rs.Fields.Item('Wyplywy').Value=acsv['Wyp�ywy']
                     if aidtransakcji:
                        awartoscwplaty=float(akwota)
                        if awartoscwplaty>0.0:
#$$IDTRANSD
                           asql="SELECT TOP 1 _OID,Kwota,PMKwotaZaplaty,PMDataZaplaty,PMBank,PMDataWplywu,PMStatusPlatnosci,IDTransakcji FROM %s WHERE IDTransakcji='%s' ORDER BY DataWymagalnosci"%(self.stn_buforpreprocesora,aidtransakcji)
                           rs1=self.GetRS(asql)
                           if rs1.State!=self.adoconst.adStateClosed and not rs1.EOF and not rs1.BOF:
                              akwotazaplaty=float(ADOLibInit.GetRSValueAsStr(rs1,'PMKwotaZaplaty'))
                              rs1.Fields.Item('PMKwotaZaplaty').Value=akwotazaplaty+awartoscwplaty
                              rs1.Fields.Item('PMDataZaplaty').Value=adataoperacji
                              rs1.Fields.Item('PMBank').Value=aRachunekDocelowy
                              rs1.Fields.Item('PMDataWplywu').Value=adataksiegowania
                              rs1.Fields.Item('PMStatusPlatnosci').Value='K1'
                              rs1.Update()
                           else:
                              astatus='E2'
                           if rs1.State<>self.adoconst.adStateClosed:
                              rs1.Close()
                           rs1=None
                     rs.Fields.Item('Status').Value=astatus
                     rs.Update()
#                     aoid=rs.Fields.Item('_OID').Value
#                     aoid=aoid.encode('cp1250')
                  else:
                     self.ImportStatus.append('Powtorzona platnosc: '+aRachunekDocelowy+' '+acsv['Kwota']+' '+acsv['RachunekZrodlowy']+' '+acsv['ID1'])
                  if rs.State<>self.adoconst.adStateClosed:
                     rs.Close()
                  rs=None
               anrpozycji=1+anrpozycji
               acsv.Next()
         finally:
            acsv.Close()
      finally:
         self.CloseConnection()
      return string.join(self.ImportStatus,'\n')
   def ProcessBankImportTest(self,afname,ddd):
#            
#         print acsv.Header
      dwyciagi={}
      acsv=CSVImport.CSVImport(adelimiter=',',atextQualifier='"')
      acsv.Open(afname)
      try:
         while not acsv.EOF:
            anrpozycji=dwyciagi.get(acsv['Wyci�g'],0)
            anrpozycji=1+anrpozycji
            dwyciagi[acsv['Wyci�g']]=anrpozycji
            asha=sha.new() #str(anrpozycji),
            for s in [acsv['Bank'],acsv['Id. rachunku'],acsv['Wyci�g'],'20'+acsv['Data waluty'],acsv['Tre�� operacji'],acsv['Kod operacji'],acsv['Referencje klienta'],acsv['Kwota'],'20'+acsv['Data ksi�g.'],acsv['Kontrahent'],acsv['Kontrahent 2'],acsv['Kod stat.'],acsv['Id. rachunku dla dyspozycji'],acsv['Nazwa rachunku'],acsv['Szczeg�y p�atno�ci']]:
               asha.update(s)
            adigest=asha.hexdigest()
            if ddd.has_key(adigest):
               print acsv['Id. rachunku'],acsv['Kwota'],acsv['Referencje klienta']
            else:
               ddd[adigest]=1
            aacc2=self.IDTransakcji.get(acsv['Bank']+acsv['Id. rachunku'],'')
            if aacc2=='':
               astatus='E1'
            areferencje=acsv['Referencje klienta']
            aidtransakcji=''
            if areferencje=='NONREF':
               astatus='I2'
            elif areferencje=='':
               astatus='I3'
            else:
               aidtransakcji=areferencje+aacc2
            if aidtransakcji:
               awartoscwplaty=acsv['Kwota',mt_Double]
               if awartoscwplaty>0.0:
                  pass
            acsv.Next()
      finally:
         acsv.Close()
   def WprowadzPotwierdzeniaOdbioru(self,lret,file=None):
      self.OpenConnection()
      try:
         for adate,aid in lret:
            sdate=ICORUtil.tdate2fmtstr(adate,delimiter='-',longfmt=1)
            aid=aid[:-1]
#$$IDTRANSD
            asql2="""
   SELECT TOP 1
   _OID,IDTransakcji,PMDataOdbioruDecyzji,PMStatusAkceptacji
   FROM
   %s
   WHERE
   IDTransakcji='%s'
   ORDER BY DataWymagalnosci
"""%(self.stn_buforpreprocesora,aid)
            rs=self.GetRS(asql2)
            if rs.State!=self.adoconst.adStateClosed and not rs.EOF and not rs.BOF:
               rs.Fields.Item('PMDataOdbioruDecyzji').Value=sdate
               rs.Fields.Item('PMStatusAkceptacji').Value='A2'
               rs.Update()
               rs.Close()
            elif not file is None:
               file.write('<h3>Identyfikator [%s] nie jest zarejestrowany w SPM</h3>\n'%aid)
            rs=None
      finally:
         self.CloseConnection()
   def PobierzInformacjeOPotwierdzeniuOdbioru(self,aid):
      adatapotwierdzenia,astatusakceptacji='',''
      ret=[]
      aid=aid[:-1]
#$$IDTRANSD
      asql2="""
   SELECT TOP 1
   _OID,IDTransakcji,Platnik,PlatnikAdres,PMDataOdbioruDecyzji,PMStatusAkceptacji
   FROM
   %s
   WHERE
   IDTransakcji='%s'
   ORDER BY DataWymagalnosci
"""%(self.stn_buforpreprocesora,aid)
      rs=self.GetRS(asql2)
      if rs.State!=self.adoconst.adStateClosed and not rs.EOF and not rs.BOF:
         ret.append(ADOLibInit.GetRSValueAsStr(rs,'Platnik'))
         ret.append(ADOLibInit.GetRSValueAsStr(rs,'PlatnikAdres'))
         adatapotwierdzenia=ADOLibInit.GetRSValueAsStr(rs,'PMDataOdbioruDecyzji')
         astatusakceptacji=ADOLibInit.GetRSValueAsStr(rs,'PMStatusAkceptacji')
         rs.Close()
      rs=None
      return string.join(ret,'\n'),adatapotwierdzenia,astatusakceptacji
   def GetCheckSum(self,s1):
      awagi=[1,3,1,3,1,3,1,3,1,3,1,3,1]
      sum=0
      for i in range(len(s1)):
         sum=sum+awagi[i]*int(s1[i:i+1])
      sum=(10-sum%10)%10
      return s1+str(sum)
   def CheckTransID(self,s1):
      sum=self.GetCheckSum(s1[:-1])
      if sum[-1:]!=s1[-1:]:
         return 0
      return 1
   def GetPrzesylkaIDByPakiet(self,apakietname):
      asql="""select top 1 %s.KodPrzesylki, %s.Status from %s inner join %s on %s._OID=%s.Pula where opis='%s' and %s.Status='D2'"""%(self.stn_kodyprzesylek,self.stn_kodyprzesylek,self.stn_kodyprzesylek,self.stn_pulakodowprzesylek,self.stn_pulakodowprzesylek,self.stn_kodyprzesylek,apakietname,self.stn_kodyprzesylek,)
      rs1=self.GetRS(asql)
      akodprzesylki=''
      if not rs1.EOF and not rs1.BOF:
         akodprzesylki=ADOLibInit.GetRSValueAsStr(rs1,"KodPrzesylki")
      if rs1.State<>self.adoconst.adStateClosed:
         rs1.Close()
      if akodprzesylki:
         asql="""update %s set Status='W1'where KodPrzesylki='%s'"""%(self.stn_kodyprzesylek,akodprzesylki)
         self.ConnectionExecute(asql)
      return akodprzesylki
   def XMLImportSOKListy(self,afpath,adomyslnystatusprzesylki='K',adomyslnystatuslisty='K',adomyslnytrybdoreczenia='ZPO',anolist=0,anadawca='',awydzialmerytoryczny='',alistafilterfunc=None,aprzesylkafilterfunc=None):
      self.ImportStatus=[]
      adir,afname=os.path.split(afpath)
      afbasename,afext=os.path.splitext(afname)
      self.BaseName=afbasename
#      self.ArchiveDir=FilePathAsSystemPath(aobj.SciezkaArchiwum)
#      ahash,asize,alastline=AppUtil.GetPackageFileInfo(afpath)
#      self.RokObliczeniowyPaczki=aobj['RokObliczeniowy']
      self.ImportStatus.append('***********************************************************')
#      self.ImportStatus.append('Import paczki dla aplikacji: '+aobj.Aplikacja+' / '+aobj.RokObliczeniowy)
#      self.ImportStatus.append('  Plik: '+afname+' Rozmiar: '+str(asize)+' Suma kontrolna: '+ahash)
      self.ImportStatus.append('  Plik: '+afname)
#      if not alastline or ahash=='':
#         self.ImportStatus.append('  Plik jest uszkodzony, b�d� nie zamkni�ty')
#         try:
#            self.SendMail('process package',self.ImportStatus)
#         except:
#            self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
#         return string.join(self.ImportStatus,'\n')
      self.OpenConnection()
      try:
#         asql="select * from %s where SumaKontrolna='%s'"%(self.stn_rejestrpaczek,ahash)
#         wexists=0
#         rs=self.GetRS(asql)
#         if rs.State!=self.adoconst.adStateClosed:
#            if not rs.EOF and not rs.BOF:
#               wexists=1
#               self.ImportStatus.append('  Paczka zosta�a ju� wcze�niej zarejestrowana.')
#         if not wexists:
         if 1:
#            rs.AddNew()
#            rs.Fields.Item('Status').Value=1
#            rs.Fields.Item('NazwaPaczki').Value=afbasename
#            rs.Fields.Item('SumaKontrolna').Value=ahash
#            rs.Fields.Item('RozmiarPliku').Value=asize
#            self.ImportStatus.append('  Pocz�tek rejestracji paczki: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
            t1=time.time()
#            aparser=AppPaymentsParser.PaymentsParser()
#            aerror=0
#            try:
#               aparser.ParseFile(self,afpath,rs,acheckonly=1,ret=self.ImportStatus)
#               self.ImportStatus.append('  Paczka sprawdzona, pocz�tek importu: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
#               rs.Update()
#               self.OIDPaczki=ADOLibInit.GetRSValueAsStr(rs,"_OID")
#               rs.Close()
#               asql="select * from %s where _OID='%s'"%(self.stn_rejestrpaczek,self.OIDPaczki)
#               rs=self.GetRS(asql)
#            except:
#               aparser.IsGood=0
#               aerror=1
#               self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
#            if aparser.IsGood:
            if 1:
               self.ImportStatus.append('  pocz�tek dodawania: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
#               amaxpayments=aparser.PaymentsCnt
#               aparser=AppPaymentsParser.PaymentsParser()
#               aparser.MaxPayments=amaxpayments
               aparser=XMLParserWydruku.ICORSOKPrzesylkiParser()
               try:
                  aparser.ParseFile(self,afpath,ret=self.ImportStatus,acompressed=0,adomyslnystatusprzesylki=adomyslnystatusprzesylki,adomyslnystatuslisty=adomyslnystatuslisty,adomyslnytrybdoreczenia=adomyslnytrybdoreczenia,anolist=anolist,anadawca=anadawca,awydzialmerytoryczny=awydzialmerytoryczny,alistafilterfunc=alistafilterfunc,aprzesylkafilterfunc=aprzesylkafilterfunc)
               except:
                  aerror=1
                  self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
#               if aerror:
#                  self.ImportStatus.append('  Zaimportowano cz�� przesylek: '+str(aparser.PaymentsCnt))
#               else:
#                  self.ImportStatus.append('  Zaimportowano p�atno�ci: '+str(aparser.PaymentsCnt))
#               if aparser.PaymentsExisting:
#                  self.ImportStatus.append('  Ilo�� ju� istniej�cych p�atno�ci: '+str(aparser.PaymentsExisting))
            t2=time.time()
#            if not aerror:
#               os.rename(afpath,adir+'/archiwum/'+afname)
#               try:
#                  rs.Fields.Item('CzasImportu').Value=int(t2-t1)
#                  if not aerror:
#                     rs.Fields.Item('Status').Value=5 # OK
#                  else:
#                     rs.Fields.Item('Status').Value=4 # Error
#                  rs.Update()
#                  rs.Close()
#               except:
#                  self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
            self.ImportStatus.append('  Koniec rejestracji paczki: '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime()))
      finally:
         try:
            self.CloseConnection()
         except:
            self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
#      try:
#         self.SendMail('process package',self.ImportStatus)
#      except:
#         self.ImportStatus.extend(ICORUtil.GetLastExceptionInfo())
      InfoStatus('')
      import win32api
      try:
         win32api.Beep(4000,150)
         win32api.Beep(2000,100)
      except:
         pass
      return string.join(self.ImportStatus,'\n')
   def GetKID(self,kcnt=1,apoid=''):
      amaxcnt=0
      aconnectionopened=1
      if self.connection is None:
         aconnectionopened=0
         self.OpenConnection()
      try:
         ret=[]
         while 1:
            if apoid:
               asql="select top %d _OID,KodPrzesylki,Status,Pula from %s where Status='G1' or Pula='%s' order by Pula desc"%(kcnt,self.stn_kodyprzesylek,apoid)
            else:
               asql="select top %d _OID,KodPrzesylki,Status,Pula from %s where Status='G1'"%(kcnt,self.stn_kodyprzesylek)
            rs=self.GetRS(asql)
            rcnt=rs.RecordCount
            if rcnt>=kcnt:
               break
            amax=1+(kcnt+20-rcnt)/10
            for i in range(amax):
               w=1
               while w:
                  l=[]
                  for j in range(10):
                     akod=self.GetCheckSum('1%06d%06d'%(random.randrange(0,1000000),random.randrange(0,1000000)))
                     l.append(akod)
                  asql="select top 1 _OID,KodPrzesylki,Status from %s where KodPrzesylki in (%s)"%(self.stn_kodyprzesylek,str(l)[1:-1])
                  rs1=self.GetRS(asql)
                  if rs1.EOF or rs1.BOF:
                     w=0
                  if rs1.State<>self.adoconst.adStateClosed:
                     rs1.Close()
               for akod in l:
                  rs.AddNew()
                  rs.Fields.Item('KodPrzesylki').Value=akod
                  rs.Fields.Item('Status').Value='G1'
            self.UpdateRS(rs)
         rs.MoveFirst()
         while not rs.EOF and not rs.BOF:
            akod=ADOLibInit.GetRSValueAsStr(rs,"KodPrzesylki")
            ret.append(akod)
            rs.MoveNext()
         if rs.State<>self.adoconst.adStateClosed:
            rs.Close()        
      finally:
         if not aconnectionopened:
            self.CloseConnection()
      return ret

ICORUtil.ExtendClass(MassPaymentsServer,AppSigid.MassPaymentsServer,AppWieczysci.MassPaymentsServer,AppWSp.MassPaymentsServer,AppSRolny.MassPaymentsServer,AppRadix.MassPaymentsServer)


