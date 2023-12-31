# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWMenuClassRecur(xmlfile,bclass,afieldname,aoid,UID):
   return

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   return

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
   return

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   eobj=aobj.FieldEvents
   defrom,deto={},{}
   ecid=-1
   while eobj:
      ecid=eobj.CID
      sn=eobj.EventKind.EventName
      sf=eobj.EventFromValue
      ss=eobj.EventSource
      sd=eobj.EventDescription
      ws=0
      if ss:
         ws=1
      if not sf:
         sf='*'
      st=eobj.EventToValue
      if not st:
         st='*'
      l=defrom.get(sf,[])
      l.append([st,sn,eobj.OID,ws,sd])
      defrom[sf]=l
      l=deto.get(st,[])
      l.append([sf,sn,eobj.OID,ws,sd])
      deto[st]=l
      eobj.Next()
   lkf=defrom.keys()
   if len(lkf)>1:
      tobj=aobj.Dotyczy
      pobj=tobj.Projekt
      aAppPath=pobj.AppPath
      if aAppPath[-1:]!='/':
         aAppPath=aAppPath+'/'
      adir=aAppPath+'dictgraphs'
      afname=adir+'/%d_%d_%s.png'%(aobj.CID,aobj.OID,aobj.NazwaID)
      d={'text':XMLUtil.GetAsXMLStringNoPL('Schemat przej��'),'action':afname}
      d['icon']='/icormanager/images/icons/silk/icons/arrow_switch_bluegreen.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d,aclosetag=1)


      lkf.sort()
      d={'text':XMLUtil.GetAsXMLStringNoPL('Zdarzenia OD'),
         'icon':'/icormanager/images/icons/silk/icons/page_lightning.png',
         'openIcon':'/icormanager/images/icons/silk/icons/page_lightning.png',
      }
      xmlfile.TagOpen('tree',d)
      for evalue in lkf:
         l=defrom[evalue]
         d={'text':XMLUtil.GetAsXMLStringNoPL(evalue),
            'icon':'/icormanager/images/icons/silk/icons/folder_page.png',
            'openIcon':'/icormanager/images/icons/silk/icons/folder_page.png',
         }
         xmlfile.TagOpen('tree',d)
         l.sort()
         for estate,ename,eoid,ws,sd in l:
            s1,s2='',''
            if ws:
               s1='<font color=brown>'
               s2='</font>'
            if sd:
               sd='<em><font color=navy>, '+XMLUtil.GetAsXMLStringNoPL(sd)+'</font></em>'
            d={
               'text':'<font color=green>'+XMLUtil.GetAsXMLStringNoPL(estate)+'</font>, '+s1+XMLUtil.GetAsXMLStringNoPL(ename)+s2+sd,
               'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%d'%(ecid,eoid,aobj.CID,aobj.OID),
               'icon':'/icormanager/images/icons/silk/icons/script_lightning.png',
               'openIcon':'/icormanager/images/icons/silk/icons/script_lightning.png',
               'context':'icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(ecid,eoid),
            }
#            d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(ecid,eoid,aobjname)
#            d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(ecid,eoid)
            xmlfile.TagOpen('tree',d)
            xmlfile.TagClose('tree')
         xmlfile.TagClose('tree')
      xmlfile.TagClose('tree')

      lkt=deto.keys()
      lkt.sort()
      d={'text':XMLUtil.GetAsXMLStringNoPL('Zdarzenia DO'),
         'icon':'/icormanager/images/icons/silk/icons/page_lightning.png',
         'openIcon':'/icormanager/images/icons/silk/icons/page_lightning.png',
      }
      xmlfile.TagOpen('tree',d)
      for evalue in lkt:
         l=deto[evalue]
         d={'text':XMLUtil.GetAsXMLStringNoPL(evalue),
            'icon':'/icormanager/images/icons/silk/icons/folder_page.png',
            'openIcon':'/icormanager/images/icons/silk/icons/folder_page.png',
         }
         xmlfile.TagOpen('tree',d)
         l.sort()
         for estate,ename,eoid,ws,sd in l:
            s1,s2='',''
            if ws:
               s1='<font color=brown>'
               s2='</font>'
            if sd:
               sd='<em><font color=navy>, '+XMLUtil.GetAsXMLStringNoPL(sd)+'</font></em>'
            d={
               'text':'<font color=green>'+XMLUtil.GetAsXMLStringNoPL(estate)+'</font>, '+s1+XMLUtil.GetAsXMLStringNoPL(ename)+s2+sd,
               'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%d'%(ecid,eoid,aobj.CID,aobj.OID),
               'icon':'/icormanager/images/icons/silk/icons/script_lightning.png',
               'openIcon':'/icormanager/images/icons/silk/icons/script_lightning.png',
               'context':'icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(ecid,eoid),
            }
#            d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(ecid,eoid,aobjname)
#            d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(ecid,eoid)
            xmlfile.TagOpen('tree',d)
            xmlfile.TagClose('tree')
         xmlfile.TagClose('tree')
      xmlfile.TagClose('tree')

   l=defrom.get('*',[])
   if l:
      d={'text':XMLUtil.GetAsXMLStringNoPL('Zdarzenia'),
         'icon':'/icormanager/images/icons/silk/icons/page_lightning.png',
         'openIcon':'/icormanager/images/icons/silk/icons/page_lightning.png',
      }
      xmlfile.TagOpen('tree',d)
      l.sort()
      for estate,ename,eoid,ws,sd in l:
         s1,s2='',''
         if ws:
            s1='<font color=brown>'
            s2='</font>'
         if sd:
            sd='<em><font color=navy>, '+XMLUtil.GetAsXMLStringNoPL(sd)+'</font></em>'
         d={
            'text':'<font color=green>'+XMLUtil.GetAsXMLStringNoPL(estate)+'</font>, '+s1+XMLUtil.GetAsXMLStringNoPL(ename)+s2+sd,
            'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%d'%(ecid,eoid,aobj.CID,aobj.OID),
            'icon':'/icormanager/images/icons/silk/icons/script_lightning.png',
            'openIcon':'/icormanager/images/icons/silk/icons/script_lightning.png',
            'context':'icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&field=&XMLData=1'%(ecid,eoid),
         }
         if estate!='*':
            l2=defrom.get(estate,[])
            if l2:
               d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=subevents&param=%s&XMLData=1'%(ecid,eoid,'')
#            d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=table&param=%s'%(ecid,eoid,aobjname)
#            d['src']='icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(ecid,eoid)
         xmlfile.TagOpen('tree',d)
         xmlfile.TagClose('tree')
      xmlfile.TagClose('tree')


