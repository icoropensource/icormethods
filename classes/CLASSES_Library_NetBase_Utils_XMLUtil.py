# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from CLASSES_Library_ICORBase_Interface_ICORTextFile import TextFile
import xmllib
import string
import re
import os
import unicodedata
import time
import win32file
import random
import types

TRANS={}
for i in range(32,128):
   TRANS[chr(i)]=chr(i)
for i in range(0,32):       
   TRANS[chr(i)]="&#"+str(i)+";"
for i in range(128,256):
   TRANS[chr(i)]="&#"+str(i)+";"
for c in ['%','\\',"'",]: #'#','/','+',
   TRANS[c]="&#"+str(ord(c))+";"
TRANS["&"]="&amp;"
TRANS["<"]="&lt;"                             
TRANS['"']="&quot;" #"
TRANS[">"]="&gt;"

TRANS_NO_PL={}
for k in TRANS.keys():
   TRANS_NO_PL[k]=TRANS[k]
for c in chr(185)+chr(230)+chr(234)+chr(179)+chr(241)+chr(243)+chr(156)+chr(159)+chr(191) + chr(165)+chr(198)+chr(202)+chr(163)+chr(209)+chr(211)+chr(140)+chr(143)+chr(175):
   TRANS_NO_PL[c]=c
TRANS_CDATA_PL={}
for k in TRANS_NO_PL.keys():
   TRANS_CDATA_PL[k]=TRANS_NO_PL[k]
TRANS_CDATA_PL["&"]="&"
TRANS_CDATA_PL["<"]="<"
TRANS_CDATA_PL['"']='"' #"
TRANS_CDATA_PL[">"]=">"

def UTF8_To_CP1250(s,amode='xmlcharrefreplace',aencoding='utf-8'):
   if not s:
      return ''.encode('cp1250',amode)
   if type(s)==type(''):
      s=unicode(s,aencoding)
   return s.encode('cp1250',amode)

def CP1250_To_UTF8(s,amode='xmlcharrefreplace'):
   return unicode(s,'cp1250','ignore').encode('utf-8',amode)

def CP1250_To_ASCII_Default(s):
   return unicodedata.normalize('NFKD',unicode(s,'cp1250')).encode('ASCII','ignore')

def CP1250_To_ASCII(s):
   import unidecode
   s=s.replace('ł','l')
   s=s.replace('Ł','L')
   s=s.replace('&oacute;','o')
   s=s.replace('&Oacute;','O')
   l=re.split('(\&\#\d+\;)',s)
   ipatt=re.compile('\&\#(\d+)\;')
   l2=[]
   for s2 in l:
      m=ipatt.match(s2)
      if m:
         l2.append(unidecode.unidecode(unichr(int(m.group(1)))).encode('ASCII','ignore'))
      elif s2:
         l2.append(unidecode.unidecode(unicode(s2,'cp1250')).encode('ASCII','ignore'))
   return ''.join(l2)

def UTF8_To_ASCII(s):
   try:
      s=s.replace('ł','l')
      s=s.replace('Ł','L')
      s=unicode(s,'cp1250','ignore')
      return unicodedata.normalize('NFKD',s).encode('ASCII','ignore')
   except:
      print s,type(s)
      raise

def IsUTF8(atext):
   if atext.find(chr(0xc4)+chr(0x85))>=0: # a
      return 1
   if atext.find(chr(0xc4)+chr(0x87))>=0: # c
      return 1
   if atext.find(chr(0xc4)+chr(0x99))>=0: # e
      return 1
   if atext.find(chr(0xc5)+chr(0x82))>=0: # l
      return 1
   if atext.find(chr(0xc5)+chr(0x84))>=0: # n
      return 1
   if atext.find(chr(0xc3)+chr(0xb3))>=0: # o
      return 1
   if atext.find(chr(0xc5)+chr(0x9b))>=0: # s
      return 1
   if atext.find(chr(0xc5)+chr(0xba))>=0: # x
      return 1
   if atext.find(chr(0xc5)+chr(0xbc))>=0: # z
      return 1
   if atext.find(chr(0xc4)+chr(0x84))>=0: # A
      return 1
   if atext.find(chr(0xc4)+chr(0x86))>=0: # C
      return 1
   if atext.find(chr(0xc4)+chr(0x98))>=0: # E
      return 1
   if atext.find(chr(0xc5)+chr(0x81))>=0: # L
      return 1
   if atext.find(chr(0xc5)+chr(0x83))>=0: # N
      return 1
   if atext.find(chr(0xc3)+chr(0x93))>=0: # O
      return 1
   if atext.find(chr(0xc5)+chr(0x9a))>=0: # S
      return 1
   if atext.find(chr(0xc5)+chr(0xb9))>=0: # X
      return 1
   if atext.find(chr(0xc5)+chr(0xbb))>=0: # Z
      return 1
   return 0

