# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import urllib

import appplatform.ldaputil as ldaputil

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   if atype=='query':
      if not brobj:
         return
      aldap=ldaputil.LDAPHelper('ldap://%s'%brobj.LDAPHost,brobj.LDAPDomain)
      try:
         aldap.Open(brobj.LDAPUserName,brobj.LDAPPassword)
         ret=aldap.GetCustomQueryTree(aobj.Query)
      finally:
         aldap.Close()
      icnt=1
      for aitem in ret:
         v=aitem.get('_dn','pozycja: %d'%icnt)
         v=XMLUtil.UTF8_To_CP1250(v)
         vq=urllib.quote(v,'')
         d={'text':XMLUtil.GetAsXMLStringNoPL(v)}
         d['action']='icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%s'%(brobj.CID,brobj.OID,aobj.CID,aobj.OID)
         d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&brCID=%d&brOID=%d&type=subquery&param=%s&context=%s&XMLData=1'%(aobj.CID,aobj.OID,brobj.CID,brobj.OID,'',vq)
         d['icon']='/icormanager/images/icons/silk/icons/server_chart.png'
         d['openIcon']=d['icon']
         xmlfile.TagOpen('tree',d,aclosetag=1)
         icnt=icnt+1
   elif atype=='subquery':
      if not brobj:
         return
      print 'CONTEXT:',acontext
      if not acontext:
         return
      aldap=ldaputil.LDAPHelper('ldap://%s'%brobj.LDAPHost,brobj.LDAPDomain)
      try:
         aldap.Open(brobj.LDAPUserName,brobj.LDAPPassword)
         ret=aldap.GetCustomQuery('(distinguishedName='+acontext+')')
      finally:
         aldap.Close()
      icnt=0
      for aitem in ret:
         icnt=icnt+1
         vcnt=0
         for akey in aitem.keys():
            if akey=='_dn':
               continue
            if aitem.get('typeCategory','') not in ['reference']:
               continue
            vcnt=vcnt+1
            aname=aitem.get('name','pozycja: %d'%icnt)
            aname=XMLUtil.UTF8_To_CP1250(aname)
            lvalue=aitem.get('value','element: %d'%vcnt)
            if type(lvalue)!=type([]):
               lvalue=[lvalue,]
            for avalue in lvalue:
               avalue=XMLUtil.UTF8_To_CP1250(avalue)
               qvalue=urllib.quote(avalue,'')
               d={'text':XMLUtil.GetAsXMLStringNoPL(aname+' - '+avalue)}
               d['action']='icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%s'%(brobj.CID,brobj.OID,aobj.CID,aobj.OID)
               d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&brCID=%d&brOID=%d&type=subquery&param=%s&context=%s&XMLData=1'%(aobj.CID,aobj.OID,brobj.CID,brobj.OID,'',qvalue)
               d['icon']='/icormanager/images/icons/silk/icons/server_chart.png'
               d['openIcon']=d['icon']
               xmlfile.TagOpen('tree',d,aclosetag=1)

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   return

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
