# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:17:34

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.wwwserver.domenuclassrecur as DoMenuClassRecur

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnGetCaption(aobj,l):
   l=[aobj.aClassName,'[%d]'%aobj.OID]
   return l

def OnGetCaptionListObjects(aobj,l):
   l.insert(0,'%09d'%aobj.OID)
   return l

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   if atype!='objects':
      return
   acidfield=aobj.Class.FieldsByName('aCID')
   bcid=acidfield.ValuesAsInt(aobj.OID)
   bclass=aICORDBEngine.Classes[bcid]
   bobj=bclass.GetFirstObject()
   if bobj:
      DoMenuClassRecur.DoGetObjects(bobj,xmlfile,UID,aprocessevents=0,asortdisable=1,brcid=-1,broid=-1,onGetCaption=OnGetCaptionListObjects,anogrouping=1)

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   acidfield=aobj.Class.FieldsByName('aCID')
   bcid=acidfield.ValuesAsInt(aobj.OID)
   bclass=aICORDBEngine.Classes[bcid]
   bobj=bclass.GetFirstObject()
   if bobj:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Obiekty w klasie: %d'%bclass.ObjectsCount())}
      d['icon']='/icormanager/images/icons/silk/icons/folder_database.png'
      d['openIcon']=d['icon']
      d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=objects&param=%s'%(aobj.CID,aobj.OID,'')
      d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=objects&param=%s&XMLData=1'%(aobj.CID,aobj.OID,'')
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