def IsCP1250(atext):
   if atext.find(chr(0xb9))>=0: # a
      return 1
   if atext.find(chr(0xe6))>=0: # c
      return 1
   if atext.find(chr(0xea))>=0: # e
      return 1
   if atext.find(chr(0xb3))>=0: # l
      return 1
   if atext.find(chr(0xf1))>=0: # n
      return 1
   if atext.find(chr(0xf3))>=0: # o
      return 1
   if atext.find(chr(0x9c))>=0: # s
      return 1
   if atext.find(chr(0x9f))>=0: # x
      return 1
   if atext.find(chr(0xbf))>=0: # z
      return 1
   if atext.find(chr(0xa5))>=0: # A
      return 1
   if atext.find(chr(0xc6))>=0: # C
      return 1
   if atext.find(chr(0xca))>=0: # E
      return 1
   if atext.find(chr(0xa3))>=0: # L
      return 1
   if atext.find(chr(0xd1))>=0: # N
      return 1
   if atext.find(chr(0xd3))>=0: # O
      return 1
   if atext.find(chr(0x8c))>=0: # S
      return 1
   if atext.find(chr(0x8f))>=0: # X
      return 1
   if atext.find(chr(0xaf))>=0: # Z
      return 1
   return 0

def UTF2Win(atext):
   atext=atext.replace(chr(0xc4)+chr(0x85),chr(0xb9)) # a
   atext=atext.replace(chr(0xc4)+chr(0x87),chr(0xe6)) # c
   atext=atext.replace(chr(0xc4)+chr(0x99),chr(0xea)) # e
   atext=atext.replace(chr(0xc5)+chr(0x82),chr(0xb3)) # l
   atext=atext.replace(chr(0xc5)+chr(0x84),chr(0xf1)) # n
   atext=atext.replace(chr(0xc3)+chr(0xb3),chr(0xf3)) # o
   atext=atext.replace(chr(0xc5)+chr(0x9b),chr(0x9c)) # s
   atext=atext.replace(chr(0xc5)+chr(0xba),chr(0x9f)) # x
   atext=atext.replace(chr(0xc5)+chr(0xbc),chr(0xbf)) # z
   atext=atext.replace(chr(0xc4)+chr(0x84),chr(0xa5)) # A
   atext=atext.replace(chr(0xc4)+chr(0x86),chr(0xc6)) # C
   atext=atext.replace(chr(0xc4)+chr(0x98),chr(0xca)) # E
   atext=atext.replace(chr(0xc5)+chr(0x81),chr(0xa3)) # L
   atext=atext.replace(chr(0xc5)+chr(0x83),chr(0xd1)) # N
   atext=atext.replace(chr(0xc3)+chr(0x93),chr(0xd3)) # O
   atext=atext.replace(chr(0xc5)+chr(0x9a),chr(0x8c)) # S
   atext=atext.replace(chr(0xc5)+chr(0xb9),chr(0x8f)) # X
   atext=atext.replace(chr(0xc5)+chr(0xbb),chr(0xaf)) # Z
   return atext

