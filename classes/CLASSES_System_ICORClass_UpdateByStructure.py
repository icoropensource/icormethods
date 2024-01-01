# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

ssg=''

def SetItemProperty(cclass,aitem,afname,apname,aoid):
   cfield=cclass.FieldsByName(afname)
   avalue=getattr(aitem,apname)
   if avalue is None:
      print afname,apname,aoid
   cfield[aoid]=avalue

def afieldfunc(aclass,afield,cclass,aoid):
   global ssg
   fclass=aICORDBEngine.Classes['CLASSES\System\ICORField']
   idclassfield=str(aclass.CID)+'_'+afield.Name
   foid=fclass.aIDClassField.Identifiers(idclassfield)
   if foid<0:
      foid=fclass.AddObject()
      fclass.aIDClassField[foid]=idclassfield
   ssg=ssg+str(foid)+':'+str(fclass.CID)+':'
   fclass.aFieldName[foid]=afield.Name
   fclass.aFieldCID[foid]=str(aclass.CID)
   fclass.aFieldAccess[foid]=str(afield.FieldAccessI)
   fattrs=(
      ('aFieldValue','FieldValueAsString'),
      ('aFieldDefaultValue','FieldDefaultValueAsString'),
      ('aFieldDescription','FieldDescription'),
      ('aFieldNameAsDisplayed','FieldNameAsDisplayed'),
      ('aFieldPosition','FieldPosition'),
      ('aFieldTypeID','FieldTypeID'),
      ('aFID','FID'),
      ('aFieldLVColWidth','FieldLVColWidth'),
      ('aFieldLeft','FieldLeft'),
      ('aFieldTop','FieldTop'),
      ('aFieldWidth','FieldWidth'),
      ('aFieldHeight','FieldHeight'),
      ('aFieldNamePosition','FieldNamePosition'),
      ('aFieldDefaultDblClickAction','FieldDefaultDblClickAction'),
      ('aFieldSheetID','FieldSheetID'),
      ('aFieldTabIndex','FieldTabIndex'),
      ('aFieldEditor','FieldEditor'),
      ('aIsAliased','IsAliased'),
      ('aIsContainer','IsContainer'),
      ('aIsFastIndexed','IsFastIndexed'),
      ('aIsIndexed','IsIndexed'),
      ('aIsInteractive','IsInteractive'),
      ('aIsObligatory','IsObligatory'),
      ('aIsVirtual','IsVirtual'),
      ('aIsCached','IsCached'),
      ('aIsReportProtected','IsReportProtected'),
      ('aIsReadOnly','IsReadOnly'),
      ('aLastModified','LastModified'),
      ('aFieldOwnerClassID','FieldOwnerClassID'),
      ('aModified','Modified'),
      ('aFieldFormat','FieldFormat'),
      ('aAlignment','Alignment')
      )
   for fattr,aattr in fattrs:
      SetItemProperty(fclass,afield,fattr,aattr,foid)
      
todo_field="""
   AllowReadGroups : CLASSES\System\GroupItemAccessLevel
   AllowWriteGroups : CLASSES\System\GroupItemAccessLevel
"""

def amethodfunc(aclass,amethod,cclass,aoid):
   global ssg
   mclass=aICORDBEngine.Classes['CLASSES\System\ICORMethod']
   idclassmethod=str(aclass.CID)+'_'+amethod.Name
   moid=mclass.aIDClassMethod.Identifiers(idclassmethod)
   if moid<0:
      moid=mclass.AddObject()
      mclass.aIDClassMethod[moid]=idclassmethod
   ssg=ssg+str(moid)+':'+str(mclass.CID)+':'
   mclass.aMethodCID[moid]=str(aclass.CID)
   mclass.aMethodName[moid]=amethod.Name
   mclass.aMethodAccess[moid]=str(amethod.MethodAccessI)
   mattrs=(
   ('aMethodDescription','MethodDescription'),
   ('aMethodPath','MethodPath'),
   ('aMID','MID'),
   ('aLastModified','LastModified'),
   ('aMethodText','MethodText'),
   ('aIsMenuHidden','IsMenuHidden')
   )
   for mattr,aattr in mattrs:
      SetItemProperty(mclass,amethod,mattr,aattr,moid)
   
def aclassfunc(aclass,cclass):
   aoid=aclass.CID
   InfoStatus(str(aoid)+':'+aclass.NameOfClass)
   cclass.CreateObjectByID(aoid)
   cclass.aCID[aoid]=str(aoid)
   cattrs=(
      ('aBaseCID','BaseCID'), \
      ('aBasePath','BasePath'), \
      ('aClassName','NameOfClass'), \
      ('aMaxMID','MaxMID'), \
      ('aMaxFID','MaxFID'), \
      ('aMaxOID','MaxOID'), \
      ('aClassDescription','ClassDescription'), \
      ('aClassColIDWidth','ClassColIDWidth'), \
      ('aClassFormLeft','ClassFormLeft'), \
      ('aClassFormTop','ClassFormTop'), \
      ('aClassFormWidth','ClassFormWidth'), \
      ('aClassFormHeight','ClassFormHeight'), \
      ('aClassFieldsHidden','ClassFieldsHidden'), \
      ('aReportClass','ReportClass'), \
      ('aIsSystem','IsSystem'), \
      ('aIsVirtual','IsVirtual'), \
      ('aLastModified','LastModified')
      )
   for cattr,aattr in cattrs:
      SetItemProperty(cclass,aclass,cattr,aattr,aoid)
   clist=aclass.GetInheritedClassesList()
   s1=''
   for icid in clist:
      s1=s1+str(icid)+':'+str(cclass.CID)+':'
   cclass.aDerivedClasses[aoid]=s1
   global ssg
   ssg=''
   aclass.ForEachField(afieldfunc,cclass,aoid)
   cclass.aFields[aoid]=ssg
   ssg=''
   aclass.ForEachMethod(amethodfunc,cclass,aoid)
   cclass.aMethods[aoid]=ssg

def aclassoidfunc(aclass,cclass):
   aoid=aclass.CID
   InfoStatus('OID update: '+str(aoid)+':'+aclass.NameOfClass)
   cclass.CreateObjectByID(aoid)
   cclass.aMaxOID[aoid]=aclass.MaxOID

todo_class="""
   aSummaries : CLASSES\System\SummaryItem
   aAllowReadGroups : CLASSES\System\GroupItemAccessLevel
   aAllowWriteGroups : CLASSES\System\GroupItemAccessLevel
"""

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   ClearStdOut()   
   aICORDBEngine.Classes.ForEachClass(aclassfunc,None,aclass)
   aICORDBEngine.Classes.ForEachClass(aclassoidfunc,None,aclass)
   InfoStatus('Koniec')
   return
