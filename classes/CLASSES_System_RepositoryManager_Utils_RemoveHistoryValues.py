# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
import os

def TraverseClasses(aclass,bclass):
   class CIterator(ICORRepositoryIterator):
      def __init__(self,bclass):
         ICORRepositoryIterator.__init__(self)
         self.UtilClass=bclass
      def OnPreClass(self,aclass):
         InfoStatus(aclass.ClassPath)
         fname=aICORDBEngine.Variables._ICOR_REPOSITORY_DIR+'/MIID/'+str(aclass.CID)+'.moi'
         if os.path.exists(fname):
            aICORDBEngine.RepositoryChange('ClassRemoveVersionInfo',aid=aclass.CID)
            self.UtilClass.RemoveHistoryValues('MOI',aclass.CID,ainternalexecute=1)
#            os.unlink(fname)
#            os.rename(fname+'.new',fname)
      def OnPostField(self,aclass,afieldname):
         InfoStatus(aclass.ClassPath+' : '+afieldname)
         afield=aclass.FieldsByName(afieldname)
         fname=aICORDBEngine.Variables._ICOR_REPOSITORY_DIR+'/MIDD/'+str(afield.FOID)+'.mfd'
         if os.path.exists(fname):
            aICORDBEngine.RepositoryChange('FieldRemoveVersionInfo',aid=afield.CID,asubitem=afield.Name)
            self.UtilClass.RemoveHistoryValues('MFD',aclass.CID,afield.Name,ainternalexecute=1)
#            os.unlink(fname)
#            os.rename(fname+'.new',fname)
   CIterator(bclass).ForEachClass(aclass)
   InfoStatus('')

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if FieldName=='MFD':
      bclass=aICORDBEngine.Classes[OID]
      afield=bclass.FieldsByName(Value)
      fname=aICORDBEngine.Variables._ICOR_REPOSITORY_DIR+'/MIDD/'+str(afield.FOID)+'.mfd'
      if os.path.exists(fname) and os.path.exists(fname+'.new'):
         aICORDBEngine.RepositoryChange('FieldRefreshProperties',aid=OID,asubitem=Value)
         os.unlink(fname)
         os.rename(fname+'.new',fname)
      return
   elif FieldName=='MOI':
      fname=aICORDBEngine.Variables._ICOR_REPOSITORY_DIR+'/MIID/'+str(OID)+'.moi'
      if os.path.exists(fname) and os.path.exists(fname+'.new'):
         aICORDBEngine.RepositoryChange('ClassRefreshProperties',aid=OID)
         os.unlink(fname)
         os.rename(fname+'.new',fname)
      return
   if not Value:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return
      Value=adialog.ClassPath
   if not Value:
      return
   aclass=aICORDBEngine.Classes[CID]
   bclass=aICORDBEngine.Classes[Value]
   TraverseClasses(bclass,aclass)
   return