def URL_UTF2Win(atext):
   atext=atext.replace('%c4%85',chr(0xb9)) # a
   atext=atext.replace('%c4%87',chr(0xe6)) # c
   atext=atext.replace('%c4%99',chr(0xea)) # e
   atext=atext.replace('%c5%82',chr(0xb3)) # l
   atext=atext.replace('%c5%84',chr(0xf1)) # n
   atext=atext.replace('%c3%b3',chr(0xf3)) # o
   atext=atext.replace('%c5%9b',chr(0x9c)) # s
   atext=atext.replace('%c5%ba',chr(0x9f)) # x
   atext=atext.replace('%c5%bc',chr(0xbf)) # z
   atext=atext.replace('%c4%84',chr(0xa5)) # A
   atext=atext.replace('%c4%86',chr(0xc6)) # C
   atext=atext.replace('%c4%98',chr(0xca)) # E
   atext=atext.replace('%c5%81',chr(0xa3)) # L
   atext=atext.replace('%c5%83',chr(0xd1)) # N
   atext=atext.replace('%c3%93',chr(0xd3)) # O
   atext=atext.replace('%c5%9a',chr(0x8c)) # S
   atext=atext.replace('%c5%b9',chr(0x8f)) # X
   atext=atext.replace('%c5%bb',chr(0xaf)) # Z

   atext=atext.replace('%C4%85',chr(0xb9)) # a
   atext=atext.replace('%C4%87',chr(0xe6)) # c
   atext=atext.replace('%C4%99',chr(0xea)) # e
   atext=atext.replace('%C5%82',chr(0xb3)) # l
   atext=atext.replace('%C5%84',chr(0xf1)) # n
   atext=atext.replace('%C3%B3',chr(0xf3)) # o
   atext=atext.replace('%C5%9B',chr(0x9c)) # s
   atext=atext.replace('%C5%BA',chr(0x9f)) # x
   atext=atext.replace('%C5%BC',chr(0xbf)) # z
   atext=atext.replace('%C4%84',chr(0xa5)) # A
   atext=atext.replace('%C4%86',chr(0xc6)) # C
   atext=atext.replace('%C4%98',chr(0xca)) # E
   atext=atext.replace('%C5%81',chr(0xa3)) # L
   atext=atext.replace('%C5%83',chr(0xd1)) # N
   atext=atext.replace('%C3%93',chr(0xd3)) # O
   atext=atext.replace('%C5%9A',chr(0x8c)) # S
   atext=atext.replace('%C5%B9',chr(0x8f)) # X
   atext=atext.replace('%C5%BB',chr(0xaf)) # Z
   return atext

def GetAsXMLString(data):
   return GetAsXMLStringSimple(data)
   res=""
   for c in data:
      res=res+TRANS[c]
   return res

def GetAsXMLStringNoPL(data):
   return GetAsXMLStringSimple(data)
   res=""
   for c in data:
      res=res+TRANS_NO_PL[c]
   return res

def GetAsXMLStringCDataNoPL(data):
   return data
   res=""
   for c in data:
      res=res+TRANS_CDATA_PL[c]
   return res

def GetAsXMLStringSimple(data):
   data=data.replace("&","&amp;")
   data=data.replace("<","&lt;")
   data=data.replace("\"","&quot;") #"
   data=data.replace(">","&gt;")
   data=data.replace(chr(9),"&#9;")
   data=data.replace(chr(10),"&#10;")
   data=data.replace(chr(13),"&#13;")
   return data

def GetXMLStringAsString(data):
   def dorepl(amatch):
      s=amatch.group(amatch.lastindex)
      if s=='amp':
         return '&'
      elif s=='gt':
         return '>'
      elif s=='lt':
         return '<'
      elif s=='quot':
         return '"'
      i=int(s)
      if i<256:
         return chr(i)
      return '&#'+s+';'
   data=re.sub('\&\#(\d+)\;|\&(amp)\;|\&(gt)\;|\&(lt)\;|\&(quot)\;',dorepl,data)
   return data

XMLFileException = 'XMLFileException'

class MXMLFile:
   def __init__(self,afile,anopl=0,aattrascdata=0,aencoding='windows-1250',astemp=0,pathpriority=None):
      self.fclose=isinstance(afile,types.StringTypes)
      self.FileName=''
      astemp=0 ### after ICORUtil.syncfile
      self.TempFile=astemp
      self.FileNameSufix=''
      if astemp:
         self.FileNameSufix='.temp_%010d'%(random.randrange(0,1000000000),)
      if self.fclose:
         afile=FilePathAsSystemPath(afile)
         self.FileName=afile
         if afile[-3:]=='.gz':
            self.TempFile=0
            self.FileNameSufix=''
            self.file=TextFile(afile,'w',aencoding=aencoding)
         else:
            self.file=ICORUtil.OpenText(afile+self.FileNameSufix,'w',aencoding,pathpriority=pathpriority)
      else:
         self.TempFile=0
         self.FileNameSufix=''
         self.file=afile
      self.NoPL=anopl
      self.AttrAsCData=aattrascdata
      self.Encoding=aencoding
      self.stack=[]
      self.current_attrs={}
   def close(self):
      if self.stack:
