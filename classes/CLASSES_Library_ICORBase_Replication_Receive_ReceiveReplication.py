# -*- coding: windows-1250 -*-
# saved: 2021/06/08 16:38:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_NetBase_Utils_FTPUtil import *
from CLASSES_Library_NetBase_Utils_XMLUtil import *
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import icorlib.wwwmenu.menuutil as MenuUtil
import icorlib.wwwmenu.xmlmenuutil as XMLMenuUtil
import xmllib #from xml.parsers 
from ftplib import FTP
import os
import string
import re

ReplicationException = 'ReplicationException'

NO_STRUCTURE_IMPORT=0

TRANSLATE_OID=[
#[51000,52000,11000],
]

TRANSLATE_VALUE_RE=''
#TRANSLATE_VALUE_RE=r'(\d\d\d\d\d)'
TRANSLATE_VALUE=[           
]

def GetListAsDateTuple(alist,x=0):
   return (int(alist[x]),int(alist[x+1]),int(alist[x+2]),int(alist[x+3]),int(alist[x+4]),int(alist[x+5]),int(alist[x+6]))

class ICORXMLReplicationParser(xmllib.XMLParser):
   def __init__(self, aprofile):
      xmllib.XMLParser.__init__(self,accept_utf8=1,accept_unquoted_attributes=1,accept_missing_endtag_name=1)
      self.ProfileClass=aICORDBEngine.Classes['CLASSES/Library/ICORBase/Replication/Receive']
      if self.ProfileClass is None:
         raise ReplicationException,'Profile class does not exists'
      if type(aprofile)==type(1):
         self.OID=aprofile
      else:
         self.OID=self.ProfileClass.Name.Identifiers(aprofile)
      if self.OID<0:
         raise ReplicationException,'Profile does not exists'
      self.MenuClass=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_Dictionary_Menu']
      c1=aICORDBEngine.Classes['CLASSES_System_GroupAccessLevel']
      c2=aICORDBEngine.Classes['CLASSES_System_GroupItemAccessLevel']
      self.dACL_CIDs={c1.CID:c1,c2.CID:c2}
      self.InitByProfile()
   def InitByProfile(self):
      self.afile=self.ProfileClass.InputFile[self.OID]
      self.allowupdateprotected=self.ProfileClass.AllowUpdateProtected.ValuesAsInt(self.OID)
      self.importmethodexecute=self.ProfileClass.ImportMethodExecute.ValuesAsInt(self.OID)
      self.verbose=self.ProfileClass.Verbose.ValuesAsInt(self.OID)
      self.overridedeleted=self.ProfileClass.OverrideDeleted.ValuesAsInt(self.OID)
      self.receivemethods=self.ProfileClass.ReceiveMethods.ValuesAsInt(self.OID)
      self.alwaysupdatemethod=self.ProfileClass.AlwaysUpdateMethod.ValuesAsInt(self.OID)
   def Parse(self,fname=''):
      self.reset()
      self.elements={}
      self.elements['REPLICATION']=(self.start_REPLICATION,self.end_REPLICATION)
      self.elements['HEADER']=(self.start_HEADER,self.end_HEADER)
      self.elements['CLASS']=(self.start_CLASS,self.end_CLASS)
      self.elements['FIELD']=(self.start_FIELD,self.end_FIELD)
      self.elements['OBJECT']=(self.start_OBJECT,self.end_OBJECT)
      self.elements['DATA']=(self.start_DATA,self.end_DATA)
      self.elements['FIELDVALUE']=(self.start_FIELDVALUE,self.end_FIELDVALUE)
      self.elements['CLASSDEFINITION']=(self.start_CLASSDEFINITION,self.end_CLASSDEFINITION)
      self.elements['FIELDDEFINITION']=(self.start_FIELDDEFINITION,self.end_FIELDDEFINITION)
      self.elements['CLASSMENUDEFINITION']=(self.start_CLASSMENUDEFINITION,self.end_CLASSMENUDEFINITION)
      self.elements['MENUITEM']=(self.start_MENUITEM,self.end_MENUITEM)
      self.elements['METHODDEFINITION']=(self.start_METHODDEFINITION,self.end_METHODDEFINITION)
      self.elements['METHODLINE']=(self.start_METHODLINE,self.end_METHODLINE)

      self.elements['MENUPAGEHTML']=(self.start_MENUPAGEHTML,self.end_MENUPAGEHTML)
      self.elements['MENUPAGEHTMLLINE']=(self.start_MENUPAGEHTMLLINE,self.end_MENUPAGEHTMLLINE)
      self.elements['REPORTS']=(self.start_REPORTS,self.end_REPORTS)
      self.elements['REPORTITEM']=(self.start_REPORTITEM,self.end_REPORTITEM)

      if fname!='':
         self.afile=fname
      if self.afile=='':
         raise ReplicationException,'No file'
      self.afile=FilePathAsSystemPath(self.afile)
      if self.afile[-3:]!='.gz':
         self.afile=self.afile+'.gz'
      self.aclass=None
      self.afield=None
      self.acmethod=None
      self.afmethod=None
      self.aomethod=None
      self.ismemo=0
      self.avalue=''
      self.avalueline=''
      self.LastField=None
      self.LastCID=None
      self.LastClassPath=None
      fsize=os.path.getsize(self.afile)
      f=TextFile(self.afile,'r')
      i=0
      try:
         s=f.readline()
         while s!='':
            self.feed(s[:-1])
            i=i+1
            if i>=120:
               i=0
               apos=f.tell()
               SetProgress(apos,fsize)
            s=f.readline()
         self.close()
      finally:
         f.close()
         SetProgress(0,0)
