# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_NetBase_Utils_HTMLChecker import HTMLChecker
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import cStringIO
import re

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('IgnoreTags',adisplayed='Ignoruj tagi',atype=mt_String,avalue='link,meta,img,br,hr,input,li,base,area')
   awwweditor.RegisterField('IndentOnly',adisplayed='Tylko indentacja',atype=mt_Bool)
   awwweditor.RegisterField('HTML',adisplayed='HTML',atype=mt_Memo,avalue='',acols=78,arows=25)
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
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      aparser=HTMLChecker(awwweditor['IgnoreTags'],aindentonly=ICORUtil.str2bool(awwweditor['IndentOnly']))
      try:
         fout=cStringIO.StringIO()
         patt1=re.compile('\<script.*?\<\/script\>',re.I|re.S)
         patt2=re.compile('\<\!\-\-.*?\-\-\>',re.I|re.S)
         atext=patt1.sub('',awwweditor['HTML'])
         atext=patt2.sub('',atext)
         aparser.Parse(atext,fout,aashtml=1)
         file.write('<pre>')
         file.write(fout.getvalue())
         file.write('</pre>')
         fout.close()
      except Exception,msg:
         file.write('<h1><font color="red">Wystąpił błąd podczas sprawdzania kodu HTML:</font></h1><h1>%s</h1>'%msg)
      awwweditor.WriteObjectView(aobj,asbutton=1)



