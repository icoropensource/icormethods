# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_NetBase_Utils_XMLUtil import *

def GenerateHeader(file,adatefrom,adatecreated,targetuser=0):
   file.write('<?xml version="1.0" encoding="Windows-1250"?>\n')
   file.write('\n')
   sd=tdatetime2str(adatefrom,' ')
   sc=tdatetime2str(adatecreated,' ')
   sheader='<HEADER SourceUser="%d" TargetUser="%d" DateFrom="%s" Created="%s" />\n\n' % (aICORDBEngine.SystemOwnerUserID,targetuser,sd,sc)
   file.write(sheader)

def DumpClassXML(file,aclass,adate):
   import string,time
   if not aclass.IsSystem=='1' and not aclass.IsVirtual=='1':
      adt=aclass.GetLastModified()
      if adt<adate:
         return
      amethod=aclass.MethodsByName('OnClassExport')
      if not amethod is None:
         aICORDBEngine.Variables._AllowClassExport='1'
         amethod.Execute()
         if aICORDBEngine.Variables._AllowClassExport!='1':
            return
      InfoStatus(aclass.NameOfClass)
      sd=tdatetime2str(adt,' ')
      sclass='<CLASS CID="%d" LastModification="%s" ClassPath="%s">\n' % (aclass.CID,sd,aclass.ClassPath)
      aclasswritten=0
      afmethod=aclass.MethodsByName('OnFieldExport')
      aomethod=aclass.MethodsByName('OnObjectExport')
      flist=aclass.GetFieldsList()
      for afname in flist:
         afield=aclass.FieldsByName(afname)
         if afield.IsInteractive=='1' and afield.AllowRead=='1' and afield.IsVirtual!='1' and afield.IsReportProtected!=1:
            ismemo=afield.IsContainer=='1' and afield.FieldTypeID==str(mt_String)
            adt=afield.GetLastModified()
            if adt<adate:
               continue
            if not afmethod is None:
               aICORDBEngine.Variables._AllowFieldExport='1'
               afmethod.Execute(afname)
               if aICORDBEngine.Variables._AllowFieldExport!='1':
                  continue
            if not aclasswritten:
               file.write(sclass)
               aclasswritten=1
            InfoStatus(aclass.NameOfClass+':'+afield.Name)
            sd=tdatetime2str(adt,' ')
            s='  <FIELD Name="%s" LastModification="%s">\n' % (afname,sd)
            file.write(s)
            aoid=afield.GetFirstValueID()
            while aoid>=0:
               adt=afield.GetValueLastModified(aoid)
               if adt<adate:
                  aoid=afield.GetNextValueID(aoid)
                  continue
               if not aomethod is None:
                  aICORDBEngine.Variables._AllowObjectExport='1'
                  aomethod.Execute(afname,aoid)
                  if aICORDBEngine.Variables._AllowObjectExport!='1':
                     aoid=afield.GetNextValueID(aoid)
                     continue
               sd=tdatetime2str(adt,' ')
               if ismemo:
                  sv=afield.ValuesAsString(aoid)
                  svl=''
                  for c in sv:
                     if c !='\015':
                        svl = svl + c
                  slist=string.split(svl,'\n')
                  s='    <OBJECT OID="%d" LastModification="%s">\n' % (aoid,sd)
                  file.write(s)
                  for sv in slist:
                     file.write('      <DATA>'+GetAsXMLString(sv)+'</DATA>\n')
               else:
                  s='    <OBJECT OID="%d" LastModification="%s">\n' % (aoid,sd)
                  file.write(s)
                  file.write('      <DATA>'+GetAsXMLString(afield.ValuesAsString(aoid))+'</DATA>\n')
               file.write('    </OBJECT>\n')
               aoid=afield.GetNextValueID(aoid)
            file.write('  </FIELD> <!-- %s -->\n\n' % (afname))
      if aclasswritten:
         file.write('</CLASS> <!-- %s -->\n\n\n' % (aclass.NameOfClass))

def GenerateReport(afname,adatefrom=(),adatecreated=(),atargetuser=0,arootclass=None):
   import gzip
   if adatefrom==():
      adatefrom=InputDateTuple('Raport od dnia:',1)
      if adatefrom==():
         return
   if adatecreated==():
      adatecreated=tdatetime()
   f=open(afname,'wb')
   f=gzip.GzipFile('data','wb',9,f)
   try:
      GenerateHeader(f,adatefrom,adatecreated,atargetuser)
      def ClassFunc(aclass,f,adatefrom):
         s=str(aclass.CID)+': '+aclass.NameOfClass
         DumpClassXML(f,aclass,adatefrom)
      aICORDBEngine.Classes.ForEachClass(ClassFunc,arootclass,f,adatefrom)
   finally:
      f.close()
      InfoStatus('')
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   afile=InputFile()
   if afile=='':
      return
   afile=FilePathAsSystemPath(afile)
   if afile[-3:]!='.gz':
      afile=afile+'.gz'
   if OID<0:
      adialog=InputElementDialog('Wybierz klasę bazową dla raportu',0,0)
      if not adialog.Show():
         return
      aclass=aICORDBEngine.Classes[adialog.ClassPath]
   else:
      aclass=aICORDBEngine.Classes[OID]
   if aclass is None:
      return
   GenerateReport(afile,(),(),-1,aclass)


