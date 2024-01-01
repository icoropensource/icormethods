# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import xmllib
import string

def GetListAsDateTuple(alist,x):
   return (int(alist[x]),int(alist[x+1]),int(alist[x+2]),int(alist[x+3]),int(alist[x+4]),int(alist[x+5]),int(alist[x+6]))

class ICORXMLReplicationParser(xmllib.XMLParser):
   def __init__(self, aallowupdateprotected=0,averbose=0,aimportmethodexecute=1):
      xmllib.XMLParser.__init__(self)
      self.allowupdateprotected=aallowupdateprotected
      self.aclass=None
      self.afield=None
      self.acmethod=None
      self.afmethod=None
      self.aomethod=None
      self.ismemo=0
      self.avalue=''
      self.avalueline=''
      self.verbose=averbose
      self.importmethodexecute=aimportmethodexecute
   def start_HEADER(self,attrs):
      self.sourceuser=int(attrs['SourceUser'])
      print 'SourceUser:',self.sourceuser
      print 'TargetUser:',attrs['TargetUser']
      alm=string.split(attrs['DateFrom'],' ')
      self.datefrom=GetListAsDateTuple(alm,0)
      print 'DateFrom:',self.datefrom
      alm=string.split(attrs['Created'],' ')
      self.created=GetListAsDateTuple(alm,0)
      print 'Created:',self.created
      print ''
   def start_CLASS(self, attrs):
      acid=int(attrs['CID'])
      alm=string.split(attrs['LastModification'],' ')
      self.aclass=aICORDBEngine.Classes[acid]
      self.afield=None
      self.acmethod=None
      self.afmethod=None
      self.aomethod=None
      self.ismemo=0
      self.classmodified=0
      if self.aclass is None:
         print '*** Class',acid,'is None! ***'
      else:
         InfoStatus(self.aclass.NameOfClass)
         if self.importmethodexecute:
            self.acmethod=self.aclass.MethodsByName('OnClassImport')
         if not self.acmethod is None:
            aICORDBEngine.Variables._AllowClassImport='1'
            self.acmethod.Execute('',-1,'0')
            if aICORDBEngine.Variables._AllowClassImport!='1':
               self.acmethod=None
               self.aclass=None
               return
         self.adtclass=GetListAsDateTuple(alm,0)
         if self.importmethodexecute:
            self.afmethod=self.aclass.MethodsByName('OnFieldImport')
            self.aomethod=self.aclass.MethodsByName('OnObjectImport')
         if self.verbose:
            print self.aclass.ClassPath,self.adtclass
   def start_FIELD(self,attrs):
      if self.aclass is None:
         return
      self.afield=self.aclass.FieldsByName(attrs['Name'])
      if not self.afield is None:
         InfoStatus(self.aclass.NameOfClass+':'+self.afield.Name)
         if not self.afmethod is None:
            aICORDBEngine.Variables._AllowFieldImport='1'
            self.afmethod.Execute(self.afield.Name)
            if aICORDBEngine.Variables._AllowFieldImport!='1':
               self.afield=None
               return
         self.ismemo=self.afield.IsMemo
         alm=string.split(attrs['LastModification'],' ')
         self.adtfield=GetListAsDateTuple(alm,0)
         if self.verbose:
            print '  ',self.afield.Name,self.ismemo,self.adtfield
   def start_OBJECT(self,attrs):
      if self.afield is None:
         return
      self.aoid=int(attrs['OID'])
      alm=string.split(attrs['LastModification'],' ')
      self.adtobject=GetListAsDateTuple(alm,0)
      self.avalue=''
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
      if self.afield is None:
         return
      wu=1
      if self.aclass.IsObjectDeleted(self.aoid) and aICORDBEngine.IsAdministrator:
         wu=0
      if not self.allowupdateprotected and self.afield.IsReportProtected=='1':
         wu=0
      if wu and not self.ismemo and self.afield[self.aoid]==self.avalue:
         wu=0
      if not self.aomethod is None and wu:
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
         self.classmodified=1
         self.afield[self.aoid]=self.avalue
         self.afield.SetValueLastModified(self.aoid,self.adtobject)
         if not self.ismemo:
            if self.verbose:
               print '      %d %s >%s<' % (self.aoid,str(self.adtobject),self.avalue)
         else:
            if self.verbose:
               print '      %d %s' % (self.aoid,str(self.adtobject))
               print self.avalue
   def end_CLASS(self):
      if self.aclass is None or not self.classmodified:
         return
      if not self.aclass.IsSystem=='1' and self.aclass.AllowRead=='1':
         if not self.acmethod is None:
            self.acmethod.Execute('',-1,'1')
   def syntax_error(self, lineno, message):
      print 'error at line %d:' % lineno, message

def ReceiveData(afname,aallowupdateprotected=0,aimportmethodexecute=1):
   import gzip
   afname=FilePathAsSystemPath(afname)
   f=open(afname,'rb')
   f=gzip.GzipFile('data','rb',9,f)
   try:
      data = f.read()
      aparser=ICORXMLReplicationParser(aallowupdateprotected,0,aimportmethodexecute)
      try:
         for c in data:
            aparser.feed(c)
      finally:
         aparser.close()
   finally:
      f.close()
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   afile=InputFile()
   if afile=='':
      return
   ReceiveData(afile)


