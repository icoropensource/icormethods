# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import icordbmain.adoutil as ADOLibInit
import CLASSES_Library_ICORBase_External_MLog as MLog
import icordbmain.dbaccess as dbaccess

import xml.etree.ElementTree as ET

VERBOSE=0

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def GetValueWin(v):
   v=v.encode('cp1250','ignore')
   return v

def OnWWWGetFieldIteratorEvent(afield,aoid,aparamobj):
   if aoid<0 and afield.Name in ['EffectSkins','ChapterView','Models','Plugins','PageTemplate','ListyWysylkowe']:
      return -1
   elif aparamobj and aoid<0:
      aobj=aparamobj.AsObject()
   elif aoid<0:
      return None
   else:
      rclass=afield.ClassItem
      aobj=rclass[aoid]
   if afield.Name=='TabelaZrodlowa':
      if aobj.CID==afield.ClassItem.CID:
         bobj=aobj.AsObject()
         sobj=None
         while 1:
            sobj=bobj.Struktura
            if sobj:              
               break
            bobj=bobj.NadRozdzial
         if sobj is None:
            return None
         return sobj.TabeleZrodlowe
      sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      if aobj.CID==sclass.CID:
         return aobj.TabeleZrodlowe
   if afield.Name=='Plugins':
      if aobj.CID==afield.ClassItem.CID:
         bobj=aobj.AsObject()
         sobj=None
         while 1:
            sobj=bobj.Struktura
            if sobj:              
               break
            bobj=bobj.NadRozdzial
         if sobj is None:
            return None
         return sobj.Plugins
      sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      if aobj.CID==sclass.CID:
         return aobj.Plugins
   if afield.Name=='PageTemplate':
      if aobj.CID==afield.ClassItem.CID:
         bobj=aobj.AsObject()
         sobj=None
         while 1:
            sobj=bobj.Struktura
            if sobj:              
               break
            bobj=bobj.NadRozdzial
         if sobj is None:
            return None
         return sobj.PageTemplate
      sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      if aobj.CID==sclass.CID:
         return aobj.PageTemplate
   if afield.Name=='ListyWysylkowe':
      if aobj.CID==afield.ClassItem.CID:
         bobj=aobj.AsObject()
         sobj=None
         while 1:
            sobj=bobj.Struktura
            if sobj:              
               break
            bobj=bobj.NadRozdzial
         if sobj is None:
            return None
         return sobj.Projekt.ListyWysylkowe
      sclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      if aobj.CID==sclass.CID:
         return aobj.Projekt.ListyWysylkowe
   if afield.Name=='EffectSkins':
      if aobj.CID==afield.ClassItem.CID:
         arefs=FieldRefIterator()
         sobj=aobj.Effects
         while sobj:
            arefs.AddRefs(sobj.Skins.AsRefs())
            sobj.Next()
         if arefs:
            return arefs.AsObject()
         return -1
   if afield.Name=='Models':
      if aobj.CID==afield.ClassItem.CID:
         return aobj.Models
   if afield.Name=='ChapterView':
      if aobj.CID==afield.ClassItem.CID:
         return aobj.ChapterView
   return None

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.OnWWWGetFieldIteratorEvent=OnWWWGetFieldIteratorEvent
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecurCheck(xmlfile,aobj,UID):
   ret=0
   if 1:
      tobj=aobj.TabelaZrodlowa
      if not tobj:
         return 0

      abasenamemodifier=tobj.Projekt.BaseNameModifier
      aprojectname=tobj.Projekt.Nazwa
      try:
         aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=tobj.Projekt.DBAccess)
      except Exception,v:
         #print 'Exception:',v
         #ADOLibInit.handle_com_error(v)
         #import traceback
         #traceback.print_exc()
         return 0
      try:
         try:
            if 0 and not aobj['SGIsTableView']:
               atable_fileuploads='%sFILEUPLOADS_0'%(abasenamemodifier,)
               atable_main='%sBZR_%d'%(abasenamemodifier,tobj.OID)
               asql="SELECT top 1 %s.* FROM %s left join %s on %s.RefOID=%s._OID where %s._chapterid=%d order by %s.Name"%(atable_fileuploads,atable_fileuploads,atable_main,atable_fileuploads,atable_main,atable_main,aobj.OID,atable_fileuploads)
               rs=aado.SQL2RS(asql)
               try:
                  if not rs.EOF and not rs.BOF:
                     ret=1
               finally:
                  rs=aado.CloseRS(rs)
            else:
               while tobj:
                  atable_main='%sBZR_%d'%(abasenamemodifier,tobj.OID)
                  asql="SELECT top 1 * FROM %s where _chapterid=%d"%(atable_main,aobj.OID)
                  rs=aado.SQL2RS(asql)
                  try:
                     if not rs.EOF and not rs.BOF:
                        ret=1
                        break
                  finally:
                     rs=aado.CloseRS(rs)
                  tobj.Next()
         except:
            import traceback
            traceback.print_exc()
      finally:
         aado.Close()
   return ret

