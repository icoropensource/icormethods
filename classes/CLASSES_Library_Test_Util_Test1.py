# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_Test_Util_DaneOsobowe as DaneOsobowe
import CLASSES_Library_Test_Util_Adresy as Adresy

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   adaneosobowe=DaneOsobowe.DaneOsobowe(aplec=-1)
   aadresy=Adresy.Adresy()
   for i in range(20):
      adaneosobowe.Init()
      #print adaneosobowe.Imie,adaneosobowe.Nazwisko,adaneosobowe.PlecKM,adaneosobowe.DataUrodzenia,ICORUtil.GetRandomPassword(8),adaneosobowe.PESEL,adaneosobowe.EMail,adaneosobowe.Telefon,aadresy.Ulica,aadresy.Numer,aadresy.Lokal
      print '|'.join([adaneosobowe.Imie,adaneosobowe.Nazwisko,adaneosobowe.Login,adaneosobowe.DataUrodzenia,ICORUtil.GetRandomPassword(8),adaneosobowe.PESEL,adaneosobowe.EMail,adaneosobowe.Telefon])
   return


