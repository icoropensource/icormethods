# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
import os

def TraverseClasses(aclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self):
         ICORRepositoryIterator.__init__(self)
      def OnPreClass(self,aclass):
         InfoStatus(aclass.ClassPath)
         fname=aICORDBEngine.Variables._ICOR_REPOSITORY_DIR+'/MIID/'+str(aclass.CID)+'.moi'
         aICORDBEngine.RepositoryChange('ClassRemoveVersionInfo',aid=aclass.CID,)
         os.unlink(fname)
         os.rename(fname+'.new',fname)
      def OnPostField(self,aclass,afieldname):
         InfoStatus(aclass.ClassPath+' : '+afieldname)
         afield=aclass.FieldsByName(afieldname)
         fname=aICORDBEngine.Variables._ICOR_REPOSITORY_DIR+'/MIDD/'+str(afield.FOID)+'.mfd'
         aICORDBEngine.RepositoryChange('FieldRemoveVersionInfo',aid=afield.CID,asubitem=afield.Name)
         os.unlink(fname)
         os.rename(fname+'.new',fname)
   CIterator().ForEachClass(aclass)
   InfoStatus('')

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   for i in range(1000):
      aoid=aclass.AddObject()
      aclass.PoleS1[aoid]='value '+str(aoid)
      aclass.DeleteObject(aoid)
   for i in range(10):
      aoid=aclass.AddObject()
      aclass.PoleS1[aoid]='value '+str(aoid)
   print 'CID:',aclass.CID,aclass.ClassPath
   print 'FieldOID:',aclass.PoleS1.FOID
   TraverseClasses(aclass)
   return



