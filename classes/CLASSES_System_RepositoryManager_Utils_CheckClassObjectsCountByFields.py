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
         self.lco=[]
         aoid=aclass.FirstObject()
         while aoid>=0:
            self.lco.append(aoid)
            aoid=aclass.NextObject(aoid)
         self.lco.sort()
         print len(self.lco),self.lco
      def OnPostField(self,aclass,afieldname):
         afield=aclass.FieldsByName(afieldname)

         aoff=afield.GetFirstDeletedOffset()
         ldo=[]
         while aoff>=0:
            #avalue=afield.GetRecValueAsString(aoff)
            aoid=afield.GetRecOID(aoff)
            if aoid>=0: # and avalue!='Error!':
               ldo.append(aoid)
            aoff=afield.GetNextDeletedOffset(aoff)
         ldo.sort()

         aid=afield.GetFirstValueID()
         acnt=0
         lfo=[]
         while aid>=0:
            lfo.append(aid)
            v=afield.Values(aid)
            acnt=acnt+1
            aid=afield.GetNextValueID(aid)
         lfo.sort()
         print '   %s%s [%d] : %s [%d]' % (' '*self.aspaces,afieldname,afield.FOID,afield.FieldType,acnt,),lfo,ldo
      def OnPostMethod(self,aclass,amethodname):
         pass
      def OnPostClass(self,aclass):
         pass
         self.aspaces=self.aspaces-3
   CIterator().ForEachClass(aclass)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   apath='CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt'
   if not apath:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if adialog.Show():
         apath=adialog.ClassPath
      else:
         return
   aclass=aICORDBEngine.Classes[apath]
   TraverseClasses(aclass)
   return
