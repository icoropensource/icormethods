# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

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

def SetIsDeleted(aobj,avalue=1):
   aobj['SGIsDeleted']=avalue
   bobj=aobj.PodRozdzialy
   while bobj:
      SetIsDeleted(bobj,avalue)
      bobj.Next()

def RestoreChapter(aobj):
   astatus='Rozdział przywrócony'
   robj=aobj.Rozdzial
   if not robj['SGIsDeleted',mt_Integer]:
      aobj.Rozdzial=''
      aobj.Class.DeleteObject(aobj.OID)
      return 'Ten rozdział jest już przywrócony'
   nobj=robj.NadRozdzial
   if nobj:
      if nobj['SGIsDeleted',mt_Integer]:
         return 'Ten rozdział może być przywrócny tylko wtedy, gdy zostanie najpierw przywrócny jego rozdział nadrzędny.'
   pobj=aobj.Struktura
   SetIsDeleted(robj,avalue=0)
   if nobj:
      robj.Class.PodRozdzialy.AddRefs(nobj.OID,[robj.OID,robj.CID],asortedreffield=robj.Class.SGTabID,dosort=1,ainsertifnotexists=1)
   else:
      pobj.Class.Rozdzialy.AddRefs(pobj.OID,[robj.OID,robj.CID],asortedreffield=robj.Class.SGTabID,dosort=1,ainsertifnotexists=1)
   aobj.Rozdzial=''
   aobj.Class.DeleteObject(aobj.OID)
   return astatus

def OnWWWAction(aobj,amenu,file):
#   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      astatus=RestoreChapter(aobj)
      file.write('<h1>'+astatus+'</h1>')
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

