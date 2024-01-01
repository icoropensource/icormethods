# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:15:48

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.msqlsecurity as MSQLSecurity
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('ACL',adisplayed='ACL',atype=mt_String,avalue='0x')
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
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Wybrałeś: %s</h1>'%awwweditor['ACL'])
      bvec=ICORUtil.BitVector(awwweditor['ACL'])
      l=MSQLSecurity.ParseProjectSecurityMap(aobj.Dane)
      d={}
      for apos,asname in l:
         d[apos]=asname
      for apos in bvec.keys():
         if d.has_key(apos):
            file.write('<h3>%s</h3>'%d[apos])
      awwweditor.WriteObjectView(aobj,asbutton=1)