def GetSubTags(child):
   dfields={}
   for subchild in child:
      sk=subchild.tag.lower()
      sv=subchild.text
      if sv:
         dfields[GetValueWin(sk)]=GetValueWin(sv)
   return dfields

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
#   print 'obj - c:',aobj.Class.CID,aobj.Class.NameOfClass,'o:',aobj.OID,'u:',UID

   if 1:
      tobj=aobj.TabelaZrodlowa
      if not tobj:
         return

      abasenamemodifier=tobj.Projekt.BaseNameModifier
      aprojectname=tobj.Projekt.Nazwa
      la=[]
      tlo=[]
      try:
         aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=tobj.Projekt.DBAccess)
      except Exception,v:
         #print 'Exception:',v
         #ADOLibInit.handle_com_error(v)
         #import traceback
         #traceback.print_exc()
         return
      try:
         try:
            if 0 and not aobj['SGIsTableView']:
               atable_fileuploads='%sFILEUPLOADS_0'%(abasenamemodifier,)
               atable_main='%sBZR_%d'%(abasenamemodifier,tobj.OID)
               asql="SELECT %s.* FROM %s left join %s on %s.RefOID=%s._OID where %s._chapterid=%d and %s.Status not in ('D','U') order by %s.Name"%(atable_fileuploads,atable_fileuploads,atable_main,atable_fileuploads,atable_main,atable_main,aobj.OID,atable_fileuploads,atable_fileuploads)
               rs=aado.SQL2RS(asql)
               try:
                  while not rs.EOF and not rs.BOF:
                     afileoid=ADOLibInit.GetRSValueAsStr(rs,'_OID',astype=1)
                     afilename=ADOLibInit.GetRSValueAsStr(rs,'Name',astype=1)
                     la.append([afileoid,afilename])
                     rs.MoveNext()
               finally:
                  rs=aado.CloseRS(rs)
            else:
               while tobj:
                  lo=[]
                  fobj=tobj.Pola
                  lfields=[]
                  lfcnt=0
                  while fobj:
                     if fobj['SGIsAliased']:
                        st=fobj.TypPolaDotyczy.Nazwa
                        if not st in ['external dict','external dict multiple']:
                           lfields.append(fobj.NazwaID.lower())
                           lfcnt=lfcnt+1
                           if lfcnt==3:
                              break
                     fobj.Next()
                  df={
                     'abasenamemodifier':abasenamemodifier,
                     'toid':tobj.OID,
                     'coid':aobj.OID,
                     'lfields':','.join(['T1.'+x for x in lfields]),
                  }
                  asql='''
            SELECT TOP 1000 
                T1._OID as '@OID', T1._OID, T1._ChapterID, replace(replace(convert(varchar(max),T1._datetime,120),'T00:00:00',''),' 00:00:00','') as _datetime,
                %(lfields)s
            , (
                select TOP 50
                    _OID as '@OID', _OID, replace(replace(convert(varchar(max),_datetime,120),'T00:00:00',''),' 00:00:00','') as _datetime, 
                    replace(replace(convert(varchar(max),_actiontime,120),'T00:00:00',''),' 00:00:00','') as _actiontime, 
                    case _action 
                        when 'INSERT' then 'nowa pozycja'
                        when 'UPDATE' then 'modyfikacja wartości'
                        when 'DELETE' then 'usunięcie pozycji'
                        else _action
                    end as _action
                from %(abasenamemodifier)sBZR_V_%(toid)d
                WHERE _OIDRef=T1._OID
                ORDER BY _datetime DESC
                for xml path('VERSION'),type 
            ) as VERSIONS
            , (
                select _OID as '@OID', 
                    _OID, Name, FileSize, replace(replace(convert(varchar(max),_datetime,120),'T00:00:00',''),' 00:00:00','') as _datetime
                from %(abasenamemodifier)sFILEUPLOADS_0 f1
                WHERE Status not in ('D','U') and RefOID=T1._OID
                ORDER BY Name
                for xml path('FILE'),type 
            ) as FILES
            FROM %(abasenamemodifier)sBZR_%(toid)d AS T1
            WHERE  (T1._ChapterID=%(coid)d)
            ORDER BY T1._datetime DESC
    for xml path('ROW'),root('ROWS')
'''%df
                  axml=''
                  asql='select ( %s ) as result'%asql
                  rs=aado.SQL2RS(asql)
                  try:
                     while not rs.EOF and not rs.BOF:
                        axml=ADOLibInit.GetRSValueAsStr(rs,'result',astype=1)
                        rs.MoveNext()
                  finally:
                     rs=aado.CloseRS(rs)
                  if axml:
                     axml='<?xml version="1.0" encoding="windows-1250"?>'+axml
                     if VERBOSE:
                        MLog.GetLogTempFileName('test',aprefix='log',asufix='chapter',avalue=axml,atrace=0)
                     root = ET.fromstring(axml)
                     for child in root:
                        cfiles,cversions=None,None
                        dfields={}
                        for subchild in child:
                           if subchild.tag=='FILES':
                              cfiles=subchild
                           elif subchild.tag=='VERSIONS':
                              cversions=subchild
                           else:
                              sk=subchild.tag.lower()
                              sv=subchild.text
                              if sv:
                                 dfields[GetValueWin(sk)]=GetValueWin(sv)
                        ltytul=[]
                        for afieldname in lfields:
                           s=dfields.get(afieldname,'')
                           if s:
                              ltytul.append(s)
                        stytul=', '.join(ltytul)
                        ioid=dfields.get('_oid','?')
                        if not stytul:
                           stytul='pozycja: '+ioid
                        lfiles=[]
                        if cfiles:
                           for subchild in cfiles:
                              d=GetSubTags(subchild)
                              lfiles.append([d.get('_oid',''),d.get('name','')])
                              #print '  FILE:',subchild.tag, subchild.attrib,
                        lo.append([ioid,stytul,lfiles])
                  if lo:
                     tlo.append([tobj.OID,tobj.Nazwa,lo])
                  tobj.Next()
         except:
            import traceback                
            traceback.print_exc()
      finally:
         aado.Close()

      if la:
         d={'text':XMLUtil.GetAsXMLStringNoPL('Załączniki')}
         d['icon']='/icorimg/silk/folder_link.png'
         d['openIcon']=d['icon']
         xmlfile.TagOpen('tree',d)
         for afileoid,afilename in la:
            d={'text':XMLUtil.GetAsXMLStringNoPL(afilename),'action':'appdata/%s/crm/FILES_DOWNLOAD_0.asp?foid=%s'%(aprojectname,afileoid,)} #cid,oid
            d['icon']=ICORUtil.GetFileExtIcon(afilename)
            d['openIcon']=d['icon']
            #d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
            #d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
            d['allowmove']='1'
            d['coid']=afileoid
            d['roid']=str(aobj.OID)
            d['rel']='attachment'
            xmlfile.TagOpen('tree',d,aclosetag=1)
         xmlfile.TagClose('tree')

      if tlo:
         for toid,tname,lo in tlo:
            d={'text':XMLUtil.GetAsXMLStringNoPL('Pozycje - '+tname)}
            d['icon']='/icorimg/silk/book_open.png'
            d['openIcon']=d['icon']
            xmlfile.TagOpen('tree',d)
            for ioid,stytul,lfiles in lo:
               d={'text':XMLUtil.GetAsXMLStringNoPL(stytul),'action':'appdata/%s/crm/BZR_%d_so.asp?ioid=%s&chapterid=%d'%(aprojectname,toid,ioid,aobj.OID)} #cid,oid
               d['icon']='/icorimg/silk/book_edit.png'
               d['openIcon']=d['icon']
               #d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
               #d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
               d['allowmove']='0'
               d['coid']=ioid
               d['roid']=str(aobj.OID)      
               d['toid']=str(toid)
               d['rel']='record'
               xmlfile.TagOpen('tree',d)
               if lfiles:
                  d={'text':XMLUtil.GetAsXMLStringNoPL('Załączniki')}
                  d['icon']='/icorimg/silk/folder_link.png'
                  d['openIcon']=d['icon']
                  xmlfile.TagOpen('tree',d)
                  for afileoid,afilename in lfiles:
                     d={'text':XMLUtil.GetAsXMLStringNoPL(afilename),'action':'appdata/%s/crm/FILES_DOWNLOAD_0.asp?foid=%s'%(aprojectname,afileoid,)} #cid,oid
                     d['icon']=ICORUtil.GetFileExtIcon(afilename)
                     d['openIcon']=d['icon']
                     #d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
                     #d['context']='icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(-1,-1) #xobj.CID,xobj.OID
                     d['allowmove']='1'
                     d['coid']=afileoid
                     d['roid']=str(aobj.OID)
                     d['rel']='attachment'
                     xmlfile.TagOpen('tree',d,aclosetag=1)
                  xmlfile.TagClose('tree')
               xmlfile.TagClose('tree')
            xmlfile.TagClose('tree')
   return

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
      if akey.find('aTableOID_')==0:
         try:
            l.append(int(atid))
            sl=akey.split('_')
            dt[sl[1]]=int(atid)
         except ValueError:
            pass
      if akey.find('aURL:')==0:
         lu.append([akey[5:],atid])
      if akey.find('aField_XMLDataID_')==0:
         sl=akey.split('_')
         lf.append([dt[sl[2]],atid])
   if aobj.Template:
      aTemplateVars=ICORUtil.ParseVars(aobj.Template.TemplateVars,{})
      for akey,atid in aTemplateVars.items():
         if akey.find('aTableOID_')==0:
            try:
               l.append(int(atid))
               sl=akey.split('_')
               dt[sl[1]]=int(atid)
            except ValueError:
               pass
         if akey.find('aURL:')==0:
            lu.append([akey[5:],atid])
         if akey.find('aField_XMLDataID_')==0:
            sl=akey.split('_')
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
         d={'text':XMLUtil.GetAsXMLStringNoPL(tobj.Nazwa),'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d&chapterid=%d'%(tobj.CID,tobj.OID,aobj.OID)}
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
   if lf:
      abasenamemodifier=aobj.Struktura.Projekt.BaseNameModifier
      df={}
      try:
         aado=ADOLibInit.ADOUtil(acnt=1,acominitialize=1,dbaccessobj=aobj.Struktura.Projekt.DBAccess)
      except Exception,v:
         #print 'Exception:',v
         #ADOLibInit.handle_com_error(v)
         #import traceback
         #traceback.print_exc()
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


