# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
import re

"""
acsv=CSVImport()
acsv.Open('file.csv')
try:
   print acsv.Header
   while not acsv.EOF:
      print acsv.Record
      acsv.Next()
finally:
   acsv.Close()
"""

class CSVImport:
   def __init__(self,adelimiter=';',atextQualifier='"',ahasheader=1,astripdata=1,acleandata=0,aheaderline=''): #"
      self.Delimiter=adelimiter
      self.TextQualifier=atextQualifier
      self.HasHeader=ahasheader
      self.StripData=astripdata
      self.CleanData=acleandata
      self.CleanPattern=re.compile('[^ -~ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]')
      self.ForceHeaderLine=aheaderline
   def __getitem__(self,name):
      atype=mt_String
      if type(name)==type(()):
         name,atype=name
      apos=self._Header[name]
      if apos<len(self.Record):
         ret=string.replace(self.Record[apos],'\\n','\n')
      else:
         ret=''
      if atype in [mt_Integer,mt_Boolean,]:
         ret=int(ret)
      elif atype in [mt_Double]:
         ret=float(ret)
      elif atype==mt_DateTime:
         ret=ICORUtil.getStrAsDate(ret)
      return ret
   def get(self,akey,adefvalue=None):
      if self._Header.has_key(akey):
         return string.replace(self.Record[self._Header[akey]],'\\n','\n')
      return adefvalue
   def ParseLine(self,line):
      delimiter=self.Delimiter
      textQualifier=self.TextQualifier
      if textQualifier:
         record = []
         inquotes = 0
         for s in line.split(delimiter):
            odd = s.count(textQualifier)%2
            if inquotes:
               accu+=delimiter + s.replace(textQualifier * 2, delimiter).replace(textQualifier, '').replace(delimiter, textQualifier)
               if odd:
                  record.append(accu)
                  inquotes = 0
            else:
               if s.count(textQualifier):
                  s = s.strip()
               if s == textQualifier * 2: 
                  s = ""
               accu = s.replace(textQualifier * 2, delimiter).replace(textQualifier, '').replace(delimiter, textQualifier)
               if odd:
                  inquotes = 1
               elif self.StripData:
                  record.append(string.strip(accu))
               else:
                  record.append(accu)
      else:
         if self.StripData:
            record=map(string.strip, line.split(delimiter))
         else:
            record=line.split(delimiter)
      return record
   def ParseLineBAD(self,aline):
      if self.StripData:
         aline=string.strip(aline)
      l=self.Pattern.findall(aline)
      ret=[]
      for s1,s2 in l:
         s=string.replace(s1 or s2,self.TextQualifier*2,self.TextQualifier)
         if self.StripData:
            s=string.strip(s)
         if self.CleanData:
            s=self.CleanPattern.sub('',s)
         ret.append(s)
      return ret
   def Open(self,afile):
      ret=[]
      if type(afile)==type(''):
         self.fin=ICORUtil.OpenText(afile,'r')
         self.fclose=1              
      else:
         self.fin=afile
         self.fclose=0
      if not self.Delimiter:
         l1=self.fin.readline()
         l2=self.fin.readline()
         self.fin.seek(0)
         amax=-1
         for c in [',',';','|',chr(9)]:
            sl1=string.split(l1,c)
            sl2=string.split(l2,c)
            if len(sl1)==len(sl2) and len(sl1)>amax:
               self.Delimiter=c
               amax=len(sl1)
      self.Pattern=re.compile('(?:(?:[%s]|^)%s(.*?)%s(?=[%s]|$))|(?:(?:[%s]|^)([^%s%s]*?)(?=[%s]|$))'%(self.Delimiter,self.TextQualifier,self.TextQualifier,self.Delimiter,self.Delimiter,self.TextQualifier,self.Delimiter,self.Delimiter),re.S)
      self._Header={}
      if self.HasHeader:
         self.headerline=self.fin.readline()
         if self.ForceHeaderLine:
            self.headerline=self.ForceHeaderLine
         if self.headerline:
            self.Header=self.ParseLine(self.headerline[:-1])
            for i in range(len(self.Header)):
               self._Header[self.Header[i]]=i
      else:
         self.Header=[]
         if self.ForceHeaderLine:
            self.headerline=self.ForceHeaderLine
            self.Header=self.ParseLine(string.replace(self.headerline,'\n',''))
            for i in range(len(self.Header)):
               self._Header[self.Header[i]]=i
      self.EOF=0
      self.Next()
   def Next(self):
      self.line=self.fin.readline()
      if self.line[-1:]=='\n':
         self.line=self.line[:-1]
      if not self.line or self.line=='KONIEC':
         self.EOF=1
         return
      self.Record=self.ParseLine(self.line)
   def Close(self):
      if self.fclose:
         self.fin.close()