#      InfoStatus('')
   def start_REPLICATION(self,attrs):
      pass
   def start_HEADER(self,attrs):
      self.sourceuser=int(attrs['SourceUser'])
      print 'SourceUser:',self.sourceuser
      self.targetuser=int(attrs['TargetUser'])
      print 'TargetUser:',self.targetuser
      alm=string.split(attrs['DateFrom'],' ')
      self.datefrom=GetListAsDateTuple(alm)
      print 'DateFrom:',self.datefrom
      alm=string.split(attrs['Created'],' ')
      self.created=GetListAsDateTuple(alm)
      print 'Created:',self.created
      print ''
   def end_HEADER(self):
      pass
   def start_CLASSDEFINITION(self, attrs):
      if NO_STRUCTURE_IMPORT:
         return
      bclass=aICORDBEngine.Classes[attrs['BasePath']]
      if bclass is None:
         return
      nclass=bclass.GetDerivedClass(attrs['NameOfClass'])
      if nclass is None:
         print 'Nowa klasa: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         nclass=bclass.AddClass(attrs['NameOfClass'])
         if nclass is None:
            print 'zla klasa: %(NameOfClass)s w klasie %(BasePath)s'%attrs
            return
      if attrs.get('ClassColIDWidth',''):
         aICORDBEngine.Classes.MetaClass.aClassColIDWidth[nclass.CID]=attrs.get('ClassColIDWidth','')
      if attrs.get('ClassDescription',''):
         aICORDBEngine.Classes.MetaClass.aClassDescription[nclass.CID]=attrs.get('ClassDescription','')
      if attrs.get('ClassFieldsHidden',''):
         aICORDBEngine.Classes.MetaClass.aClassFieldsHidden[nclass.CID]=attrs.get('ClassFieldsHidden','')
      if attrs.get('ClassFormHeight',''):
         aICORDBEngine.Classes.MetaClass.aClassFormHeight[nclass.CID]=attrs.get('ClassFormHeight','')
      if attrs.get('ClassFormLeft',''):
         aICORDBEngine.Classes.MetaClass.aClassFormLeft[nclass.CID]=attrs.get('ClassFormLeft','')
      if attrs.get('ClassFormTop',''):
         aICORDBEngine.Classes.MetaClass.aClassFormTop[nclass.CID]=attrs.get('ClassFormTop','')
      if attrs.get('ClassFormWidth',''):
         aICORDBEngine.Classes.MetaClass.aClassFormWidth[nclass.CID]=attrs.get('ClassFormWidth','')
      if attrs.get('IsReadOnly',''):
         aICORDBEngine.Classes.MetaClass.aIsReadOnly[nclass.CID]=attrs.get('IsReadOnly','')
      if attrs.get('IsSystem',''):
         aICORDBEngine.Classes.MetaClass.aIsSystem[nclass.CID]=attrs.get('IsSystem','')
      if attrs.get('IsVirtual',''):
         aICORDBEngine.Classes.MetaClass.aIsVirtual[nclass.CID]=attrs.get('IsVirtual','')
      if attrs.get('ReportClass',''):
         aICORDBEngine.Classes.MetaClass.aReportClass[nclass.CID]=attrs.get('ReportClass','')
      if attrs.get('WWWDescription',''):
         aICORDBEngine.Classes.MetaClass.aWWWDescription[nclass.CID]=attrs.get('WWWDescription','')
      if attrs.get('WWWDisableDescription',''):
         aICORDBEngine.Classes.MetaClass.aWWWDisableDescription[nclass.CID]=attrs.get('WWWDisableDescription','')
      if attrs.get('WWWJumpToBackRefObject',''):
         aICORDBEngine.Classes.MetaClass.aWWWJumpToBackRefObject[nclass.CID]=attrs.get('WWWJumpToBackRefObject','')
      if attrs.get('WWWMaxColDictDescription',''):
         aICORDBEngine.Classes.MetaClass.aWWWMaxColDictDescription[nclass.CID]=attrs.get('WWWMaxColDictDescription','')
      if attrs.get('AllowReadGroups',''):
         aICORDBEngine.Classes.MetaClass.aAllowReadGroups[nclass.CID]=ICORSecurity.GetStringAsAccessLevelRefs(attrs.get('AllowReadGroups','')).AsString()
      if attrs.get('AllowWriteGroups',''):
         aICORDBEngine.Classes.MetaClass.aAllowWriteGroups[nclass.CID]=ICORSecurity.GetStringAsAccessLevelRefs(attrs.get('AllowWriteGroups','')).AsString()
      s=attrs.get('EditorSheets','')
      if s:
         l=string.split(s,chr(10))
         aICORDBEngine.Classes.MetaClass.aEditorSheets.DeleteReferencedObjects(nclass.CID)
         sclass=aICORDBEngine.Classes.MetaClass.aEditorSheets.ClassOfType
         lrefs=[]
         for si in l:
            l1=string.split(si,chr(9))
            soid=sclass.AddObject()
            sclass.Name[soid]=l1[0]
            if l1[1]:
               sclass.WWWDisabled[soid]=l1[1]
            lrefs.append([soid,sclass.CID])
         aICORDBEngine.Classes.MetaClass.aEditorSheets.AddRefs(nclass.CID,lrefs)
      s=attrs.get('WWWMenuImageClass','')
      if s:
         sclass=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClass.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0 and s[:3]=='aa_':
            soid=sclass.Name.Identifiers(s[3:])
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClass "%(WWWMenuImageClass)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageClass[nclass.CID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageClosedClass','')
      if s:
         sclass=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedClass.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0 and s[:3]=='aa_':
            soid=sclass.Name.Identifiers(s[3:])
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClosedClass "%(WWWMenuImageClosedClass)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedClass[nclass.CID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageClosedObject','')
      if s:
         sclass=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedObject.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0 and s[:3]=='aa_':
            soid=sclass.Name.Identifiers(s[3:])
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClosedObject "%(WWWMenuImageClosedObject)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedObject[nclass.CID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageObject','')
      if s:
         sclass=aICORDBEngine.Classes.MetaClass.aWWWMenuImageObject.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0 and s[:3]=='aa_':
            soid=sclass.Name.Identifiers(s[3:])
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageObject "%(WWWMenuImageObject)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageObject[nclass.CID]=[soid,sclass.CID]
   def start_FIELDDEFINITION(self, attrs):
      if NO_STRUCTURE_IMPORT:
         return
      bclass=aICORDBEngine.Classes[attrs.get('ClassPath','')]
      if bclass is None:
         print 'Dla pola %s nie istnieje klasa %s'%(attrs.get('Name',''),attrs.get('ClassPath',''))
         return
      ftid=aICORDBEngine.Classes.GetTypeIDByType(attrs.get('FieldType',''))
      if ftid<0:
         print 'Pole %s w klasie %s posiada nieprawid�owy typ: %s'%(attrs.get('Name',''),attrs.get('ClassPath',''),attrs.get('FieldType',''))
         return
      if bclass.IsFieldInClass(attrs.get('Name','')):
         bfield=bclass.FieldsByName(attrs.get('Name',''))
         if bfield.FieldTID!=ftid:
            print 'Pole %s w klasie %s posiada inny typ (%s) ni� zadeklarowany w replikacji nieprawid�owy typ: %s'%(attrs.get('Name',''),attrs.get('ClassPath',''),bfield.FieldType,attrs.get('FieldType',''))
            return
      else:
         fdef=ICORFieldDefinition(attrs['Name'],ftid)
         fdef.FInteractive=int(attrs.get('IsInteractive',''))
         fdef.FObligatory=int(attrs.get('IsObligatory',''))
         fdef.FContainerType=int(attrs.get('IsContainer',''))
         fdef.FAlias=int(attrs.get('IsAliased',''))
         bfield=bclass.AddField(fdef)
         if bfield is None:
            print 'Pole %s w klasie %s nie zosta�o dodane!'%(attrs.get('Name',''),attrs.get('ClassPath',''))
            return
         print 'Nowe pole: %(Name)s w klasie %(ClassPath)s'%attrs
      sfnad=attrs.get('FieldNameAsDisplayed','') #
      if sfnad!='' and sfnad!=attrs.get('Name',''):
         bfield.FieldNameAsDisplayed=sfnad
      if attrs.get('WWWDisabled',''):
         bfield.WWWDisabled=attrs.get('WWWDisabled','')
      if attrs.get('WWWDefaultInput',''):
         bfield.WWWDefaultInput=attrs.get('WWWDefaultInput','')
      if attrs.get('WWWSingleValue',''):
         bfield.WWWSingleValue=attrs.get('WWWSingleValue','')
      if attrs.get('WWWBackRefField',''):
         bfield.WWWBackRefField=attrs.get('WWWBackRefField','')
      if attrs.get('WWWDefaultCheck',''):
         bfield.WWWDefaultCheck=attrs.get('WWWDefaultCheck','')
      if attrs.get('WWWDefaultValue',''):
         bfield.WWWDefaultValue=attrs.get('WWWDefaultValue','')
      if attrs.get('WWWFilter',''):
         bfield.WWWFilter=attrs.get('WWWFilter','')
      if attrs.get('WWWLowercase',''):
         bfield.WWWLowercase=attrs.get('WWWLowercase','')
      if attrs.get('WWWMask',''):
         bfield.WWWMask=attrs.get('WWWMask','')
      if attrs.get('WWWMaxValue',''):
         bfield.WWWMaxValue=attrs.get('WWWMaxValue','')
      if attrs.get('WWWMinValue',''):
         bfield.WWWMinValue=attrs.get('WWWMinValue','')
      if attrs.get('WWWNoSpace',''):
         bfield.WWWNoSpace=attrs.get('WWWNoSpace','')
      if attrs.get('WWWRegex',''):
         bfield.WWWRegex=attrs.get('WWWRegex','')
      if attrs.get('WWWTreeRecur',''):
         bfield.WWWTreeRecur=attrs.get('WWWTreeRecur','')
      if attrs.get('WWWTreeRecurObjects',''):
         bfield.WWWTreeRecurObjects=attrs.get('WWWTreeRecurObjects','')
      try:
         if attrs.get('WWWSortable',''):
            bfield.WWWSortable=attrs.get('WWWSortable','')
      except:
         pass
      if attrs.get('WWWUnsigned',''):
         bfield.WWWUnsigned=attrs.get('WWWUnsigned','')
      if attrs.get('WWWUpdateRefs',''):
         bfield.WWWUpdateRefs=attrs.get('WWWUpdateRefs','')
      if attrs.get('WWWUppercase',''):
         bfield.WWWUppercase=attrs.get('WWWUppercase','')
      if attrs.get('WWWUnique',''):
         bfield.WWWUnique=attrs.get('WWWUnique','')
      if attrs.get('FieldFormat',''):
         bfield.FieldFormat=attrs.get('FieldFormat','') #
      if attrs.get('IsReportProtected',''):
         bfield.IsReportProtected=attrs.get('IsReportProtected','')
      if attrs.get('Alignment',''):
         bfield.Alignment=attrs.get('Alignment','')
      if attrs.get('FieldEditor',''):
         feclass=aICORDBEngine.Classes['CLASSES_System_SystemDictionary_FieldEditor']
         feoid=feclass.Name.Identifiers(attrs.get('FieldEditor',''))
         if feoid>=0:
            bfield.FieldEditor=feclass.Name[feoid]

      if attrs.get('FieldAccess',''):
         aICORDBEngine.Classes.MetaField.aFieldAccess[bfield.FOID]=attrs.get('FieldAccess','')
      if attrs.get('FieldAlignment',''):
         aICORDBEngine.Classes.MetaField.aFieldAlignment[bfield.FOID]=attrs.get('FieldAlignment','')
      if attrs.get('FieldDefaultDblClickAction',''):
         aICORDBEngine.Classes.MetaField.aFieldDefaultDblClickAction[bfield.FOID]=attrs.get('FieldDefaultDblClickAction','')
      if attrs.get('FieldDefaultValue',''):
         aICORDBEngine.Classes.MetaField.aFieldDefaultValue[bfield.FOID]=attrs.get('FieldDefaultValue','')
      if attrs.get('FieldDescription',''):
         aICORDBEngine.Classes.MetaField.aFieldDescription[bfield.FOID]=attrs.get('FieldDescription','')
      if attrs.get('FieldHeight',''):
         aICORDBEngine.Classes.MetaField.aFieldHeight[bfield.FOID]=attrs.get('FieldHeight','')
      if attrs.get('FieldLeft',''):
         aICORDBEngine.Classes.MetaField.aFieldLeft[bfield.FOID]=attrs.get('FieldLeft','')
      if attrs.get('FieldLVColWidth',''):
         aICORDBEngine.Classes.MetaField.aFieldLVColWidth[bfield.FOID]=attrs.get('FieldLVColWidth','')
      if attrs.get('FieldNamePosition',''):
         aICORDBEngine.Classes.MetaField.aFieldNamePosition[bfield.FOID]=attrs.get('FieldNamePosition','')
      if attrs.get('FieldPosition',''):
         aICORDBEngine.Classes.MetaField.aFieldPosition[bfield.FOID]=attrs.get('FieldPosition','')
      if attrs.get('FieldSheetID',''):
         aICORDBEngine.Classes.MetaField.aFieldSheetID[bfield.FOID]=attrs.get('FieldSheetID','')
      if attrs.get('FieldTabIndex',''):
         aICORDBEngine.Classes.MetaField.aFieldTabIndex[bfield.FOID]=attrs.get('FieldTabIndex','')
      if attrs.get('FieldTop',''):
         aICORDBEngine.Classes.MetaField.aFieldTop[bfield.FOID]=attrs.get('FieldTop','')
