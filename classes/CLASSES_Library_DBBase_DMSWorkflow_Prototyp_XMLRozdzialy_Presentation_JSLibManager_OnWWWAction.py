# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

try:
   import simplejson as json
except:
   import json

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   return

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   #print '$$ obj - c:',aobj.Class.CID,aobj.Class.NameOfClass,'o:',aobj.OID,'u:',UID
   s=aobj.Skrypt
   if not s:
      return
   dd=json.loads(s,encoding='cp1250')
   if not type(dd)==type({}):
      return
   if not dd.has_key('dependencies'):
      return

   l=[]
   for sk,sv in dd['dependencies'].items():
      if sv.find('http')<0:
         ss=' - '+sv
         sv='https://libraries.io/npm/'+sk
      else:
         ss=''
      l.append([sk+ss,'!'+sv])

   if l:
      l.sort()
      d={'text':XMLUtil.GetAsXMLStringNoPL('Zasoby')}
      d['icon']='/icormanager/images/icons/silk/icons/package_se.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      for atext,aurl in l:
         d={'text':atext,'action':aurl}
         d['icon']='/icormanager/images/icons/silk/icons/package_link.png'
         d['openIcon']=d['icon']
         d['action']=aurl #'icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(tobj.CID,tobj.OID,aobjname)
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
   return

def OnWWWGetFieldAutoCompleteValues(aobj,afield):
   if afield.Name in ['XXX']:
      return aobj._backreffield._referencedfield
   return

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()
