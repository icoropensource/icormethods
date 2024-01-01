# -*- coding: windows-1250 -*-
# saved: 2023/03/04 17:15:16

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icorlib.projekt.mcrmwwwmenu as MCRMWWWMenu

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnGetCaption(aobj,l):
   return l

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   return

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_PageTemplate']
   wobj=aobj.Struktura
   aTemplateXML = MCRMWWWMenu.ICORBIPTemplateParser()
   aTemplateXML.Parse(None, aobj.PageXML)
   joids = aTemplateXML.Variables.get('jinja_Libs', None)
   la=[]
   if joids is not None:
      lt = ICORUtil.SafeSplitInt(joids)
      for toid in lt:
         tobj=tclass[toid]
         la.append([tobj.Template+' [%d]'%toid,toid])
   if la:
      d={'text':XMLUtil.GetAsXMLStringNoPL('JinjaLibs')}
      d['icon']='/icormanager/images/icons/silk/icons/layout.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      for atext,atid in la:
         if not tclass.ObjectExists(atid):
            continue
         tobj=tclass[atid]
         d={'text':XMLUtil.GetAsXMLStringNoPL(atext),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(tobj.CID,tobj.OID)}
         d['icon']='/icormanager/images/icons/silk/icons/theme.png'
         d['openIcon']=d['icon']
#         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(tobj.CID,tobj.OID,aobjname)
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(tobj.CID,tobj.OID)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(tobj.CID,tobj.OID)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')

   joids = aTemplateXML.Variables.get('template_keys', None)
   lp=[]
   if joids is not None:
      lk = ICORUtil.SafeSplit(joids)
      if lk:
         pobj = wobj.Plugins
         while pobj:
            eobj=pobj.PluginEvents
            while eobj:
               if eobj.EventKey in lk:
                  lp.append(eobj.AsObject())
               eobj.Next()
            tobj=pobj.Template
            while tobj:
               eobj=tobj.TemplateEvents
               while eobj:
                  if eobj.EventKey in lk:
                     lp.append(eobj.AsObject())
                  eobj.Next()
               tobj.Next()
            pobj.Next()
   if lp:
      d={'text':XMLUtil.GetAsXMLStringNoPL('TemplateKeys')}
      d['icon']='/icormanager/images/icons/silk/icons/plugin.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      for tobj in lp:
         d={'text':XMLUtil.GetAsXMLStringNoPL('%s, %s [%d]'%(tobj.EventKind.EventName,tobj.EventKey,tobj.OID)),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(tobj.CID,tobj.OID)}
         d['icon']='/icormanager/images/icons/silk/icons/page_lightning.png'
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
