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
      defaultres=['Wszystkie obiekty','Pokaż strukturę','Zestawienia','Szukaj','-']
      if not CLIENT_VERSION:
         defaultres.pop()
         defaultres.extend(['Przejdź do klasy','-','Nowe','\+','Klasa pochodna','Pole','Metoda','Obiekt','\-','Skasuj klasę','-','Replikacja','\+','Replikuj dane','Pobierz replikację','\-','Obsługa','\+','Sprawdź referencje','Sprawdź obiekty w klasie słownikowej','Drukuj strukturę repozytorium','Ustaw kardynalność pól','Dodaj menu WWW dla edycji obiektów','Dodaj menu WWW dla kasowania obiektów','Dodaj menu WWW dla uruchamiania metod','Wyświetl skrypt PG - create','Wyświetl skrypt PG - select','Wyświetl skrypt PG - select JSONB','-','Skasuj wszystkie obiekty','\-','Wyszukiwanie','\+','Tekst w metodach','\-']) #,'Tekst RE w metodach'
      bclass=aICORDBEngine.Classes[OID]
      if not bclass is None:
         if bclass.IsFieldInClass('GeoInfo') and bclass.IsFieldInClass('GeoIndex'):
            defaultres.extend(['Geo','\+','Import danych mapowych','Przeliczenie wartości','\-'])
      defaultres.extend(['Właściwości pól','Formatuj'])
   elif FieldName=='Field':
      bclass=aICORDBEngine.Classes[OID]
      if bclass is None:
         return ''
      afield=bclass.FieldsByName(Value)
      if afield is None:
         return ''
      defaultres=['Pokaż wartości',]
      if not afield.ClassOfType is None:
         defaultres.extend(['Typ pola',])
      defaultres.extend(['Szukaj',])
      if not CLIENT_VERSION:
         defaultres.extend(['-',])
         if not afield.ClassOfType is None:
            defaultres.extend(['Nowe','\+','Referencja zwrotna do tej klasy','\-'])
         defaultres.extend(['Skasuj pole','-','Obsługa','\+','Zamień wartości pola'])
         if not afield.ClassOfType is None:
            defaultres.extend(['Skasuj puste referencje','Uzupełnij pola UpdateRefs klasie słownikowej o BackRef'])
         defaultres.extend(['Zapisz wartości archiwalne','Zapisz wszystkie wartości','Importuj wartości z katalogu','\-',])
      defaultres.extend(['Formatuj',])
   elif FieldName=='Method':
      if not CLIENT_VERSION:
         defaultres=['Uruchomienie metody','Edycja metody','Szukaj','-','Skasuj metodę','-','Obsługa','\+','Zapisz wartości archiwalne','\-','Formatuj']
   elif FieldName=='MenuItem':
      pass
   elif FieldName=='WWWServer':
      defaultres=['Edycja',]
   elif FieldName=='WWWIntroduction':
      defaultres=['Edycja',]
   elif FieldName=='WWWMenu':
      defaultres=['Edycja',]
   elif FieldName=='WWWMenuItem':
      defaultres=['Edycja','-','Nowe','\+','Podpozycja','Pozycja przed','Zestawienie','Raport','\-','Wyłącz pozycję','Przywróc widoczność','-','Skasuj','-','Obsługa','\+','Zaznacz zestawienia typu Worksheet','Odłącz możliwość edycji treści','\-','XML','\+','Export XML podpozycji','Import XML podpozycji','\-','Opis HTML','\+','Edycja HTML','Zapamiętaj','Otwórz','-','Czyść','\-','Treść HTML','\+','Edycja HTML','Sprawdź treść','Generuj projekt HTML Help','Zapamiętaj','Otwórz','-','Czyść','\-',]
   elif FieldName=='WWWReportItem':
      defaultres=['Edycja','Przejdź do metody','-','Skasuj']
   elif FieldName=='WWWSummaryItem':
      defaultres=['Edycja',]
      SummaryClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Report_SummaryInfo']
      summoid=SummaryClass.Summary.ValuesAsInt(OID)
      if summoid>=0:
         defaultres.extend(['Pokaż zestawienie','Przejdź do klasy bazowej zestawienia',]) #'Duplikuj zestawienie'
      if SummaryClass.CustomPageByMethod[OID]!='':
         defaultres.extend(['Przejdź do metody',])
      defaultres.extend(['-','Skasuj'])
   elif FieldName=='RFSServer':
      defaultres=['Edycja',]
   elif FieldName=='RFSCollection':
      defaultres=['Edycja','Otwórz','-','Kasuj','-','Aktualizuj z dysku']
   elif FieldName=='RFSItem':
      defaultres=['Edycja','Uruchom','-','Kasuj','-']
   elif FieldName=='StructureField':
      defaultres=['Pokaż w strukturze klas','Pokaż wartości']
      if not CLIENT_VERSION:
         defaultres.extend(['Generuj kod','\+','Dostęp do wszystkich wartości pola','Dostęp do jednej wartości pola','\-'])
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
      defaultres=['Edycja','Pokaż GeoProject','Pokaż GeoProject - GD','Czyść cache']
   elif FieldName=='GeoLayer':
      defaultres=['Edycja','Czyść cache']
   elif FieldName=='EditorText':
      defaultres=['Konwersje','\+','XML Encode','XML Decode','Py2HTML','Otwórz plik i dokonaj konwersji tabulatorów','\-']
   elif FieldName=='HTMLEditorText':
      defaultres=['Konwersje','\+','XML Encode','XML Decode','ISO2Win','Win2ISO','\-']
   else:
      pass
   return string.join(defaultres,chr(255))


