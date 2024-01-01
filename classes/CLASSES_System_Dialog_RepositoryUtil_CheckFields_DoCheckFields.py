# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

INDENT='   '

class RepositoryPrinter:
   def __init__(self,pclass,poid):
      self.indent=0
      self.ignoreAllFields=0
      s=pclass.IgnoreFields[poid]
      sl=string.split(s,'\n')
      self.ignorefields=[]
      for sf in sl:
         sl1=string.split(sf,',')
         for sf1 in sl1:
            s=string.strip(sf1)
            if s:
               self.ignorefields.append(s)
            if s=='*':
               self.ignoreAllFields=1
      self.showfieldcreation=pclass.ShowFieldCreation.ValuesAsInt(poid)
      self.showfieldmodification=pclass.ShowFieldModification.ValuesAsInt(poid)
      self.showfieldnameas=pclass.ShowFieldNameAs.ValuesAsInt(poid)
      self.showfieldtype=pclass.ShowFieldType.ValuesAsInt(poid)
      self.showmethodlastmodification=pclass.ShowMethodLastModification.ValuesAsInt(poid)
      self.showfieldwarnings=pclass.ShowFieldWarnings.ValuesAsInt(poid)
      self.showclassimages=pclass.ShowClassImages.ValuesAsInt(poid)
      self.showmethods=pclass.ShowMethods.ValuesAsInt(poid)
   def IgnoreField(self,aname):
      return aname in self.ignorefields
   def IncIndent(self):
      self.indent=self.indent+1
   def DecIndent(self):
      self.indent=self.indent-1
   def PrintClass(self,aclass):
      sl=[INDENT*self.indent,'class %s, CID=%4d' % (aclass.NameOfClass,aclass.CID),]
      if self.showclassimages:
         for idesc,irefs in [[' ImageClass: ',aclass.WWWMenuImageClass],[' ImageClosedClass: ',aclass.WWWMenuImageClosedClass],[' ImageObject: ',aclass.WWWMenuImageObject],[' ImageClosedObject: ',aclass.WWWMenuImageClosedObject],]:
            if irefs:
               sl.append(idesc)
               sl.append('['+irefs.Name[irefs.OID]+']')
      print string.join(sl,'')
   def PrintField(self,afield):
      if self.ignoreAllFields:
         return
      sl=[INDENT*(self.indent+1),]
      if self.showfieldnameas:
         sl.append(afield.FieldNameAsDisplayed)
      else:
         sl.append(afield.Name)
      if self.showfieldtype:
         sl.append(' : ')
         sl.append(afield.FieldType)
      if self.showfieldmodification:
         sl.append(', modyfikacja: ')
         sl.append(tdatetime2fmtstr(afield.GetLastModified()))
      if self.showfieldcreation:
         sl.append(', utworzono: ')
         sl.append(tdatetime2fmtstr(afield.FieldCreated))
      if self.showfieldwarnings:
         if afield.FieldTID>MAX_ICOR_SYSTEM_TYPE:
            bclass=afield.ClassOfType
            if bclass is None:
               sl.insert(1,'*NON_EXISTING_CLASS* ')
            else:
               bcp=bclass.ClassPath
               if string.find(bcp,'CLASSES\\System')>=0:
                  sl.insert(1,'*SYSTEM_CLASS* ')
               if string.find(bcp,'CLASSES\\Library')>=0:
                  sl.insert(1,'*LIBRARY_CLASS* ')
               if afield.FieldCreated<afield.ClassOfType.ClassCreated:
                  sl.insert(1,'*FIELD_CREATED_BEFORE_CLASS* ')
      print string.join(sl,'')
   def PrintMethod(self,amethod):
      if not self.showmethods:
         return
      sl=[INDENT*(self.indent+1),'<',amethod.Name,'>']
      if self.showmethodlastmodification:
         sl.append(', modyfikacja: ')
         sl.append(tdatetime2fmtstr(amethod.GetLastModified()))
      print string.join(sl,'')

class CIterator(ICORRepositoryIterator,RepositoryPrinter):
   def __init__(self,pclass,poid):
      ICORRepositoryIterator.__init__(self)
      RepositoryPrinter.__init__(self,pclass,poid)
   def OnPreClass(self,aclass):
      self.IncIndent()
      self.PrintClass(aclass)
   def OnPostClass(self,aclass):
      self.DecIndent()
   def OnPreField(self,aclass,afieldname):
      afield=aclass.FieldsByName(afieldname)
      self.PrintField(afield)
   def OnPreMethod(self,aclass,amethodname):
      amethod=aclass.MethodsByName(amethodname)
      self.PrintMethod(amethod)

class FIterator(ICORRepositoryIterator,RepositoryPrinter):
   def __init__(self,pclass,poid):
      ICORRepositoryIterator.__init__(self)
      RepositoryPrinter.__init__(self,pclass,poid)
      self.recur=[]
   def OnPreClass(self,aclass):
      self.IncIndent()
   def OnPostClass(self,aclass):
      self.DecIndent()
   def OnPreField(self,aclass,afieldname):
      afield=aclass.FieldsByName(afieldname)
      self.PrintField(afield)
   def OnPreMethod(self,aclass,amethodname):
      amethod=aclass.MethodsByName(amethodname)
      self.PrintMethod(amethod)
   def OnBeforeRecursiveField(self,aclass,afield):
      return not self.IgnoreField(afield.Name)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      return
   bclass=aICORDBEngine.Classes[OID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   if not aclass.EditObject(aoid):
      return
   aobj=aclass[aoid]
   tobj=aobj.TraverseMethod
   if tobj.Name=='Fields':
      aiterator=FIterator(aclass,aoid)
      aiterator.ForEachClass(bclass,afieldrecursive=1)
   else:
      aiterator=CIterator(aclass,aoid)
      aiterator.ForEachClass(bclass)
   MessageDialog('Koniec sprawdzania pól.')
   return
                      
