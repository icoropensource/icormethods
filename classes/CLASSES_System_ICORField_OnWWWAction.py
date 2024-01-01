# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   return

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   toid=aobj['aFieldTypeID',mt_Integer]
   if toid>MAX_ICOR_SYSTEM_TYPE:
      tclass=aICORDBEngine.Classes[toid]
      d={'text':XMLUtil.GetAsXMLStringNoPL('Typ pola')}
      SetXMLClassImages(tclass,d)
      xmlfile.TagOpen('tree',d)
      if 1:
         tcid=aICORDBEngine.Classes.MetaClass.CID
         d={'text':XMLUtil.GetAsXMLStringNoPL('%s [%d]'%(tclass.NameOfClass,toid)),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(tcid,toid)}
   #         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(tobj.CID,tobj.OID,aobjname)
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(tcid,toid)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(tcid,toid)
         SetXMLObjectImages(tclass,d)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
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
