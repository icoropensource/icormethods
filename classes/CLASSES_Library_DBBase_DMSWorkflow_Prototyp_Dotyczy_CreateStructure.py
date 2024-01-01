# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import str2ProperID
import string
import re

def Test1(aclass):
   aoid=aclass.AddObject()
   aobj=aclass[aoid]
   aobj.NazwaObiektu='aaaa'
   aobj.Pola.AddRefs(aoid,[[poid1,pcid],[poid2,pcid]],aobj.Pola.ClassOfType.Nazwa,)
#   aclass.Dotyczy

def CreateStruktureFromList(CID=-1,aoid=-1,aGroup='',aTableName='',aPrettyTableName='',aFieldList='',aPrettyNamesList=''):
   if aTableName=='':
      return
   POID=3 #UMSkarbnik
   aclassproject=aICORDBEngine.Classes[1747]
   aclassDotyczy=aICORDBEngine.Classes[CID]
   atabindex=10
   if aoid<0:
      TOID=aclassDotyczy.AddObject()
      aclassDotyczy.Nazwa[TOID]=aPrettyTableName
      aclassDotyczy.NazwaTabeli[TOID]=aTableName
      aclassDotyczy.Grupa[TOID]=aGroup
      aclassDotyczy.NazwaObiektu[TOID]='1 obiekt'
      aclassDotyczy.Projekt[TOID]='%d:1747:'%POID
   else:
      TOID=aoid
      tobj=aclassDotyczy[TOID]
      pobj=tobj.Pola
      while pobj:
         ptid=pobj.Class.SGTabIndex.ValuesAsInt(pobj.OID)
         if ptid>=atabindex:
            atabindex=ptid+10
         pobj.Next()
   if aFieldList=='':
      return
   if aPrettyNamesList=='':
      aPrettyNamesList=aFieldList
   ListaNazw=string.split(aFieldList, ';')
   ListaAliasow=string.split(aPrettyNamesList, ';')
   aclassIdFields=aclassDotyczy.Pola.ClassOfType.CID
   aclass=aICORDBEngine.Classes[aclassIdFields]
   aclassproject.BazyZrodlowe.AddRefs(POID,[TOID,CID],ainsertifnotexists=1)
   for afield in ListaNazw:
      i=ListaNazw.index(afield)
      aprettyname=ListaAliasow[i]
      OID=aclass.AddObject()
      aclassDotyczy.Pola.AddRefs(TOID,[OID,aclassIdFields])
      aclass.Nazwa[OID]=afield
      aclass.NazwaWidoczna[OID]=aprettyname
      if re.compile('data'.upper(),re.M).search(aprettyname.upper()) or re.compile('termin'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='11:1746:' #data
         aclass.SGIsSearch[OID]='1'
         aclass.SGIsIndexed[OID]='1'
      elif re.compile('ident'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='1:1746:' #Identyfikator
         aclass.SGIsSearch[OID]='1'
         aclass.SGIsIndexed[OID]='1'
      elif re.compile('kod poczt'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='3:1746:' #kod pocztowy
#         aclass.SGIsSearch[OID]='1'
#         aclass.SGIsIndexed[OID]='1'
      elif re.compile('kwota'.upper(),re.M).search(aprettyname.upper()) or re.compile('rata'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='14:1746:' #pieniadze
#         aclass.SGIsSearch[OID]='1'
#         aclass.SGIsIndexed[OID]='1'
      elif re.compile('miejsce'.upper(),re.M).search(aprettyname.upper()) or re.compile('adres'.upper(),re.M).search(aprettyname.upper()) or re.compile('ulic'.upper(),re.M).search(aprettyname.upper()) or re.compile('miast'.upper(),re.M).search(aprettyname.upper()) or re.compile('domu'.upper(),re.M).search(aprettyname.upper()) or re.compile('lokal'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='2:1746:' #adres
         aclass.SGIsSearch[OID]='1'
         aclass.SGIsIndexed[OID]='1'
      elif re.compile('nip'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='7:1746:' #nip
         aclass.SGIsSearch[OID]='1'
         aclass.SGIsIndexed[OID]='1'
      elif re.compile('regon'.upper(),re.M).search(aprettyname.upper()):
         aclass.SGIsSearch[OID]='1'
         aclass.SGIsIndexed[OID]='1'
         aclass.TypPolaDotyczy[OID]='23:1746:' #regon
      elif re.compile('pesel'.upper(),re.M).search(aprettyname.upper()):
         aclass.SGIsSearch[OID]='1'
         aclass.SGIsIndexed[OID]='1'
         aclass.TypPolaDotyczy[OID]='22:1746:' #pesel
      elif re.compile('telefon'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='4:1746:' #telefon
#         aclass.SGIsSearch[OID]='1'
#         aclass.SGIsIndexed[OID]='1'
      elif re.compile('nazwa'.upper(),re.M).search(aprettyname.upper()) or re.compile('nazwisko'.upper(),re.M).search(aprettyname.upper()) or re.compile('imię'.upper(),re.M).search(aprettyname.upper()):
         aclass.TypPolaDotyczy[OID]='1:1746:' #string
         aclass.SGIsSearch[OID]='1'
#         aclass.SGIsSorted[OID]='1'
         aclass.SGSortStyle[OID]='2:1866:'
         aclass.SGIsIndexed[OID]='1'
      else:
         aclass.TypPolaDotyczy[OID]='1:1746:' #string
      aclass.SGIsAliased[OID]='1'
      aclass.SGTabIndex[OID]=atabindex
      aclass.SGIsDictViewHidden[OID]='1'
      atabindex=atabindex+10
   print 'OK'                                
   return          
def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):

   aFieldList='Klasyfikacja;Analityka;Dochód Wydatek;Dysponent;Dział;Jednostka;Kierunek wydatkowania;Konto;Paragraf;Rodzaj zadania;Rozdział;Zadanie'
   aPrettyNamesList='Klasyfikacja;Analityka;Dochód Wydatek;Dysponent;Dział;Jednostka;Kierunek wydatkowania;Konto;Paragraf;Rodzaj zadania;Rozdział;Zadanie'
   aTableName='OF-PodRolny-KK'
   aPrettyTableName='Osoby fizyczne, podatek rolny, kartoteka księgowa'

   CreateStruktureFromList(CID,41,'',aTableName,aPrettyTableName,aFieldList,aPrettyNamesList)
   return




