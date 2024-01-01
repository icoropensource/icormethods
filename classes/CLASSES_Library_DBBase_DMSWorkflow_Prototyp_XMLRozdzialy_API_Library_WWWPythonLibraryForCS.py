# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

LIB_START='''# -*- coding: utf-8 -*-
import urllib
import xml2dict

class %sServiceBase(object):
   def __init__(self,aapi):
      self.api=aapi
'''

LIB_CLASS_0='''
class %s%s(%sServiceBase):
'''

LIB_METHOD_0='''   def %s(self,%s):
      d={%s}
      return self.api.Call%s('%s/%s',d)
'''

LIB_ATTR_0='''      self.%s=%s%s(self)
'''

LIB_FINISH_0='''
class %sAPI(object):
   def __init__(self,abaseurl,ajson=0,averbose=0):
      self.base_url=abaseurl
      self.use_json=ajson #format danych to JSON lub XML
      self.verbose=averbose
%s   def Call%s(self,aurl,adata):
      aurl=self.base_url+aurl
      if self.use_json:
         urllib._urlopener=urllib.FancyURLopener()
         urllib._urlopener.addheader('Content-Type','application/json; charset=utf-8')
         atext=urllib.urlopen(aurl,str(adata)).read()
         adict=eval(atext)
      else:
         urllib._urlopener=None
         atext=urllib.urlopen(aurl,urllib.urlencode(adata)).read()
         try:
            adict=xml2dict.XML2Dict().fromstring(atext)
         except:
            if self.verbose:
               print atext
            raise
      if self.verbose:
         print aurl,'->',atext
      return adict
'''

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Nazwa',aoid=aoid)
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def OnWWWActionGetLink(aobj,amenu):
   return ''

def GetDoc(s):
   if not s:
      s='&nbsp;-&nbsp;'
   s=s.replace('\n','<br>\n')
   return s

def OnWWWAction(aobj,amenu,file):
   #awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   #if amenu.Action=='ObjectApplyMethods':
      #awwweditor.Write()

   file.write('<pre>\n')
   file.write(LIB_START%(aobj.LibraryPrefix))

   lnamespaces=[]
   nobj=aobj.Namespaces
   while nobj:
      lnamespaces.append(nobj.Nazwa)
      file.write(LIB_CLASS_0%(aobj.LibraryPrefix,nobj.Nazwa,aobj.LibraryPrefix))
      #file.write('<tr><td>URL:</td><td colspan=2><a href="%s">%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,aobj.URLBase+nobj.URLPath,))
      #file.write('<tr><td>WSDL:</td><td colspan=2><a href="%s?WSDL">%s?WSDL</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,aobj.URLBase+nobj.URLPath,))
      mobj=nobj.Metody
      while mobj:
         lparams=[]
         pobj=mobj.Parameters
         while pobj:
            lparams.append(pobj.Nazwa)
            pobj.Next()
         sparams=','.join(lparams)
         sdparams=','.join(["'%s':%s"%(x,x) for x in lparams])
         file.write(LIB_METHOD_0%(mobj.Nazwa,sparams,sdparams,aobj.LibraryPrefix,nobj.URLPath,mobj.URLMethod))
         #file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(mobj.Dokumentacja),))
         #file.write('<tr><td>Dokumentacja wyniku:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(mobj.DokumentacjaRet),))
         #file.write('<tr><td>URL - opis, parametry, wyniki:</td><td colspan=2><a href="%s?op=%s">%s?op=%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,mobj.URLMethod,aobj.URLBase+nobj.URLPath,mobj.URLMethod))
         #file.write('<tr><td>URL do wywołania:</td><td colspan=2><a href="%s/%s">%s/%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,mobj.URLMethod,aobj.URLBase+nobj.URLPath,mobj.URLMethod))
         mobj.Next()
      nobj.Next()
   sattrs=''.join([LIB_ATTR_0%(x,aobj.LibraryPrefix,x) for x in lnamespaces])
   file.write(LIB_FINISH_0%(aobj.LibraryPrefix,sattrs,aobj.LibraryPrefix,))
   file.write('</pre>\n')
   return 0

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 0</h1>')
      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])
