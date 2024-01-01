# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   return

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   tclass=aICORDBEngine.Classes['CLASSES_System_User']
   l=tclass.GetObjectsInRange(aobj['IDMin',mt_Integer],aobj['IDMax',mt_Integer])
   if l:
      lusers=[]
      for atid in l:
         lusers.append([tclass.UserName[atid],atid])
      lusers.sort()
      d={'text':XMLUtil.GetAsXMLStringNoPL('Użytkownicy w zakresie (%d)'%(len(lusers),))}
      d['icon']='/icormanager/images/icons/silk/icons/group_go.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      for ausername,atid in lusers:
         #if not tclass.ObjectExists(atid):
         #   continue
         tobj=tclass[atid]
         d={'text':XMLUtil.GetAsXMLStringNoPL(ausername),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(tobj.CID,tobj.OID)}
         d['icon']='/icormanager/images/icons/silk/icons/user_go.png'
         d['openIcon']=d['icon']
#         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(tobj.CID,tobj.OID,aobjname)
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(tobj.CID,tobj.OID)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(tobj.CID,tobj.OID)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')
   return

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
   return

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

