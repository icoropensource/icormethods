# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

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

   file.write('<h1>%s</h1>\n'%(aobj.Nazwa,))
   file.write('<table border=1>')
   file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(aobj.Dokumentacja),))
   file.write('<tr><td>Bazowy URL:</td><td colspan=2>%s</td></tr>\n'%(aobj.URLBase,))
   file.write('</table>')
   nobj=aobj.Namespaces
   while nobj:
      file.write('<h2>Grupa/klasa: %s</h2>\n'%(nobj.Nazwa,))
      file.write('<table border=1>')
      file.write('<tr><td>URL:</td><td colspan=2><a href="%s">%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,aobj.URLBase+nobj.URLPath,))
      file.write('<tr><td>WSDL:</td><td colspan=2><a href="%s?WSDL">%s?WSDL</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,aobj.URLBase+nobj.URLPath,))
      file.write('</table>')
      mobj=nobj.Metody
      while mobj:
         file.write('<h3>Metoda: %s</h3>\n'%(mobj.Nazwa,))
         file.write('<table border=1>\n')
         file.write('<tr><td>Nazwa:</td><td colspan=2>%s</td></tr>\n'%(mobj.Nazwa,))
         file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(mobj.Dokumentacja),))
         file.write('<tr><td>Dokumentacja wyniku:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(mobj.DokumentacjaRet),))
         file.write('<tr><td>URL - opis, parametry, wyniki:</td><td colspan=2><a href="%s?op=%s">%s?op=%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,mobj.URLMethod,aobj.URLBase+nobj.URLPath,mobj.URLMethod))
         file.write('<tr><td>URL do wywołania:</td><td colspan=2><a href="%s/%s">%s/%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,mobj.URLMethod,aobj.URLBase+nobj.URLPath,mobj.URLMethod))
         file.write('</table>\n')
         file.write('<h4>Parametry metody: %s</h4>\n'%(mobj.Nazwa,))
         pobj=mobj.Parameters
         while pobj:
            file.write('<table border=1>\n')
            file.write('<tr><td>Nazwa:</td><td colspan=2>%s</td></tr>\n'%(pobj.Nazwa,))
            file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(pobj.Dokumentacja),))
            file.write('<tr><td>Typ (opis):</td><td colspan=2>%s</td></tr>\n'%(pobj.ParameterType.Opis,))
            file.write('<tr><td>Typ:</td><td colspan=2>%s</td></tr>\n'%(pobj.ParameterType.Nazwa,))
            file.write('</table><br>\n')
            pobj.Next()
         file.write('<h4>Wynik działania metody: %s</h4>\n'%(mobj.Nazwa,))
         robj=mobj.ReturnStruct
         DumpReturnStruct(file,robj)
         file.write('<br>\n')
         mobj.Next()
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
