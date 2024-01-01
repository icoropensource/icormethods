# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   ClearStdOut()
   if OID<0:
      return
   bclass=aICORDBEngine.Classes[OID]
   if bclass is None:
      return
   bfield=bclass.FieldsByName(Value)
   if bfield is None:
      return
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   foid=aICORDBEngine.Classes.MetaField.aIDClassField.Identifiers(str(bclass.CID)+'_'+Value)
   if foid<0:
      return
   #description
   aclass.FPDescription[aoid]=bfield.FieldDescription
   #wwwdisabled
   aclass.FPWWWDisabled[aoid]=str(bfield.WWWDisabled)
   aclass.FPWWWSingleValue[aoid]=str(bfield.WWWSingleValue)
   aclass.FPWWWDefaultInput[aoid]=str(bfield.WWWDefaultInput)
   aclass.FPWWWDefaultCheck[aoid]=str(bfield.WWWDefaultCheck)
   aclass.FPWWWUpdateRefs[aoid]=str(bfield.WWWUpdateRefs)
   aclass.FPWWWBackRefField[aoid]=str(bfield.WWWBackRefField)
   aclass.FPWWWTreeRecur[aoid]=str(bfield.WWWTreeRecur)
   aclass.FPWWWTreeRecurObjects[aoid]=str(bfield.WWWTreeRecurObjects)
   aclass.FPWWWSortable[aoid]=str(bfield.WWWSortable)

   aclass.FPWWWLowercase[aoid]=str(bfield.WWWLowercase)
   aclass.FPWWWUppercase[aoid]=str(bfield.WWWUppercase)
   aclass.FPWWWNoSpace[aoid]=str(bfield.WWWNoSpace)
   aclass.FPWWWUnsigned[aoid]=str(bfield.WWWUnsigned)
   aclass.FPWWWUnique[aoid]=str(bfield.WWWUnique)
   aclass.FPWWWFilter[aoid]=bfield.WWWFilter
   aclass.FPWWWMask[aoid]=bfield.WWWMask
   aclass.FPWWWRegex[aoid]=bfield.WWWRegex
   aclass.FPWWWMinValue[aoid]=bfield.WWWMinValue
   aclass.FPWWWMaxValue[aoid]=bfield.WWWMaxValue
   aclass.FPWWWDefaultValue[aoid]=bfield.WWWDefaultValue
   aclass.FPWWWMenuImageField[aoid]=bfield.WWWMenuImageField.AsString()
   aclass.FPWWWMenuImageClosedField[aoid]=bfield.WWWMenuImageClosedField.AsString()

   aclass.FPAllowReadGroups[aoid]=aICORDBEngine.Classes.MetaField.aAllowReadGroups[bfield.FOID]
   aclass.FPAllowWriteGroups[aoid]=aICORDBEngine.Classes.MetaField.aAllowWriteGroups[bfield.FOID]

   #isinteractive
   aclass.FPIsInteractive[aoid]=bfield.IsInteractive
   aclass.FPIsAliased[aoid]=bfield.IsAliased
   aclass.FPIsObligatory[aoid]=bfield.IsObligatory
   #isreadonly
   aclass.FPIsReadOnly[aoid]=bfield.IsReadOnly
   #fieldnameasdisplayed
   aclass.FPNameAsDisplayed[aoid]=bfield.FieldNameAsDisplayed
   #alignment
   s=aICORDBEngine.Classes.MetaField.aFieldAlignment[foid]
   tclass=aICORDBEngine.Classes['CLASSES/System/SystemDictionary/Alignment']
   toid=tclass.ID.Identifiers(s)
   if toid<0:
      toid=tclass.Name.Identifiers('Default')
   aclass.FPAlignment[aoid]=str(toid)+':'+str(tclass.CID)+':'
   #editor
   s=aICORDBEngine.Classes.MetaField.aFieldEditor[foid]
   tclass=aICORDBEngine.Classes['CLASSES/System/SystemDictionary/FieldEditor']
   toid=tclass.ID.Identifiers(s)
   if toid>=0:
      aclass.FPEditor[aoid]=str(toid)+':'+str(tclass.CID)+':'
   else:
      aclass.FPEditor[aoid]=''
   #format
   s=aICORDBEngine.Classes.MetaField.aFieldFormat[foid]
   if s!='':
      tclass=aICORDBEngine.Classes['CLASSES/System/SystemDictionary/FieldFormat']
      toid=tclass.Name.Identifiers(s)
      if toid<=0:
         toid=tclass.AddObject()
         tclass.Name[toid]=s
      aclass.FPFormat[aoid]=str(toid)+':'+str(tclass.CID)+':'
   else:
      aclass.FPFormat[aoid]=''

   if not aclass.EditObject(aoid):
      return

   #wwwdisabled
   bfield.WWWDisabled=aclass.FPWWWDisabled[aoid]
   bfield.WWWSingleValue=aclass.FPWWWSingleValue[aoid]
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

   #isinteractive
   bfield.IsInteractive=aclass.FPIsInteractive[aoid]
   bfield.IsAliased=aclass.FPIsAliased[aoid]
   bfield.IsObligatory=aclass.FPIsObligatory[aoid]

   #isreadonly
   bfield.IsReadOnly=aclass.FPIsReadOnly[aoid]

   #fieldnameasdisplayed
   bfield.FieldNameAsDisplayed=aclass.FPNameAsDisplayed[aoid]

   #description
   bfield.FieldDescription=aclass.FPDescription[aoid]

   #alignment
   arefs=aclass.FPAlignment.GetRefList(aoid)
   if arefs.position>=0:
      s=arefs.ID[arefs.OID]
   else:
      s=''
   aICORDBEngine.Classes.MetaField.aFieldAlignment[foid]=s

   #editor
   arefs=aclass.FPEditor.GetRefList(aoid)
   if arefs.position>=0:
      s=arefs.ID[arefs.OID]
   else:
      s=''
   aICORDBEngine.Classes.MetaField.aFieldEditor[foid]=s

   #format
   arefs=aclass.FPFormat.GetRefList(aoid)
   if arefs.position>=0:
      s=arefs.Name[arefs.OID]
      bfield.FieldFormat=s
   else:
      bfield.FieldFormat=''
   aICORDBEngine.Classes.MetaField.aAllowReadGroups[bfield.FOID]=aclass.FPAllowReadGroups[aoid]
   aICORDBEngine.Classes.MetaField.aAllowWriteGroups[bfield.FOID]=aclass.FPAllowWriteGroups[aoid]
   return

