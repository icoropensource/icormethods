# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   aobj=aclass[aoid].BazyZrodlowe
   while aobj:
      awwweditor.RegisterField('BZR_'+str(aobj.OID),adisplayed=aobj.Nazwa+' [%sBZR_%d]'%(aclass.BaseNameModifier[aoid],aobj.OID),atype=mt_Bool)
      aobj.Next()
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
      file.write('<hr><pre>')
      bobj=aobj.BazyZrodlowe
      while bobj:
         file.write('call python2 %s_UTIL_%sBZR_%d.py CREATE\n'%(aobj.Nazwa,aobj.BaseNameModifier,bobj.OID))
         bobj.Next()
      file.write('</pre>')
      file.write('<hr><pre>')
      bobj=aobj.BazyZrodlowe
      while bobj:
         file.write('call python2 %s_UTIL_%sBZR_%d.py CREATESP\n'%(aobj.Nazwa,aobj.BaseNameModifier,bobj.OID))
         bobj.Next()
      file.write('</pre>')
   return 0 # show back reference to main object

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      bobj=aobj.BazyZrodlowe
      while bobj:
         w=ICORUtil.str2bool(awwweditor['BZR_'+str(bobj.OID)])
         if w:
            file.write('<h2>Generowanie tabeli %s jako %sBZR_%d</h2>'%(bobj.Nazwa,aobj.BaseNameModifier,bobj.OID))
            bobj.Class.MainImportCreate('CREATE',bobj.OID,aobj.Nazwa)
         bobj.Next()
      awwweditor.WriteObjectView(aobj,asbutton=1)



