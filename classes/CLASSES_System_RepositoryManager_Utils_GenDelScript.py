# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
      def OnPreClass(self,aclass):
         print 'del %d.moi'%(aclass.CID)
      def OnPostField(self,aclass,afieldname):
         afield=aclass.FieldsByName(afieldname)
         print 'del %d.mfd'%(afield.FOID)
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   __import__('CLASSES_Library_ICORBase_Interface_ICORDebugger').set_trace()
   acpaths=[]
   for acpath in acpaths:
      aclass=aICORDBEngine.Classes[acpath]
      TraverseClasses(aclass)
   MessageDialog('OK')
   return

   adialog=InputElementDialog('Wybierz klas�',0,0)
   w=1
   while w:
      w=0
      if adialog.Show():
         aclass=aICORDBEngine.Classes[adialog.ClassPath]
         TraverseClasses(aclass)
         ret=MessageDialog('OK: '+aclass.ClassPath+', repeat?',mtConfirmation,mbYesNoCancel)
         if ret==mrYes:
            w=1
   return

