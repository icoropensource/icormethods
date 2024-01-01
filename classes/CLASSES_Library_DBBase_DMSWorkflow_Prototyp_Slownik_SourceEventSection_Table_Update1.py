# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def Update1Field(aclass,afield):
   print '  ',afield.Name
   if afield.Name=='EventValue':
      return
   if afield.Name=='SectionText':
      afield.IsAliased='0'
   else:
      afield.IsAliased='1'
   afield.WWWDefaultInput='1'
   if afield.Name=='Group':
      afield.WWWMenuImageField='814:678:'
      afield.WWWMenuImageClosedField='814:678:'
      afield.WWWTreeRecur=1

def Update1Class(aclass):
   print aclass.NameOfClass
   aclass.WWWJumpToBackRefObject=1
   aclass.WWWMenuImageClass='1029:678:'
   aclass.WWWMenuImageObject='1029:678:'
   aclass.WWWMaxColDictDescription='4'

   aclass.Description.FieldTabIndex='4'
   aclass.Description.FieldPosition='5'
   if aclass.NameOfClass not in ['SourceEventSection']:
      aclass.EventValue.FieldTabIndex='6'
      aclass.EventValue.FieldPosition='6'
   aclass.Group.FieldTabIndex='3'
   aclass.Group.FieldPosition='3'
   aclass.SectionKey.FieldTabIndex='2'
   aclass.SectionKey.FieldPosition='2'
   aclass.SectionName.FieldTabIndex='0'
   aclass.SectionName.FieldPosition='0'
   aclass.SectionText.FieldTabIndex='5'
   aclass.SectionText.FieldPosition='4'
   aclass.SectionType.FieldTabIndex='1'
   aclass.SectionType.FieldPosition='1'

   aclass.Description.FieldNameAsDisplayed='Opis'
   if aclass.NameOfClass not in ['SourceEventSection']:
      aclass.EventValue.FieldNameAsDisplayed='Zdarzenie'
   aclass.Group.FieldNameAsDisplayed='Grupa'
   aclass.SectionKey.FieldNameAsDisplayed='Klucz'
   aclass.SectionName.FieldNameAsDisplayed='Nazwa'
   aclass.SectionText.FieldNameAsDisplayed='Treść'
   aclass.SectionType.FieldNameAsDisplayed='Typ'

   aclass.ForEachField(Update1Field)

def Update2Class(aclass):
   if aclass.NameOfClass not in ['SourceEventSection']:
      print aclass.NameOfClass,aclass.OnClassExport(Value='objects')

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if 1:
      #aclass.ForEachDerivedClass(Update1Class)
      aclass.ForEachDerivedClass(Update2Class)
   return
