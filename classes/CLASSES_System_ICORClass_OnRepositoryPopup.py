# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import sys
from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   defaultres='opcja 1'+chr(255)+'opcja 2'
#   print 'FieldName:',FieldName,'OID:',OID,'Value:',Value
   InfoStatus(FieldName)
   if aICORDBEngine.Variables._FOR_CLIENT_VERSION=='1':
      CLIENT_VERSION=1
   else:
      CLIENT_VERSION=0
   defaultres=[]
   if FieldName=='None':
      pass
   elif FieldName=='Class':
      defaultres=['Wszystkie obiekty','Poka� struktur�','Zestawienia','Szukaj','-']
      if not CLIENT_VERSION:
         defaultres.pop()
         defaultres.extend(['Przejd� do klasy','-','Nowe','\+','Klasa pochodna','Pole','Metoda','Obiekt','\-','Skasuj klas�','-','Replikacja','\+','Replikuj dane','Pobierz replikacj�','\-','Obs�uga','\+','Sprawd� referencje','Sprawd� obiekty w klasie s�ownikowej','Drukuj struktur� repozytorium','Ustaw kardynalno�� p�l','Dodaj menu WWW dla edycji obiekt�w','Dodaj menu WWW dla kasowania obiekt�w','Dodaj menu WWW dla uruchamiania metod','Wy�wietl skrypt PG - create','Wy�wietl skrypt PG - select','Wy�wietl skrypt PG - select JSONB','-','Skasuj wszystkie obiekty','\-','Wyszukiwanie','\+','Tekst w metodach','\-']) #,'Tekst RE w metodach'
      bclass=aICORDBEngine.Classes[OID]
      if not bclass is None:
         if bclass.IsFieldInClass('GeoInfo') and bclass.IsFieldInClass('GeoIndex'):
            defaultres.extend(['Geo','\+','Import danych mapowych','Przeliczenie warto�ci','\-'])
      defaultres.extend(['W�a�ciwo�ci p�l','Formatuj'])
   elif FieldName=='Field':
      bclass=aICORDBEngine.Classes[OID]
      if bclass is None:
         return ''
      afield=bclass.FieldsByName(Value)
      if afield is None:
         return ''
      defaultres=['Poka� warto�ci',]
      if not afield.ClassOfType is None:
         defaultres.extend(['Typ pola',])
      defaultres.extend(['Szukaj',])
      if not CLIENT_VERSION:
         defaultres.extend(['-',])
         if not afield.ClassOfType is None:
            defaultres.extend(['Nowe','\+','Referencja zwrotna do tej klasy','\-'])
         defaultres.extend(['Skasuj pole','-','Obs�uga','\+','Zamie� warto�ci pola'])
         if not afield.ClassOfType is None:
            defaultres.extend(['Skasuj puste referencje','Uzupe�nij pola UpdateRefs klasie s�ownikowej o BackRef'])
         defaultres.extend(['Zapisz warto�ci archiwalne','Zapisz wszystkie warto�ci','Importuj warto�ci z katalogu','\-',])
      defaultres.extend(['Formatuj',])
   elif FieldName=='Method':
      if not CLIENT_VERSION:
         defaultres=['Uruchomienie metody','Edycja metody','Szukaj','-','Skasuj metod�','-','Obs�uga','\+','Zapisz warto�ci archiwalne','\-','Formatuj']
   elif FieldName=='MenuItem':
      pass
   elif FieldName=='WWWServer':
      defaultres=['Edycja',]
   elif FieldName=='WWWIntroduction':
      defaultres=['Edycja',]
   elif FieldName=='WWWMenu':
      defaultres=['Edycja',]
   elif FieldName=='WWWMenuItem':
      defaultres=['Edycja','-','Nowe','\+','Podpozycja','Pozycja przed','Zestawienie','Raport','\-','Wy��cz pozycj�','Przywr�c widoczno��','-','Skasuj','-','Obs�uga','\+','Zaznacz zestawienia typu Worksheet','Od��cz mo�liwo�� edycji tre�ci','\-','XML','\+','Export XML podpozycji','Import XML podpozycji','\-','Opis HTML','\+','Edycja HTML','Zapami�taj','Otw�rz','-','Czy��','\-','Tre�� HTML','\+','Edycja HTML','Sprawd� tre��','Generuj projekt HTML Help','Zapami�taj','Otw�rz','-','Czy��','\-',]
   elif FieldName=='WWWReportItem':
      defaultres=['Edycja','Przejd� do metody','-','Skasuj']
   elif FieldName=='WWWSummaryItem':
      defaultres=['Edycja',]
      SummaryClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Report_SummaryInfo']
      summoid=SummaryClass.Summary.ValuesAsInt(OID)
      if summoid>=0:
         defaultres.extend(['Poka� zestawienie','Przejd� do klasy bazowej zestawienia',]) #'Duplikuj zestawienie'
      if SummaryClass.CustomPageByMethod[OID]!='':
         defaultres.extend(['Przejd� do metody',])
      defaultres.extend(['-','Skasuj'])
   elif FieldName=='RFSServer':
      defaultres=['Edycja',]
   elif FieldName=='RFSCollection':
      defaultres=['Edycja','Otw�rz','-','Kasuj','-','Aktualizuj z dysku']
   elif FieldName=='RFSItem':
      defaultres=['Edycja','Uruchom','-','Kasuj','-']
   elif FieldName=='StructureField':
      defaultres=['Poka� w strukturze klas','Poka� warto�ci']
      if not CLIENT_VERSION:
         defaultres.extend(['Generuj kod','\+','Dost�p do wszystkich warto�ci pola','Dost�p do jednej warto�ci pola','\-'])
   elif FieldName=='SecurityUserUser':
      defaultres=['Edycja',]
   elif FieldName=='SecurityGroupUser':
      defaultres=['Edycja',]
   elif FieldName=='SecurityAccessLevelUser':
      defaultres=['Edycja',]
   elif FieldName=='SecurityProfileGroupUser':
      defaultres=['Edycja',]
   elif FieldName=='GeoStructItem':
      defaultres=['Edycja',]
   elif FieldName=='GeoProject':
      defaultres=['Edycja','Poka� GeoProject','Poka� GeoProject - GD','Czy�� cache']
   elif FieldName=='GeoLayer':
      defaultres=['Edycja','Czy�� cache']
   elif FieldName=='EditorText':
      defaultres=['Konwersje','\+','XML Encode','XML Decode','Py2HTML','Otw�rz plik i dokonaj konwersji tabulator�w','\-']
   elif FieldName=='HTMLEditorText':
      defaultres=['Konwersje','\+','XML Encode','XML Decode','ISO2Win','Win2ISO','\-']
   else:
      pass
   return string.join(defaultres,chr(255))


