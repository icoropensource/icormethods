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
   idmin=aobj['IDMin',mt_Integer]
   idmax=aobj['IDMax',mt_Integer]
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy','Nazwa','Tabele')
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial','Naglowek','Rozdziały')
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_XMLData_TableXMLData','Name','XML')
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_TableLink','LinkName','Połączenia między tabelami')
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Chapter_EventValue','EventKind.EventName','Zdarzenia w rozdziałach')
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Plugin_EventValue','EventKind.EventName','Zdarzenia we wtyczkach','EventKey')
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_Table_EventValue','EventKind.EventName','Zdarzenia w tabelach')
   GetMenuByObjectsInRange(xmlfile,idmin,idmax,'CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_SourceEvents_XMLData_EventValue','EventKind.EventName','Zdarzenia w XMLData')

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
   return

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

