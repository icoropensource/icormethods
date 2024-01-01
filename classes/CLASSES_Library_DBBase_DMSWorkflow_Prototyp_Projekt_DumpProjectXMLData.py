# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:13:19

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import icorlib.projekt.mcrmbase as mcrmbase
import CLASSES_Library_ICORBase_Interface_ICORUtil
import CLASSES_Library_ICORBase_External_MLog as MLog

def GetCRMByItem(pobj):
   acrm=mcrmbase.MCRM(pobj.Nazwa,acreatetables=0,abasenamemodifier=pobj.BaseNameModifier)
   adir=FilePathAsSystemPath(aICORWWWServerInterface.AppPath)+pobj.AppPath
   acrm.PreProcess(pobj,adir)
   return acrm

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aoid=aclass.Nazwa.Identifiers('???')
   if aoid<0:
      print 'brak projektu'
      return
   pobj=aclass[aoid]
   acrm=GetCRMByItem(pobj)
   tobj=pobj.BazyZrodlowe
   while tobj:
      print tobj.OID,tobj.Nazwa
      asrctable=acrm.sourcetables[tobj.OID]
      aresponse=ICORUtil.Response()
      asrctable.DumpAsXML(aresponse,{'_MAX_TABLE_RECUR':3})
      axml=aresponse.AsText(aashtmlstring=0)
      fout=open('e:/icor/sql/tables/%d.xml'%(tobj.OID,),'w')
      fout.write(axml)
      fout.close()
      tobj.Next()
   return

