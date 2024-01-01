# -*- coding: windows-1250 -*-
# saved: 2021/06/08 16:39:15

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import ICORRepositoryIterator
from CLASSES_Library_NetBase_Utils_XMLUtil import *
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import icorlib.wwwmenu.menuutil as MenuUtil
import icorlib.wwwmenu.xmlmenuutil as XMLMenuUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import string
import time

# FTP replication
from CLASSES_Library_NetBase_Utils_FTPUtil import *
from ftplib import FTP
import os          

ReplicationException = 'ReplicationException'

OIDs_ACCEPTED={}

DISABLE_StructDefinitions=0

class ICORReplicationIterator:
   def __init__(self,aprofile,atargetuser=-1,afile='',adatefrom=(),acallbackobjectfunc=None,adisablestructdefinitions=DISABLE_StructDefinitions):
      self.CallbackObjectFunc=acallbackobjectfunc
      self.ProfileClass=aICORDBEngine.Classes['CLASSES/Library/ICORBase/Replication/Send']
      if self.ProfileClass is None:
         raise ReplicationException,'Profile class does not exists'
      if type(aprofile)==type(1):
         self.OID=aprofile
      else:
         self.OID=self.ProfileClass.Name.Identifiers(aprofile)
      if self.OID<0:
         raise ReplicationException,'Profile does not exists'
      if afile=='':
         self.afile=self.ProfileClass.OutputFile[self.OID]
      else:
         self.afile=afile
      if adatefrom==():
         self.adate=self.ProfileClass.DateFrom.ValuesAsDateTime(self.OID)
      else:
         self.adate=adatefrom
      self.adatecreated=self.ProfileClass.DateCreated.ValuesAsDateTime(self.OID)
      if self.adatecreated==ZERO_DATE:
         self.adatecreated=tdatetime()
      arefs=self.ProfileClass.TargetUser.GetRefList(self.OID)
      if arefs.position>=0:
         self.targetuser=arefs.OID
      else:
         self.targetuser=-1
      if atargetuser>=0:
         self.targetuser=atargetuser
      self.disableStructDefinitions=adisablestructdefinitions
      self.allowsystem=self.ProfileClass.AllowSystem.ValuesAsInt(self.OID)
      self.disableclassmethods=self.ProfileClass.DisableClassMethods.ValuesAsInt(self.OID)
      self.disablefieldmethods=self.ProfileClass.DisableFieldMethods.ValuesAsInt(self.OID)
      self.disableobjectmethods=self.ProfileClass.DisableObjectMethods.ValuesAsInt(self.OID)
      self.sendmethods=self.ProfileClass.SendMethods.ValuesAsInt(self.OID)
      self.file=None
      c1=aICORDBEngine.Classes['CLASSES_System_GroupAccessLevel']
      c2=aICORDBEngine.Classes['CLASSES_System_GroupItemAccessLevel']
      self.dACL_CIDs={c1.CID:c1,c2.CID:c2}
      arefs=self.ProfileClass.OIDRanges.GetRefList(self.OID)
      self.ObjectsDisabled=0
      self.OIDRanges=[]
      while arefs:
         amin=arefs.IDMin.ValuesAsInt(arefs.OID)
         if amin>=2000000000:
            self.ObjectsDisabled=1
         self.OIDRanges.append([amin,arefs.IDMax.ValuesAsInt(arefs.OID)])
         arefs.Next()
   def Generate(self,fname=''):
      if fname!='':
         self.afile=fname
      if self.afile=='':
         raise ReplicationException,'File does not exists'
      self.file=MXMLFile(self.afile)
      self.file.Header()
      self.file.TagOpen('REPLICATION')
      d={'SourceUser':aICORDBEngine.SystemOwnerUserID,'TargetUser':self.targetuser,'DateFrom':self.adate,'Created':self.adatecreated}
      self.file.TagOpen('HEADER',d,aclosetag=1)
