# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()
   aprofile=ICORSecurity.ICORSecurityProfile()
   aprofile.SetByUser(amenu.uid)
   aprofile.GetItemGroups()
   aprofile.GetUsers()
   l=[]
   for agname in aprofile.Groups.keys():
      if aprofile.ItemGroups.has_key(agname):
         l.append(agname)
   l.sort()
   file.write('<h2>Lista dostępnych grup bezpieczeństwa:</h2>')
   file.write('<pre>')
   for agname in l:
      file.write('%s\n'%agname)
   file.write('</pre>')

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   if 1:
      sobj=aobj.Projekt.AccessLevelView
      if sobj:
         dp={}
         pclass=sobj.Profile.Class
         while sobj:
            pobj=sobj.Profile
            dp[pobj.OID]=1
            sobj.Next()
         lp=[]
         for poid in dp.keys():
            lp.append([pclass.Name[poid],poid])
         lp.sort()
         for pname,poid in lp:
            d={'text':XMLUtil.GetAsXMLStringNoPL('Profil bezpieczeństwa: %s'%pname),
               'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
               'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
               'src':'icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(pclass.CID,poid),
               'context': 'icormain.asp?jobtype=menuclassrecurcontext&CID=%d&OID=%d&XMLData=1&brCID=%d&brOID=%d'%(pclass.CID,poid,-1,-1),
               'action':'icormain.asp?jobtype=objectedit&CID=%d&OID=%d&brCID=%d&brOID=%d'%(pclass.CID,poid,-1,-1),
            }
            xmlfile.TagOpen('tree',d)

         if 0:
            gobj=pobj.UserGroups
            while gobj:
               d={'text':XMLUtil.GetAsXMLStringNoPL(gobj.Name),
                  'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
                  'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
               }
               xmlfile.TagOpen('tree',d)
               uobj=gobj.Users
               while uobj:
                  d={'text':XMLUtil.GetAsXMLStringNoPL(uobj.UserName),
                     'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
                     'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
                  }
                  xmlfile.TagOpen('tree',d)
                  xmlfile.TagClose('tree')
      
                  uobj.Next()
               xmlfile.TagClose('tree')
               gobj.Next()
   
         xmlfile.TagClose('tree')

