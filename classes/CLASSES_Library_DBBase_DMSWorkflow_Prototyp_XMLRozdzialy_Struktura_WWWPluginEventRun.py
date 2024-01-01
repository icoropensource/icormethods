# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:17:16

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icorlib.projekt.mcrmbasesimple as MCRMBaseSimple

def Main(apluginoid,akey,aioid):
   uclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Component_Plugin']
   acms=MCRMBaseSimple.CMS(alogname='pluginrun',aconsole=1,acominitialize=1)
   aobj=uclass[apluginoid]
   if aobj:
      aplugin=None
      eobj=aobj.PluginEvents
      while eobj:
         aeventkey=eobj.EventKey
         if aeventkey==akey:
            if aplugin is None:
               aproject=acms.GetProject(aobj.Struktura.Projekt)
               awwwmenustruct=aproject.GetWWWMenuStruct(aobj.Struktura)
               aplugin=awwwmenustruct.GetPlugin(aobj)
            aevent=aplugin.GetEvent(eobj,eobj.EventKind.EventName,eobj.EventSource)
         eobj.Next()
      tobj=aobj.Template
      while tobj:
         atemplate=None
         eobj=tobj.TemplateEvents
         while eobj:
            aeventkey=eobj.EventKey
            if aeventkey==akey:
               if aplugin is None:
                  aproject=acms.GetProject(aobj.Struktura.Projekt)
                  awwwmenustruct=aproject.GetWWWMenuStruct(aobj.Struktura)
                  aplugin=awwwmenustruct.GetPlugin(aobj)
               if atemplate is None:
                  atemplate=aplugin.GetTemplate(tobj)
               aevent=atemplate.GetEvent(eobj,eobj.EventKind.EventName,eobj.EventSource)
            eobj.Next()
         tobj.Next()
   acms.UserParameters['ioid']=aioid
   acms.UserParameters['returnValue']='x'
   acms.ProcessEvents()
   return acms.UserParameters['returnValue']

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   akey=FieldName
   apluginoid=OID
   aioid=Value
   ret=Main(apluginoid,akey,aioid)
   return ret