#iterate
      self.ClassCount=0
      self.ClassFieldsDict={}
      bobj=self.ProfileClass[self.OID]
      cobj=bobj.BaseClasses
      self.CheckedObjectCache={}
      self.CheckedClasses={}
      cpos,cmax=1,len(cobj)
      while cobj:
         isclassrecursive=0
         if cobj.Class.IsClassRecursive.ValuesAsInt(cobj.OID)>0:
            isclassrecursive=1
         isfieldrecursive=0
         if cobj.Class.IsFieldRecursive.ValuesAsInt(cobj.OID)>0:
            isfieldrecursive=1
         self.bpath=cobj.Name
         bclass=aICORDBEngine.Classes[self.bpath]
         if bclass is None:
            cobj.Next()
            continue
         self.Status=str(cpos)+'/'+str(cmax)+' : '+bclass.NameOfClass
         cpos=cpos+1
         InfoStatus(self.Status)
         if not bclass is None:
            self.RecurObjects=[]
            aobj=bclass.GetFirstObject()
            self.OnClass(bclass,aobj,isclassrecursive,isfieldrecursive,0)
         cobj.Next()
# write footer
      self.file.TagClose('REPLICATION')
      if not self.file is None:
         self.file.close()
      self.CheckedObjectCache={}
      SetProgress(0,0)
      InfoStatus('')
   def IsOIDInRange(self,aoid,acid=-1):
      if acid>=0:
         l=OIDs_ACCEPTED.get(acid,[])
         if l:
            if aoid in l:
               return 1
            return 0
      if not self.OIDRanges:
         return 1
      for aidmin,aidmax in self.OIDRanges:
         if aoid>=aidmin and aoid<=aidmax:
            return 1
      return 0
   def CheckClasses(self,aclass):
      if self.disableStructDefinitions:
         return 0
      DoEvents()
      bclass=aICORDBEngine.Classes[aclass.BasePath]
      if (bclass is not None) and (self.CheckedClasses.get(bclass.CID,0)==0):
         self.CheckClasses(bclass)
      if self.CheckedClasses.get(aclass.CID,0)==0:
         arefs=aclass.EditorSheets
         lsheets=[]
         while arefs:
            lsheets.append(arefs.Name[arefs.OID]+chr(9)+arefs.WWWDisabled[arefs.OID])
            arefs.Next()
         seditorsheets=string.join(lsheets,chr(10))
         sWWWMenuImageClass,sWWWMenuImageClosedClass,sWWWMenuImageObject,sWWWMenuImageClosedObject='','','',''
         arefs=aclass.WWWMenuImageClass
         if arefs:
            sWWWMenuImageClass=arefs.Name[arefs.OID]
         arefs=aclass.WWWMenuImageClosedClass
         if arefs:
            sWWWMenuImageClosedClass=arefs.Name[arefs.OID]
         arefs=aclass.WWWMenuImageObject
         if arefs:
            sWWWMenuImageObject=arefs.Name[arefs.OID]
         arefs=aclass.WWWMenuImageClosedObject
         if arefs:
            sWWWMenuImageClosedObject=arefs.Name[arefs.OID]
         if not self.disableStructDefinitions:
            d={
               'AllowReadGroups':ICORSecurity.GetAccessLevelRefsAsString(aclass.AllowReadGroups),
               'AllowWriteGroups':ICORSecurity.GetAccessLevelRefsAsString(aclass.AllowWriteGroups),
               'BasePath':GetSafeRepositoryPath(aclass.BasePath),
               'NameOfClass':aclass.NameOfClass,
               'ClassColIDWidth':aclass.ClassColIDWidth,
               'ClassDescription':aclass.ClassDescription,
               'ClassFieldsHidden':aclass.ClassFieldsHidden,
               'ClassFormHeight':aICORDBEngine.Classes.MetaClass.aClassFormHeight[aclass.CID],
               'ClassFormLeft':aICORDBEngine.Classes.MetaClass.aClassFormLeft[aclass.CID],
               'ClassFormTop':aICORDBEngine.Classes.MetaClass.aClassFormTop[aclass.CID],
               'ClassFormWidth':aICORDBEngine.Classes.MetaClass.aClassFormWidth[aclass.CID],
               'EditorSheets':seditorsheets,
               'IsReadOnly':aclass.IsReadOnly,
               'IsSystem':aclass.IsSystem,
               'IsVirtual':aclass.IsVirtual,
               'ReportClass':aclass.ReportClass,
               'Summaries':'',
               'WWWDescription':aclass.WWWDescription,
               'WWWDisableDescription':aclass.WWWDisableDescription,
               'WWWEditPageBottomHTML':'',
               'WWWEditPageTopHTML':'',
               'WWWJumpToBackRefObject':aclass.WWWJumpToBackRefObject,
               'WWWMenu':'',
               'WWWMenuImageClass':sWWWMenuImageClass,
               'WWWMenuImageClosedClass':sWWWMenuImageClosedClass,
               'WWWMenuImageClosedObject':sWWWMenuImageClosedObject,
               'WWWMenuImageObject':sWWWMenuImageObject,
               'WWWMaxColDictDescription':aclass.WWWMaxColDictDescription,
            }
            self.file.TagOpen('CLASSDEFINITION',d,aclosetag=1)
         self.CheckedClasses[aclass.CID]=1
         flist=aclass.GetFieldsList()
         for afname in flist:
            afield=aclass.FieldsByName(afname)
            if afield.ClassOfType is not None:
               self.CheckClasses(afield.ClassOfType)
            sWWWMenuImageClosedField,sWWWMenuImageField='',''
            arefs=afield.WWWMenuImageClosedField
            if arefs:
               sWWWMenuImageClosedField=arefs.Name[arefs.OID]
            arefs=afield.WWWMenuImageField
            if arefs:
               sWWWMenuImageField=arefs.Name[arefs.OID]
            if not self.disableStructDefinitions:
               try:
                  d={
                     'Alignment':afield.Alignment,
                     'AllowReadGroups':ICORSecurity.GetAccessLevelRefsAsString(afield.AllowReadGroups),
                     'AllowWriteGroups':ICORSecurity.GetAccessLevelRefsAsString(afield.AllowWriteGroups),
                     'ClassPath':GetSafeRepositoryPath(aclass.ClassPath),
                     'FieldAccess':afield.FieldAccess,
                     'FieldAlignment':aICORDBEngine.Classes.MetaField.aFieldAlignment[afield.FOID],
                     'FieldDefaultDblClickAction':afield.FieldDefaultDblClickAction,
                     'FieldDefaultValue':afield.FieldDefaultValueAsString,
                     'FieldDescription':afield.FieldDescription,
                     'FieldEditor':afield.FieldEditor,
                     'FieldFormat':afield.FieldFormat,
                     'FieldHeight':afield.FieldHeight,
                     'FieldLeft':afield.FieldLeft,
                     'FieldLVColWidth':afield.FieldLVColWidth,
                     'Name':afield.Name,
                     'FieldNameAsDisplayed':afield.FieldNameAsDisplayed,
                     'FieldNamePosition':afield.FieldNamePosition,
                     'FieldPosition':afield.FieldPosition,
                     'FieldSheetID':afield.FieldSheetID,
                     'FieldTabIndex':afield.FieldTabIndex,
                     'FieldTop':afield.FieldTop,
                     'FieldType':afield.FieldType,
                     'FieldValueAsString':afield.FieldValueAsString,
                     'FieldWidth':afield.FieldWidth,
                     'IsAliased':afield.IsAliased,
                     'IsCached':afield.IsCached,
                     'IsContainer':afield.IsContainer,
                     'IsFastIndexed':afield.IsFastIndexed,
                     'IsIndexed':afield.IsIndexed,
                     'IsInteractive':afield.IsInteractive,
                     'IsObligatory':afield.IsObligatory,
                     'IsReadOnly':afield.IsReadOnly,
                     'IsReportProtected':afield.IsReportProtected,
                     'IsVirtual':afield.IsVirtual,
                     'SummaryDisabled':aICORDBEngine.Classes.MetaField.aSummaryDisabled[afield.FOID],
                     'WWWBackRefField':afield.WWWBackRefField,
                     'WWWDefaultCheck':afield.WWWDefaultCheck,
                     'WWWDefaultInput':afield.WWWDefaultInput,
                     'WWWDefaultValue':afield.WWWDefaultValue,
                     'WWWDisabled':afield.WWWDisabled,
                     'WWWFilter':afield.WWWFilter,
                     'WWWLowercase':afield.WWWLowercase,
                     'WWWMask':afield.WWWMask,
                     'WWWMaxValue':afield.WWWMaxValue,
                     'WWWMenuImageClosedField':sWWWMenuImageClosedField,
                     'WWWMenuImageField':sWWWMenuImageField,
                     'WWWMinValue':afield.WWWMinValue,
                     'WWWNoSpace':afield.WWWNoSpace,
                     'WWWRegex':afield.WWWRegex,
                     'WWWSingleValue':afield.WWWSingleValue,
                     'WWWTreeRecur':afield.WWWTreeRecur,
                     'WWWTreeRecurObjects':afield.WWWTreeRecurObjects,
                     'WWWSortable':afield.WWWSortable,
                     'WWWUnique':afield.WWWUnique,
                     'WWWUnsigned':afield.WWWUnsigned,
                     'WWWUpdateRefs':afield.WWWUpdateRefs,
                     'WWWUppercase':afield.WWWUppercase,
                  }
               except:
                  print 'ERROR #1:',aclass.CID,afname
                  raise
               self.file.TagOpen('FIELDDEFINITION',d,aclosetag=1)
         mrefs=aclass.GetWWWMenuRefs()
         if mrefs:
            if not self.disableStructDefinitions:
               d={
                  'BasePath':GetSafeRepositoryPath(aclass.BasePath),
                  'NameOfClass':aclass.NameOfClass,
               }
               self.file.TagOpen('CLASSMENUDEFINITION',d,aclosetag=0)
               aexporter=XMLMenuUtil.XMLMenuExporter()
               while mrefs:
                  amenu=MenuUtil.ICORWWWMenuItem(GetUID(),mrefs.OID)
                  aexporter.XMLExportSingleItem(amenu,self.file)
                  mrefs.Next()
               self.file.TagClose('CLASSMENUDEFINITION')
         if self.sendmethods and not self.disableStructDefinitions:
            mlist=aclass.GetMethodsList(ainherited=0)
            for amname in mlist:
               amethod=aclass.MethodsByName(amname)
               sWWWMenuImageLink=''
               arefs=amethod.WWWMenuImageLink
               if arefs:
                  sWWWMenuImageLink=arefs.Name[arefs.OID]
               d={
                  'AllowReadGroups':ICORSecurity.GetAccessLevelRefsAsString(amethod.AllowReadGroups),
                  'AllowWriteGroups':ICORSecurity.GetAccessLevelRefsAsString(amethod.AllowWriteGroups),
                  'ClassPath':GetSafeRepositoryPath(aclass.ClassPath),
                  'IsMenuHidden':amethod.IsMenuHidden,
                  'IsParallel':amethod.IsParallel,
                  'IsQueued':amethod.IsQueued,
                  'Language':amethod.Language,
                  'LastModified':tdatetime2str(str2DateTime(amethod.LastModified),' '),
                  'MethodDescription':amethod.MethodDescription,
                  'Name':amethod.Name,
                  'WWWConfirmExecute':amethod.WWWConfirmExecute,
                  'WWWDescription':amethod.WWWDescription,
                  'WWWMenuImageLink':sWWWMenuImageLink,
                  'WWWMethod':amethod.WWWMethod,
               }
               self.file.TagOpen('METHODDEFINITION',d)
               sv=amethod.MethodText
               slist=string.split(string.replace(sv,'\015',''),'\n')
               d={}
               for sv in slist:
                  d['Value']=sv
                  self.file.TagOpen('METHODLINE',d,aclosetag=1)
               self.file.TagClose('METHODDEFINITION')
         return 1
      return 0
   def OnClass(self,aclass,aobj,isclassrecursive,isfieldrecursive,level):
