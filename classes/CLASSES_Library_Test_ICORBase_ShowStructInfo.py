# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
         self.aspaces=-3
      def OnPreClass(self,aclass):
         self.aspaces=self.aspaces+3
         aname=aclass.NameOfClass
         print '%s[%s :%4d] "%s" {' % (' '*self.aspaces,aname,aclass.CID,aclass.WWWDescription)
         #InfoStatus(aname)
      def OnPostField(self,aclass,afieldname):
         afield=aclass.FieldsByName(afieldname)
         if 0:
            print '   %s%s : %s' % (' '*self.aspaces,afieldname,afield.FieldType)
      def OnPostMethod(self,aclass,amethodname):
         if 0:
            print '   %s<%s>' % (' '*self.aspaces,amethodname)
      def OnPostClass(self,aclass):
         if 0:
            print '%s}' % (' '*self.aspaces)
         self.aspaces=self.aspaces-3
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass)
   return
