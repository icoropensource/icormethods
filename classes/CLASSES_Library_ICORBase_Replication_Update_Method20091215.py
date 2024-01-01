# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aclass=aICORDBEngine.Classes[CID]
#   aupdate='2009_12_15 Nazwy praw dost�pu'
#   if not UpdateManager.CheckUpdate(aupdate):
#      return

   aclass=aICORDBEngine.Classes['CLASSES_System_ICORField']
   aobj=aclass.GetFirstObject()
   d={
      'AccessLevelView':'Wymagane uprawnienia do przegl�dania',
      'AccessLevelDeleteInherited':'Odziedziczone wymagane uprawnienia do kasowania',
      'AccessLevelFilesUpload':'Wymagane uprawnienia do dodawania plik�w',
      'AccessLevelEditInherited':'Odziedziczone wymagane uprawnienia do edycji i dodawania',
      'AccessLevelEdit':'Wymagane uprawnienia do edycji i dodawania',
      'AccessLevelStored':'Zapami�tane uprawnienia',
      'AccessLevelWrite':'Wymagane uprawnienia do edycji, dodawania i zapisu',
      'AccessLevelRead':'Wymagane uprawnienia do przegl�dania i odczytu',
      'AccessLevelDelete':'Wymagane uprawnienia do kasowania',
      'AccessLevelTableEdit':'Wymagane uprawnienia do edycji tabeli',
      'AccessLevel':'Wymagane uprawnienia do przegl�dania',
   }
   while aobj:
      s=aobj.aFieldName
      if d.has_key(s):
         aobj.aFieldNameAsDisplayed=d[s]
      aobj.Next()
   return