# ogranicznik do kilku klas :-(        
#      self.ClassCount=self.ClassCount+1
#      if self.ClassCount>=5:
#         return
# zaglebienie w/g klas dziedziczonych
      if self.CheckClasses(aclass):
         if isclassrecursive:
            InfoStatus(aclass.NameOfClass)
      if isclassrecursive:
         alist=aclass.GetInheritedClassesList()
         for icid in alist:
            bclass=aICORDBEngine.Classes[icid]
            if not bclass is None:
               bobj=bclass.GetFirstObject()
               self.OnClass(bclass,bobj,isclassrecursive,isfieldrecursive,0)
# sprawdzenie czy mozna eksportowac klase
      if (not self.allowsystem and aclass.IsSystem=='1') or (aclass.IsVirtual=='1'):
         return
      if not isfieldrecursive:
         adt=aclass.GetLastModified()
         if adt<self.adate:
            return
      if not self.disableclassmethods:
         amethod=aclass.MethodsByName('OnClassExport')
         if not amethod is None:
            aICORDBEngine.Variables._AllowClassExport='1'
            amethod.Execute()
            if aICORDBEngine.Variables._AllowClassExport!='1':
               return
# zbudowanie listy pol do replikacji w klasie
      if self.ClassFieldsDict.has_key(aclass.CID):
         afields=self.ClassFieldsDict[aclass.CID]
      else:
         afields=[]
         afmethod=aclass.MethodsByName('OnFieldExport')
         armethod=aclass.MethodsByName('OnRecursiveFieldExport')
         flist=aclass.GetFieldsList()
         for afname in flist:
            afield=aclass.FieldsByName(afname)
            if (afield.IsInteractive!='$$$') and (afield.IsVirtual!='1'):
               arecur=1
               if not isfieldrecursive:
                  adt=afield.GetLastModified()
                  if adt<self.adate and afield.ClassOfType is None:
                     continue
               else:
                  if not armethod is None:
                     ret=armethod.Execute(afname)
                     if ret!='1':
                        arecur=0
               if not afmethod is None and not self.disablefieldmethods:
                  aICORDBEngine.Variables._AllowFieldExport='1'
                  afmethod.Execute(afname)
                  if aICORDBEngine.Variables._AllowFieldExport!='1':
                     continue
               afields.append([afield,arecur])
         self.ClassFieldsDict[aclass.CID]=afields
