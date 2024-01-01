# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import os
import re
import sys
import string
import cStringIO
import sha

from spmprint import pmwydruki
#from spmprint import pmwydruksigid
from spmprint import pmwydrukradix
from spmprint import pmwydrukiconst

class ICORPMPrintPrzesylkiParser(XMLUtil.ICORBaseXMLParser):
   def ParseFile(self,afpath,aodbiorca=None,dformcodes=None,alastidtransakcji='',akorektax=0,akorektay=0):
      if aodbiorca is None:
         aodbiorca=['','','']
      if dformcodes is None:
         dformcodes={}       
      self.odbiorca=aodbiorca
      self.dformcodes=dformcodes
      self.wchangeskip=0
      self.skipforms=0
      self.lastidtransakcji=''
      if alastidtransakcji:
         self.lastidtransakcji=alastidtransakcji
         self.skipforms=1

      self.wydruk=pmwydruki.Wydruk(akorektax=akorektax,akorektay=akorektay)
      self.LISTA_attrs={}
      self.LISTA_adresy={}
      self.IDListy=''
      self.DataUtworzeniaWydruku=''
      self.AutorWydruku=''
      self.formularzcnt=0

      self.pakietcnt=1
      self.reset()
      amsize=os.path.getsize(afpath)
      self.ProgressEstimator=ICORUtil.TimeProgressEstimator(amsize)
      aasize=0
      fout=open(afpath,'rb')
      self.stopparsing=0
      try:
         while not self.stopparsing:
            v=fout.read(8192)
            aasize=aasize+len(v)
            self.Elapsed,self.Estimated,self.Remaining=self.ProgressEstimator.SetProgress(aasize)
            print '%d %s %s %s'%(amsize-aasize,self.Elapsed,self.Estimated,self.Remaining),'                         \r',
            if len(v)<=0:
               break
            self.feed(v)
      finally:
         fout.close()
      self.Rysuj()
   def IncLicznik(self):
      self.formularzcnt=1+self.formularzcnt
      if self.formularzcnt>0:
         self.stopparsing=1
   def Rysuj(self):
      self.wydruk.Rysuj()
   def Save(self,afname):
      self.wydruk.Save(afname)
   def Print(self,aprinter='',aejectpages=0):
      self.wydruk.Print(aprinter,aejectpages=aejectpages)
   def start_PMWYDRUKI(self,attrs):
      #< wersja="1.0.1">
      pass
   def end_PMWYDRUKI(self):
      pass
   def start_NAGLOWEK(self,attrs):
      pass
   def end_NAGLOWEK(self):
      pass
   def start_DANE(self,attrs):
      if attrs['nazwa']=="DataUtworzenia":
         self.DataUtworzeniaWydruku=attrs['wartosc']
      if attrs['nazwa']=="Autor":
         self.AutorWydruku=attrs['wartosc']
   def end_DANE(self):
      pass
   def start_PAKIETY(self,attrs):
      if self.stopparsing:
         return
   def end_PAKIETY(self):
      if self.stopparsing:
         return
   def start_LISTA(self,attrs):
      self.pakietcnt=1
      if self.stopparsing:
         return
      self.LISTA_attrs=attrs
      self.LISTA_adresy={}
      self.IDListy=''
   def end_LISTA(self):
      if self.stopparsing:
         return
      acode=self.dformcodes.get('um-lista-1','')
      if len(self.LISTA_adresy.keys()):
         bformularz=pmwydrukradix.F_RADIX_Lista(self.IDListy,self.LISTA_attrs,self.LISTA_adresy,acode=acode)
         if not self.skipforms:
            self.wydruk.DodajFormularz(bformularz)
#      self.IncLicznik()
   def start_PAKIET(self,attrs):
      if self.stopparsing:
         return
#kodprzesylki="0"
#nrkolejny="1"
      self.PAKIET_attrs=attrs
   def end_PAKIET(self):
      self.pakietcnt=1+self.pakietcnt
      if self.wchangeskip:
         self.wchangeskip=0
         self.skipforms=0
      if self.stopparsing:
         return
   def start_FORMULARZ(self,attrs):
      if self.stopparsing:
         return
      self.FORMULARZ_idformularza=attrs.get('idformularza','')
      self.FORMULARZ_pola={}
   def end_FORMULARZ(self):
      if self.stopparsing:
         return
#      print
#      print 'formularz:',self.FORMULARZ_idformularza,self.PAKIET_attrs.get('kodprzesylki',''),self.PAKIET_attrs.get('nrkolejny','')
      acode=self.dformcodes.get(self.FORMULARZ_idformularza,'')
#      print 'id form:',self.FORMULARZ_idformularza,acode
      if self.FORMULARZ_idformularza=='um-czysty-1':
         if len(self.FORMULARZ_pola.get('TrescDecyzji',''))>10:
            bformularz=pmwydrukradix.F_RADIX_Decyzja(self.FORMULARZ_pola,acode=acode)
            if not self.skipforms:
               self.wydruk.DodajFormularz(bformularz)
      elif self.FORMULARZ_idformularza=='um-przelew-2':
         bformularz=pmwydrukradix.F_RADIX_Nr1(self.FORMULARZ_pola,acode=acode,aodbiorca=self.odbiorca)
         if not self.skipforms:
            self.wydruk.DodajFormularz(bformularz)
      elif self.FORMULARZ_idformularza=='um-przelew-3':
         bformularz=pmwydrukradix.F_RADIX_Nr1(self.FORMULARZ_pola,acode=acode,aodbiorca=self.odbiorca)
         if not self.skipforms:
            self.wydruk.DodajFormularz(bformularz)
   def start_POLE(self,attrs):
      if self.stopparsing:
         return
      self.FORMULARZ_pola[attrs.get('nazwa','')]=attrs.get('wartosc','')
      if not self.IDListy and attrs.get('nazwa','')=='IDTransakcji':
         self.IDListy=attrs.get('wartosc','')
      if attrs.get('nazwa','') in ["IDPlatnika","Platnik","IDTransakcji","PlatnikAdres"]:
         self.LISTA_adresy[attrs.get('nazwa','')+'_'+str(self.pakietcnt)]=attrs.get('wartosc','')

      if self.lastidtransakcji:
         if attrs.get('nazwa','') in ["IDTransakcji","IDTransakcji_1","IDTransakcji_2"]:
            if self.lastidtransakcji==attrs.get('wartosc',''):
               self.wchangeskip=1

   def end_POLE(self):
      if self.stopparsing:
         return




