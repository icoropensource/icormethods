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
         self.wc=1
      def OnPostField(self,aclass,afieldname):
         afield=aclass.FieldsByName(afieldname)
         aoff=afield.GetFirstDeletedOffset()
         d={}
         while aoff>=0:
            avalue=afield.GetRecValueAsString(aoff)
            aoid=afield.GetRecOID(aoff)
            if aoid>=0 and avalue!='Error!':
               l=d.get(aoid,[])
               l.append(avalue)
               d[aoid]=l
            aoff=afield.GetNextDeletedOffset(aoff)
         aoid=afield.GetFirstValueID()
         while aoid>=0:
            avalue=afield[aoid]
            if not avalue:
               l=d.get(aoid,[])
               l=filter(None,l)
               if l:
                  if self.wc:
                     print '[%s :%4d]' % (aclass.ClassPath,aclass.CID)
                     self.wc=0
                  print '   %s : %d [%s]' % (afieldname,aoid,l[-1][:100])
            aoid=afield.GetNextValueID(aoid)
      def OnPostMethod(self,aclass,amethodname):
         pass
      def OnPostClass(self,aclass):
         pass
         self.aspaces=self.aspaces-3
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      TraverseClasses(aclass)
   return

