# -*- coding: windows-1250 -*-
# saved: 2023/01/24 22:44:33

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_NetBase_WWW_Dictionary_Menu_MenuUtil import ICORWWWMenuItem,JSONMenu
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
from CLASSES_Library_NetBase_WWW_HTML_Tree_SimpleLinks_Main import SimpleLinksHTMLTree
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_NetBase_WWW_Server_DoMenuWorkflowRecur as DoMenuWorkflowRecur
import string
import cStringIO

class ICORWWWServer:
   def __init__(self,aname='Default'):
      self.srvclass=aICORDBEngine.Classes['CLASSES\Library\NetBase\WWW\Server']
      self.OID=self.srvclass.Name.Identifiers(aname)
      if self.OID<0:
         raise exception,'Bad server name!'
      self.UID=0
      self.file=None
   def Generate(self,fname,auid):
      self.UID=auid
      self.cntWWWMenuClassRecur=0
      self.file=open(fname,'wb')
      self.level=0
      self.GenerateMenuXML()
      self.file.close()
   def WriteMenu(self,s):
      self.file.write(' '*self.level)
      self.file.write(s+'\n')
   def IncLevel(self):
      self.level=self.level+4
   def DecLevel(self):
      self.level=self.level-4
   def GenerateMenuXML(self):
      arefs=self.srvclass.Menu.GetRefList(self.OID)
      while arefs:
         amenu=ICORWWWMenuItem(self.UID,arefs.OID)
         self.GenerateMenuItemXML(amenu)
         arefs.Next()
   def GenerateMenuItemXML(self,amenu):
      if not amenu.IsVisibleByProfile(self.UID) or amenu.Caption=='Konfiguracja projektu':
         return
      self.DoGenerateMenuItemXML(amenu)
      self.IncLevel()
      arefs=self.srvclass.Menu.ClassOfType.SubMenu.GetRefList(amenu.oid)
      while arefs:
         bmenu=ICORWWWMenuItem(self.UID,arefs.OID)
         self.GenerateMenuItemXML(bmenu)
         arefs.Next()
      self.DecLevel()
   def DoGenerateMenuItemXML(self,amenu):
      self.WriteMenu('[m:%d] '%(amenu.oid,)+amenu.Caption)
      aclass=amenu.MenuClass
      aoid=amenu.oid
      aobj=aclass[aoid]
      if aobj.Action.Name=='Workflow Project':
         arefs=aclass.WorkflowMenuStruct.GetRefList(aoid)
         while arefs:
            self.IncLevel()
            self.DoMenuWorkflowRecur(arefs.OID,-1)
            self.DecLevel()
            arefs.Next()
   def DoMenuWorkflowRecur(self,aoid,coid,isgroup=0):
      bclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
      rclass=bclass.Rozdzialy.ClassOfType
      aclose=0
      aobj=bclass[aoid]
      if not aobj:
         pass
      elif coid<0:
         gobj=aobj.GrupyRozdzialow
         while gobj:
            if ICORSecurity.CheckRecursiveAccessLevelForUser(gobj,'AccessLevelView',self.UID):
               self.WriteMenu('[g:%d] '%(gobj.OID,)+gobj.Nazwa)
               self.IncLevel()
               robj=gobj.Rozdzialy
               while robj:
                  self.DoMenuWorkflowRecur(aoid,robj.OID,isgroup=1)
                  robj.Next()
               self.DecLevel()
            gobj.Next()
         robj=aobj.Rozdzialy
         #DoGetObjects(aobj,robj,None,xmlfile,UID,anogrouping=1)
         while robj:
            self.DoMenuWorkflowRecur(aoid,robj.OID)
            robj.Next()
      elif coid>=0:
         robj=rclass[coid]
         if not ICORSecurity.CheckRecursiveAccessLevelForUser(robj,'AccessLevelView',self.UID):
            return
         if not isgroup and robj.GrupaRozdzialow:
            return
         aname=robj.NaglowekMenu
         if not aname:
            aname=robj.Naglowek
         self.WriteMenu('[c:%d] '%(robj.OID,)+aname)
         self.IncLevel()
         pobj=robj.PodRozdzialy
         while pobj:
            self.DoMenuWorkflowRecur(aoid,pobj.OID)
            pobj.Next()
         self.DecLevel()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   fname=FilePathAsSystemPath('d:/icor/rozdzialy.txt')
   aserver=ICORWWWServer()
   auid=2136 #LPiorkowski
   aserver.Generate(fname,auid)
   return

