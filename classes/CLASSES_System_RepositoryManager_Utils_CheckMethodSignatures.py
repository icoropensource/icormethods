# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
import md5

DD={
}

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
      def OnPreMethod(self,aclass,amethodname):
         amethod=aclass.MethodsByName(amethodname)
         atext=amethod.MethodText
         atext=atext.strip()
         atext=atext.replace(chr(10),'')
         atext=atext.replace(chr(13),'')
         ahash=md5.new(atext).hexdigest()
         akey="%s_%s"%(string.replace(aclass.ClassPath,'\\','_'),amethodname)
         if DD:
            if DD.has_key(akey):
               if DD[akey]!=ahash:
                  print akey
         else:
            print "'%s':'%s',"%(akey,ahash)
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   adialog=InputElementDialog('Wybierz klasę',0,0)
   if adialog.Show():
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
      ClearStdOut()
      TraverseClasses(aclass)
   return

