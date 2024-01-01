# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil

import urllib

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

def DumpReturnStruct(file,robj,aindent=0):
   while robj:
      file.write('<table border=1>\n')
      file.write('<tr><td>Nazwa:</td><td colspan=2>%s</td></tr>\n'%(robj.Nazwa,))
      file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(robj.Dokumentacja),))
      file.write('<tr><td colspan=3>Parametry:</td></tr>\n')
      file.write('<tr><td colspan=3>\n')
      pobj=robj.Parameters
      while pobj:
         file.write('<table border=1>\n')
         file.write('<tr><td>Nazwa:</td><td colspan=2>%s</td></tr>\n'%(pobj.Nazwa,))
         file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(pobj.Dokumentacja),))
         file.write('<tr><td>Typ (opis):</td><td colspan=2>%s</td></tr>\n'%(pobj.Opis,))
         file.write('<tr><td>Typ:</td><td colspan=2>%s</td></tr>\n'%(pobj.ParameterType.Nazwa,))
         if pobj.ListElementType:
            file.write('<tr><td colspan=3>\n')
            DumpReturnStruct(file,pobj.ListElementType,aindent+1)
            file.write('</td></tr>\n')
         file.write('</table><br>\n')
         pobj.Next()
      file.write('</td></tr>\n')
      file.write('</table><br>\n')
      robj.Next()

def OnWWWAction(aobj,amenu,file):
   #awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   #if amenu.Action=='ObjectApplyMethods':
      #awwweditor.Write()

   file.write('''<style type="text/css">
BODY { color: #000000; background-color: white; font-family: Verdana; margin-left: 0px; margin-top: 0px; }
.content { margin-left: 30px; font-size: .70em; padding-bottom: 2em; }
A:link { color: #336699; font-weight: bold; text-decoration: underline; }
A:visited { color: #6699cc; font-weight: bold; text-decoration: underline; }
A:active { color: #336699; font-weight: bold; text-decoration: underline; }
A:hover { color: cc3300; font-weight: bold; text-decoration: underline; }
P { color: #000000; margin-top: 0px; margin-bottom: 12px; font-family: Verdana; }
pre { background-color: #e5e5cc; padding: 5px; font-family: Courier New; font-size: x-small; margin-top: -5px; border: 1px #f0f0e0 solid; }
td { color: #000000; font-family: Verdana; font-size: .7em; }
h2 { font-size: 1.5em; font-weight: bold; margin-top: 25px; margin-bottom: 10px; border-top: 1px solid #003366; margin-left: 15px; color: #003366; }
h3 { font-size: 1.1em; color: #000000; margin-left: 15px; margin-top: 10px; margin-bottom: 10px; }
ul { margin-top: 10px; margin-left: 20px; }
ol { margin-top: 10px; margin-left: 20px; }
li { margin-top: 10px; color: #000000; }
font.value { color: darkblue; font: bold; }
font.key { color: darkgreen; font: bold; }
font.error { color: darkred; font: bold; }
.heading1 { color: #ffffff; font-family: Tahoma; font-size: 26px; font-weight: normal; background-color: #003366; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 10px; padding-bottom: 3px; padding-left: 15px; width: 105%; }
.button { background-color: #dcdcdc; font-family: Verdana; font-size: 1em; border-top: #cccccc 1px solid; border-bottom: #666666 1px solid; border-left: #cccccc 1px solid; border-right: #666666 1px solid; }
.frmheader { color: #000000; background: #dcdcdc; font-family: Verdana; font-size: .7em; font-weight: normal; border-bottom: 1px solid #dcdcdc; padding-top: 2px; padding-bottom: 2px; }
.frmtext { font-family: Verdana; font-size: .7em; margin-top: 8px; margin-bottom: 0px; margin-left: 32px; }
.frmInput { font-family: Verdana; font-size: 1em; }
.intro { margin-left: -15px; }
</style>
''')
   file.write('<h1>%s</h1>\n'%(aobj.Nazwa,))
   #file.write('<table border=1>')
   #file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(aobj.Dokumentacja),))
   #file.write('<tr><td>Bazowy URL:</td><td colspan=2>%s</td></tr>\n'%(aobj.URLBase,))
   #file.write('</table>')
   nobj=aobj.Namespaces
   while nobj:
      file.write('<h2>Grupa/klasa: %s</h2>\n'%(nobj.Nazwa,))
      file.write('<div class="content">')
      aurl='%s?WSDL'%(aobj.URLBase+nobj.URLPath,)
      atext=urllib.urlopen(aurl).read()
      file.write('<pre>')
      file.write(XMLUtil.GetAsXMLStringNoPL(XMLUtil.UTF8_To_CP1250(atext)))
      file.write('</pre>')
      file.write('</div>')
      nobj.Next()
   return 0 # show back reference to main object (1-link, 2-button)

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
