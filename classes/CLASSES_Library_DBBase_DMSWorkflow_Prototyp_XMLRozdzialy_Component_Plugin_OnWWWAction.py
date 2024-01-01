# -*- coding: windows-1250 -*-
# saved: 2023/03/11 21:57:10

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import icordbmain.adoutil as ADOLibInit
import string
import icordbmain.dbaccess as dbaccess

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWGetFieldIteratorEvent(afield,aoid,aparamobj):
   if aoid<0 and afield.Name in ['Skin','Extensions','EffectSkins']:
      return -1
   elif aparamobj and aoid<0:
      aobj=aparamobj.AsObject()
   elif aoid<0:
      return None
   else:
      rclass=afield.ClassItem
      aobj=rclass[aoid]
   if afield.Name=='Skin':
      if aobj.CID==afield.ClassItem.CID:
         if aobj.Template:
            return aobj.Template.PluginSkin
         return -1
   if afield.Name=='Extensions':
      if aobj.CID==afield.ClassItem.CID:
         if aobj.Template:
            return aobj.Template.PluginExtension
         return -1
   if afield.Name=='EffectSkins':
      if aobj.CID==afield.ClassItem.CID:
         arefs=FieldRefIterator()
         sobj=aobj.Effects
         while sobj:
            arefs.AddRefs(sobj.Skins.AsRefs())
            sobj.Next()
         tobj=aobj.Template
         while tobj:
            sobj=tobj.Effects
            while sobj:
               arefs.AddRefs(sobj.Skins.AsRefs())
               sobj.Next()
            tobj.Next()
         if arefs:
            return arefs.AsObject()
         return -1
   return None

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
#   print 'obj - c:',aobj.Class.CID,aobj.Class.NameOfClass,'o:',aobj.OID,'u:',UID
   abasenamemodifier=aobj.Struktura.Projekt.BaseNameModifier
   tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
   aPluginVars=ICORUtil.ParseVars(aobj.PluginVars,{})
   dt={}
   l=[]
   la=[]
   lu=[]
   lf=[]
   sta=aPluginVars.get('aTableOIDs_Allowed','')
   if sta:
      lta=map(int,sta.split(','))
      for atid in lta:
         if not tclass.ObjectExists(atid):
            continue
         tobj=tclass[atid]
         la.append([tobj.Nazwa,atid])
      la.sort()
   for akey,atid in aPluginVars.items():
      if string.find(akey,'aTableOID_')==0:
         try:
            l.append(int(atid))
            sl=string.split(akey,'_')
            dt[sl[1]]=int(atid)
         except ValueError:
            pass
      if string.find(akey,'aURL:')==0:
         lu.append([akey[5:],atid])
      if string.find(akey,'aField_XMLDataID_')==0:
         sl=string.split(akey,'_')
         lf.append([dt[sl[2]],atid])
   if aobj.Template:
      aTemplateVars=ICORUtil.ParseVars(aobj.Template.TemplateVars,{})
      for akey,atid in aTemplateVars.items():
         if string.find(akey,'aTableOID_')==0:
            try:
               l.append(int(atid))
               sl=string.split(akey,'_')
               dt[sl[1]]=int(atid)
            except ValueError:
               pass
         if string.find(akey,'aURL:')==0:
            lu.append([akey[5:],atid])
         if string.find(akey,'aField_XMLDataID_')==0:
            sl=string.split(akey,'_')
            if dt.has_key(sl[2]):
               lf.append([dt[sl[2]],atid])
   if l:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Tabele')}
      d['icon']='/icormanager/images/icons/silk/icons/table_multiple.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      for atid in l:
         if not tclass.ObjectExists(atid):
            continue
         tobj=tclass[atid]
         d={'text':XMLUtil.GetAsXMLStringNoPL(tobj.Nazwa),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(tobj.CID,tobj.OID)}
         d['icon']='/icormanager/images/icons/silk/icons/table_go.png'
         d['openIcon']=d['icon']
#         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(tobj.CID,tobj.OID,aobjname)
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(tobj.CID,tobj.OID)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(tobj.CID,tobj.OID)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')
   if la:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Tabele dozwolone')}
      d['icon']='/icormanager/images/icons/silk/icons/table_multiple.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      for atname,atid in la:
         tobj=tclass[atid]
         d={'text':XMLUtil.GetAsXMLStringNoPL(atname),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(tobj.CID,tobj.OID)}
         d['icon']='/icormanager/images/icons/silk/icons/table_go.png'
         d['openIcon']=d['icon']
#         d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(tobj.CID,tobj.OID,aobjname)
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(tobj.CID,tobj.OID)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(tobj.CID,tobj.OID)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)
      xmlfile.TagClose('tree')
   if lu:
      for atext,aurl in lu:
         d={'text':XMLUtil.GetAsXMLStringNoPL(atext),'action':aurl}
         d['icon']='/icormanager/images/icons/silk/icons/link_go.png'
         d['openIcon']=d['icon']
         d['action']=aurl #'icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(tobj.CID,tobj.OID,aobjname)
