# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import cStringIO
import string
import xmllib
import sys

__VERSION__=1,0,4

class ICORXMLTemplateParser(xmllib.XMLParser):
   def __init__(self,axmlfileparser):
      xmllib.XMLParser.__init__(self,accept_utf8=1,accept_unquoted_attributes=1,accept_missing_endtag_name=1)
      self.XMLFileParser=axmlfileparser
   def Parse(self,afname):
      self.reset()
      self.elements={}
      self.elements['queries']=(self.start_queries,self.end_queries)
      self.elements['var']=(self.start_var,self.end_var)
      self.elements['query']=(self.start_query,self.end_query)
      self.elements['dimension']=(self.start_dimension,self.end_dimension)
      self.elements['filter']=(self.start_filter,self.end_filter)
      self.elements['external']=(self.start_external,self.end_external)
      self.elements['externallib']=(self.start_externallib,self.end_externallib)
      atext=self.XMLFileParser.GetInputText(afname)
      self.feed(atext)
   def start_var(self,attrs):
      self.XMLFileParser.SetVariable(attrs.get('name',''),attrs.get('value',''))
   def end_var(self):
      pass
   def start_queries(self,attrs):
      pass
   def end_queries(self):
      pass
   def start_query(self,attrs):
      attrs['caption']=self.XMLFileParser.Caption
      attrs['subtitle']=self.XMLFileParser.SubTitle
      self.XMLFileParser.XMLOutput.TagOpen('query',attrs)
   def end_query(self):
      self.XMLFileParser.XMLOutput.TagClose('query')
   def start_dimension(self,attrs):
      attrs['formulaname']=self.XMLFileParser.ReplaceVars(attrs.get('formulaname',''))
      attrs['formulatext']=self.XMLFileParser.ReplaceVars(attrs.get('formulatext',''))
      self.XMLFileParser.XMLOutput.TagOpen('dimension',attrs)
   def end_dimension(self):
      self.XMLFileParser.XMLOutput.TagClose('dimension')
   def start_filter(self,attrs):
      attrs['accountfrom']=self.XMLFileParser.ReplaceVars(attrs.get('accountfrom',''))
      attrs['accountto']=self.XMLFileParser.ReplaceVars(attrs.get('accountto',''))
      attrs['accountmask']=self.XMLFileParser.ReplaceVars(attrs.get('accountmask',''))
      self.XMLFileParser.XMLOutput.TagOpen('filter',attrs)
   def end_filter(self):
      self.XMLFileParser.XMLOutput.TagClose('filter')
   def start_external(self,attrs):
      afname=attrs.get('file','')
      print '  external:',afname#,self.XMLFileParser.Vars.items()
      aparser=ICORXMLTemplateParser(self.XMLFileParser)
      aparser.Parse(afname)
   def end_external(self):
      pass
   def start_externallib(self,attrs):
      pass
   def end_externallib(self):
      pass

class ICORXMLFilesParser(xmllib.XMLParser):
   def __init__(self,aparser=None):
      xmllib.XMLParser.__init__(self,accept_utf8=1,accept_unquoted_attributes=1,accept_missing_endtag_name=1)
      self.Parser=aparser
      if aparser is None:
         self.Vars={}
   def __getattr__(self,name):
      if not self.Parser is None:
         return getattr(self.Parser,name)
   def Parse(self,aclass,aoid=-1):
      if type(aclass)==type(''):
         atext=aclass
         wlast=0
      else:
         self.ClassItem=aclass
         self.QueryClass=self.ClassItem.Queries.ClassOfType
         self.OID=aoid
         atext=self.ClassItem.SourceData[self.OID]
         wlast=1
      self.reset()
      self.elements={}
      self.elements['preprocessing']=(self.start_preprocessing,self.end_preprocessing)
      self.elements['outputitems']=(self.start_outputitems,self.end_outputitems)
      self.elements['output']=(self.start_output,self.end_output)
      self.elements['var']=(self.start_var,self.end_var)
      self.elements['external']=(self.start_external,self.end_external)
      self.elements['externallib']=(self.start_externallib,self.end_externallib)
      self.feed(atext)
      if wlast:
         self.ClassItem.LastGenerated[self.OID]=ICORUtil.tdatetime()
   def SetVariable(self,name,value):
      if not value:
         if self.Vars.has_key(name):
            del self.Vars[name]
         return
      self.Vars[name]=value
   def ReplaceVars(self,s):
      for afrom,ato in self.Vars.items():
         s=string.replace(s,afrom,ato)
      return s
   def GetInputText(self,aname):
      arefs=self.ClassItem.FileItems.GetRefList(self.OID)
      apos,afind=arefs.FindRefByValue('Name',aname)
      if afind:
         arefs.SetByPosition(apos)
         return arefs.SourceData[arefs.OID]
      else:
         print 'Unknown XML file name:',aname
      return ''
   def start_preprocessing(self,attrs):
      pass
   def end_preprocessing(self):
      pass
   def start_outputitems(self,attrs):
      self.InputFile=attrs.get('infile','')
      self.OutputFile=attrs.get('outfile','')
      self.Title=attrs.get('title','')
      self.StructName=attrs.get('structname','')
      self.FKDataPath=attrs.get('fkdatapath','')
      self.DBPath=attrs.get('dbpath','')
   def start_output(self,attrs):
      self.SubTitle=attrs.get('subtitle','')
      self.Caption=attrs.get('caption','')
      self.OutFile=cStringIO.StringIO()
      self.XMLOutput=XMLUtil.MXMLFile(self.OutFile)
      self.XMLOutput.Header()
      self.XMLOutput.TagOpen('queries',{'title':self.Title})
   def start_var(self,attrs):
      self.SetVariable(attrs.get('name',''),attrs.get('value',''))
   def end_var(self):
      pass
   def end_output(self):
      print 'parsing: %s, "%s", "%s"'%(self.InputFile,self.Caption,self.SubTitle)#,self.Vars.items()
      aparser=ICORXMLTemplateParser(self)
      aparser.Parse(self.InputFile)
      self.XMLOutput.TagClose('queries')
      self.XMLOutput.close()
      boid=self.QueryClass.AddObject()
      self.QueryClass.Caption[boid]=self.Caption
      self.QueryClass.Name[boid]=self.StructName
      self.QueryClass.SourceXML[boid]=self.OutFile.getvalue()
      self.QueryClass.FKDataPath[boid]=self.FKDataPath
      self.QueryClass.DBPath[boid]=self.DBPath
      self.ClassItem.Queries.AddRefs(self.OID,[boid,self.QueryClass.CID])
   def end_outputitems(self):
      pass
   def start_external(self,attrs):
      afname=attrs.get('file','')
      print '  external output:',afname
      aparser=ICORXMLFilesParser(self)
      atext=self.GetInputText(afname)
      aparser.Parse(atext)
   def end_external(self):
      pass
   def start_externallib(self,attrs):
      pass
   def end_externallib(self):
      pass

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   OID=1
   aclass=aICORDBEngine.Classes[CID]
   aclass.Queries.DeleteReferencedObjects(OID)
   aparser=ICORXMLFilesParser()
   aparser.Parse(aclass,OID)
   return



