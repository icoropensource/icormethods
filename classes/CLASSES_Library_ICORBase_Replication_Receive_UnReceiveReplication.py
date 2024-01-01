# -*- coding: windows-1250 -*-
# saved: 2021/06/08 16:39:02

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_NetBase_Utils_XMLUtil import *
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import icorlib.wwwmenu.menuutil as MenuUtil
import icorlib.wwwmenu.xmlmenuutil as XMLMenuUtil
import xmllib #from xml.parsers 
import os
import string

ReplicationException = 'ReplicationException'

NO_STRUCTURE_IMPORT=0

def GetListAsDateTuple(alist,x=0):
   return (int(alist[x]),int(alist[x+1]),int(alist[x+2]),int(alist[x+3]),int(alist[x+4]),int(alist[x+5]),int(alist[x+6]))

class ICORXMLReplicationParser(xmllib.XMLParser):
   def __init__(self,aprofile):
      global NO_STRUCTURE_IMPORT
      NO_STRUCTURE_IMPORT=1
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
      if fname!='':
         self.afile=fname
      if self.afile=='':
         raise ReplicationException,'No file'
      self.afile=FilePathAsSystemPath(self.afile)
      self.logfname=self.afile+'.log'
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
      self.stopparsing=0
      self.fields_history={}
      fsize=os.path.getsize(self.afile)
      self.valuecnt=0
      f=open(self.afile,'r')
      i=0
      try:
         s=f.readline()
         while s!='' and not self.stopparsing:
            self.feed(s[:-1])
            i=i+1
            if i>=120:
               i=0
               apos=f.tell()
               SetProgress(apos,fsize)
            s=f.readline()
         if not self.stopparsing:
            self.close()
      finally:
         f.close()
         SetProgress(0,0)
