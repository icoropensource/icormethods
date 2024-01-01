# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import string
import xmllib

class MHTMLXLSCell:
   def __init__(self,atable):
      self.Table=atable
      self.Attrs={}
      self.Data=[]
      self._Text,self._Value,self._Formula,self._Line,self._ValueAsString=None,None,None,None,None
      self.IsCalculated=0
   def __getattr__(self,name):
      if name=='Text':
         if self._Text is None:
            self._Text=string.join(map(string.strip,filter(lambda x: type(x)==type(''),self.Data)),'')
            self._Text=string.replace(self._Text,chr(10),'')
            self._Text=string.replace(self._Text,chr(13),'')
         return self._Text
      elif name=='Line':
         if self._Line is None:
            self._Line=''
            for adata in acell.Data:
               if type(adata)==type(''):
                  self._Line=self._Line+XMLUtil.GetAsXMLStringNoPL(adata)
               else:
                  s1,da=adata
                  if da is None:
                     self._Line=self._Line+s1
                  else:
                     self._Line=self._Line+'<'+s1
                     lkeys=da.keys()
                     lkeys.sort()
                     for akey in lkeys:
                        self._Line=self._Line+' %s="%s"'%(akey,da[akey])
                     self._Line=self._Line+'>'
         return self._Line
      elif name=='Value':
         if self._Value is None:
            if self.Attrs.has_key('x:num'):
               self._Value=float(self.Attrs['x:num'])
            else:
               self._Value=string.join(map(string.strip,filter(lambda x: type(x)==type(''),self.Data)),'')
               self._Value=string.replace(self._Value,chr(10),'')
               self._Value=string.replace(self._Value,chr(13),'')
         return self._Value
      elif name=='ValueAsInt':
         if self._Value is None:
            if self.Attrs.has_key('x:num'):
               self._Value=self.Attrs['x:num']
            else:
               self._Value=string.join(map(string.strip,filter(lambda x: type(x)==type(''),self.Data)),'')
               self._Value=string.replace(self._Value,chr(10),'')
               self._Value=string.replace(self._Value,chr(13),'')
            try:
               self._Value=int(self._Value)
            except:
               self._Value=0
         return self._Value
      elif name=='ValueAsString':
         if self._ValueAsString is None:
            v=self.Value
            if type(v)==type(''):
               self._ValueAsString=v
            else:
               self._ValueAsString=str(v)
               if self._ValueAsString[-2:]=='.0':
                  self._ValueAsString=self._ValueAsString[:-2]
         return self._ValueAsString
      elif name=='Formula':
         if self._Formula is None:
            self._Formula=self.Attrs.get('x:fmla','')
         return self._Formula
   def SetValue(self,avalue):
      try:
         bvalue=float(avalue)
         self.Attrs['x:num']=avalue
      except ValueError:
         bvalue=avalue
      self.IsCalculated=1
      self._Value=bvalue
      self._ValueAsString=None

class MHTMLXLSTable:
   def __init__(self):
      self.Rows=[]
      self.RowAttrs={}
      self.HTMLTextBefore=''
      self.HTMLTextAfter=''
      self.MaxCol,self.MaxRow=-1,-1
   def __getitem__(self,key):
      acol,arow=key
      self.MaxCol=max(acol,self.MaxCol)
      self.MaxRow=max(arow,self.MaxRow)
      while arow>len(self.Rows):
         self.Rows.append([])
      lrow=self.Rows[arow-1]
      while acol>len(lrow):
         lrow.append(None)
      acell=self.Rows[arow-1][acol-1]
      if acell is None:
         acell=MHTMLXLSCell(self)
         self.Rows[arow-1][acol-1]=acell
      return acell
   def ProcessSpannedCells(self):
      arow,mrow=0,len(self.Rows)
      while arow<mrow:
         lrow=self.Rows[arow]
         acol,mcol=0,len(lrow)
         while acol<mcol:
            acell=lrow[acol]
            if not acell is None:
               if acell.Attrs.has_key('x:str'):
                  acell.Data.append(acell.Attrs['x:str'])
                  del acell.Attrs['x:str']
               if acell.Attrs.has_key('x:num') and not acell.Data:
                  acell.Data.append(acell.Attrs['x:num'])
               acspan=int(acell.Attrs.get('colspan','0'))
               for i1 in range(acspan-1):
                  lrow.insert(acol+1,None)
                  mcol=mcol+1
            acol=acol+1
         arow=arow+1
      arow,mrow=0,len(self.Rows)
      while arow<mrow:
         lrow=self.Rows[arow]
         acol,mcol=0,len(lrow)
         while acol<mcol:
            acell=lrow[acol]
            if not acell is None:
               arspan=int(acell.Attrs.get('rowspan','0'))
               if arspan:
                  acspan=int(acell.Attrs.get('colspan','1'))
                  for i2 in range(arspan-1):
                     l2row=self.Rows[arow+i2+1]
                     for i1 in range(acspan):
                        l2row.insert(acol,None)
            acol=acol+1
         arow=arow+1
   def DumpAsHTML(self,fout,aasvisible=0):
      fout.write(self.HTMLTextBefore)
      irow=1
      for arow in self.Rows:
         da=self.RowAttrs.get(irow,{})
         lkeys=da.keys()
         if lkeys:
            lkeys.sort()
            fout.write('<tr')
            for akey in lkeys:
               fout.write(' %s="%s"'%(akey,da[akey]))
            fout.write('>\n')
         else:
            fout.write('<tr>\n')
         icell=1
         for acell in arow:
            if not acell is None:
               fout.write('  <td')
               lkeys=acell.Attrs.keys()
               lkeys.sort()
               for akey in lkeys:
                  fout.write(' %s="%s"'%(akey,acell.Attrs[akey]))
               s='>'
               w1=acell.IsCalculated and aasvisible
               w2=1
               for adata in acell.Data:
                  if type(adata)==type(''):
                     w3=0
                     if w1 and adata[:3]=='#!=':
                        adata=acell.ValueAsString
                        w3=1
                     if w2:
                        s=s+XMLUtil.GetAsXMLStringNoPL(adata)
                     if w3:
                        w2=0
                  else:
                     s1,da=adata
                     if da is None:
                        s=s+s1
                     else:
                        s=s+'<'+s1
                        lkeys=da.keys()
                        lkeys.sort()
                        for akey in lkeys:
                           s=s+' %s="%s"'%(akey,da[akey])
                        s=s+'>'
               fout.write(s)
               fout.write('</td>\n')
            icell=icell+1
         fout.write('</tr>\n')
         irow=irow+1
      fout.write(self.HTMLTextAfter)
   
