# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

import sys
import string
from CLASSES_Library_NetBase_Utils_HTMLParser import HTMLParser
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil

class HTMLChecker(HTMLParser):
   def __init__(self,aignorelinks='',aindentonly=0):
      HTMLParser.__init__(self)
      self.tablestack=[]
      self.inputlines=[]
      self.ignoretags=['link','meta','img','br','hr','input','li',]
      if aignorelinks:
         self.ignoretags=[]
         l=string.split(aignorelinks,',')
         for atag in l:
            self.ignoretags.append(string.strip(atag))
      self.indentonly=aindentonly
   def Parse(self,atext,fout,aashtml=0):
      if self.indentonly:
         atext=string.replace(atext,'>\n','>')
         atext=string.replace(atext,'>','>\n')
         atext=string.replace(atext,'\n\n','\n')
      l=string.split(atext,'\n')
      for aline in l:
         self.inputlines.append([-1,string.strip(aline),'',' '])
      self.errcount=0
      self.feed(atext)
      if self.tablestack and not self.errcount:
         acomment='*** ERROR *** Unknown error: tag stack is not empty - check everything! %s'%str(self.tablestack)
         self.inputlines.append([0,'',acomment,'#'])
#         print acomment
      aindent=0
      sindent=''
      c=''
      i=1
      for apos,aline,acomment,achar in self.inputlines:
         if self.indentonly:
            if apos>=0:
               sindent='  '*apos
            if aashtml and aline:
               aline=XMLUtil.GetAsXMLStringNoPL(aline)
            fout.write('%s%s\n'%(sindent,aline))
         else:
            if apos>=0:
               sindent='.'*apos
            if aashtml:
               if achar!=' ':
                  achar='<font color="red"><b>%s</b></font>'%achar
               if aline:
                  aline=XMLUtil.GetAsXMLStringNoPL(aline)
               if acomment:
                  acomment='<font color="red">%s</font>'%acomment
               fout.write('%s%10d:%s%s%s\n'%(achar,i,sindent,aline,acomment))
            else:
               if acomment:
                  acomment='<!-- %s -->'%acomment
               fout.write('%s%10d:%s%s%s\n'%(achar,i,sindent,aline,acomment))
         i=i+1
   def handle_starttag(self, tag, attrs):
      if not tag in self.ignoretags:
         self.inputlines[self.lineno-1][0]=len(self.tablestack)
         self.tablestack.append([tag,self.lineno])
   def handle_endtag(self, tag):
      if tag in self.ignoretags:
         return
      if self.tablestack:
         s,lineno=self.tablestack.pop()
         self.inputlines[self.lineno-1][0]=len(self.tablestack)
         if s!=tag:
            acomment='*** ERROR *** encountered "%s", should be "%s" at line %d (start line at %d)'%(tag,s,self.lineno,lineno)
            acomment2='*** ERROR *** unmatched tag - this is start of error at line %d (encountered "%s" should be "%s")'%(self.lineno,tag,s)
#            print acomment
            self.inputlines[self.lineno-1][2]=acomment
            self.inputlines[self.lineno-1][3]='-'
            self.inputlines[lineno-1][2]=acomment2
            self.inputlines[lineno-1][3]='+'
            self.errcount=self.errcount+1
      else:
         acomment='*** ERROR *** closing tag "%s" when the stack is empty at line %d'%(tag,self.lineno)
#         print acomment
         self.inputlines[self.lineno-1][2]=acomment
         self.inputlines[self.lineno-1][3]='*'
         self.errcount=self.errcount+1



