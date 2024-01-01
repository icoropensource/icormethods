# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import icordbmain.adoutil as ADOLibInit
import os
import re
import sys
import string
import cStringIO
import sha

class ICORProfficeParser(XMLUtil.ICORBaseXMLParser):
   def ParseFile(self,apaymentsserver,afpath):
      self.PaymentsServer=apaymentsserver
      self.adolib=self.PaymentsServer.adolib
      self.adoconst=self.PaymentsServer.adoconst
      self.IsGood=1
      self.reset()
      self.asha=sha.new()
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
            InfoStatus('%d %s %s %s'%(amsize-aasize,self.Elapsed,self.Estimated,self.Remaining))
            if len(v)<=0:
               break
            self.feed(v)
      finally:
         fout.close()
      InfoStatus('')
      SetProgress(0,0)
   def start_DANE(self,attrs):
      attrs=self.Attrs_UTF8_To_CP1250(attrs)
#      self.ElementInfo()
      lattr=['xmlns:xsi','xsi:noNamespaceSchemaLocation','datagenerowania','czasgenerowania']
      self.DataGenerowania=attrs.get('datagenerowania','')
      self.CzasGenerowania=attrs.get('czasgenerowania','')
   def end_DANE(self):
      pass
   def start_TRANSAKCJE(self,attrs):
      attrs=self.Attrs_UTF8_To_CP1250(attrs)
#      self.ElementInfo()
      lattr=['nrrachunku','nrrachunkumaski','datawyciagu','waluta','liczbaoperacji','obrot',]
      self.NrRachunku=attrs.get('nrrachunku','')
      self.NrRachunkuMaski=attrs.get('nrrachunkumaski','')
      self.DataWyciagu=attrs.get('datawyciagu','')
      self.Waluta=attrs.get('waluta','')
      self.LiczbaOperacji=attrs.get('liczbaoperacji','')
      self.LiczbaOperacjiCnt=0
      self.Obrot=attrs.get('obrot','')
   def end_TRANSAKCJE(self):
      pass
   def XMLDate2SQLDate(self,adate):
      return adate[:4]+'-'+adate[4:6]+'-'+adate[6:]
   def start_OPERACJA(self,attrs):
      attrs=self.Attrs_UTF8_To_CP1250(attrs)
#      self.ElementInfo()
      lattr=[
'id',
'kodwewn',
   'nrrachunkuplatnika',
'kwota',
'dataksiegowania',
'datawplaty',
   'wplacajacy1',
   'wplacajacy2',
   'wplacajacy3',
   'wplacajacy4',
'numerbanku',
'kodnrb',
'rozszerznrrachunku',
   'ktr',
   'szczegolyplatnosci1',
   'szczegolyplatnosci2',
   'szczegolyplatnosci3',
   'szczegolyplatnosci4',
'numerunikalny',
'numerbankuwplaty',
'rachunekwirtualny',
]
      self.PaymentsServer.ImportStatus.append(attrs['rachunekwirtualny']+' '+attrs['kwota']+' '+attrs['rozszerznrrachunku']+' '+self.DataWyciagu)
#         asha=sha.new()
#         for s in [acsv['Bank'],acsv['Id. rachunku'],acsv['Wyciąg'],'20'+acsv['Data waluty'],acsv['Treść operacji'],acsv['Kod operacji'],acsv['Referencje klienta'],acsv['Kwota'],'20'+acsv['Data księg.'],acsv['Kontrahent'],acsv['Kontrahent 2'],acsv['Kod stat.'],acsv['Id. rachunku dla dyspozycji'],acsv['Nazwa rachunku'],acsv['Szczegóły płatności']]: #str(anrpozycji),
#            asha.update(s)
#         adigest=asha.hexdigest()
      adigest=attrs['numerunikalny']
      asql="SELECT * FROM %s WHERE SumaKontrolna='%s'"%(self.PaymentsServer.stn_pozycjewyciagu,adigest)
      rs=self.PaymentsServer.GetRS(asql,aclient=1)
      astatus='I1'
      if rs.State!=self.adoconst.adStateClosed:
         if rs.EOF or rs.BOF:
            rs.AddNew()
            aidtransakcji=attrs['rozszerznrrachunku']
            rs.Fields.Item('IDTransakcji').Value=aidtransakcji
            rs.Fields.Item('PozycjaNaWyciagu').Value=attrs['id']
            rs.Fields.Item('SumaKontrolna').Value=adigest
            rs.Fields.Item('Bank').Value=attrs['numerbankuwplaty']
            rs.Fields.Item('IdRachunku').Value=self.NrRachunku
            rs.Fields.Item('Wyciag').Value=self.DataWyciagu #acsv['Wyciąg']
            rs.Fields.Item('DataWaluty').Value=self.XMLDate2SQLDate(attrs['datawplaty'])
            rs.Fields.Item('SzczegolyPlatnosci').Value=(attrs.get('szczegolyplatnosci1','')+attrs.get('szczegolyplatnosci2','')+attrs.get('szczegolyplatnosci3','')+attrs.get('szczegolyplatnosci4',''))[:199]