class MHTMLXLSTableParser(xmllib.XMLParser):
   def __init__(self):
      xmllib.XMLParser.__init__(self,accept_unquoted_attributes=1,accept_utf8=1,map_case=1,accept_missing_endtag_name=1)
      self.__accept_unquoted_attributes=1
      self.HTMLText=''
      self.Table=MHTMLXLSTable()
      self.status=[]
      self.lines=[]
      self.Row,self.Col=1,1
      self.InTD=0
   def GetTableText(self,atext):
      apos=string.find(atext,'<tr ')
      if apos>=0:
         self.Table.HTMLTextBefore=atext[:apos]
         atext=atext[apos:]
      apos=string.rfind(atext,'</tr>')
      if apos>=0:
         self.Table.HTMLTextAfter=atext[apos+5:]
         atext=atext[:apos+5]
      self.HTMLText=atext
   def Process(self,atext):
      self.GetTableText(atext)
      self.reset()
      self.elements={}
      self.elements['table']=(self.start_TABLE,self.end_TABLE)
      self.elements['tr']=(self.start_TR,self.end_TR)
      self.elements['td']=(self.start_TD,self.end_TD)
      self.feed('<table>'+self.HTMLText+'</table>')
   def start_TABLE(self,attrs):
      pass
   def start_TR(self,attrs):
      self.Table.RowAttrs[self.Row]=attrs
   def start_TD(self,attrs):
      acell=self.Table[self.Col,self.Row]
      acell.Attrs=attrs
      self.lines=[]
      self.InTD=1
   def handle_data(self,data):
      s=string.replace(data,'\n','')
      s=string.replace(s,'\r ','')
      self.lines.append(s)
   def end_TR(self):
      self.Row=self.Row+1
      self.Col=1
   def end_TD(self):
      acell=self.Table[self.Col,self.Row]
      acell.Data=self.lines[:]
      self.Col=self.Col+1
      self.InTD=0
   def end_TABLE(self):
      self.Table.ProcessSpannedCells()
   def syntax_error(self,message):
      self.status.append('error in data: %s'%(message))
   def unknown_starttag(self,tag,attrs):
      if self.InTD:
         self.lines.append([tag,attrs])
      else:
         self.status.append('unknown starttag: %s'%tag)
   def unknown_endtag(self,tag):
      if self.InTD:
         self.lines.append(['/'+tag,{}])
      else:
         self.status.append('unknown endtag: %s'%tag)
   def unknown_entityref(self,ref):
      if ref=='nbsp' and self.InTD:
         self.lines.append(['&nbsp;',None])
      else:
         self.status.append('unknown entityref: %s'%ref)
   def unknown_charref(self,ref):
      self.status.append('unknown charref: %s'%ref)

def _Test():
   fin=open('data2.htm','r')
   atext=fin.read()
   fin.close()
   
   amhtmltableparser=MHTMLXLSTableParser()
   amhtmltableparser.Process(atext)
   
   fout=open('out.htm','w')
   amhtmltableparser.Table.DumpAsHTML(fout)
   fout.close()
   
   if amhtmltableparser.status:
      fout=open('status.txt','w')
      for s in amhtmltableparser.status:
         fout.write(s+'\n')
      fout.close()



