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
         print '%s[%s :%4d] {' % (' '*self.aspaces,aname,aclass.CID)
      def OnPostField(self,aclass,afieldname):
         afield=aclass.FieldsByName(afieldname)
         aid=afield.GetFirstValueID()
         acnt=0
         while aid>=0:
            v=afield.Values(aid)
            acnt=acnt+1
            aid=afield.GetNextValueID(aid)
         print '   %s%s : %s [%d]' % (' '*self.aspaces,afieldname,afield.FieldType,acnt)
      def OnPostMethod(self,aclass,amethodname):
         pass
#         print '   %s<%s>' % (' '*self.aspaces,amethodname)
      def OnPostClass(self,aclass):
         pass
#         print '%s}' % (' '*self.aspaces)
         self.aspaces=self.aspaces-3
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass)
   return
