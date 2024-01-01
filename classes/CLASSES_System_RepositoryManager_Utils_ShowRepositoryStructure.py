# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def TraverseClasses(aclass,aslist=0):
   class CIterator(ICORRepositoryIterator):
      def __init__(self,aslist=0):
         ICORRepositoryIterator.__init__(self)
         self.aslist=aslist
         self.aspaces=-3
         self.data=[]
      def OnPreClass(self,aclass):
         if self.aslist:
            self.data.append(aclass.ClassPath)
            return
         self.aspaces=self.aspaces+3
         aname=aclass.NameOfClass
         print '%s[%s :%4d] {' % (' '*self.aspaces,aname,aclass.CID)
         InfoStatus(aname)
      def OnPostField(self,aclass,afieldname):
         if self.aslist:
            return
         afield=aclass.FieldsByName(afieldname)
         print '   %s%s : %s' % (' '*self.aspaces,afieldname,afield.FieldType)
      def OnPostMethod(self,aclass,amethodname):
         if self.aslist:
            return
         print '   %s<%s>' % (' '*self.aspaces,amethodname)
      def OnPostClass(self,aclass):
         if self.aslist:
            return
         print '%s}' % (' '*self.aspaces)
         self.aspaces=self.aspaces-3
      def Dump(self):
         self.data.sort()
         for s in self.data:
            print "'%s',"%s

   aci=CIterator(aslist=aslist)
   aci.ForEachClass(aclass)
   if aslist:
      aci.Dump()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass,aslist=1)
   return