#            rs.Fields.Item('TrescOperacji').Value=''
            rs.Fields.Item('KodOperacji').Value=attrs['kodwewn']
            rs.Fields.Item('ReferencjeKlienta').Value=aidtransakcji[:7]
            rs.Fields.Item('Kwota').Value=attrs['kwota']
            rs.Fields.Item('DataKsiegowania').Value=self.XMLDate2SQLDate(attrs['dataksiegowania'])
            rs.Fields.Item('Kontrahent').Value=string.strip(attrs.get('wplacajacy1','')+' '+attrs.get('wplacajacy2','')+' '+attrs.get('wplacajacy3','')+' '+attrs.get('wplacajacy4',''))[:199]
#            rs.Fields.Item('KodStatystyczny').Value=''
#            rs.Fields.Item('Storno').Value=''
#            rs.Fields.Item('Aktualizacja').Value=''
            rs.Fields.Item('DataWyciagu').Value=self.XMLDate2SQLDate(self.DataWyciagu)
            rs.Fields.Item('IdRachunkuDlaDyspozycji').Value=attrs.get('nrrachunkuplatnika','')
#            rs.Fields.Item('IdRachunkuDlaFk').Value=''
#            rs.Fields.Item('KlasaRachunku').Value=''
#            rs.Fields.Item('KodOperacji2').Value=''
#            rs.Fields.Item('KwotaOperacji').Value=''
            rs.Fields.Item('NazwaRachunku').Value=attrs['rachunekwirtualny']
#            rs.Fields.Item('Prowizje').Value=''
            rs.Fields.Item('SaldoKoncowe').Value=self.Obrot
#            rs.Fields.Item('SaldoPoczatkowe').Value=''
#            rs.Fields.Item('Wplywy').Value=''
#            rs.Fields.Item('Wyplywy').Value=''

            awartoscwplaty=float(attrs['kwota'])
            if awartoscwplaty>0.0:
#$$IDTRANSD
               asql="SELECT TOP 1 _OID,Kwota,PMKwotaZaplaty,PMDataZaplaty,PMBank,PMDataWplywu,PMStatusPlatnosci,IDTransakcji FROM %s WHERE IDTransakcji='%s' ORDER BY DataWymagalnosci"%(self.PaymentsServer.stn_buforpreprocesora,aidtransakcji)
               rs1=self.PaymentsServer.GetRS(asql)
               if rs1.State!=self.adoconst.adStateClosed and not rs1.EOF and not rs1.BOF:
                  akwotazaplaty=float(ADOLibInit.GetRSValueAsStr(rs1,'PMKwotaZaplaty'))
                  rs1.Fields.Item('PMKwotaZaplaty').Value=akwotazaplaty+awartoscwplaty
                  rs1.Fields.Item('PMDataZaplaty').Value=self.XMLDate2SQLDate(attrs['datawplaty'])
                  rs1.Fields.Item('PMBank').Value=attrs['numerbankuwplaty']
                  rs1.Fields.Item('PMDataWplywu').Value=self.XMLDate2SQLDate(attrs['dataksiegowania'])
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
            self.PaymentsServer.ImportStatus.append('Powtorzona platnosc: '+attrs['rachunekwirtualny']+' '+attrs['kwota']+' '+attrs['rozszerznrrachunku']+' '+self.DataWyciagu)
      if rs.State<>self.adoconst.adStateClosed:
         rs.Close()
      rs=None
   def end_OPERACJA(self):
      pass
   def start_KONTROLA(self,attrs):
#      self.ElementInfo()
      self.TagData=''
   def end_KONTROLA(self):
      pass