#         print self.stack
         raise XMLFileException,'Closing XML file with nonclosed tags'
      if self.fclose:
         self.file.close()
      if self.TempFile and self.FileNameSufix:
         acnt=10
         while acnt:
            acnt=acnt-1
            try:
               if 0:
                  if os.path.exists(self.FileName):
                     os.unlink(self.FileName)
                  os.rename(self.FileName+self.FileNameSufix,self.FileName)
               else:
                  win32file.MoveFileEx(self.FileName+self.FileNameSufix,self.FileName,win32file.MOVEFILE_REPLACE_EXISTING)
               break
            except:
               time.sleep(3.0)
               if not acnt:
                  print 'UNABLE TO RENAME FILE: "%s" to "%s"'%(self.FileName+self.FileNameSufix,self.FileName)
                  raise
   def write(self,atext):
#      if self.Encoding=='utf-8':
#         atext=CP1250_To_UTF8(atext)
      self.file.write(atext)
   def Header(self,aencoding=None,astandalone=''):
      if aencoding is None:
         aencoding=self.Encoding
      if astandalone:
         astandalone=' standalone="%s"'%astandalone
      self.write('<?xml version="1.0" encoding="%s"%s?>\n\n'%(aencoding,astandalone))
   def Comment(self,acomment):
      if acomment:
         aindent='   '*len(self.stack)
         l=string.split(acomment,'\n')
         if l:
            if not string.strip(l[-1]):
               l=l[-1:]
         self.write('%s<!--\n'%(aindent,))
         for s in l:
            self.write('%s   %s\n'%(aindent,string.strip(s)))
         self.write('%s-->\n'%(aindent,))
   def TagOpen(self,atag,d=None,aindent='',aclosetag=0,ainsertemptyattributes=0,anoattributeconversion=0,anl='\n',asortattrnames=None,avalue='',avalueascdata=1,aproperxmlattrs=None):
      if not aindent:
         aindent='   '*len(self.stack)
      if aproperxmlattrs is None:
         aproperxmlattrs=[]
      if asortattrnames is None:
         asortattrnames=[]
      sa,sc,lv='',' />',[]
      if not d is None:
         self.current_attrs=d
         lk=d.keys()
         lk.sort()
         if asortattrnames:
            for aattr in lk:
               if not aattr in asortattrnames:
                  asortattrnames.append(aattr)
            lk=asortattrnames
         for aattr in lk:
            if not d.has_key(aattr):
               continue
            v=d[aattr]
            if type(v)==type(()) and len(v) in [3,7]:
               v=ICORUtil.tdatetime2str(v,' ')
            elif v is None and aattr in asortattrnames:
               pass
            elif v is None:
               raise XMLFileException,'attribute value is None: "%s"'%aattr
            elif not isinstance(v,types.StringTypes):
               v=str(v)
            if v or ainsertemptyattributes:
               if anoattributeconversion or aattr in aproperxmlattrs:
                  lv.append('%s="%s"'%(aattr,v))
               elif self.Encoding=='utf-8':
                  lv.append('%s="%s"'%(aattr,GetAsXMLStringSimple(v)))
               elif self.NoPL:
                  lv.append('%s="%s"'%(aattr,GetAsXMLStringNoPL(v)))
               elif self.AttrAsCData:
#                  lv.append('%s="%s"'%(aattr,GetAsXMLStringCDataNoPL(v)))
                  lv.append('%s="%s"'%(aattr,GetAsXMLString(v.replace(']]','] ]'))))
               else:
                  lv.append('%s="%s"'%(aattr,GetAsXMLString(v)))
      else:
         self.current_attrs={}
      if lv:
         sa=' '+string.join(lv,' ')
      se=''
      if not aclosetag:
         self.stack.append(atag)
         sc='>'
      elif avalue:
         sc='>'
         se='</'+atag+'>'
      if avalue and avalueascdata:
         if self.Encoding=='utf-8':
            avalue='<![CDATA[%s]]>'%avalue.replace(']]','] ]')
         else:
            avalue='<![CDATA[%s]]>'%GetAsXMLStringCDataNoPL(avalue.replace(']]','] ]'))
      self.write('%s<%s%s%s%s%s%s'%(aindent,atag,sa,sc,avalue,se,anl))
   def TagClose(self,atag='',aindent=''):
      if not atag:
         atag=self.stack.pop()
      else:
         btag=self.stack.pop()
         if btag!=atag:
            raise XMLFileException,'Tag stack is incorrect: "%s" - should be "%s"'%(atag,btag)
      if aindent==0:
         aindent=''
      elif not aindent:
         aindent='   '*len(self.stack)
      self.write('%s</%s>\n'%(aindent,atag))

