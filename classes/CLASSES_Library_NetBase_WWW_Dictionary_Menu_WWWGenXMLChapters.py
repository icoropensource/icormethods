# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:19:19

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from icorlib.projekt.mcrmwwwmenu import *
import cStringIO

class ICORMenuStructGenerator(object):
   def StoreXMLSourceChapter(self,robj,axml):
      d={}
      #d['oid']=robj.OID
      d['title']=robj.Name
      d['titlemenu']=robj.Caption
      if robj.Action.Name=='HTML Redirect':
         d['href']=robj.ParamValue1
      #d['hrefapp']=robj.SGHrefApp
      #d['hrefparams']=robj.SGHrefParams
      #d['target']=robj.SGTarget
      #d['comment']=robj.Komentarz
      sobj=robj.SubMenu
      w=1                    
      if sobj:
         w=0
      axml.TagOpen('rozdzial',d,aclosetag=w,asortattrnames=['oid','title','titlemenu','href'])
      while sobj:
         self.StoreXMLSourceChapter(sobj,axml)
         sobj.Next()
      if not w:
         axml.TagClose()
   def StoreXMLSource(self,aobj):
      fout=cStringIO.StringIO()
      axml=XMLUtil.MXMLFile(fout,anopl=1)
      axml.Header()
      axml.TagOpen('struktura')
      self.StoreXMLSourceChapter(aobj,axml)
      axml.TagClose('struktura')
      axml.close()
      ret=fout.getvalue()
      fout.close()
      return ret


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

def OnWWWAction(aobj,amenu,file):
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      aparser=ICORMenuStructGenerator()
      ret=aparser.StoreXMLSource(aobj)
      file.write('<textarea style="width:100%;height:60vh;">')
      file.write(ret)
      file.write('</textarea>')
#      awwweditor.Write()
   return 2 # show back reference to main object (1-link, 2-button)

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