# obsluga cache
#      if len(self.CheckedObjectCache.keys())>18500:
##         print 'Cache flush...'
#         self.CheckedObjectCache={}
# eksport w/g pol
      wallobjects=0
      if not self.disableclassmethods:
         acmethod=aclass.MethodsByName('OnClassExport')
         if not acmethod is None:
            ret=acmethod(Value='objects')
            if type(ret)==type(1) and ret==1:
               wallobjects=1
      if not wallobjects and self.ObjectsDisabled:
         return
      aomethod=aclass.MethodsByName('OnObjectExport')
      fmax=len(afields)
      if not level:
         progresspos,progressmax=0,fmax*len(aobj)
      sclasspath=GetSafeRepositoryPath(aclass.ClassPath)
      aobj.First()
      while aobj:
         aoid=aobj.OID
         if not level:
            InfoStatus(self.Status+'/'+str(aoid))
            if not progresspos%3:
               SetProgress(progresspos,progressmax)
            progresspos=progresspos+1
         ro=(aclass.CID,aoid)
         if self.CheckedObjectCache.get(ro,0)==2:
            aobj.Next()
            continue
         self.CheckedObjectCache[ro]=2
         for i in range(fmax):
            afield,arecur=afields[i]
            ismemo=afield.IsContainer=='1' and afield.FieldTypeID==str(mt_String)
            if not wallobjects and not self.IsOIDInRange(aoid,aclass.CID):
               aobj.Next()
               continue
            adt=afield.GetValueLastModified(aoid)
            if adt<self.adate:
               aobj.Next()
               continue
            if self.CallbackObjectFunc:
               if not self.CallbackObjectFunc(aclass,afield,aoid):
                  aobj.Next()
                  continue
            if not aomethod is None and not self.disableobjectmethods:
               aICORDBEngine.Variables._AllowObjectExport='1'
               aomethod.Execute(afield.Name,aoid)
               if aICORDBEngine.Variables._AllowObjectExport!='1':
                  aobj.Next()
                  continue
            if isfieldrecursive and arecur:
               if not afield.ClassOfType is None:
                  brefs=afield.GetRefList(aoid)
                  bobj=brefs.AsObject()
                  if bobj:
                     self.OnClass(bobj.Class,bobj,isclassrecursive,isfieldrecursive,level+1)
            sd=tdatetime2str(adt,' ')
