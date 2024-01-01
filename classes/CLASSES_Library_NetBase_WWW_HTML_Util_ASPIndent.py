# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string
import re
import types

class ASPIndentedFile:
   def open(self,fout,fileclose=None):
      if isinstance(fout,types.StringTypes):
         self.fout=open(fout,'w')
         self.fileclose=1
      else:
         self.fileclose=0
         self.fout=fout
      if not fileclose is None:
         self.fileclose=fileclose
      self.invb,self.aindent,self.ashiftr=0,0,0
   def close(self):
      if self.fileclose:
         self.fout.close()
   def write(self,atext):
      sl=string.split(atext,'\n')
      for s in sl:
         s=string.replace(s,chr(13),'')
         if s[:2]==r'<%':
            self.invb=1
         if string.strip(s)[:2]=='%>' or string.strip(s)[-2:]=='%>':
            self.invb=0
         if self.invb:
            so=s=string.strip(s)
            aic=string.find(s,"'")
            if aic>=0:
               s=string.strip(s[:aic])
            slow=s[:9].lower()
            if slow[:3]=='if ':
               if not string.find(s,'then ')>3:
                  self.ashiftr=1
            elif slow[:4]=='sub ':
               self.ashiftr=1
            elif slow[:9]=='function ':
               self.ashiftr=1
            elif slow[:3]=='do ' or slow=='do':
               self.ashiftr=1
            elif slow[:4]=='for ':
               self.ashiftr=1
            elif slow[:4]=='else':
               self.aindent=self.aindent-1
               self.ashiftr=1
            elif slow[:7]=='select ':
               self.ashiftr=1
            if slow[:4]=='end ':
               self.aindent=self.aindent-1
            elif slow[:4]=='loop':
               self.aindent=self.aindent-1
            elif slow[:4]=='next':
               self.aindent=self.aindent-1
            if self.aindent<0:
               self.aindent=0
            if so[:2]=='%>' or so[:2]=='<%':
               s=so+'\n'
            else:
               s='%s%s\n'%('   '*self.aindent,so)
            self.fout.write(s)
            if self.ashiftr:
               self.aindent=self.aindent+1
               self.ashiftr=0
         else:
            self.fout.write(s+'\n')



