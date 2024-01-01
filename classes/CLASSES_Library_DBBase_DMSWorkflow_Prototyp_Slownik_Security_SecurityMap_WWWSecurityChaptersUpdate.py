# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_WWW_Server_ServerUtil as ServerUtil
import cStringIO
import string

ReplicationException = 'ReplicationException'

class ICORXMLSecurityChapterParser(XMLUtil.ICORBaseXMLParser):
   def Parse(self,atext='',fname=''):
      if atext:
         XMLUtil.ICORBaseXMLParser.Parse(self,atext)
      else:
         if fname!='':
            self.afile=fname
         if self.afile=='':
            raise ReplicationException,'No file'
         self.afile=FilePathAsSystemPath(self.afile)
         fsize=os.path.getsize(self.afile)
         f=TextFile(self.afile,'r')
         i=0
         try:
            s=f.readline()
            while s!='':
               self.feed(s[:-1])
               i=i+1
               if i>=120:
                  i=0
                  apos=f.tell()
                  SetProgress(apos,fsize)
               s=f.readline()
            self.close()
         finally:
            f.close()
            SetProgress(0,0)
   def start_CHAPTERSECURITY(self,attrs):
      self.ElementInfo()
      self.ChapterClass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Rozdzial']
      self.ACLClass=aICORDBEngine.Classes['CLASSES_System_GroupItemAccessLevel']
      self.DefaultAccessLevelView=0
      self.DefaultAccessLevelEdit=0
      self.DefaultAccessLevelTableEdit=0
      self.DefaultSecurity=[]
      self.DefaultAccessLevel=0
   def end_CHAPTERSECURITY(self):
      pass
   def start_PROJECT(self,attrs):
      self.ElementInfo(attrs.get('Project',''),astatus=1)
      if attrs.get('DefaultAccessLevelView','0')=='1':
         self.DefaultAccessLevelView=1
      if attrs.get('DefaultAccessLevelEdit','0')=='1':
         self.DefaultAccessLevelEdit=1
      if attrs.get('DefaultAccessLevelTableEdit','0')=='1':
         self.DefaultAccessLevelTableEdit=1
      self.DefaultAccessLevel=self.DefaultAccessLevelView+self.DefaultAccessLevelEdit+self.DefaultAccessLevelTableEdit
   def end_PROJECT(self):
      pass
   def start_CHAPTER(self,attrs):
      self.ElementInfo(attrs.get('Name',''),astatus=1)
      self.COID=int(attrs.get('OID','-1'))
      if self.COID<0:
         raise ReplicationException,'Bad chapter OID: '+attrs.get('Name','')
      if self.DefaultAccessLevel:
         sname=attrs.get('Name',ServerUtil.SPLIT_CHAR_PARAM)
         soid=self.ACLClass.Name.Identifiers(sname)
         if soid>=0:
            if self.DefaultAccessLevelView:
               self.ChapterClass.AccessLevelView.AddRefs(self.COID,[soid,self.ACLClass.CID]+self.DefaultSecurity,asortedreffield=self.ACLClass.Name,dosort=1,ainsertifnotexists=1)
            if self.DefaultAccessLevelEdit:
               self.ChapterClass.AccessLevelEdit.AddRefs(self.COID,[soid,self.ACLClass.CID]+self.DefaultSecurity,asortedreffield=self.ACLClass.Name,dosort=1,ainsertifnotexists=1)
            if self.DefaultAccessLevelTableEdit:
               self.ChapterClass.AccessLevelTableEdit.AddRefs(self.COID,[soid,self.ACLClass.CID]+self.DefaultSecurity,asortedreffield=self.ACLClass.Name,dosort=1,ainsertifnotexists=1)
   def end_CHAPTER(self):
      pass
   def start_ACCESSLEVELVIEW(self,attrs):
      self.ElementInfo(attrs.get('Name',''),astatus=1)
      amode=attrs.get('mode','')
      sname=attrs.get('Name',ServerUtil.SPLIT_CHAR_PARAM)
      if ICORUtil.strLowerPL(sname) in ICORSecurity.PROTECTED_GROUPS:
         return
      soid=self.ACLClass.Name.Identifiers(sname)
      if soid<0:
         raise ReplicationException,'Bad ACL: '+sname
      if amode=='update':
         self.ChapterClass.AccessLevelView.AddRefs(self.COID,[soid,self.ACLClass.CID]+self.DefaultSecurity,asortedreffield=self.ACLClass.Name,dosort=1,ainsertifnotexists=1)
      elif amode=='delete':
         self.ChapterClass.AccessLevelView.DeleteRefs(self.COID,[soid,self.ACLClass.CID])
      if attrs.get('isDefaultSecurity','0')=='1':
         self.DefaultSecurity=self.DefaultSecurity+[soid,self.ACLClass.CID]
   def end_ACCESSLEVELVIEW(self):
      pass
   def start_ACCESSLEVELEDIT(self,attrs):
      self.ElementInfo(attrs.get('Name',''),astatus=1)
      amode=attrs.get('mode','')
      sname=attrs.get('Name',ServerUtil.SPLIT_CHAR_PARAM)
      if ICORUtil.strLowerPL(sname) in ICORSecurity.PROTECTED_GROUPS:
         return
      soid=self.ACLClass.Name.Identifiers(sname)
      if soid<0:
         raise ReplicationException,'Bad ACL: '+sname
      if amode=='update':
         self.ChapterClass.AccessLevelEdit.AddRefs(self.COID,[soid,self.ACLClass.CID]+self.DefaultSecurity,asortedreffield=self.ACLClass.Name,dosort=1,ainsertifnotexists=1)
      elif amode=='delete':
         self.ChapterClass.AccessLevelEdit.DeleteRefs(self.COID,[soid,self.ACLClass.CID])
      if attrs.get('isDefaultSecurity','0')=='1':
         self.DefaultSecurity=self.DefaultSecurity+[soid,self.ACLClass.CID]
   def end_ACCESSLEVELEDIT(self):
      pass
   def start_ACCESSLEVELTABLEEDIT(self,attrs):
      self.ElementInfo(attrs.get('Name',''),astatus=1)
      amode=attrs.get('mode','')
      sname=attrs.get('Name',ServerUtil.SPLIT_CHAR_PARAM)
      if ICORUtil.strLowerPL(sname) in ICORSecurity.PROTECTED_GROUPS:
         return
      soid=self.ACLClass.Name.Identifiers(sname)
      if soid<0:
         raise ReplicationException,'Bad ACL: '+sname
      if amode=='update':
         self.ChapterClass.AccessLevelTableEdit.AddRefs(self.COID,[soid,self.ACLClass.CID]+self.DefaultSecurity,asortedreffield=self.ACLClass.Name,dosort=1,ainsertifnotexists=1)
      elif amode=='delete':
         self.ChapterClass.AccessLevelTableEdit.DeleteRefs(self.COID,[soid,self.ACLClass.CID])
      if attrs.get('isDefaultSecurity','0')=='1':
         self.DefaultSecurity=self.DefaultSecurity+[soid,self.ACLClass.CID]
   def end_ACCESSLEVELTABLEEDIT(self):
      pass

