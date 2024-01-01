# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return
      bclass=aICORDBEngine.Classes[adialog.ClassPath]
      if bclass is None:
         return
   else:
      bclass=aICORDBEngine.Classes[OID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   s=aICORDBEngine.Classes.MetaClass.aEditorSheets[bclass.CID]
   aclass.CPEditorSheets[aoid]=s
   aclass.CPReadOnly[aoid]=bclass.IsReadOnly
   aclass.CPAllowReadGroups[aoid]=aICORDBEngine.Classes.MetaClass.aAllowReadGroups[bclass.CID]
   aclass.CPAllowWriteGroups[aoid]=aICORDBEngine.Classes.MetaClass.aAllowWriteGroups[bclass.CID]
   aclass.CPWWWDescription[aoid]=bclass.WWWDescription
   aclass.CPWWWDisableDescription[aoid]=str(bclass.WWWDisableDescription)
   aclass.CPWWWJumpToBackRefObject[aoid]=str(bclass.WWWJumpToBackRefObject)
   aclass.CPWWWMenu[aoid]=aICORDBEngine.Classes.MetaClass.aWWWMenu[bclass.CID]
   aclass.CPWWWEditPageTopHTML[aoid]=aICORDBEngine.Classes.MetaClass.aWWWEditPageTopHTML[bclass.CID]
   aclass.CPWWWEditPageBottomHTML[aoid]=aICORDBEngine.Classes.MetaClass.aWWWEditPageBottomHTML[bclass.CID]
   aclass.CPWWWMaxColDictDescription[aoid]=aICORDBEngine.Classes.MetaClass.aWWWMaxColDictDescription[bclass.CID]
   aclass.CPWWWMenuImageClass[aoid]=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClass[bclass.CID]
   aclass.CPWWWMenuImageClosedClass[aoid]=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedClass[bclass.CID]
   aclass.CPWWWMenuImageObject[aoid]=aICORDBEngine.Classes.MetaClass.aWWWMenuImageObject[bclass.CID]
   aclass.CPWWWMenuImageClosedObject[aoid]=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedObject[bclass.CID]
   if not aclass.EditObject(aoid):
      return
   bclass.WWWDescription=aclass.CPWWWDescription[aoid]
   bclass.WWWDisableDescription=aclass.CPWWWDisableDescription.ValuesAsInt(aoid)
   bclass.WWWJumpToBackRefObject=aclass.CPWWWJumpToBackRefObject.ValuesAsInt(aoid)
   bclass.IsReadOnly=aclass.CPReadOnly[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWMenu[bclass.CID]=aclass.CPWWWMenu[aoid]
   aICORDBEngine.Classes.MetaClass.aAllowReadGroups[bclass.CID]=aclass.CPAllowReadGroups[aoid]
   aICORDBEngine.Classes.MetaClass.aAllowWriteGroups[bclass.CID]=aclass.CPAllowWriteGroups[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWMaxColDictDescription[bclass.CID]=aclass.CPWWWMaxColDictDescription[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWEditPageTopHTML[bclass.CID]=aclass.CPWWWEditPageTopHTML[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWEditPageBottomHTML[bclass.CID]=aclass.CPWWWEditPageBottomHTML[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWMenuImageClass[bclass.CID]=aclass.CPWWWMenuImageClass[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedClass[bclass.CID]=aclass.CPWWWMenuImageClosedClass[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWMenuImageObject[bclass.CID]=aclass.CPWWWMenuImageObject[aoid]
   aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedObject[bclass.CID]=aclass.CPWWWMenuImageClosedObject[aoid]
   return