#      InfoStatus('')
   def Log(self,s=''):
      f=open(self.logfname,'a+')
      if s[-1:]!='\n':
         s=s+'\n'
      f.write(s)
      f.close()
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
      print '?'
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
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClass "%(WWWMenuImageClass)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageClass[nclass.CID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageClosedClass','')
      if s:
         sclass=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedClass.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClosedClass "%(WWWMenuImageClosedClass)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedClass[nclass.CID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageClosedObject','')
      if s:
         sclass=aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedObject.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClosedObject "%(WWWMenuImageClosedObject)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageClosedObject[nclass.CID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageObject','')
      if s:
         sclass=aICORDBEngine.Classes.MetaClass.aWWWMenuImageObject.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageObject "%(WWWMenuImageObject)s" w klasie: %(NameOfClass)s w klasie %(BasePath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaClass.aWWWMenuImageObject[nclass.CID]=[soid,sclass.CID]
   def start_FIELDDEFINITION(self, attrs):
      if NO_STRUCTURE_IMPORT:
         return
      print '?'
      return
      bclass=aICORDBEngine.Classes[attrs.get('ClassPath','')]
      ftid=aICORDBEngine.Classes.GetTypeIDByType(attrs.get('FieldType',''))
      if ftid<0:
         print 'Pole %s w klasie %s posiada nieprawidłowy typ: %s'%(attrs.get('Name',''),attrs.get('ClassPath',''),attrs.get('FieldType',''))
      if bclass.IsFieldInClass(attrs.get('Name','')):
         bfield=bclass.FieldsByName(attrs.get('Name',''))
         if bfield.FieldTID!=ftid:
            print 'Pole %s w klasie %s posiada inny typ (%s) niż zadeklarowany w replikacji nieprawidłowy typ: %s'%(attrs.get('Name',''),attrs.get('ClassPath',''),bfield.FieldType,attrs.get('FieldType',''))
            return
      else:
         fdef=ICORFieldDefinition(attrs['Name'],ftid)
         fdef.FInteractive=int(attrs.get('IsInteractive',''))
         fdef.FObligatory=int(attrs.get('IsObligatory',''))
         fdef.FContainerType=int(attrs.get('IsContainer',''))
         fdef.FAlias=int(attrs.get('IsAliased',''))
         bfield=bclass.AddField(fdef)
         if bfield is None:
            print 'Pole %s w klasie %s nie zostało dodane!'%(attrs.get('Name',''),attrs.get('ClassPath',''))
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
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageClosedField "%(WWWMenuImageClosedField)s" w polu: %(Name)s w klasie %(ClassPath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaField.aWWWMenuImageClosedField[bfield.FOID]=[soid,sclass.CID]
      s=attrs.get('WWWMenuImageField','')
      if s:
         sclass=aICORDBEngine.Classes.MetaField.aWWWMenuImageField.ClassOfType
         soid=sclass.Name.Identifiers(s)
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageField "%(WWWMenuImageField)s" w polu: %(Name)s w klasie %(ClassPath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaField.aWWWMenuImageField[bfield.FOID]=[soid,sclass.CID]
   def start_CLASSMENUDEFINITION(self, attrs):
      if NO_STRUCTURE_IMPORT:
         return
      print '?'
      return
      bclass=aICORDBEngine.Classes[attrs['BasePath']]
      if bclass is None:
         return
      self.menubaseclass=bclass.GetDerivedClass(attrs['NameOfClass'])
   def start_MENUITEM(self,attrs):
      if NO_STRUCTURE_IMPORT:
         return
      print '?'
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
      print '?'
      return
      self.updatemethod=None
      self.methodlines=[]
      if not self.receivemethods:
         return
      bclass=aICORDBEngine.Classes[attrs.get('ClassPath','')]
      if not bclass.IsMethodInThisClass(attrs.get('Name','')):
         mdef=ICORMethodDefinition(attrs.get('Name',''))
         mdef.MDescription=attrs.get('MethodDescription','') #GetXMLStringAsString(attrs.get('MethodDescription',''))
         mdef.MLanguage=attrs.get('Language','')
         mdef.MIsParallel=int(attrs.get('IsParallel','0'))
         bmethod=bclass.AddMethod(mdef)
         if bmethod is None:
            print 'Metoda %s nie została dodana!'%(attrs.get('Name',''),)
            return
         self.updatemethod=bmethod
         print 'dodano metodę %s w klasie %s'%(attrs.get('Name',''),attrs.get('ClassPath',''))
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
         if soid<0:
            print 'nieistniejacy atrybut WWWMenuImageLink "%(WWWMenuImageLink)s" w metodzie: %(Name)s w klasie %(ClassPath)s'%attrs
         else:
            aICORDBEngine.Classes.MetaMethod.aWWWMenuImageLink[bmethod.MOID]=[soid,sclass.CID]
   def start_METHODLINE(self,attrs):
      if NO_STRUCTURE_IMPORT:
         return
      print '?'
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
      if not self.afield is None:
         self.ismemo=self.afield.IsMemo
#         alm=string.split(attrs['LastModification'],' ')
#         self.adtfield=GetListAsDateTuple(alm,0)
#         if self.verbose:
#            print '  ',self.afield.Name,self.ismemo,self.adtfield
   def start_OBJECT(self,attrs):
      if self.afield is None:
         return
      self.aoid=int(attrs['OID'])
      alm=string.split(attrs['LastModification'],' ')
      self.adtobject=GetListAsDateTuple(alm)
      self.avalue=''
   def start_FIELDVALUE(self,attrs):
      if self.stopparsing:
         return
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
         arefs=ICORSecurity.GetStringAsAccessLevelRefs(self.avalue,self.dACL_CIDs[self.afield.ClassOfType.CID])
         self.avalue=arefs.AsString()
      elif not self.afield.ClassOfType is None:
         acid=self.afield.ClassOfType.CID
         arefs=FieldRefIterator(self.avalue)
         for i in range(len(arefs.refs)):
            arefs.refs[i][1]=acid
         self.avalue=arefs.AsString()
      wu=1
#      if not self.overridedeleted and self.aclass.IsObjectDeleted(self.aoid) and aICORDBEngine.IsAdministrator:
#         wu=0
#      if not self.allowupdateprotected and self.afield.IsReportProtected=='1':
#         wu=0
#      if wu and not self.ismemo and self.afield[self.aoid]==self.avalue:
#         wu=0
      if wu:
         self.PrepareHistory(self.afield)
         ev=self.afield[self.aoid]
         edt=self.afield.GetValueLastModified(self.aoid)
         astate,odt,ov=self.GetHistoryValue(self.afield,self.aoid,edt,ev,self.adtobject,self.avalue,(2006, 4, 19, 14, 17, 0, 0))
         #(2006, 4, 19, 14, 19, 44, 737)
#         if ov!=self.avalue or odt!=self.adtobject:
#            print self.afield.Name,self.afield.CID
#            print '      %d %s %s' % (self.aoid,str(odt),ov[:40])
#            print '      %d %s %s' % (self.aoid,str(self.adtobject),self.avalue[:40])
         if 1:
            self.afield[self.aoid]=ov
            self.afield.SetValueLastModified(self.aoid,odt)
            self.classmodified=1
   def PrepareHistory(self,afield):
      if self.fields_history.has_key(afield.FOID):
         return
#      print 'preparing history for field:',afield.Name,afield.CID
      aoffset=afield.GetFirstDeletedOffset()
      while aoffset>=0:
         avalue=afield.GetRecValueAsString(aoffset)
         adt=afield.GetRecLastModification(aoffset)
         aoid=afield.GetRecOID(aoffset)
         df=self.fields_history.get(afield.FOID,{})
         lo=df.get(aoid,[])
         lo.insert(0,[adt,avalue])
         df[aoid]=lo
         self.fields_history[afield.FOID]=df
         aoffset=afield.GetNextDeletedOffset(aoffset)
   def GetHistoryValue(self,afield,aoid,edt,ev,ndt,nv,mdt):
      seq='EQ'
      if ev!=nv:
         seq='NQ'
      self.Log('printing history for field: '+afield.Name+' '+str(afield.CID)+' '+str(aoid)+' '+seq)
      self.Log('    original value: '+str(edt)+' '+ev[:40])
      self.Log('    XML value: '+str(ndt)+' '+nv[:40])
      df=self.fields_history.get(afield.FOID,{})
      lo=df.get(aoid,[])
      if lo:
         astate=0
         adt,avalue=lo[0][0],lo[0][1]
#         for adt,avalue in lo[:10]:
#            return 0,adt,avalue
#            self.Log('     '+str(aoid)+' '+str(adt)+' '+avalue[:40])
      elif ndt==edt:
         astate=1
         adt=edt
         avalue=ev
#         adt=(1899, 12, 30, 0, 0, 0, 0)
#         avalue=''
      else:
         astate=2
         adt=ndt
         avalue=nv
#      avalue=afield.ValuesAsString(aoid)
#      adt=afield.GetValueLastModified(aoid)
#      return 1,adt,avalue
      self.Log('    Result: '+str(astate)+' '+str(adt)+' '+avalue[:40])
      return astate,adt,avalue
   def end_FIELDVALUE(self):
      self.end_OBJECT()
      self.end_FIELD()
      self.end_CLASS()
      self.valuecnt=1+self.valuecnt
#      if self.valuecnt>100:
#         self.stopparsing=1
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
      print '?'
      return
      if not self.receivemethods or (self.updatemethod is None):
         return
      self.methodlines.append('')
      self.updatemethod.MethodText=string.join(self.methodlines,'\n')
      print 'zmodyfikowano treść metody %s'%(self.updatemethod.MethodPath,)
   def end_FIELDDEFINITION(self):
      pass
   def end_CLASSDEFINITION(self):
      pass
   def end_REPLICATION(self):
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

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   ReceiveReplicationByFTP('Default')
#   return
   OID=10
   if OID>=0:
      aparser=ICORXMLReplicationParser(OID)
   else:
      MessageDialog('Aby odebrać informacje o zmianach należy wybrać profil.',mtError,mbOK)
      return
   aparser.Parse()



