# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import re

class Response:
   def __init__(self):
      self.HTMLDocument=''
   def write(self,adata):
      self.HTMLDocument=self.HTMLDocument+adata

def GetTextAsHTMLText(s,repldict={}):
   for akey in repldict.keys():
      c=re.compile('\<\%\= *'+akey+' *\%\>', re.I)
      s=c.sub(repldict[akey],s)
   c=re.compile('\<\%', re.I)
   s=c.sub('""")',s) #"""
   c=re.compile('\%\>', re.I)
   s=c.sub('Response.write("""',s) #"""
   s=CLASSES_Library_ICORBase_Interface_ICORUtil.str2HTMLstr(s)
   s='Response.write("""'+s+'""")'
   aresponse=Response()
   gdict={'Response':aresponse,'aICORDBEngine':aICORDBEngine,'ICORInterface':CLASSES_Library_ICORBase_Interface_ICORInterface}
   exec s in gdict
   return aresponse.HTMLDocument

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   aclass=aICORDBEngine.Classes[CID]
   s=aclass.HTMLMethod2.MethodText
   adict={'DHandle':'000000','DName':'DialogName','FieldName':'FieldName','CID':'CID','OID':'OID','Value':'Value'}
   s=GetTextAsHTMLText(s,adict)
   print s
   return