class MXMLRecordset(MXMLFile):
   def __init__(self,afile):
      MXMLFile.__init__(self,afile,anopl=1)
      self.nodeSchema,self.nodeElementType,self.NodeData=0,0,0
      self.Cols={}
      self.ColsCnt=0
      self.Record={}
      self.RecordDefault={}
   def Header(self,aencoding='Windows-1250'):
      MXMLFile.Header(self,aencoding)
      d={'xmlns:s':'uuid:BDC6E3F0-6DA3-11d1-A2A3-00AA00C14882','xmlns:dt':'uuid:C2F41010-65B3-11d1-A29F-00AA00C14882','xmlns:rs':'urn:schemas-microsoft-com:rowset','xmlns:z':'#RowsetSchema',}
      self.TagOpen('xml',d,anoattributeconversion=1)
   def close(self):
      if self.NodeData:
         self.TagClose('rs:data')
         self.NodeData=0
      if self.nodeElementType:
         self.TagClose('s:ElementType')
         self.nodeElementType=0
      if self.nodeSchema:
         self.TagClose('s:Schema')
         self.nodeSchema=0
      self.TagClose('xml')
      MXMLFile.close(self)
   def AddRow(self,aname='',arsname='',atype=mt_String,amaxlength=200):
      if not self.nodeSchema:
         self.nodeSchema=1
         d={'id':'RowsetSchema'}
         self.TagOpen('s:Schema',d)
      if not self.nodeElementType:
         self.nodeElementType=1
         d={'name':'row','content':'eltOnly','rs:CommandTimeout':'30'}
         self.TagOpen('s:ElementType',d)
      self.ColsCnt=self.ColsCnt+1
#      if not aname or self.Cols.has_key(aname):
      scname='c'+str(self.ColsCnt)
#      else:
#         scname=aname
      self.Cols[aname]=scname,atype
      self.Cols[scname]=scname,atype
      d={'name':scname,'rs:name':arsname,'rs:number':str(self.ColsCnt),'rs:writeunknown':'true'}
      self.TagOpen('s:AttributeType',d)
      if atype==mt_String:
         d={'dt:type':'string','rs:dbtype':'str','dt:maxLength':str(amaxlength),'rs:maybenull':'false'}
         self.RecordDefault[scname]=''
         self.Record[scname]=''
      elif atype==mt_Integer:
         d={'dt:type':'int','dt:maxLength':'4','rs:precision':'10','rs:fixedlength':'true','rs:maybenull':'false'}
         self.RecordDefault[scname]=0
         self.Record[scname]=0
      elif atype==mt_DateTime:
         d={'dt:type':'dateTime','rs:dbtype':'timestamp','dt:maxLength':'16','rs:scale':'0','rs:precision':'16','rs:fixedlength':'true','rs:maybenull':'false'}
         self.RecordDefault[scname]='1900-01-01T00:00:00'
         self.Record[scname]='1900-01-01T00:00:00'
      elif atype==mt_Double:
         d={'dt:type':'number','rs:dbtype':'numeric','dt:maxLength':'19','rs:precision':'10','rs:scale':'4','rs:precision':'19','rs:fixedlength':'true','rs:maybenull':'false'}
         self.RecordDefault[scname]=0.0
         self.Record[scname]=0.0
      elif atype==mt_Memo:
         d={'dt:type':'string','rs:dbtype':'str','dt:maxLength':'2147483647','rs:long':'true','rs:maybenull':'false'}
         self.RecordDefault[scname]=''
         self.Record[scname]=''
      elif atype==mt_Boolean:
         d={'dt:type':'boolean','dt:maxLength':'2','rs:fixedlength':'true','rs:maybenull':'false'}
         self.RecordDefault[scname]='0'
         self.Record[scname]='0'
      else:
         raise XMLFileException,'Unknown type "%d" for row "%s/%s"'%(atype,aname,arsname,)
      self.TagOpen('s:datatype',d,aclosetag=1)
      self.TagClose('s:AttributeType')
   def __setitem__(self,key,value):
      if not self.Cols.has_key(key):
         raise XMLFileException,'Unknown column name "%s"'%(key,)
      acol,atype=self.Cols[key]
      if atype==mt_DateTime or type(value)==type(()):
         if isinstance(value,types.StringTypes):
            value=ICORUtil.getStrAsDate(value)
         value=ICORUtil.tdate2fmtstr(value,delimiter='-',longfmt=1)+'T'+ICORUtil.ttime2fmtstr(value,longfmt=1)
      elif atype==mt_Boolean:
         if type(value)!=type(1):
            value=ICORUtil.str2bool(value)
         if value:
            value='True'
         else:
            value='False'
      if isinstance(value,types.StringTypes):
         self.Record[acol]=value[:200]
      else:
         self.Record[acol]=value
   def AddData(self,adata=None):
      if self.nodeElementType:
         self.TagClose('s:ElementType')
         self.nodeElementType=0
      if self.nodeSchema:
         self.TagClose('s:Schema')
         self.nodeSchema=0
      if not self.NodeData:
         self.NodeData=1
         self.TagOpen('rs:data')
      if not adata is None:
         self.Record=adata
      self.TagOpen('z:row',self.Record,aclosetag=1,ainsertemptyattributes=1)
      for akey in self.RecordDefault.keys():
         self.Record[akey]=self.RecordDefault[akey]

