# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def SkasujPola(aclass):
   fields=('FieldAccess',
      'FieldDefaultValue',
      'FieldType',
      'FieldValue',
      'FieldDescription',
      'FieldNameAsDisplayed',
      'FieldOwnerClassID',
      'FieldPosition',
      'FieldTypeID',
      'FID',
      'FieldLVColWidth',
      'FieldLeft',
      'FieldTop',
      'FieldWidth',
      'FieldHeight',
      'FieldNamePosition',
      'FieldDefaultDblClickAction',
      'FieldSheetID',
      'FieldTabIndex',
      'FieldEditor',
      'IsAliased',
      'IsContainer',
      'IsFastIndexed',
      'IsIndexed',
      'IsInteractive',
      'IsObligatory',
      'IsVirtual',
      'IsCached',
      'IsReportProtected',
      'IsReadOnly',
      'LastModified',
      'AllowReadGroups',
      'AllowWriteGroups',
      'FieldName',
      'IDClassField',
      'Modified',
      'FieldFormat',
      'FieldPath')
   for afname in fields:
      aclass.DeleteField(afname)      

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   d={}
   while aobj:
      s=aobj.aIDClassField
      if d.has_key(s):
         print s
      else:
         d[s]=1
      aobj.Next()
   return
   SkasujPola(aclass)
   return

   def fieldfunc(aclass,afield):
      aclass.CopyField(aclass.CID,afield.Name,0,-1,'a'+afield.Name)
   aclass.ForEachField(fieldfunc)
   return