#            if aclass.CID==744:
#               file.write('<tt>%d %d</tt>\n'%(aoid,self.IsOIDInRange(aoid,aclass.CID)))
            ftype=afield.FieldType
            ftype=ftype.replace('\\','_')
            if ismemo:
               s='<FIELDVALUE ClassPath="%s" CID="%d" Name="%s" OID="%d" LastModification="%s" FieldType="%s">\n' % (sclasspath,aclass.CID,afield.Name,aoid,sd,ftype)
               self.file.write(s)
               sv=afield.ValuesAsString(aoid)
               slist=string.split(string.replace(sv,'\015',''),'\n')
               for sv in slist:
                  self.file.write(' <DATA>')
                  self.file.write(GetAsXMLString(sv))
                  self.file.write('</DATA>\n')
            else:
               s='<FIELDVALUE ClassPath="%s" CID="%d" Name="%s" OID="%d" LastModification="%s" FieldType="%s">\n' % (sclasspath,aclass.CID,afield.Name,aoid,sd,ftype)
               self.file.write(s)
               if not afield.ClassOfType is None and self.dACL_CIDs.has_key(afield.ClassOfType.CID):
                  sdv=GetAsXMLString(ICORSecurity.GetAccessLevelRefsAsString(afield.GetRefList(aoid)))
               else:
                  sdv=GetAsXMLString(afield.ValuesAsString(aoid))
               self.file.write(' <DATA>'+sdv+'</DATA>\n')
            self.file.write(' </FIELDVALUE>\n')
         aobj.Next()
   def DumpClasses(self):
      aclist=[]
      for acid in self.CheckedClasses.keys():
         aclass=aICORDBEngine.Classes[acid]
         aclist.append(aclass.ClassPath)
      aclist.sort()
      print '*** Lista zreplikowanych klas: ***'
      for acpath in aclist:
         print acpath
                       
