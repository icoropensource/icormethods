# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import random

osobowemajatkowe=[
   'Bankowe Towarzystwo Ubezpiecze� i Reasekuracji HEROS S.A.',
   'COMMERCIAL UNION Polska - Towarzystwo Ubezpiecze� Og�lnych S.A.',
   'DAEWOO Towarzystwo Ubezpieczeniowe S.A.',
   'GERLING POLSKA Towarzystwo Ubezpiecze� S.A.',
   'Generali T.U. S.A.',
   'Korporacja Ubezpieczeniowa FILAR SA',
   'Korporacja Ubezpiecze� Kredyt�w Eksportowych SA',
   'Powszechne Towarzystwo Ubezpieczeniowe ENERGO-ASEKURACJA S.A.',
   'Powszechny Zak�ad Ubezpiecze� S.A.',
   'Sampo Towarzystwo Ubezpiecze� S.A.',
   'Sopockie Towarzystwo Ubezpieczeniowe Ergo HESTIA S.A.',
   'TU ALLIANZ Polska SA',
   'TUwRiG� AGROPOLISA SA',
   'Towarzystwo Ubezpieczeniowe COMPENSA S.A.',
   'Towarzystwo Ubezpieczeniowe EUROPA S.A.',
   'Towarzystwo Ubezpieczeniowe Inter Polska S.A.',
   'Towarzystwo Ubezpieczeniowe PBK S.A.',
   'Towarzystwo Ubezpieczeniowe SAMOPOMOC S.A.',
   'Towarzystwo Ubezpiecze� Polski Zwi�zek Motorowy S.A.',
   'Towarzystwo Ubezpiecze� i Reasekuracji CIGNA STU S.A.',
   'Towarzystwo Ubezpiecze� i Reasekuracji PARTNER S.A.',
   'Towarzystwo Ubezpiecze� i Reasekuracji WARTA S.A.',
   'ZURICH TU SA',
   'Zak�ad Ubezpiecze� i Reasekuracji POLONIA S.A.',
   ]

nazycie=[
   'CIGNA S.A.',
   'COMMERCIAL UNION Polska - Towarzystwo Ubezpiecze� na �ycie S.A.',
   'DAEWOO-�YCIE Towarzystwo Ubezpieczeniowe S.A.',
   'FIAT Ubezpieczenia �yciowe S.A.',
   'GERLING POLSKA Towarzystwo Ubezpiecze� na �ycie S.A.',
   'Generali �ycie TU S.A.',
   'Korporacja Ubezpieczeniowa FILAR-�YCIE SA',
   'Metropolitan Life Ubezpieczenia na �ycie S.A.',
   'NATIONWIDE Towarzystwo Ubezpiecze� na �ycie S.A.',
   'Nationale-Nederlanden Employee Benefits Polska SA',
   'Nordea Polska Towarzystwo Ubezpiecze� na �ycie',
   'PAPTUn�iR AMPLICO - LIFE SA',
   'Powszechny Zak�ad Ubezpiecze� na �ycie S.A.',
   'Prumerica Towarzystwo Ubezpiecze� na �ycie S.A.',
   'SKANDIA �YCIE S.A.',
   'Sopockie Towarzystwo Ubezpieczeniowe na �ycie Ergo HESTIA S.A.',
   'TU ALLIANZ �ycie Polska SA',
   'Towarzystwo Ubezpieczeniowe "SAMOPOMOC �YCIE" S.A.',
   'Towarzystwo Ubezpieczeniowe COMPENSA �YCIE S.A.',
   'Towarzystwo Ubezpieczeniowe Winterthur �ycie S.A.',
   'Towarzystwo Ubezpiecze� GARDA LIFE S.A.',
   'Towarzystwo Ubezpiecze� na �ycie CARDIF Polska S.A.',
   'Towarzystwo Ubezpiecze� na �ycie INTER-�YCIE Polska S.A.',
   'Towarzystwo Ubezpiecze� na �ycie NATIONALE-NEDERLANDEN Polska S.A.',
   'Towarzystwo Ubezpiecze� na �ycie POLISA-�YCIE S.A.',
   'Towarzystwo Ubezpiecze� na �ycie ROYAL PBK S.A.',
   'Towarzystwo Ubezpiecze� na �ycie Vienna Life S.A.',
   'Towarzystwo Ubezpiecze� na �ycie WARTA VITA S.A.',
   'W�STENROT �YCIE Towarzystwo Ubezpieczeniowe S.A.',
   'ZURICH TU na �ycie SA',
   'Zak�ad Ubezpiecze� i Reasekuracji POLONIA-�YCIE S.A.',
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
   print '*** Na �ycie: ***'
   for i in range(15):
      print aubezpieczyciele.NaZycie
   return



