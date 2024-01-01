# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *

def ExportStructChapters(robj,file,agrupa,alevel=1):
   while robj:
      if not agrupa and robj.GrupaRozdzialow:
         robj.Next()
         continue
      file.write('%s<node TEXT="%s">\n'%('  '*alevel,ICORUtil.GetStringAsSafeScriptString(robj.Naglowek),))
      sobj=robj.PodRozdzialy
      if sobj:
         ExportStructChapters(sobj,file,agrupa,alevel+1)
      file.write('%s</node>\n'%('  '*alevel,))
      robj.Next()

def ExportStructChaptersFreeMind(aobj,file):
   file.write('<textarea style="width:80%;height:440px;">\n')
   file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><map version="0.8.1">\n')
   file.write('<node TEXT="%s">\n'%(ICORUtil.GetStringAsSafeScriptString(aobj.Nazwa),))

   file.write('  <node TEXT="Rozdzia�y">\n')
   ExportStructChapters(aobj.Rozdzialy,file,0)
   file.write('  </node>\n')

   gobj=aobj.GrupyRozdzialow
   while gobj:
      file.write('<node TEXT="%s">\n'%(ICORUtil.GetStringAsSafeScriptString(gobj.Nazwa),))
      ExportStructChapters(gobj.Rozdzialy,file,1)
      file.write('</node>\n')
      gobj.Next()

   file.write('</node</map>\n')
   file.write('\n</textarea>\n\n')

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

def OnWWWAction(aobj,amenu,file):
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      ExportStructChaptersFreeMind(aobj,file)
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