#      if attrs.get('FieldValueAsString',''):
#         aICORDBEngine.Classes.MetaField.aFieldValueAsString[bfield.FOID]=attrs.get('FieldValueAsString','')
      if attrs.get('FieldWidth',''):
         aICORDBEngine.Classes.MetaField.aFieldWidth[bfield.FOID]=attrs.get('FieldWidth','')
      if attrs.get('IsCached',''):
         aICORDBEngine.Classes.MetaField.aIsCached[bfield.FOID]=attrs.get('IsCached','')
      if attrs.get('IsFastIndexed',''):
         aICORDBEngine.Classes.MetaField.aIsFastIndexed[bfield.FOID]=attrs.get('IsFastIndexed','')
      if attrs.get('IsIndexed',''):
         aICORDBEngine.Classes.MetaField.aIsIndexed[bfield.FOID]=attrs.get('IsIndexed','')
      if attrs.get('IsReadOnly',''):
         aICORDBEngine.Classes.MetaField.aIsReadOnly[bfield.FOID]=attrs.get('IsReadOnly','')
      if attrs.get('IsVirtual',''):
         aICORDBEngine.Classes.MetaField.aIsVirtual[bfield.FOID]=attrs.get('IsVirtual','')
      if attrs.get('SummaryDisabled',''):
         aICORDBEngine.Classes.MetaField.aSummaryDisabled[bfield.FOID]=attrs.get('SummaryDisabled','')
      if attrs.get('AllowReadGroups',''):
         aICORDBEngine.Classes.MetaField.aAllowReadGroups[bfield.FOID]=ICORSecurity.GetStringAsAccessLevelRefs(attrs.get('AllowReadGroups','')).AsString()
      if attrs.get('AllowWriteGroups',''):
         aICORDBEngine.Classes.MetaField.aAllowWriteGroups[bfield.FOID]=ICORSecurity.GetStringAsAccessLevelRefs(attrs.get('AllowWriteGroups','')).AsString()
      s=attrs.get('WWWMenuImageClosedField','')
      if s:
         sclass=aICORDBEngine.Classes.MetaField.aWWWMenuImageClosedField.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0 and s[:3]=='aa_':
            soid=sclass.Name.Identifiers(s[3:])
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClosedField "%(WWWMenuImageClosedField)s" w polu: %(Name)s w klasie %(ClassPath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaField.aWWWMenuImageClosedField[bfield.FOID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageField','')
      if s:
         sclass=aICORDBEngine.Classes.MetaField.aWWWMenuImageField.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0 and s[:3]=='aa_':
            soid=sclass.Name.Identifiers(s[3:])
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageField "%(WWWMenuImageField)s" w polu: %(Name)s w klasie %(ClassPath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaField.aWWWMenuImageField[bfield.FOID]=[soid,sclass.CID]
   def start_CLASSMENUDEFINITION(self, attrs):
      if NO_STRUCTURE_IMPORT:
         return
      bclass=aICORDBEngine.Classes[attrs['BasePath']]
      if bclass is None:
         return
      self.menubaseclass=bclass.GetDerivedClass(attrs['NameOfClass'])
   def start_MENUITEM(self,attrs):
      if NO_STRUCTURE_IMPORT:
         return
      if self.menubaseclass is None:
         return
      wc,wn=attrs.has_key('Caption'),attrs.has_key('Name')
      if wc and not wn:
         acaption=GetXMLStringAsString(attrs['Caption'])
         aname=acaption
      elif not wc and wn:
         aname=GetXMLStringAsString(attrs['Name'])
         acaption=aname
      elif wc and wn:
         aname=GetXMLStringAsString(attrs['Name'])
         acaption=GetXMLStringAsString(attrs['Caption'])
      if string.find(aname,'&#')>=0:
         aname=GetXMLStringAsString(aname)
      if string.find(acaption,'&#')>=0:
         acaption=GetXMLStringAsString(acaption)
      mrefs=self.menubaseclass.GetWWWMenuRefs()
      apos,afind=mrefs.FindRefByValue('Name',aname)
      moid=-1
      if afind:
         moid,mcid=mrefs[apos]
      aaction=attrs.get('Action','')
      if moid<0:
         moid=self.MenuClass.AddObject()
      self.MenuClass.Name[moid]=aname
      self.MenuClass.Caption[moid]=acaption
      if not aaction:
         aaction='MenuAsPage'
      toid=self.MenuClass.Action.ClassOfType.Name.Identifiers(aaction)
      if toid>=0:
         self.MenuClass.Action[moid]=[toid,self.MenuClass.Action.ClassOfType.CID]
      bmenu=MenuUtil.ICORWWWMenuItem(GetUID(),moid)
      la=['ParamItem','ParamSubItem','ParamValue1','ParamValue2','ParamValue3','AsPageSubCaption','AsPageDescription','AsPageShortDescription','AsPageCaption','ConfirmHRef']
      for sfn in la:
         sfv=GetXMLStringAsString(attrs.get(sfn,''))
         if sfv:          
            mfield=bmenu.MenuClass.FieldsByName(sfn)
            if mfield:
               mfield[bmenu.oid]=sfv
      if attrs.get('AccessLevel',''):
         bmenu.AccessLevel=ICORSecurity.GetStringAsAccessLevelRefs(GetXMLStringAsString(attrs.get('AccessLevel','')))
      if attrs.get('AccessLevelEdit',''):
         bmenu.AccessLevelEdit=ICORSecurity.GetStringAsAccessLevelRefs(GetXMLStringAsString(attrs.get('AccessLevelEdit','')))
      if attrs.get('AccessLevelStored',''):
         bmenu.AccessLevelStored=ICORSecurity.GetStringAsAccessLevelRefs(GetXMLStringAsString(attrs.get('AccessLevelStored','')))
      if attrs.has_key('worksheetqueryid'):
         bmenu.WorkSheetQueriesIDs=GetXMLStringAsString(attrs.get('worksheetqueryid',''))
      if not mrefs.RefExists(moid):
         mrefs.AddRef(moid,self.MenuClass.CID)
         mrefs.Store()
   def end_MENUITEM(self):
      pass
   def end_CLASSMENUDEFINITION(self):
      self.menubaseclass=None
   def start_METHODDEFINITION(self,attrs):
      if NO_STRUCTURE_IMPORT:
         return
      self.updatemethod=None
      self.methodlines=[]
      if not self.receivemethods:
         return
      bclass=aICORDBEngine.Classes[attrs.get('ClassPath','')]
      if bclass is None:
         print 'Dla metody %s nie istnieje klasa %s'%(attrs.get('Name',''),attrs.get('ClassPath',''))
         return
      if not bclass.IsMethodInThisClass(attrs.get('Name','')):
         mdef=ICORMethodDefinition(attrs.get('Name',''))
         mdef.MDescription=attrs.get('MethodDescription','') #GetXMLStringAsString(attrs.get('MethodDescription',''))
         mdef.MLanguage=attrs.get('Language','')
         mdef.MIsParallel=int(attrs.get('IsParallel','0'))
         bmethod=bclass.AddMethod(mdef)
         if bmethod is None:
            print 'Metoda %s nie zosta�a dodana!'%(attrs.get('Name',''),)
            return
         self.updatemethod=bmethod
         print 'dodano metod� %s w klasie %s'%(attrs.get('Name',''),attrs.get('ClassPath',''))
      else:
         bmethod=bclass.MethodsByName(attrs.get('Name',''))
         if bmethod is None:
            print 'Metoda %s nie istnieje!'%(attrs.get('Name',''),)
            return
         if self.alwaysupdatemethod:
            self.updatemethod=bmethod  
         else:
            alm=string.split(attrs.get('LastModified','9999 99 99 99 99 99 99'),' ')
            utime=GetListAsDateTuple(alm)
            mtime=str2DateTime(bmethod.LastModified)
            if utime>=mtime:
               self.updatemethod=bmethod
      bmethod.IsMenuHidden=attrs.get('IsMenuHidden','0')
      bmethod.IsQueued=attrs.get('IsQueued','0')
      bmethod.WWWMethod=attrs.get('WWWMethod','0')
      bmethod.WWWConfirmExecute=attrs.get('WWWConfirmExecute','0')
      bmethod.WWWDescription=attrs.get('WWWDescription','') #GetXMLStringAsString(attrs.get('WWWDescription',''))
      if attrs.get('AllowReadGroups',''):
         aICORDBEngine.Classes.MetaMethod.aAllowReadGroups[bmethod.MOID]=ICORSecurity.GetStringAsAccessLevelRefs(attrs.get('AllowReadGroups','')).AsString()
      if attrs.get('AllowWriteGroups',''):
         aICORDBEngine.Classes.MetaMethod.aAllowWriteGroups[bmethod.MOID]=ICORSecurity.GetStringAsAccessLevelRefs(attrs.get('AllowWriteGroups','')).AsString()
      s=attrs.get('WWWMenuImageLink','')
      if s:
         sclass=aICORDBEngine.Classes.MetaMethod.aWWWMenuImageLink.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0 and s[:3]=='aa_':
            soid=sclass.Name.Identifiers(s[3:])
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageLink "%(WWWMenuImageLink)s" w metodzie: %(Name)s w klasie %(ClassPath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaMethod.aWWWMenuImageLink[bmethod.MOID]=[soid,sclass.CID]
   def start_METHODLINE(self,attrs):
      if NO_STRUCTURE_IMPORT:
         return
      if not self.receivemethods or (self.updatemethod is None):
         return
      self.methodlines.append(attrs.get('Value','')) #GetXMLStringAsString(attrs.get('Value','')))
   def start_CLASS(self, attrs):
      acpath,acid=attrs.get('ClassPath',''),int(attrs['CID'])
      w=0
      if acpath:
         if acpath!=self.LastClassPath:
            self.LastClassPath=acpath
            self.aclass=aICORDBEngine.Classes[acpath]
            w=1
      elif self.LastCID!=acid:
         self.LastCID=acid
         self.aclass=aICORDBEngine.Classes[acid]
         w=1
      if w:
#      alm=string.split(attrs['LastModification'],' ')
         self.afield=None
         self.LastField=None
         self.acmethod=None
         self.afmethod=None
         self.aomethod=None
         self.ismemo=0
         self.classmodified=0
#         if not self.aclass is None:
#            InfoStatus(self.aclass.NameOfClass)
      if self.aclass is None:
         print '*** Class:',acpath,'[',acid,'] is None! ***'
         return
      if self.importmethodexecute:
         self.acmethod=self.aclass.MethodsByName('OnClassImport')
      if not self.acmethod is None:
         aICORDBEngine.Variables._AllowClassImport='1'
         self.acmethod.Execute('',-1,'0')
         if aICORDBEngine.Variables._AllowClassImport!='1':
            self.acmethod=None
            self.aclass=None
            return
#         self.adtclass=GetListAsDateTuple(alm,0)
      if self.importmethodexecute:
         self.afmethod=self.aclass.MethodsByName('OnFieldImport')
         self.aomethod=self.aclass.MethodsByName('OnObjectImport')
#         if self.verbose:
#            print self.aclass.ClassPath,self.adtclass
   def start_FIELD(self,attrs):
      if self.aclass is None:
         return
      fname=attrs['Name']
      if fname=='Password' and self.aclass.CID==aICORDBEngine.User.CID:
         aICORDBEngine.UserVars['PasswordChange']=1
      else:
         aICORDBEngine.UserVars['PasswordChange']=0
      if self.LastField!=fname:
         self.LastField=fname
         self.afield=self.aclass.FieldsByName(fname)
#         InfoStatus(self.aclass.NameOfClass+':'+fname)
      if not self.afield is None:
         if not self.afmethod is None:
            aICORDBEngine.Variables._AllowFieldImport='1'
            self.afmethod.Execute(self.afield.Name)
            if aICORDBEngine.Variables._AllowFieldImport!='1':
               self.afield=None
               return
         self.ismemo=self.afield.IsMemo
      self.wupdaterefs=0
      if not self.afield is None:
         if not self.afmethod is None:
            ret=self.afmethod(FieldName=self.afield.Name,Value='updaterefs')
            if type(ret)==type(1) and ret==1:
               self.wupdaterefs=1
#         alm=string.split(attrs['LastModification'],' ')
#         self.adtfield=GetListAsDateTuple(alm,0)
#         if self.verbose:
#            print '  ',self.afield.Name,self.ismemo,self.adtfield
   def TranslateOID(self,aoid):
      for aoidmin,aoidmax,aadd in TRANSLATE_OID:
         if aoid>=aoidmin and aoid<aoidmax:
            aoid=aoid+aadd
            break
      return aoid
   def TranslateValue(self,avalue):
      s=avalue
      for s1,s2 in TRANSLATE_VALUE:
         s=string.replace(avalue,s1,s2)
      def dorepl(amatch,self=self):
         i=int(amatch.group(amatch.lastindex))
         i=self.TranslateOID(i)
         return str(i)
      if TRANSLATE_VALUE_RE:
         s=re.sub(TRANSLATE_VALUE_RE,dorepl,s)
      return s
   def start_OBJECT(self,attrs):
      if self.afield is None:
         return
      self.aoid=self.TranslateOID(int(attrs['OID']))
      alm=string.split(attrs['LastModification'],' ')
      self.adtobject=GetListAsDateTuple(alm)
      self.avalue=''
   def start_FIELDVALUE(self,attrs):
      self.start_CLASS(attrs)
      self.start_FIELD(attrs)
      self.start_OBJECT(attrs)
   def start_DATA(self,attrs):
      self.avalueline=''
   def handle_data(self,data):
      self.avalueline=self.avalueline+data
   def end_DATA(self):
      if self.avalue=='':
         self.avalue=self.avalueline
      else:
         self.avalue=self.avalue+'\n'+self.avalueline
   def end_OBJECT(self):
      if self.aclass is None:
         return
      if self.afield is None:
         return
      if not self.afield.ClassOfType is None and self.dACL_CIDs.has_key(self.afield.ClassOfType.CID):
         self.avalue=self.TranslateValue(self.avalue)
         arefs=ICORSecurity.GetStringAsAccessLevelRefs(self.avalue,self.dACL_CIDs[self.afield.ClassOfType.CID])
         self.avalue=arefs.AsString()
      elif not self.afield.ClassOfType is None:
         acid=self.afield.ClassOfType.CID
         arefs=FieldRefIterator(self.avalue)
         for i in range(len(arefs.refs)):
            arefs.refs[i][0]=self.TranslateOID(arefs.refs[i][0])
            arefs.refs[i][1]=acid
         self.avalue=arefs.AsString()
      else:
         self.avalue=self.TranslateValue(self.avalue)
      wu=1
#      try:
      if not self.overridedeleted and self.aclass.IsObjectDeleted(self.aoid) and aICORDBEngine.IsAdministrator:
         wu=0
#      except:
#         print 'Except!'
#         wu=0
      if not self.allowupdateprotected and self.afield.IsReportProtected=='1':
         wu=0
#      if wu and not self.ismemo and self.afield[self.aoid]==self.avalue:
#         wu=0
      if wu and (not self.aomethod is None):
         if self.verbose:
            print '*** Execute ***'
         aICORDBEngine.Variables._AllowObjectImport='1'
         aICORDBEngine.Variables._ObjectImportValue=self.avalue
         aICORDBEngine.Variables._ObjectImportDate=tdatetime2fmtstr(self.adtobject)
         self.aomethod.Execute(self.afield.Name,self.aoid)
         if aICORDBEngine.Variables._AllowObjectImport!='1':
            wu=0
         else:
            if not self.ismemo:
               self.avalue=aICORDBEngine.Variables._ObjectImportValue
      if wu:
         if not self.aclass.ObjectExists(self.aoid):
            self.aclass.CreateObjectByID(self.aoid)
         if self.wupdaterefs and not self.afield.ClassOfType is None:
            self.afield.AddRefs(self.aoid,arefs.refs,ainsertifnotexists=1)
         else:
            self.afield[self.aoid]=self.avalue
         self.afield.SetValueLastModified(self.aoid,self.adtobject)
         self.classmodified=1
         if self.verbose:
            if not self.ismemo:
               print '      %d %s >%s<' % (self.aoid,str(self.adtobject),self.avalue)
            else:
               print '      %d %s' % (self.aoid,str(self.adtobject))
               print self.avalue
   def end_FIELDVALUE(self):
      self.end_OBJECT()
      self.end_FIELD()
      self.end_CLASS()
   def end_FIELD(self):
      pass
   def end_CLASS(self):
      aICORDBEngine.UserVars['PasswordChange']=0
      if self.aclass is None or not self.classmodified:
         return
      if not self.aclass.IsSystem=='1' and self.aclass.AllowRead=='1':
         if not self.acmethod is None:
            self.acmethod.Execute('',-1,'1')
   def end_METHODLINE(self):
      pass
   def end_METHODDEFINITION(self):
      if NO_STRUCTURE_IMPORT:
         return
      if not self.receivemethods or (self.updatemethod is None):
         return
      self.methodlines.append('')
      self.updatemethod.MethodText=string.join(self.methodlines,'\n')
#      print 'zmodyfikowano tre�� metody %s'%(self.updatemethod.MethodPath,)
   def end_FIELDDEFINITION(self):
      pass
   def end_CLASSDEFINITION(self):
      pass
   def end_REPLICATION(self):
      pass
   def start_MENUPAGEHTML(self,attrs):
      pass
   def end_MENUPAGEHTML(self):
      pass
   def start_MENUPAGEHTMLLINE(self,attrs):
      pass
   def end_MENUPAGEHTMLLINE(self):
      pass
   def start_REPORTS(self,attrs):
      pass
   def end_REPORTS(self):
      pass
   def start_REPORTITEM(self,attrs):
      pass
   def end_REPORTITEM(self):
      pass
   def syntax_error(self, lineno, message):
      print 'error in data at line %d:' % lineno, message
   def unknown_starttag(self, tag, attrs):
      print 'unknown starttag:',tag
   def unknown_endtag(self, tag):
      print 'unknown endtag:',tag
   def unknown_entityref(self, ref):
      print 'unknown entityref:',ref
   def unknown_charref(self, ref):
      print 'unknown charref:',ref

def ReceiveReplicationByFTP(aprofile,afilereceived=None,aparseallfiles=0):
   ClearStdOut()
   aparser=ICORXMLReplicationParser(aprofile)
   arefs=aparser.ProfileClass.FTPProfile.GetRefList(aparser.OID)
   if not afilereceived:
      ftp=GetReplicationFTP(arefs)
      if ftp is None:
         MessageDialog('B��d podczas nawi�zywania komunikacji z serwerem.\nSprawd�, czy serwer jest aktywny.',mtError,mbOK)
         return
      afilepath=FilePathAsSystemPath(arefs.FTPLocalDir[arefs.OID])
   else:
      ftp=None
      afilepath,afilereceived=os.path.split(FilePathAsSystemPath(afilereceived))
   try:
      afmanager=FTPFileManager(ftp)
      if ftp:
         flist=afmanager.GetFileList()
      else:
         flist=[afilereceived]
      for afile in flist:
         fnl=string.split(afile,'_')
         if len(afile)>2 and afile[-3:]=='.gz' and (aparseallfiles or fnl[0]==str(aICORDBEngine.SystemOwnerUserID) or fnl[0]=='-1'):
            afmanager.Download(afile,afilepath)
            afmanager.Move(afile,'archive/')
            afmanager.CloseFile()
            try:
               afpath=afilepath
               if afpath[-1]!='\\':
                  afpath=afpath+'\\'
               afpath=afpath+afile
               print 'Parse:',afpath
               aparser.Parse(afpath)
            finally:
               pass
#               try:
#                  os.unlink(afpath)
#               except:
#                  pass
   finally:
      del afmanager
      if ftp:
         ftp.quit()
   MessageDialog('Koniec pobierania danych.',mtInformation,mbOK)   

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   ReceiveReplicationByFTP('Default')
#   return
   if OID>=0:
      aparser=ICORXMLReplicationParser(OID)
   else:
      MessageDialog('Aby odebra� informacje o zmianach nale�y wybra� profil.',mtError,mbOK)
      return
   aparser.Parse()



