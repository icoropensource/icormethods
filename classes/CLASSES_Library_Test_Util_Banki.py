# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import random

banki={
   'Pekao SA':15,
   'PKO BP':18,
   'Bank Śląski':12,
   'WBK / BZ':10,
   'BPH':10,
   'PBK':2,
   'BWR':1,
   'BIG BG':7,
   'Kredyt Bank':4,
   'BRE':8,
   'BGŻ':7,
   'BOŚ':1,
   'Handlobank':1,
   'Invest Bank':2,
   'Raiffeisen':2,
   }

karty={
   'American Express':4,
   'Diners Club':6,
   'Eurocard/MasterCard':17,
   'Maestro':12,
   'Cirrus':2,
   'PKO Express':1,
   'PolCard':2,
   'PolCard Bis':1,
   'PolCard Tempo':1,
   'Sezam':1,
   'SkokCard':2,
   'Visa':20,
   'Visa Electron':30,
   'PLUS':1,
   }

class Banki:
   def __init__(self):
      self.Banki=banki
      self.Karty=karty
      self._Banki=[]
      for akey,avalue in banki.items():
         tl=[akey,]*avalue
         self._Banki.extend(tl)
      self._Karty=[]
      for akey,avalue in karty.items():
         tl=[akey,]*avalue
         self._Karty.extend(tl)
   def __getattr__(self,name):
      if name=='Bank':
         return self._Banki[random.randint(0,len(self._Banki)-1)]
      if name=='Karta':
         return self._Karty[random.randint(0,len(self._Karty)-1)]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   abanki=Banki()
   for i in range(15):
      print abanki.Bank,abanki.Karta
   return



