# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import random

osobowemajatkowe=[
   'Bankowe Towarzystwo Ubezpieczeń i Reasekuracji HEROS S.A.',
   'COMMERCIAL UNION Polska - Towarzystwo Ubezpieczeń Ogólnych S.A.',
   'DAEWOO Towarzystwo Ubezpieczeniowe S.A.',
   'GERLING POLSKA Towarzystwo Ubezpieczeń S.A.',
   'Generali T.U. S.A.',
   'Korporacja Ubezpieczeniowa FILAR SA',
   'Korporacja Ubezpieczeń Kredytów Eksportowych SA',
   'Powszechne Towarzystwo Ubezpieczeniowe ENERGO-ASEKURACJA S.A.',
   'Powszechny Zakład Ubezpieczeń S.A.',
   'Sampo Towarzystwo Ubezpieczeń S.A.',
   'Sopockie Towarzystwo Ubezpieczeniowe Ergo HESTIA S.A.',
   'TU ALLIANZ Polska SA',
   'TUwRiGŻ AGROPOLISA SA',
   'Towarzystwo Ubezpieczeniowe COMPENSA S.A.',
   'Towarzystwo Ubezpieczeniowe EUROPA S.A.',
   'Towarzystwo Ubezpieczeniowe Inter Polska S.A.',
   'Towarzystwo Ubezpieczeniowe PBK S.A.',
   'Towarzystwo Ubezpieczeniowe SAMOPOMOC S.A.',
   'Towarzystwo Ubezpieczeń Polski Związek Motorowy S.A.',
   'Towarzystwo Ubezpieczeń i Reasekuracji CIGNA STU S.A.',
   'Towarzystwo Ubezpieczeń i Reasekuracji PARTNER S.A.',
   'Towarzystwo Ubezpieczeń i Reasekuracji WARTA S.A.',
   'ZURICH TU SA',
   'Zakład Ubezpieczeń i Reasekuracji POLONIA S.A.',
   ]

nazycie=[
   'CIGNA S.A.',
   'COMMERCIAL UNION Polska - Towarzystwo Ubezpieczeń na Życie S.A.',
   'DAEWOO-ŻYCIE Towarzystwo Ubezpieczeniowe S.A.',
   'FIAT Ubezpieczenia Życiowe S.A.',
   'GERLING POLSKA Towarzystwo Ubezpieczeń na Życie S.A.',
   'Generali Życie TU S.A.',
   'Korporacja Ubezpieczeniowa FILAR-ŻYCIE SA',
   'Metropolitan Life Ubezpieczenia na Życie S.A.',
   'NATIONWIDE Towarzystwo Ubezpieczeń na Życie S.A.',
   'Nationale-Nederlanden Employee Benefits Polska SA',
   'Nordea Polska Towarzystwo Ubezpieczeń na Życie',
   'PAPTUnŻiR AMPLICO - LIFE SA',
   'Powszechny Zakład Ubezpieczeń na Życie S.A.',
   'Prumerica Towarzystwo Ubezpieczeń na Życie S.A.',
   'SKANDIA ŻYCIE S.A.',
   'Sopockie Towarzystwo Ubezpieczeniowe na Życie Ergo HESTIA S.A.',
   'TU ALLIANZ Życie Polska SA',
   'Towarzystwo Ubezpieczeniowe "SAMOPOMOC ŻYCIE" S.A.',
   'Towarzystwo Ubezpieczeniowe COMPENSA ŻYCIE S.A.',
   'Towarzystwo Ubezpieczeniowe Winterthur Życie S.A.',
   'Towarzystwo Ubezpieczeń GARDA LIFE S.A.',
   'Towarzystwo Ubezpieczeń na Życie CARDIF Polska S.A.',
   'Towarzystwo Ubezpieczeń na Życie INTER-ŻYCIE Polska S.A.',
   'Towarzystwo Ubezpieczeń na Życie NATIONALE-NEDERLANDEN Polska S.A.',
   'Towarzystwo Ubezpieczeń na Życie POLISA-ŻYCIE S.A.',
   'Towarzystwo Ubezpieczeń na Życie ROYAL PBK S.A.',
   'Towarzystwo Ubezpieczeń na Życie Vienna Life S.A.',
   'Towarzystwo Ubezpieczeń na Życie WARTA VITA S.A.',
   'WÜSTENROT ŻYCIE Towarzystwo Ubezpieczeniowe S.A.',
   'ZURICH TU na Życie SA',
   'Zakład Ubezpieczeń i Reasekuracji POLONIA-ŻYCIE S.A.',
   ]

class Ubezpieczyciele:
   def __init__(self):
      self._OsoboweMajatkowe=osobowemajatkowe
      self._NaZycie=nazycie
   def __getattr__(self,name):
      if name=='OsoboweMajatkowe':
         return self._OsoboweMajatkowe[random.randint(0,len(self._OsoboweMajatkowe)-1)]
      if name=='NaZycie':
         return self._NaZycie[random.randint(0,len(self._NaZycie)-1)]

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aubezpieczyciele=Ubezpieczyciele()
   print '*** Osobowe, majatkowe: ***'
   for i in range(15):
      print aubezpieczyciele.OsoboweMajatkowe
   print '*** Na życie: ***'
   for i in range(15):
      print aubezpieczyciele.NaZycie
   return