class ICORBaseXMLParser(xmllib.XMLParser):
   def __init__(self):
      xmllib.XMLParser.__init__(self,accept_utf8=1,accept_unquoted_attributes=1,accept_missing_endtag_name=1)
      self.Comments=[]
      self.TagData=''
      self.DisableEndTag=1
      self.status=[]
   def Parse(self,ainput,afname=''):
      self.status=[]
      self.reset()
      if afname:
         ainput=open(afname,'r')
      try:
         if isinstance(ainput,types.StringTypes):
            self.feed(ainput)
         else:
            while 1:
               l=ainput.readline()
               if not l:
                  break
               self.feed(l)
      finally:
         if afname:
            ainput.close()
   def CheckAttrs(self,attrs,lvalid):
      ret=[]
      for akey in attrs.keys():
         if not akey in lvalid:
            ret.append(akey)
      return ret
   def ElementInfo(self,astr='',astatus=0):
      if astatus:
         self.status.append(' '*len(self.stack)+' '+self.stack[len(self.stack)-1][2]+' '+astr)
      else:
         print ' '*len(self.stack),self.stack[len(self.stack)-1][2],astr
   def Attrs_UTF8_To_CP1250(self,attrs):
      d={}
      for aattr in attrs.keys():
         d[aattr]=unicode(attrs.get(aattr,''),'utf-8').encode('cp1250')
      return d
   def Dump(self,fout=None,anoprint=0):
      for aline in self.status:
         if not anoprint:
            print aline
         if fout:
            fout.write(aline+'\n')
   def GetComments(self,aclear=1):
      ret=string.join(self.Comments,'\n')
      if aclear:
         self.Comments=[]
      return ret
   def ClearComments(self):
      self.Comments=[]
   def syntax_error(self,message):
      self.status.append('błąd w danych XML w linii %d: %s'%(self.lineno,message))
   def unknown_starttag(self,tag,attrs):
      self.status.append('nieznany tag początkowy w linii %d: %s'%(self.lineno,tag))
   def unknown_endtag(self,tag):
      if not self.DisableEndTag:
         self.status.append('nieznany tag końcowy w linii %d: %s'%(self.lineno,tag))
   def unknown_entityref(self,ref):
      self.status.append('nieznany wielkość referencyjna w linii %d: %s'%(self.lineno,ref))
   def unknown_charref(self,ref):
      self.status.append('nieznany wartość referencyjna w linii %d: %s'%(self.lineno,ref))
   def handle_comment(self,comment):
      comment=string.replace(comment,chr(13),'')
      if comment[:1]==chr(10):
         comment=comment[1:]
      if comment[-1:]==chr(10):
         comment=comment[:-1]
      self.Comments.append(comment)
   def handle_data(self,data):
      self.TagData=self.TagData+data
   def handle_cdata(self,data):
      self.TagData=self.TagData+data



