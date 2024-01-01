# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

# Metoda uaktualnia atrybuty bezpieczenstwa dla metod w klasach
# pochodnych zgodnie z atrybutami klasy wybranej

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
         self.mclass=aICORDBEngine.Classes['CLASSES\System\Security\MethodSecurityInfo']
      def OnPreClass(self,aclass):
         aname=aclass.NameOfClass
         InfoStatus(aname)
         moid=self.mclass.ItemPath.Identifiers(aclass.ClassPath)
         if moid<0:
            moid=self.mclass.AddObject()
            self.mclass.ItemPath[moid]=aclass.ClassPath
         self.mclass.AllowGetGroups[moid]=self.mclass.AllowGetGroups[self.BaseSecurityOID]
         self.mclass.AllowImportGroups[moid]=self.mclass.AllowImportGroups[self.BaseSecurityOID]
         self.mclass.AllowUpdateGroups[moid]=self.mclass.AllowUpdateGroups[self.BaseSecurityOID]
   citerator=CIterator()
   moid=citerator.mclass.ItemPath.Identifiers(aclass.ClassPath)
   if moid<0:
      return
   citerator.BaseSecurityOID=moid
   citerator.ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass)
   return