def ProcessRozdzial(robj,afile,rpath,alevel=0):
   acaption=robj.Naglowek
   acaptionm=robj.NaglowekMenu
   if acaptionm:
      acaption=acaptionm
   rpath.append(acaption)
   l1obj=robj.AccessLevelView
   l2obj=robj.AccessLevelEdit
   l3obj=robj.AccessLevelTableEdit
   sobj=robj.PodRozdzialy
   w=0
   if l1obj or sobj:
      w=0
   d={'OID':str(robj.OID),'Name':string.join(rpath,' - ')}
   afile.TagOpen('CHAPTER',d,aclosetag=w)
   while l1obj:
      d={'Name':l1obj.Name,'mode':'update'}
      afile.TagOpen('ACCESSLEVELVIEW',d,aclosetag=1)
      l1obj.Next()
   while l2obj:
      d={'Name':l2obj.Name,'mode':'update'}
      afile.TagOpen('ACCESSLEVELEDIT',d,aclosetag=1)
      l2obj.Next()
   while l3obj:
      d={'Name':l3obj.Name,'mode':'update'}
      afile.TagOpen('ACCESSLEVELTABLEEDIT',d,aclosetag=1)
      l3obj.Next()
   while sobj:
      ProcessRozdzial(sobj,afile,rpath,alevel=alevel+1)
      sobj.Next()
   if not w:
      afile.TagClose('CHAPTER')
   rpath.pop()

def GetMenuXMLForProject(sfile,pobj,asecprofile):
   afile=XMLUtil.MXMLFile(sfile,anopl=1)
   afile.Header()
   afile.TagOpen('CHAPTERSECURITY')
   pname=asecprofile.ProfileClass[asecprofile.ProfileOIDs[0]].Name
   afile.TagOpen('PROJECT',{'Name':pobj.Nazwa})
   wobj=pobj.WWWMenuStruct
   while wobj:
      mname=wobj.Nazwa
      robj=wobj.Rozdzialy
      while robj:
         ProcessRozdzial(robj,afile,[pname,mname])
         robj.Next()
      wobj.Next()
   afile.TagClose('PROJECT')
   afile.TagClose('CHAPTERSECURITY')
   afile.close()

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   svalue=''
   if areport is None:
      bfile=cStringIO.StringIO()
      pobj=aclass[aoid].Projekt
      asecprofile=ICORSecurity.ICORSecurityProfile()
      asecprofile.SetByUser(amenu.uid)
      GetMenuXMLForProject(bfile,pobj,asecprofile)
      svalue=bfile.getvalue()
      bfile.close()
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
#   awwweditor.RegisterField('Nazwa',aoid=aoid)
   awwweditor.RegisterField('Ustawienia',adisplayed='Ustawienia',atype=mt_Memo,avalue=svalue)
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
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
         file.write('&lt;ACCESSLEVELVIEW Name="%s" mode="update" /&gt;\n'%agname)
      file.write('</pre>')
      file.write('<hr><pre>')
      for agname in l:
         file.write('&lt;ACCESSLEVELEDIT Name="%s" mode="update" /&gt;\n'%agname)
      file.write('</pre>')
      file.write('<hr><pre>')
      for agname in l:
         file.write('&lt;ACCESSLEVELTABLEEDIT Name="%s" mode="update" /&gt;\n'%agname)
      file.write('</pre>')
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      asecload=ICORXMLSecurityChapterParser()
      asecload.Parse(awwweditor['Ustawienia'])
      file.write('<pre>')
      asecload.Dump(file,anoprint=1)
      file.write('</pre>')
      awwweditor.WriteObjectView(aobj,asbutton=1)



