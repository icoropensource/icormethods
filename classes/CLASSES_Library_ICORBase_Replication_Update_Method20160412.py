# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:17:25

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Replication_Update_UpdateManager as UpdateManager
import icorlib.projekt.mcrmwwwmenuview as MCRMWWWMenuView
import icorlib.projekt.mcrmwwwmenumodel as MCRMWWWMenuModel

def CreateViewByData(apresentation,akind,atype,aiscustom,atext):
   btext=atext.replace(chr(10),'')
   btext=atext.replace(chr(13),'')
   btext=atext.replace(chr(32),'')
   if not btext:
      return
   dkind_oid={'dane':1,'tabela':2,'lista':3}
   dtype_oid={'xsl':1,'quasar':2}
   aview=apresentation.GetView(akind,atype)
   if aview is None:
      vclass=apresentation.Obj.Class.ChapterView.ClassOfType
      void=vclass.AddObject(arangeobject=apresentation.Obj)
      if void<0:
         print 'brak zakresu OID dla ChapterID:',apresentation.OID
         return None

      vclass.IsCustom[void]=aiscustom
      vclass.Kind[void]=[dkind_oid[akind],vclass.Kind.ClassOfType.CID]
      vclass.ViewType[void]=[dtype_oid[atype],vclass.ViewType.ClassOfType.CID]
      vclass.ViewText[void]=atext
      apresentation.Obj.Class.ChapterView.AddRefs(apresentation.OID,[void,vclass.CID])
   return

def CreateModelByData(amodels,akind,atype,aiscustom,atext):
   btext=atext.replace(chr(10),'')
   btext=atext.replace(chr(13),'')
   btext=atext.replace(chr(32),'')
   if not btext:
      return
   dkind_oid={'struktura':1}
   dtype_oid={'sqlshape':1,'sqlxml':2}
   amodel=amodels.GetModel(akind,atype)
   if amodel is None:
      mclass=amodels.Obj.Class.Models.ClassOfType
      moid=mclass.AddObject(arangeobject=amodels.Obj)
      if moid<0:
         print 'brak zakresu OID dla ChapterID:',amodels.OID
         return None
      mclass.IsCustom[moid]=aiscustom
      mclass.Kind[moid]=[dkind_oid[akind],mclass.Kind.ClassOfType.CID]
      mclass.ModelType[moid]=[dtype_oid[atype],mclass.ModelType.ClassOfType.CID]
      mclass.ModelText[moid]=atext
      amodels.Obj.Class.Models.AddRefs(amodels.OID,[moid,mclass.CID])
   return

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aupdate='2016_04_12 ChapterViews'
   #if not UpdateManager.CheckUpdate(aupdate):
   #   return

   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
   aobj=aclass.GetFirstObject()
   while aobj:
      if 0:
         apresentation=MCRMWWWMenuView.WWWMenuChapterPresentation(aobj)
         # Kind: dane, tabela, lista
         # Type: xsl, quasar
         CreateViewByData(apresentation,'dane','xsl',aobj.IsCustomXSLSO,aobj.XSLDataSO)
         CreateViewByData(apresentation,'tabela','xsl',aobj.IsCustomXSL,aobj.XSLData)
         CreateViewByData(apresentation,'lista','xsl',aobj.IsCustomXSLList,aobj.XSLDataList)
         CreateViewByData(apresentation,'dane','quasar',aobj.IsCustomHandlebarsSO,aobj.HandlebarsDataSO)
         CreateViewByData(apresentation,'tabela','quasar',aobj.IsCustomHandlebars,aobj.HandlebarsData)
         CreateViewByData(apresentation,'lista','quasar',aobj.IsCustomHandlebarsList,aobj.HandlebarsDataList)
      if 1:
         amodels=MCRMWWWMenuModel.WWWMenuChapterModels(aobj)
         CreateModelByData(amodels,'struktura','sqlshape',aobj.IsCustomSQL,aobj.SQLData)
         CreateModelByData(amodels,'struktura','sqlxml',aobj.IsCustomSQLXML,aobj.SQLXMLData)
      aobj.Next()
   return
