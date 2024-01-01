# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import tokenize
import token
import keyword
import string
import StringIO

class PrettyPyPrinter:
   def __init__(self,aspage=0):
      self.AsPage=aspage
   def TokenEater(self,atokentype,atokenstring,abeginrowcolumntuple,aendrowcolumntuple,aline):
      brow,bcol=abeginrowcolumntuple
      erow,ecol=aendrowcolumntuple
      self.token_list.append([brow,bcol,erow,ecol,atokentype,atokenstring])
   def Process(self,atext):
      fin=StringIO.StringIO(atext)
      self.Tokenize(fin)
      self.result=[]
      self.Generate()
      return string.join(self.result,'\n')
   def InsertTag(self,arow,acol,s):
      self.lines[arow-1]=self.lines[arow-1][:acol]+s+self.lines[arow-1][acol:]
   def ReplaceString(self,arow,acol1,acol2,s):
      self.lines[arow-1]=self.lines[arow-1][:acol1]+s+self.lines[arow-1][acol2:]
   def Tokenize(self,fin):
      self.token_list=[]
      tokenize.tokenize(fin.readline,self.TokenEater)
      fin.seek(0)
      self.lines=fin.readlines()
      self.token_list.sort()
      self.token_list.reverse()
   def Generate(self):
      for i in range(len(self.token_list)):
         brow,bcol,erow,ecol,atokentype,atokenstring=self.token_list[i]
         processed=' '
         if atokentype==token.OP:
            self.InsertTag(erow,ecol,'</font>')
            self.InsertTag(brow,bcol,'<font color="PURPLE">')
            processed='*'
         elif atokentype==token.NAME:
            if keyword.iskeyword(atokenstring):
               self.InsertTag(erow,ecol,'</b></font>')
               self.InsertTag(brow,bcol,'<font color="NAVY"><b>')
            elif atokenstring=='None':
               self.InsertTag(erow,ecol,'</font>')
               self.InsertTag(brow,bcol,'<font color="RED">')
            elif __builtins__.__dict__.has_key(atokenstring) and self.token_list[i+1][5]!='.':
               self.InsertTag(erow,ecol,'</font>')
               self.InsertTag(brow,bcol,'<font color="NAVY">')
            elif i>0 and self.token_list[i+1][5] in ['def','class']:
               self.InsertTag(erow,ecol,'</B></font>')
               self.InsertTag(brow,bcol,'<font color="BLUE"><B>')
            elif i>0 and self.token_list[i-1][5]=='(':
               self.InsertTag(erow,ecol,'</font>')
               self.InsertTag(brow,bcol,'<font color="PURPLE">')
            else:
               self.InsertTag(erow,ecol,'</font>')
               self.InsertTag(brow,bcol,'<font color="BLACK">')
            processed='*'
         elif atokentype==token.NUMBER:
            self.InsertTag(erow,ecol,'</font>')
            self.InsertTag(brow,bcol,'<font color="RED">')
            processed='*'
         elif atokentype==token.STRING:
            self.InsertTag(erow,ecol,'</font>')
            if brow==erow:
               atokenstring=string.replace(atokenstring,'&','&amp;')
               atokenstring=string.replace(atokenstring,'"','&quot;') #"
               atokenstring=string.replace(atokenstring,'<','&lt;')
               atokenstring=string.replace(atokenstring,'>','&gt;')
               self.ReplaceString(brow,bcol,ecol,atokenstring)
            self.InsertTag(brow,bcol,'<font color="MAGENTA">')
            processed='*'
         elif atokentype==token.N_TOKENS:
            self.InsertTag(erow,ecol,'</I></font>')
            self.InsertTag(brow,bcol,'<font color="NAVY" style="background=YELLOW;"><I>')
            processed='*'
         elif atokentype in [token.NEWLINE,token.INDENT,token.DEDENT,token.ENDMARKER,40]: #40==NL
            processed='*'
         if processed==' ':
            print '%s %5d%5d%5d%5d | %d%20s >%s<'%(processed,brow,bcol,erow,ecol,atokentype,token.tok_name[atokentype],str(atokenstring))
         i=i+1
      if self.AsPage:
         self.result.append('<html><body>\n')
      self.result.append('<pre>')
      for aline in self.lines:
         s=string.replace(aline,'\n','<br>\n')
         #s=string.replace(aline,chr(255),'&nbsp;')
         self.result.append(s)
      self.result.append('</pre>')
      if self.AsPage:
         self.result.append('\n</body></html>')

def PrettyPyPrint(atext):
   aprinter=PrettyPyPrinter()
   s=string.replace(aprinter.Process(atext),chr(13),'')
   s=string.replace(s,chr(10)+chr(10),chr(10))
   return s



