# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_NetBase_Utils_XMLUtil import *
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import xmllib #from xml.parsers 
import os
import string

ReplicationException = 'ReplicationException'

def GetListAsDateTuple(alist,x=0):
   return (int(alist[x]),int(alist[x+1]),int(alist[x+2]),int(alist[x+3]),int(alist[x+4]),int(alist[x+5]),int(alist[x+6]))

class ICORXMLReplicationParser(xmllib.XMLParser):
   def __init__(self, aprofile):
      xmllib.XMLParser.__init__(self)
      self.ProfileClass=aICORDBEngine.Classes['CLASSES/Library/ICORBase/Replication/Receive']
      if self.ProfileClass is None:
         raise ReplicationException,'Profile class does not exists'
      if type(aprofile)==type(1):
         self.OID=aprofile
      else:
         self.OID=self.ProfileClass.Name.Identifiers(aprofile)
      if self.OID<0:
         raise ReplicationException,'Profile does not exists'
      self.InitByProfile()
   def InitByProfile(self):
      self.afile=self.ProfileClass.InputFile[self.OID]
   def Parse(self,fname=''):
      self.reset()
      self.elements={}
      self.elements['METHODDEFINITION']=(self.start_METHODDEFINITION,self.end_METHODDEFINITION)
      self.elements['METHODLINE']=(self.start_METHODLINE,self.end_METHODLINE)
      if fname!='':
         self.afile=fname
      if self.afile=='':
         raise ReplicationException,'No file'
      self.afile=FilePathAsSystemPath(self.afile)
      self.filedir,s=os.path.split(self.afile)
      if self.afile[-3:]!='.gz':
         self.afile=self.afile+'.gz'
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
   def start_METHODDEFINITION(self,attrs):
      self.methodlines=[]
      self.ClassPath=attrs.get('ClassPath','')
      self.MethodName=attrs.get('Name','')
   def start_METHODLINE(self,attrs):
      self.methodlines.append(GetXMLStringAsString(attrs.get('Value','')))
   def end_METHODLINE(self):
      pass
   def end_METHODDEFINITION(self):
      self.methodlines.append('')
      self.MethodText=string.join(self.methodlines,'\n')
      bclass=aICORDBEngine.Classes[self.ClassPath]
      bmethod=bclass.MethodsByName(self.MethodName)
      s1=string.replace(bmethod.MethodText,chr(10),'')
      s1=string.replace(s1,chr(13),'')
      s2=string.replace(self.MethodText,chr(10),'')
      s2=string.replace(s2,chr(13),'')
      if s1!=s2:
         f=open(self.filedir+'/'+self.ClassPath+'_'+self.MethodName+'.py1','w')
         f.write(self.MethodText)
         f.close()
         f=open(self.filedir+'/'+self.ClassPath+'_'+self.MethodName+'.py2','w')
         f.write(bmethod.MethodText)
         f.close()
   def syntax_error(self, lineno, message):
      print 'error in data at line %d:' % lineno, message
   def unknown_starttag(self, tag, attrs):
      pass
   def unknown_endtag(self, tag):
      pass
   def unknown_entityref(self, ref):
      pass
   def unknown_charref(self, ref):
      pass

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes['CLASSES_System_Dialog_Replikacja_Receive']
   bclass=aICORDBEngine.Classes[CID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   if not aclass.EditObject(aoid):
      return
   rclass=aICORDBEngine.Classes[CID]
   roid=rclass.Name.Identifiers('CLASS_REPLICATION')
   if roid<0:
      print 'Klasa odpowiedzialna za replikację nie posiada wzorca głównego replikacji'
      return
   aobj,robj=aclass[aoid],rclass[roid]
   robj.AllowUpdateProtected=aobj.AllowUpdateProtected
   robj.ImportMethodExecute=aobj.ImportMethodExecute
   robj.InputFile=aobj.InputFile
   robj.OverrideDeleted=aobj.OverrideDeleted
   robj.ReceiveMethods=aobj.ReceiveMethods
   robj.AlwaysUpdateMethod=aobj.AlwaysUpdateMethod
   aparser=ICORXMLReplicationParser(roid)
   aparser.Parse()
   return



