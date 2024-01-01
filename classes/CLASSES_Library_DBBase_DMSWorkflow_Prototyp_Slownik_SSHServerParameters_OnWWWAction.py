# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

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

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   d={'text':XMLUtil.GetAsXMLStringNoPL('Stan serwera')}
   d['icon']='/icormanager/images/icons/silk/icons/server_connect.png'
   d['openIcon']=d['icon']
   d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=dir&param=%s'%(aobj.CID,aobj.OID,'')
   d['src']='icormain.asp?jobtype=menuclassrecuraction&CID=%d&OID=%d&type=dir&param=%s&XMLData=1'%(aobj.CID,aobj.OID,'')
   xmlfile.TagOpen('tree',d,aclosetag=1)

L_MENU=[
   ['Operating system / version','os_version'],
   ['Operating system / distribution','os_distribution'],
   ['Network configuration','network_configuration'],
   ['Network configuration / IP Address','networkipaddress'],
   ['Processor / cores','processor_cores'],
   ['Disk','disk'],
   ['Memory','memory'],
   ['UpTime','uptime'],
   ['Check limits','check_limits'],
   ['OpenResty','openresty'],
   ['Certbot / Certificates','certificates'],
   ['Active server connections','netstatservers'],
   ['Process / Tree','processtree'],
   ['Process / by memory','processbymemory'],
   ['Process / by CPU','processbycpu'],
]

def OnWWWMenuClassRecurAction(xmlfile,aobj,brobj,atype,aparam,acontext,UID):
   if atype!='dir':
      return
   for atext,aparam in L_MENU:
      d={'text':XMLUtil.GetAsXMLStringNoPL(atext)}
      d['action']='icormain.asp?jobtype=menuobjrecuraction&CID=%d&OID=%d&type=info&param=%s'%(aobj.CID,aobj.OID,aparam)
      d['icon']='/icormanager/images/icons/silk/icons/server_chart.png'
      d['openIcon']=d['icon']
      xmlfile.TagOpen('tree',d,aclosetag=1)

def OnWWWMenuObjRecurAction(file,aobj,atype,aparam,UID):
   file.write('<body topmargin="10">')
   dmenu={}
   for btext,bparam in L_MENU:
      dmenu[bparam]=btext
   if atype=='info':
      import appplatform.sshutilinfo as sshutilinfo
      asshmanager=sshutilinfo.SSHManager(aobj.SSHHost,aobj.SSHUserName,aobj.SSHPassword,aobj.SSHPort,anginxbasedir=aobj.NGINXBaseDir,aopenresty=aobj.OpenRestyExecutable)
      asshmanager.Open()
      try:
         sshutilinfo.VERBOSE=0
         asshinfosystem=sshutilinfo.SSHInfoSystem(asshmanager)
      finally:
         asshmanager.Close()
      atext=dmenu.get(aparam,'Info')
      if aparam=='os_version':
         asshinfosystem.InfoVersion()
      elif aparam=='check_limits':
         asshinfosystem.InfoLimits()
      elif aparam=='network_configuration':
         asshinfosystem.InfoNetwork()
      elif aparam=='os_distribution':
         asshinfosystem.InfoOperatingSystem()
      elif aparam=='processor_cores':
         asshinfosystem.InfoProcessors()
      elif aparam=='disk':
         asshinfosystem.InfoDisk()
      elif aparam=='memory':
         asshinfosystem.InfoMemory()
      elif aparam=='uptime':
         asshinfosystem.InfoUpTime()
      elif aparam=='openresty':
         asshinfosystem.InfoOpenResty()
      elif aparam=='certificates':
         asshinfosystem.InfoCertbot()
      elif aparam=='netstatservers':
         asshinfosystem.InfoNetstatServers()
      elif aparam=='networkipaddress':
         asshinfosystem.InfoNetworkIPAddress()
      elif aparam=='processtree':
         asshinfosystem.InfoProcessTree()
      elif aparam=='processbymemory':
         asshinfosystem.InfoProcessByMemory()
      elif aparam=='processbycpu':
         asshinfosystem.InfoProcessByCPU()

      file.write('<h1>'+atext+'</h1>')
      file.write("<textarea id='Tresc' name='Tresc' wrap='Off' style='width:100%;height:600px;' >") #cols=32 rows=6
      for atime,aname,stdout,stderr in asshinfosystem.data:
         for s in stdout:
            file.write(s+'\n')
         for s in stderr:
            file.write(s+'\n')
      file.write('</textarea>')

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