def SendReplicationByFTP(aprofile,auserid=-1,adatefrom=(),abyftp=1,acallbackobjectfunc=None,adefaultfilepath='',aprompt=1):
#   if achecksystemuser and aICORDBEngine.SystemOwnerUserID==0:
#      MessageDialog('Server w centrali nie wysy�a raport�w z zmianach.',mtWarning,mbOK)
#      return ''
   citerator=ICORReplicationIterator(aprofile,atargetuser=auserid,afile='',adatefrom=adatefrom,acallbackobjectfunc=acallbackobjectfunc)
   arefs=citerator.ProfileClass.FTPProfile.GetRefList(citerator.OID)
   if abyftp:
      ftp=GetReplicationFTP(arefs)
      if ftp is None:
         MessageDialog('B��d podczas nawi�zywania komunikacji z serwerem.\nSprawd�, czy serwer jest aktywny.',mtError,mbOK)
         return ''
   else:
      ftp=None
   try:
      afmanager=FTPFileManager(ftp)
      try:
         afname=afmanager.GetStdName(auserid)
         if adefaultfilepath=='':
            afilepath=FilePathAsSystemPath(arefs.FTPLocalDir[arefs.OID])
         else:
            afilepath=FilePathAsSystemPath(adefaultfilepath)
         afpath=afilepath+'\\'+afname
         if auserid<0:
            auserid=aICORDBEngine.SystemOwnerUserID
         if not (adatefrom==() or adatefrom==tzerodatetime()):
            citerator.adate=adatefrom
         else:
            citerator.adate=aICORDBEngine.User.LastReportDate.ValuesAsDateTime(auserid)
         citerator.adatecreated=afmanager.FileTime
         citerator.Generate(afpath)
         afmanager.Upload(afname,afilepath)
         aICORDBEngine.User.LastReportDate.SetValuesAsDateTime(auserid,afmanager.FileTime)
      finally:
         del afmanager
         if ftp:
            ftp.quit()             
   finally:
      pass
#      os.unlink(afpath)
   if aprompt:
      if abyftp:
         MessageDialog('Koniec generowania danych o zmianach.',mtInformation,mbOK)
      else:
         MessageDialog('Koniec generowania danych o zmianach. Plik z raportem znajduje si� w:'+chr(10)+afpath+chr(10)+'teraz mo�esz przegra� go np. na dyskietk� aby samodzielnie wykona� import/export.',mtInformation,mbOK)
   return afpath

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   start=time.clock()
   if OID>=0:
      citerator=ICORReplicationIterator(OID)
   else:
      MessageDialog('Aby wys�a� informacje o zmianach nale�y wybra� profil.',mtError,mbOK)
      return
   citerator.Generate()
   finish=time.clock()
   print 'Koniec',finish-start