class CSVExport:
   def __init__(self,adelimiter=';',atextQualifier='"',ahasheader=1,astripdata=1,areducefloatprecision=1,acleandata=0,aemptyvalues=1): #"
      self.Delimiter=adelimiter
      self.TextQualifier=atextQualifier
      self.HasHeader=ahasheader
      self.StripData=astripdata
      self.ReduceFloatPrecision=areducefloatprecision
      self.Header=[]
      self.CleanData=acleandata
      self.CleanPattern=re.compile('[^ -~ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]')
      self.EmptyValues=aemptyvalues
   def __setitem__(self,name,value):
      self.Record[name]=value
   def __getitem__(self,name):
      return string.replace(self.Record.get(name,''),'\\n','\n')
   def Open(self,afile):
      ret=[]
      if type(afile)==type(''):
         self.fout=ICORUtil.OpenText(afile,'w')
         self.fclose=1
      else:
         self.fout=afile
         self.fclose=0
      self._Header={}
      l=[]
      for i in range(len(self.Header)):
         self._Header[self.Header[i]]=i
         s=self.Header[i]
         if self.TextQualifier:
            s=self.TextQualifier+string.replace(s,self.TextQualifier,'')+self.TextQualifier
         l.append(s)
      if self.HasHeader:
         s=string.join(l,self.Delimiter)
         self.fout.write(s+'\n')
      self.Record={}
   def AssignFromCSV(self,afname,afile,anoempty=0):
      self.Header=afile.Header
      self.Open(afname)
      while not afile.EOF:
         for acol in self.Header:
            s=afile[acol]
            s=string.strip(s)
            if anoempty and not s:
               s=" "
            self.Record[acol]=s
         afile.Next()
         self.Next()
   def GetValueAsString(self,avalue):
      if type(avalue)==type(''):
         if self.StripData:
            avalue=string.strip(avalue)
         if self.TextQualifier:
            avalue=self.TextQualifier+string.replace(avalue,self.TextQualifier,'')+self.TextQualifier
      elif type(avalue)==type(()) or type(avalue)==type([]):
         if len(avalue)==3:
            y,m,d=avalue
            y,m,d=ICORUtil.normalizeDate(y,m,d)
            while y>=3000:
               y=y-1000
            avalue='%04d-%02d-%02d'%(y,m,d)
         else:
            l=list(avalue)
            avalue=''
            for avi in l:
               s=self.GetValueAsString(avi)
               if avalue:
                  avalue=avalue+'-'
               avalue=avalue+s
      elif type(avalue)==type(0.0):
         if self.ReduceFloatPrecision:
            avalue='%0.2f'%avalue
         else:
            avalue=str(avalue)
      else:
         avalue=str(avalue)
      avalue=string.replace(avalue,'\n','\\n')
      if self.CleanData:
         avalue=self.CleanPattern.sub('',avalue)
      return avalue
   def Next(self):
      if not self.Record:
         return
      l=[]
      for i in range(len(self.Header)):
         afield=self.Header[i]
         avalue=self.Record.get(afield,'')
         if self.EmptyValues and avalue=='':
            pass
         else:
            avalue=self.GetValueAsString(avalue)
         l.append(avalue)
      s=string.join(l,self.Delimiter)
      self.fout.write(s+'\n')
      self.Record={}
   def Close(self):
      if self.fclose:
         self.fout.close()

def GetSimpleDictFromCSV(afile,acolkey,acolvalue):
   ret={}
   acsv=CSVImport()
   acsv.Open(afile)
   while not acsv.EOF:
      ret[acsv[acolkey]]=acsv[acolvalue]
      acsv.Next()
   return ret

class DictFromCSV:
   def __init__(self,afile,acolkeys):
      self.Dict={}
      acsv=CSVImport(acleandata=1)
      acsv.Open(afile)
      while not acsv.EOF:
         akey=[]
         for acol in acolkeys:
            akey.append(acsv[acol])
         d={}
         for acol in acsv.Header:
            d[acol]=acsv[acol]
         self.Dict[string.join(akey,'_')]=d
         acsv.Next()
   def __getitem__(self,akey):
      ret={}
      if type(akey)==type(''):
         ret=self.Dict.get(akey,{})
      elif type(akey)==type(()):
         akey,acols=akey
         if type(akey)==type([]):
            akey=string.join(akey,'_')
         d=self.Dict.get(akey,{})
         if type(acols)==type(''):
            ret=d.get(acols,'')
         elif type(acols)==type(()):
            acol,atype=acols
            ret=d.get(acol,'')
            if atype in [mt_Integer,mt_Boolean,]:
               ret=int(ret)
            elif atype in [mt_Double]:
               ret=float(ret)
            elif atype==mt_DateTime:
               ret=ICORUtil.getStrAsDate(ret)
         elif type(acols)==type([]):
            ret=[]
            for acol in acols:
               if type(acol)==type(''):
                  ret.append(d.get(acol,''))
               elif type(acol)==type(()):
                  acol,atype=acol
                  s=d.get(acol,'')
                  if atype in [mt_Integer,mt_Boolean,]:
                     s=int(s)
                  elif atype in [mt_Double]:
                     s=float(s)
                  elif atype==mt_DateTime:
                     s=ICORUtil.getStrAsDate(s)
                  ret.append(s)
               else:
                  ret.append('')
      return ret



