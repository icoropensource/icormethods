# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return '0'
      bclass=aICORDBEngine.Classes[adialog.ClassPath]
      if bclass is None:
         return '0'
   else:
      bclass=aICORDBEngine.Classes[OID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   sl=string.split(Value,ServerUtil.SPLIT_CHAR_PARAM)
   if len(sl)==5:
      vname,vnameasdisp,vdesc,vtype,vtypeclass=sl
      vtoid=aclass.NFFieldType.ClassOfType.Name.Identifiers(vtype)
      if vtoid>=0:
         aclass.NFFieldType[aoid]=[vtoid,aclass.NFFieldType.ClassOfType.CID]
   else:
      vname,vnameasdisp,vdesc,vtype,vtypeclass='','','','',''
   aclass.NFName[aoid]=vname
   aclass.FPNameAsDisplayed[aoid]=vnameasdisp
   aclass.FPDescription[aoid]=vdesc
   aclass.NFTypeClass[aoid]=vtypeclass
   aclass.FPAllowReadGroups[aoid]=''
   aclass.FPAllowWriteGroups[aoid]=''

   aclass.NFDefaultValue[aoid]=''
   aclass.NFIsInteractive[aoid]='1'
   aclass.NFIsObligatory[aoid]='0'
   aclass.FPIsReadOnly[aoid]='0'
   aclass.FPWWWDisabled[aoid]='0'
   aclass.FPWWWDefaultInput[aoid]='1'
   aclass.FPWWWDefaultCheck[aoid]='0'
   aclass.FPWWWUpdateRefs[aoid]='0'
   aclass.FPWWWBackRefField[aoid]='0'
   aclass.FPWWWTreeRecur[aoid]='0'
   aclass.FPWWWTreeRecurObjects[aoid]='0'
   aclass.FPWWWSortable[aoid]='0'

   aclass.FPWWWLowercase[aoid]='0'
   aclass.FPWWWUppercase[aoid]='0'
   aclass.FPWWWNoSpace[aoid]='0'
   aclass.FPWWWUnsigned[aoid]='0'
   aclass.FPWWWUnique[aoid]='0'
   aclass.FPWWWFilter[aoid]=''
   aclass.FPWWWMask[aoid]=''
   aclass.FPWWWRegex[aoid]=''
   aclass.FPWWWMinValue[aoid]=''
   aclass.FPWWWMaxValue[aoid]=''
   aclass.FPWWWDefaultValue[aoid]=''
   aclass.FPWWWMenuImageField[aoid]=''
   aclass.FPWWWMenuImageClosedField[aoid]=''

   isContainer=0
   aclass.NFIsAliased[aoid]='1'
   aclass.NFIsVirtual[aoid]='0'
   aclass.NFIsCached[aoid]='0'
   if not aclass.EditObject(aoid):
      return '0'
   fdef=ICORFieldDefinition(aclass.NFName[aoid],mt_String)
   arefs=aclass.NFFieldType.GetRefList(aoid)
   if arefs.position>=0:
      s=arefs.Name[arefs.OID]
   else:
      s=''
   if s=='Memo':
      s='String'
      isContainer=1
   if s=='Class':
      s=aclass.NFTypeClass[aoid]
   fdef.FTypeID=aICORDBEngine.Classes.GetTypeIDByType(s)
   if fdef.FTypeID<0:
      print 'Zły typ pola!'
      return '0'
   fdef.FDefaultValue=aclass.NFDefaultValue[aoid]
   fdef.FInteractive=aclass.NFIsInteractive.ValuesAsInt(aoid)
   fdef.FObligatory=aclass.NFIsObligatory.ValuesAsInt(aoid)
   fdef.FContainerType=isContainer
   fdef.FAlias=aclass.NFIsAliased.ValuesAsInt(aoid)
   fdef.FVirtual=aclass.NFIsVirtual.ValuesAsInt(aoid)
   fdef.FCached=aclass.NFIsCached.ValuesAsInt(aoid)
   bfield=bclass.AddField(fdef)
   if bfield is None:
      print 'Pole nie zostało dodane!'
      return '0'
   bfield.WWWDisabled=aclass.FPWWWDisabled[aoid]
   bfield.WWWDefaultInput=aclass.FPWWWDefaultInput[aoid]
   bfield.WWWDefaultCheck=aclass.FPWWWDefaultCheck[aoid]
   bfield.WWWUpdateRefs=aclass.FPWWWUpdateRefs[aoid]
   bfield.WWWBackRefField=aclass.FPWWWBackRefField[aoid]
   bfield.WWWTreeRecur=aclass.FPWWWTreeRecur[aoid]
   bfield.WWWTreeRecurObjects=aclass.FPWWWTreeRecurObjects[aoid]
   bfield.WWWSortable=aclass.FPWWWSortable[aoid]

   bfield.WWWLowercase=aclass.FPWWWLowercase[aoid]
   bfield.WWWUppercase=aclass.FPWWWUppercase[aoid]
   bfield.WWWNoSpace=aclass.FPWWWNoSpace[aoid]
   bfield.WWWUnsigned=aclass.FPWWWUnsigned[aoid]
   bfield.WWWUnique=aclass.FPWWWUnique[aoid]
   bfield.WWWFilter=aclass.FPWWWFilter[aoid]
   bfield.WWWMask=aclass.FPWWWMask[aoid]
   bfield.WWWRegex=aclass.FPWWWRegex[aoid]
   bfield.WWWMinValue=aclass.FPWWWMinValue[aoid]
   bfield.WWWMaxValue=aclass.FPWWWMaxValue[aoid]
   bfield.WWWDefaultValue=aclass.FPWWWDefaultValue[aoid]
   bfield.WWWMenuImageField=aclass.FPWWWMenuImageField[aoid]
   bfield.WWWMenuImageClosedField=aclass.FPWWWMenuImageClosedField[aoid]

   bfield.IsReadOnly=aclass.FPIsReadOnly[aoid]
   bfield.FieldNameAsDisplayed=aclass.FPNameAsDisplayed[aoid]
   bfield.FieldDescription=aclass.FPDescription[aoid]
   #alignment
   arefs=aclass.FPAlignment.GetRefList(aoid)
   if arefs.position>=0:
      s=arefs.ID[arefs.OID]
      aICORDBEngine.Classes.MetaField.aFieldAlignment[bfield.FOID]=s
   #editor
   arefs=aclass.FPEditor.GetRefList(aoid)
   if arefs.position>=0:
      s=arefs.ID[arefs.OID]
      aICORDBEngine.Classes.MetaField.aFieldEditor[bfield.FOID]=s
   #format
   arefs=aclass.FPFormat.GetRefList(aoid)
   if arefs.position>=0:
      s=arefs.Name[arefs.OID]
      bfield.FieldFormat=s

   aICORDBEngine.Classes.MetaField.aAllowReadGroups[bfield.FOID]=aclass.FPAllowReadGroups[aoid]
   aICORDBEngine.Classes.MetaField.aAllowWriteGroups[bfield.FOID]=aclass.FPAllowWriteGroups[aoid]

   return '1'