#         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(tobj.CID,tobj.OID)
   #               if wcontext:
   #      d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=%s&XMLData=1'%(acid,aoid,bfield.Name)
   #                  print 'Context 2:',d['context']
         xmlfile.TagOpen('tree',d,aclosetag=1)

   df={}
   if lf:
      try:
         aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=aobj.Struktura.Projekt.DBAccess)
      except Exception,v:
         print 'Exception:',v
         ADOLibInit.handle_com_error(v)
         import traceback
         traceback.print_exc()
         return
      try:
         for atid,afieldname in lf:
            try:
               rs=aado.SQL2RS("select %s from %sBZR_%d group by %s"%(afieldname,abasenamemodifier,atid,afieldname))
               try:
                  while not rs.EOF and not rs.BOF:
                     axmldataid=ADOLibInit.GetRSValueAsStr(rs,afieldname,astype=1)
                     df[axmldataid]=1
                     rs.MoveNext()
               finally:
                  rs=aado.CloseRS(rs)
            except:
               print 'TID:',atid,'FieldName:',afieldname
               import traceback
               traceback.print_exc()
      finally:
         aado.Close()

   xclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_XMLData_TableXMLData']
   lfn=[]
   for axmldataid in df.keys():
      xobj=xclass[axmldataid]
      if xobj:
         lfn.append([xobj.Grupa,xobj.Name,axmldataid,xobj])
   if lfn:
      lfn.sort()
      d={'text':XMLUtil.GetAsXMLStringNoPL('Zapytania XML')}
      d['icon']='/icormanager/images/icons/silk/icons/folder_page_white.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      algrupa=''
      wgrupa=0
      for agrupa,aname,axmldataid,xobj in lfn:
         if agrupa!=algrupa:
            if wgrupa:
               xmlfile.TagClose('tree')
            d={'text':XMLUtil.GetAsXMLStringNoPL(agrupa)}
            d['icon']='/icormanager/images/icons/silk/icons/page_white_code.png'
            d['openIcon']=d['icon']
            xmlfile.TagOpen('tree',d)
            wgrupa=1
            algrupa=agrupa
         d={'text':XMLUtil.GetAsXMLStringNoPL(aname),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(xobj.CID,xobj.OID)}
         d['icon']='/icormanager/images/icons/silk/icons/page_white_code_red.png'
         d['openIcon']=d['icon']
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(xobj.CID,xobj.OID)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(xobj.CID,xobj.OID)
         xmlfile.TagOpen('tree',d,aclosetag=1)
      if wgrupa:
         xmlfile.TagClose('tree')
      xmlfile.TagClose('tree')

   sta=aPluginVars.get('aTableOID_AssignedTables','')
   lat=[]
   if sta:
      try:
         aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=aobj.Struktura.Projekt.DBAccess)
      except Exception,v:
         print 'Exception:',v
         ADOLibInit.handle_com_error(v)
         import traceback
         traceback.print_exc()
         return
      try:
         try:
            rs=aado.SQL2RS("select distinct Rozdzial,IDObiektu,XMLDataID from %sBZR_%s"%(abasenamemodifier,sta))
            try:
               while not rs.EOF and not rs.BOF:
                  axmldataid=ADOLibInit.GetRSValueAsStr(rs,'XMLDataID',astype=1)
                  arozdzial=ADOLibInit.GetRSValueAsStr(rs,'Rozdzial',astype=1)
                  aidobiektu=ADOLibInit.GetRSValueAsStr(rs,'IDObiektu',astype=1)
                  lat.append([axmldataid,arozdzial,aidobiektu])
                  rs.MoveNext()
            finally:
               rs=aado.CloseRS(rs)
         except:
            import traceback
            traceback.print_exc()
      finally:
         aado.Close()
   lat2=[]
   if lat:
      xclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_XMLData_TableXMLData']
      rclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
      for axmldataid,arozdzial,aidobiektu in lat:
         xobj=xclass[axmldataid]
         robj=rclass[arozdzial]
         if xobj and robj:
            lat2.append([xobj.OID,robj.OID,aidobiektu,xobj,robj])
      lat2.sort()

   if lat2:
      aprojectname=aobj.Struktura.Projekt.Nazwa
      d={'text':XMLUtil.GetAsXMLStringNoPL('XML w rozdziałach')}
      d['icon']='/icormanager/images/icons/silk/icons/folder_page_white.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d)
      for xoid,roid,aidobiektu,xobj,robj in lat2:
         d={'text':XMLUtil.GetAsXMLStringNoPL('%d (%d) - %s'%(xobj.OID,robj.OID, xobj.Name))}
         d['icon']='/icormanager/images/icons/silk/icons/page_white_code.png'
         d['openIcon']=d['icon']
         xmlfile.TagOpen('tree',d)

         d={'text':XMLUtil.GetAsXMLStringNoPL(xobj.Name),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(xobj.CID,xobj.OID)}
         d['icon']='/icormanager/images/icons/silk/icons/page_white_code_red.png'
         d['openIcon']=d['icon']
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(xobj.CID,xobj.OID)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(xobj.CID,xobj.OID)
         xmlfile.TagOpen('tree',d,aclosetag=1)

         d={'text':XMLUtil.GetAsXMLStringNoPL(robj.Naglowek),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d'%(robj.CID,robj.OID)}
         d['icon']='/icormanager/images/wfxtree/items/book_closed_brown.png'
         d['openIcon']=d['icon']
         d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(robj.CID,robj.OID)
         d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(robj.CID,robj.OID)
         xmlfile.TagOpen('tree',d,aclosetag=1)

         tobj=robj.TabelaZrodlowa
         if tobj:
            d={'text':XMLUtil.GetAsXMLStringNoPL('Pozycja - '+tobj.Nazwa+' ['+aidobiektu+']'),'action':'appdata/%s/crm/BZR_%d_so.asp?ioid=%s&chapterid=%d'%(aprojectname,tobj.OID,aidobiektu,robj.OID)}
            d['icon']='/icormanager/images/icons/silk/icons/book_edit.png'
            d['openIcon']=d['icon']
            #d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
            #d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
            d['allowmove']='0'
            d['coid']=aidobiektu
            d['roid']=str(robj.OID)
            d['toid']=str(tobj.OID)
            d['rel']='record'
            xmlfile.TagOpen('tree',d,aclosetag=1)

         xmlfile.TagClose('tree')
      xmlfile.TagClose('tree')

