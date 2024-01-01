# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

# Metoda uaktualnia atrybuty bezpieczenstwa dla metod w klasie
# zgodnie z atrybutami klasy bazowej

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
         self.mclass=aICORDBEngine.Classes['CLASSES\System\Security\MethodSecurityInfo']
      def OnPreClass(self,aclass):
         aname=aclass.NameOfClass
         InfoStatus(aname)
         iclass=aclass.Inherited
         if iclass is None:
            return
         aoid=self.mclass.ItemPath.Identifiers(iclass.ClassPath)
         moid=self.mclass.ItemPath.Identifiers(aclass.ClassPath)
         if aoid>0:
            if moid<0:
               moid=self.mclass.AddObject()
               self.mclass.ItemPath[moid]=aclass.ClassPath
            if self.mclass.RecurrencyContinue[moid]==TRUE_STRING:
               return
            self.mclass.AllowGetGroups[moid]=self.mclass.AllowGetGroups[aoid]
            self.mclass.AllowImportGroups[moid]=self.mclass.AllowImportGroups[aoid]
            self.mclass.AllowUpdateGroups[moid]=self.mclass.AllowUpdateGroups[aoid]
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass)
   return
