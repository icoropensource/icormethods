# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   if atype=='default':
      qoid=aobj.Class.Nazwa.Identifiers('ICOR_Default')
      if qoid<0:
         return
      qobj=aobj.Class.ADQueries.ClassOfType[qoid]
      while qobj:
         d={'text':XMLUtil.GetAsXMLStringNoPL(qobj.Nazwa)}
         d['action']='icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%s'%(qobj.CID,qobj.OID,aobj.CID,aobj.OID)
         d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&brCID=%d&brOID=%d&type=query&param=%s&context=%s&XMLData=1'%(qobj.CID,qobj.OID,aobj.CID,aobj.OID,'','')
         d['icon']='/icormanager/images/icons/silk/icons/server_chart.png'
         d['openIcon']=d['icon']
         xmlfile.TagOpen('tree',d,aclosetag=1)
         qobj.Next()
   elif atype=='profil':
      qobj=aobj.ADQueries
      while qobj:
         d={'text':XMLUtil.GetAsXMLStringNoPL(qobj.Nazwa)}
         d['action']='icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%s'%(qobj.CID,qobj.OID,aobj.CID,aobj.OID)
         d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&brCID=%d&brOID=%d&type=query&param=%s&context=%s&XMLData=1'%(qobj.CID,qobj.OID,aobj.CID,aobj.OID,'','')
         d['icon']='/icormanager/images/icons/silk/icons/server_chart.png'
         d['openIcon']=d['icon']
         xmlfile.TagOpen('tree',d,aclosetag=1)
         qobj.Next()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   if aobj.ADQueries:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Zapytania z profilu')}
      d['icon']='/icormanager/images/icons/silk/icons/server_connect.png'
      d['openIcon']=d['icon']
      #d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=profil&param=%s'%(aobj.CID,aobj.OID,'')
      d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=profil&param=%s&XMLData=1'%(aobj.CID,aobj.OID,'')
      xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Zapytania domyślne')}
   d['icon']='/icormanager/images/icons/silk/icons/server_connect.png'
   d['openIcon']=d['icon']
   #d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=default&param=%s'%(aobj.CID,aobj.OID,'')
   d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=default&param=%s&XMLData=1'%(aobj.CID,aobj.OID,'')
   xmlfile.TagOpen('tree',d,aclosetag=1)

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
