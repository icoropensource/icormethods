# -*- coding: windows-1250 -*-
# saved: 2021/05/16 16:12:21

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_Win32_IIS_IISUtil as IISUtil
import icorlib.projekt.sqlrun as SQLRun
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import CLASSES_Library_ICORBase_External_MLog as MLog
import os
import re
import sys
import shutil
import string
import cStringIO
import types

class VariablesParser(XMLUtil.ICORBaseXMLParser):
   def Parse(self,aprofile,atext):
      self.IsGood=1
      self.Profile=aprofile
      XMLUtil.ICORBaseXMLParser.Parse(self,atext)
   def start_PARAMETERS(self,attrs):
      self.ElementInfo()
   def end_PARAMETERS(self):
      pass
   def start_VAR(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','external','if','inputname',])
      if l:
         self.Profile.IsGood=0
         print 'nieznane atrybuty w tagu <VAR>: %s'%str(l)
      self.ThisVarName=attrs.get('name','')
      self.TagData=''
      self.varif=1
      if attrs.get('if',''):
         self.varif=self.Profile.GetEval(attrs.get('if',''))
      aexternal=self.Profile.GetValue(attrs.get('external',''))
      self.ExternalData=''
      if aexternal:
         self.ExternalData=self.Profile.ParseData(aname=aexternal)
      if attrs.get('inputname',''):
         self.Profile.InputVariables.append([self.ThisVarName,attrs.get('inputname','')])
   def end_VAR(self):
      if self.varif:
         self.Profile[self.ThisVarName]=self.ExternalData+self.TagData
   def start_CONST(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','external','if','inputname'])
      if l:
         self.Profile.IsGood=0
         print 'nieznane atrybuty w tagu <CONST>: %s'%str(l)
      self.ThisVarName=attrs.get('name','')
      self.TagData=''
      self.varif=1
      if attrs.get('if',''):
         self.varif=self.Profile.GetEval(attrs.get('if',''))
      aexternal=self.Profile.GetValue(attrs.get('external',''))
      self.ExternalData=''
      if aexternal:
         self.ExternalData=self.Profile.ParseData(aname=aexternal)
   def end_CONST(self):
      if self.varif:
         self.Profile[self.ThisVarName]=self.ExternalData+self.TagData

class DataParser(XMLUtil.ICORBaseXMLParser):
   def Parse(self,aprofile,atext):
      self.IsGood=1
      self.Profile=aprofile
      XMLUtil.ICORBaseXMLParser.Parse(self,atext)
      self.UserGroupClass=aICORDBEngine.Classes['CLASSES_System_GroupAccessLevel']
      self.ItemGroupClass=aICORDBEngine.Classes['CLASSES_System_GroupItemAccessLevel']
   def start_LOG(self,attrs):
      self.ElementInfo()
      l=self.CheckAttrs(attrs,['text','file'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <LOG>: %s'%str(l)
      atext=self.Profile.GetValue(attrs['text'])
      afile=FilePathAsSystemPath(self.Profile.GetValue(attrs.get('file',r'%ICOR%\log\metagenerate_log.txt')))
      MLog.Log(atext,fname=afile,aconsole=1)
   def end_LOG(self):
      pass
   def start_SLEEP(self,attrs):
      self.ElementInfo()
      l=self.CheckAttrs(attrs,['time',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <SLEEP>: %s'%str(l)
      avalue=self.Profile.GetEval(attrs['time'])
      if self.Profile.mode in ['build','undo']:
         time.sleep(avalue)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_SLEEP(self):
      pass
   def start_DATA(self,attrs):
      self.ElementInfo()
      pass
   def end_DATA(self):
      pass
   def start_VAR(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','external','if'])
      if l:
         self.Profile.IsGood=0
         print 'nieznane atrybuty w tagu <VAR>: %s'%str(l)
      self.ThisVarName=attrs.get('name','')
      self.TagData=''
      self.varif=1
      if attrs.get('if',''):
         self.varif=self.Profile.GetEval(attrs.get('if',''))
      aexternal=self.Profile.GetValue(attrs.get('external',''))
      self.ExternalData=''
      if aexternal:
         self.ExternalData=self.Profile.ParseData(aname=aexternal)
   def end_VAR(self):
      if self.varif:
         self.Profile[self.ThisVarName]=self.ExternalData+self.TagData
   def start_CONST(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','external','if'])
      if l:
         self.Profile.IsGood=0
         print 'nieznane atrybuty w tagu <CONST>: %s'%str(l)
      self.ThisVarName=attrs.get('name','')
      self.TagData=''
      self.varif=1
      if attrs.get('if',''):
         self.varif=self.Profile.GetEval(attrs.get('if',''))
      aexternal=self.Profile.GetValue(attrs.get('external',''))
      self.ExternalData=''
      if aexternal:
         self.ExternalData=self.Profile.ParseData(aname=aexternal)
   def end_CONST(self):
      if self.varif:
         self.Profile[self.ThisVarName]=self.ExternalData+self.TagData
   def start_DIRCREATE(self,attrs):
      self.ElementInfo(attrs.get('path',''))
      l=self.CheckAttrs(attrs,['path','var','if'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <DIRCREATE>: %s'%str(l)
      if attrs.get('var',''):
         self.Profile[attrs.get('var','')]=attrs['path']
      avalue=self.Profile.GetValue(attrs['path'])
      if self.Profile.mode=='build':
         if os.path.exists(avalue):
            print 'katalog juz istnieje: '+avalue
         else:
            self.varif=1
            if attrs.get('if',''):
               self.varif=self.Profile.GetEval(attrs.get('if',''))
            if self.varif:
               os.makedirs(avalue)
               print 'nowy katalog: '+avalue
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
         if os.path.exists(avalue):
            print 'katalog juz istnieje: '+avalue
         else:
            print 'katalog nie istnieje: '+avalue
   def end_DIRCREATE(self):
      pass
   def start_DIRDELETE(self,attrs):
      self.ElementInfo(attrs.get('path',''))
      l=self.CheckAttrs(attrs,['path','var','if','recursive'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <DIRDELETE>: %s'%str(l)
      if attrs.get('var',''):
         self.Profile[attrs.get('var','')]=attrs['path']
      avalue=self.Profile.GetValue(attrs['path'])
      if self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
         if os.path.exists(avalue):
            print 'katalog juz istnieje: '+avalue
         else:
            print 'katalog nie istnieje: '+avalue
      elif self.Profile.mode=='undo':
         print 'usuwam katalog: '+avalue
         if not os.path.exists(avalue):
            print 'katalog do usuniecia nie istnieje: '+avalue
         else:
            try:
               self.varif=1
               if attrs.get('if',''):
                  self.varif=self.Profile.GetEval(attrs.get('if',''))
               if self.varif:
                  if attrs.get('recursive','')=='1':
                     shutil.rmtree(avalue)
                  else:
                     os.removedirs(avalue)
                  print 'katalog usuniety: '+avalue
            except:
               print 'katalog do usuniecia nie jest pusty lub brak praw dostepu: '+avalue
   def end_DIRDELETE(self):
      pass
   def start_INDEXCREATE(self,attrs):
      self.ElementInfo(attrs.get('catalog',''))
      l=self.CheckAttrs(attrs,['catalog','path'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <INDEXCREATE>: %s'%str(l)
      acatalog=self.Profile.GetValue(attrs['catalog'])
      apath=self.Profile.GetValue(attrs['path'])
      if self.Profile.mode=='build':
         print 'nowy index katalog: '+acatalog
         ret=IISUtil.ISAddCatalog(acatalog,apath)
         if not ret:
            print 'wystapil blad podczas tworzenia index katalogu: '+acatalog
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
         if os.path.exists(apath):
            print 'katalog juz istnieje w systemie plikow: '+apath
         else:
            print 'katalog nie istnieje w systemie plikow: '+apath
   def end_INDEXCREATE(self):
      pass
   def start_INDEXDELETE(self,attrs):
      self.ElementInfo(attrs.get('catalog',''))
      l=self.CheckAttrs(attrs,['catalog',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <INDEXDELETE>: %s'%str(l)
      acatalog=self.Profile.GetValue(attrs['catalog'])
      if self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='undo':
         print 'usuwam index katalog: '+acatalog
         ret=IISUtil.ISDeleteCatalog(acatalog)
         if not ret:
            print 'wystapil blad podczas usuwania index katalogu: '+acatalog
   def end_INDEXDELETE(self):
      pass
   def start_INDEXSCOPECREATE(self,attrs):
      self.ElementInfo(attrs.get('catalog',''))
      l=self.CheckAttrs(attrs,['catalog','path'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <INDEXSCOPECREATE>: %s'%str(l)
      acatalog=self.Profile.GetValue(attrs['catalog'])
      apath=self.Profile.GetValue(attrs['path'])
      if self.Profile.mode=='build':
         print 'nowy index scope katalog: '+acatalog
         ret=IISUtil.ISAddScope(acatalog,apath)
         if not ret:
            print 'wystapil blad podczas tworzenia index scope katalogu: '+acatalog
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
         if os.path.exists(apath):
            print 'katalog juz istnieje w systemie plikow: '+apath
         else:
            print 'katalog nie istnieje w systemie plikow: '+apath
      elif self.Profile.mode=='undo':
         print 'usuwam index scope katalog: '+acatalog
         ret=IISUtil.ISRemoveScope(acatalog,apath)
         if not ret:
            print 'wystapil blad podczas usuwania index scope katalogu: '+acatalog
   def end_INDEXSCOPECREATE(self):
      pass
   def start_IISVIRTUALDIRECTORYCREATE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','path','app','if','serviceid','host'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <IISVIRTUALDIRECTORYCREATE>: %s'%str(l)
      aname=self.Profile.GetValue(attrs['name'])
      apath=self.Profile.GetValue(attrs['path'])
      aapp=int(self.Profile.GetValue(attrs.get('app','1')))
      aserviceid=self.Profile.GetValue(attrs.get('serviceid','1'))
      ahost=self.Profile.GetValue(attrs.get('host','localhost'))
      if self.Profile.mode=='build':
         self.varif=1
         if attrs.get('if',''):
            self.varif=self.Profile.GetEval(attrs.get('if',''))
         if self.varif:
            print 'nowy iis virtual directory: '+aname
            ret=IISUtil.IISCreateVirtualDirectory(aname,apath,aapp,aserviceid,ahost)
            if not ret:
               print 'wystapil blad podczas tworzenia iis virtual directory: '+aname
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
         if os.path.exists(apath):
            print 'iis virtual directory juz istnieje w systemie plikow: '+apath
         else:
            print 'iis virtual directory nie istnieje w systemie plikow: '+apath
   def end_IISVIRTUALDIRECTORYCREATE(self):
      pass
   def start_IISVIRTUALDIRECTORYDELETE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','serviceid','host'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <IISVIRTUALDIRECTORYDELETE>: %s'%str(l)
      aname=self.Profile.GetValue(attrs['name'])
      aserviceid=self.Profile.GetValue(attrs.get('serviceid','1'))
      ahost=self.Profile.GetValue(attrs.get('host','localhost'))
      if self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='undo':
         print 'usuwam iis virtual directory: '+aname
         ret=IISUtil.IISDeleteVirtualDirectory(aname,aserviceid,host)
         if not ret:
            print 'wystapil blad podczas usuwania iis virtual directory: '+aname
   def end_IISVIRTUALDIRECTORYDELETE(self):
      pass
   def start_SQLEXEC(self,attrs):
      self.ElementInfo(attrs.get('connection',''))
      l=self.CheckAttrs(attrs,['connection','external','if','file'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <SQLEXEC>: %s'%str(l)
      self.ThisConnection=self.Profile.GetValue(attrs['connection'])
      self.TagData=''
      self.varif=1
      if attrs.get('if',''):
         self.varif=self.Profile.GetEval(attrs.get('if',''))
      aexternal=self.Profile.GetValue(attrs.get('external',''))
      self.SQLFile=self.Profile.GetValue(attrs.get('file',''))
      self.ExternalData=''
      if aexternal:
         self.ExternalData=self.Profile.ParseData(aname=aexternal)
   def end_SQLEXEC(self):
      if self.Profile.mode in ['build','undo']:
         if self.varif:
            print 'uruchamiam skrypt SQL'
            asql=self.ExternalData+self.Profile.GetValue(self.TagData)
            if self.SQLFile:
               fin=ICORUtil.OpenText(self.SQLFile,'r')
               try:
                  asql=asql+'\n\n'+fin.read()
               finally:
                  fin.close()
            SQLRun.ExecuteGoSplitSQLCommand(self.ThisConnection,asql,aprint=1,acominitialize=0)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def start_SECURITYPROFILE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <SECURITYPROFILE>: %s'%str(l)
      aname=self.Profile.GetValue(attrs['name'])
      if self.Profile.mode=='build':
         self.secprofile=ICORSecurity.ICORSecurityProfile()
         ret=self.secprofile.SetByProfileName(aname)
         if not ret:
            self.secprofile.AddProfile(aname)
            print 'nowy profil bezpieczenstwa: %s'%aname
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_SECURITYPROFILE(self):
      pass
   def start_SECURITYITEMGROUP(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','accesslevel','var','category','kind'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <SECURITYITEMGROUP>: %s'%str(l)
      if self.Profile.mode=='build':
         self.groupname=self.Profile.GetValue(attrs['name'])
         self.securityvar=attrs.get('var','')
         self.groupcategory=attrs.get('category','')
         self.groupkind=attrs.get('kind','')
         self.groupaccesslevel=int(self.Profile.GetEval(attrs.get('accesslevel','0')))
         self.basegroups=[]
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_SECURITYITEMGROUP(self):
      if self.Profile.mode=='build':
         if not self.basegroups:
            self.basegroups.append(self.groupname)
         goid=self.secprofile.UpdateItemGroup(self.groupname,self.groupaccesslevel,self.basegroups,acategory=self.groupcategory,akind=self.groupkind)
         if self.securityvar:
            self.Profile[self.securityvar]=str(goid)
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
#         self.secprofile.RemoveItemGroup(self.groupname)
   def start_SECURITYBASEGROUP(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      if self.Profile.mode=='build':
         l=self.CheckAttrs(attrs,['name',])
         if l:
            self.IsGood=0
            print 'nieznane atrybuty w tagu <SECURITYBASEGROUP>: %s'%str(l)
         aname=self.Profile.GetValue(attrs.get('name',''))
         self.basegroups.append(aname)
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_SECURITYBASEGROUP(self):
      pass
   def start_SECURITYUSERGROUP(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','accesslevel','var','category','kind'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <SECURITYUSERGROUP>: %s'%str(l)
      if self.Profile.mode=='build':
         self.groupname=self.Profile.GetValue(attrs['name'])
         self.groupcategory=attrs.get('category','')
         self.groupkind=attrs.get('kind','')
         self.securityvar=attrs.get('var','')
         self.groupaccesslevel=int(self.Profile.GetEval(attrs.get('accesslevel','0')))
         self.basegroups=[]
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_SECURITYUSERGROUP(self):
      if self.Profile.mode=='build':
         if not self.basegroups:
            self.basegroups.append(self.groupname)
         goid=self.secprofile.UpdateUserGroup(self.groupname,self.groupaccesslevel,self.basegroups,acategory=self.groupcategory,akind=self.groupkind)
         if self.securityvar:
            self.Profile[self.securityvar]=str(goid)
      elif self.Profile.mode=='undo':
         pass
#         self.secprofile.RemoveItemGroup(self.groupname)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def start_OIDRANGE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <OIDRANGE>: %s'%str(l)
      aname=self.Profile.GetValue(attrs.get('name',''))
      if self.Profile.mode=='build':
         self.secprofile.UpdateOIDRange(aname)
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_OIDRANGE(self):
      pass
   def start_UIDRANGE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <UIDRANGE>: %s'%str(l)
      aname=self.Profile.GetValue(attrs.get('name',''))
      if self.Profile.mode=='build':
         self.secprofile.UpdateUIDRange(aname)
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_UIDRANGE(self):
      pass
   def start_USER(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','password','firstname','lastname','email','var','uid','hash','oidranges','keepoldpassword'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <USER>: %s'%str(l)
      self.username=self.Profile.GetValue(attrs.get('name',''))
      self.userpassword=self.Profile.GetValue(attrs.get('password',''))
      self.userfirstname=self.Profile.GetValue(attrs.get('firstname',''))
      self.userlastname=self.Profile.GetValue(attrs.get('lastname',''))
      self.useremail=self.Profile.GetValue(attrs.get('email',''))
      self.uservar=self.Profile.GetValue(attrs.get('var',''))
      self.useruid=int(self.Profile.GetValue(attrs.get('uid','-1')))
      self.userhash=int(self.Profile.GetValue(attrs.get('hash','0')))
      self.useroidranges=string.split(self.Profile.GetValue(attrs.get('oidranges','')),',')
      self.userkeepoldpassword=int(self.Profile.GetValue(attrs.get('keepoldpassword','0')))
      if not self.userpassword:
         self.userpassword=self.username
      self.usergroups=[]
      if self.Profile.mode=='build':
         pass
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_USER(self):
      if self.Profile.mode=='build':
         agroups=ICORSecurity.GetStringAsAccessLevelRefs(self.usergroups,self.secprofile.UserGroupClass)
         ret=self.secprofile.AddUser(self.username,self.userpassword,agroups.AsString(),self.userfirstname,self.userlastname,self.useremail,self.useruid,self.userhash,self.useroidranges,self.userkeepoldpassword)
         if not ret:
            self.IsGood=0
            self.Profile.IsGood=self.IsGood
         if self.uservar:
            auid=self.secprofile.UserClass.UserName.Identifiers(self.username)
            if auid>=0:
               self.Profile[self.uservar]=str(auid)
            else:
               self.IsGood=0
               self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def start_USERGROUP(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <USERGROUP>: %s'%str(l)
      aname=self.Profile.GetValue(attrs.get('name',''))
      if self.Profile.mode=='build':
         self.usergroups.append(aname)
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_USERGROUP(self):
      pass
   def start_IMPERSONATE(self,attrs):
      self.ElementInfo(attrs.get('user',''))
      l=self.CheckAttrs(attrs,['user',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <IMPERSONATE>: %s'%str(l)
      if self.Profile.mode=='build':
         auid=self.Profile.GetEval(attrs.get('user',''))
         if auid>=0:
            self.Profile.Impersonate(auid)
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_IMPERSONATE(self):
      pass
   def start_REVERTTOSELF(self,attrs):
      self.ElementInfo()
      if self.Profile.mode=='build':
         self.Profile.RevertToSelf()
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_REVERTTOSELF(self):
      pass
   def start_OBJECT(self,attrs):
      self.ElementInfo(attrs.get('class',''))
      l=self.CheckAttrs(attrs,['class','oid','fieldname','fieldvalue','minoid','var','isnewobject','check'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <OBJECT>: %s'%str(l)
      sclass=self.Profile.GetValue(attrs['class'])
      self.objectclass=aICORDBEngine.Classes[sclass]
      if self.objectclass is None:
         self.IsGood=0
         print 'nieznana klasa w tagu <OBJECT>: %s'%sclass
         return
      if self.Profile.mode=='build':
         UID=self.Profile.GetUID()
         aoid=-1
         print 'obiekt w klasie: '+sclass
         soid=attrs.get('oid','')
         if soid:
            soid=self.Profile.GetEval(soid)
         if soid:
            aoid=int(soid)
         elif attrs.get('fieldname','') and attrs.get('fieldvalue',''):
            afield=self.objectclass.FieldsByName(attrs['fieldname'])
            if afield is None:
               self.IsGood=0
               print 'nieznane pole w tagu <OBJECT>: %s'%attrs['fieldname']
               return
            afieldvalue=self.Profile.GetValue(attrs['fieldvalue'])
            aoid=afield.Identifiers(afieldvalue)
         if attrs.get('minoid','') and attrs.get('fieldname','') and aoid<0:
            aoid=int(self.Profile.GetEval(attrs['minoid']))
            afield=self.objectclass.FieldsByName(attrs['fieldname'])
            if afield is None:
               self.IsGood=0
               print 'nieznane pole w tagu <OBJECT>: %s'%attrs['fieldname']
               return
            while 1:
               avalue=afield[aoid]
               if not avalue:
                  break
               aoid=aoid+1
         if aoid<0 and not attrs.get('check',''):
            aoid=self.objectclass.AddObject()
            if attrs.get('isnewobject',''):
               self.Profile[attrs['isnewobject']]='1'
         if attrs.get('var',''):
            self.Profile[attrs['var']]=str(aoid)
         self.objectoid=aoid
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
      elif self.Profile.mode=='undo':
         aoid=-1
         soid=attrs.get('oid','')
         if soid:
            soid=self.Profile.GetEval(soid)
         if soid:
            aoid=int(soid)
         elif attrs.get('fieldname','') and attrs.get('fieldvalue',''):
            afield=self.objectclass.FieldsByName(attrs['fieldname'])
            if afield is None:
               self.IsGood=0
               print 'nieznane pole w tagu <OBJECT>: %s'%attrs['fieldname']
               return
            afieldvalue=self.Profile.GetValue(attrs['fieldvalue'])
            aoid=afield.Identifiers(afieldvalue)
         if attrs.get('minoid','') and attrs.get('fieldname','') and aoid<0:
            aoid=int(self.Profile.GetEval(attrs['minoid']))
            afield=self.objectclass.FieldsByName(attrs['fieldname'])
            if afield is None:
               self.IsGood=0
               print 'nieznane pole w tagu <OBJECT>: %s'%attrs['fieldname']
               return
            while 1:
               avalue=afield[aoid]
               if not avalue:
                  break
               aoid=aoid+1
         if aoid<0 and attrs.get('isnewobject',''):
            self.Profile[attrs['isnewobject']]='1'
         if aoid>=0 and attrs.get('var',''):
            self.Profile[attrs['var']]=str(aoid)
         self.objectoid=aoid
   def end_OBJECT(self):
      pass
   def start_FIELDVALUE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','value','mode','list','external','if','before'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <FIELDVALUE>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         self.fieldname=self.Profile.GetValue(attrs['name'])
         self.fieldmode=self.Profile.GetValue(attrs.get('mode',''))
         self.fieldlist=self.Profile.GetValue(attrs.get('list',''))
         self.TagData=''
         self.varif=1
         if attrs.get('if',''):
            self.varif=self.Profile.GetEval(attrs.get('if',''))
         self.fieldbefore=-1
         if attrs.get('before',''):
            self.fieldbefore=self.Profile.GetEval(attrs.get('before',''))
         aexternal=self.Profile.GetValue(attrs.get('external',''))
         self.ExternalData=''
         if aexternal:
            self.ExternalData=self.Profile.ParseData(aname=aexternal)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_FIELDVALUE(self):
      if self.Profile.mode in ['build','undo']:
         if not self.varif:
            return
         UID=self.Profile.GetUID()
         afield=self.objectclass.FieldsByName(self.fieldname)
         if afield.FieldTID<MAX_ICOR_SYSTEM_TYPE:
            avalue=self.ExternalData+self.Profile.GetValue(self.TagData)
            afield[self.objectoid]=avalue
         else:
            avalue=self.Profile.GetEval(self.TagData,alist=1,acid=afield.FieldTID) #self.ExternalData ???
            if self.fieldmode=='update':
               abefore=None
               aremoveexisting=0
               if self.fieldbefore>=0:
                  abefore=[self.fieldbefore,afield.FieldTID]
                  aremoveexisting=1
               afield.AddRefs(self.objectoid,avalue,ainsertifnotexists=1,aremoveexisting=aremoveexisting,ainsertbefore=abefore)
            else:
               afield[self.objectoid]=avalue
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def start_FIELDVALUEREPLACE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','valuefrom','valueto','if'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <FIELDVALUEREPLACE>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         self.fieldname=self.Profile.GetValue(attrs['name'])
         self.fieldvaluefrom=self.Profile.GetValue(attrs['valuefrom'])
         self.fieldvalueto=self.Profile.GetValue(attrs['valueto'])
         self.TagData=''
         self.varif=1
         if attrs.get('if',''):
            self.varif=self.Profile.GetEval(attrs.get('if',''))
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_FIELDVALUEREPLACE(self):
      if self.Profile.mode in ['build','undo']:
         if not self.varif:
            return
         UID=self.Profile.GetUID()
         afield=self.objectclass.FieldsByName(self.fieldname)
         avalue=afield[self.objectoid]
         afield[self.objectoid]=string.replace(avalue,self.fieldvaluefrom,self.fieldvalueto)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def start_FIELDVALUESEARCH(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','reffield','reffieldvalue','var'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <FIELDVALUESEARCH>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         afieldname=self.Profile.GetValue(attrs['name'])
         afield=self.objectclass.FieldsByName(afieldname)
         arefs=afield.GetRefList(self.objectoid)
         arfieldname=self.Profile.GetValue(attrs.get('reffield',''))
         arvalue=self.Profile.GetValue(attrs.get('reffieldvalue',''))
         aasoidsearch=0
         if arfieldname:
            rfield=afield.ClassOfType.FieldsByName(arfieldname)
            if not rfield.ClassOfType is None:
               aasoidsearch=1
               arvalue=int(arvalue)
         apos,afind=arefs.FindRefByValue(arfieldname,arvalue,aasoidsearch=aasoidsearch)
         if afind:
            aoid=arefs.refs[apos][0]
            if attrs.get('var',''):
               self.Profile[attrs['var']]=str(aoid)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_FIELDVALUESEARCH(self):
      pass
   def start_GETFIELDVALUE(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','var'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <FIELDGETVALUE>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         afieldname=self.Profile.GetValue(attrs['name'])
         afield=self.objectclass.FieldsByName(afieldname)
         avalue=''
         if self.objectclass.ObjectExists(self.objectoid):
            avalue=afield[self.objectoid]
         if attrs.get('var',''):
            self.Profile[attrs['var']]=avalue
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_GETFIELDVALUE(self):
      pass
   def start_METHODEXEC(self,attrs):
      self.ElementInfo(attrs['method'])
      l=self.CheckAttrs(attrs,['class','method','oid','fieldname','value','uid','var'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <METHODEXEC>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         mname=self.Profile.GetValue(attrs['class'])
         mname=string.replace(mname,'\\','_')
         mname=string.replace(mname,'/','_')
         mclass=aICORDBEngine.Classes[mname]
         amethod=self.Profile.GetValue(attrs['method'])
         mpath=mname+'_'+amethod
         mpath=mpath.replace('\\','_')
         mpath=mpath.replace('/','_')
         pagemethod=__import__(mpath)
         pageevent=getattr(pagemethod,'ICORMain')
         aoid=int(self.Profile.GetValue(attrs.get('oid','-1')))
         auid=int(self.Profile.GetValue(attrs.get('uid','0')))
         afieldname=self.Profile.GetValue(attrs.get('fieldname',''))
         avalue=self.Profile.GetValue(attrs.get('value',''))
         ret=''
         if not pageevent is None:
            ret=apply(pageevent,(mclass.CID,afieldname,aoid,avalue,auid))
         if attrs.get('var',''):
            if ret is None:
               ret=''
            if not isinstance(ret,types.StringTypes):
               ret=str(ret)
            self.Profile[attrs['var']]=ret
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_METHODEXEC(self):
      pass
   def start_DELETEREFS(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name','objectdelete'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <DELETEREFS>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         self.fieldname=self.Profile.GetValue(attrs['name'])
         self.objectdelete=self.Profile.GetEval(attrs.get('objectdelete','0'))
         self.TagData=''
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_DELETEREFS(self):
      if self.Profile.mode in ['build','undo']:
         UID=self.Profile.GetUID()
         afield=self.objectclass.FieldsByName(self.fieldname)
         avalue=self.Profile.GetEval(self.TagData,alist=1,acid=afield.FieldTID) #self.ExternalData ???
         if avalue:
            afield.DeleteRefs(self.objectoid,avalue,aobjectdelete=self.objectdelete)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def start_EXEC(self,attrs):
      self.ElementInfo()
      l=self.CheckAttrs(attrs,['external','if','cmdsave','disablerun','nowait','batch'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <EXEC>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         self.TagData=''
         self.varif=1
         if attrs.get('if',''):
            self.varif=self.Profile.GetEval(attrs.get('if',''))
         aexternal=self.Profile.GetValue(attrs.get('external',''))
         self.ExecDisableRun=self.Profile.GetValue(attrs.get('disablerun','0'))
         self.ExecCMDSave=self.Profile.GetValue(attrs.get('cmdsave',''))
         self.EXECNoWait=self.Profile.GetValue(attrs.get('nowait','0'))
         self.EXECBatch=self.Profile.GetValue(attrs.get('batch','0'))
         self.ExternalData=''
         if aexternal:
            self.ExternalData=self.Profile.ParseData(aname=aexternal)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_EXEC(self):
      if self.Profile.mode in ['build','undo']:
         if not self.varif:
            return
         acmd=self.ExternalData+self.Profile.GetValue(self.TagData)
         if acmd:
            if self.ExecCMDSave:
               fout=ICORUtil.OpenText(self.ExecCMDSave,'w')
               try:
                  fout.write(acmd)
               finally:
                  fout.close()
            if self.ExecDisableRun=='0':
               if self.EXECBatch=='1':
                  if self.EXECNoWait=='1':
                     print 'wykonuje batch asynchronicznie:',self.ExecCMDSave
                     try:
                        ret=os.spawnl(os.P_NOWAIT,self.ExecCMDSave)
                     except:
                        print 'wystapil blad podczas uruchamiania batcha asynchronicznie:',self.ExecCMDSave
                        import traceback
                        traceback.print_exc()
                  else:
                     print 'wykonuje batch synchronicznie:',acmd
                     try:
                        fin,fout,ferr=os.popen3(self.ExecCMDSave,'t')
                        l=fout.readline()
                        while l:
                           print l[:-1]
                           l=fout.readline()
                        l=ferr.readline()
                        while l:
                           print l[:-1]
                           l=ferr.readline()
                     except:
                        print 'wystapil blad podczas uruchamiania batcha synchronicznie:',acmd
               else:
                  acmds=string.split(acmd,'\n')
                  for acmd in acmds:
                     acmd=string.strip(acmd)
                     if not acmd:
                        continue
                     if self.EXECNoWait=='1':
                        print 'wykonuje komende asynchronicznie:',acmd
                        try:
                           ret=os.spawnl(os.P_NOWAIT,acmd) #SK dokonczyc parametry, wywala babol!!!
                        except:
                           print 'wystapil blad podczas uruchamiania komendy asynchronicznie:',acmd
                           import traceback
                           traceback.print_exc()
                     else:
                        print 'wykonuje komende synchronicznie:',acmd
                        try:
                           fin,fout,ferr=os.popen3(acmd,'t')
                           l=fout.readline()
                           while l:
                              print l[:-1]
                              l=fout.readline()
                           l=ferr.readline()
                           while l:
                              print l[:-1]
                              l=ferr.readline()
                        except:
                           print 'wystapil blad podczas uruchamiania komendy synchronicznie:',acmd

      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def start_OBJECTDELETE(self,attrs):
      self.ElementInfo()
   def end_OBJECTDELETE(self):
      pass
   def DeleteObjectsInRange(self,aclass,aoidfrom,aoidto):
      l=aclass.GetObjectsInRange(aoidfrom,aoidto)
      if l:
         print 'DELETEOBJECTS:',aclass.ClassPath,aclass.NameOfClass,aoidfrom,aoidto,l
         lfields=aclass.GetReferencingFields()
         self.classreffields.extend(lfields)
         for aoid in l:
            aclass.DeleteObject(aoid)
   def start_DELETEOBJECTSINRANGE(self,attrs):
      self.ElementInfo(attrs.get('class',''))
      l=self.CheckAttrs(attrs,['class','oidfrom','oidto','oid'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <DELETEOBJECTSINRANGE>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         sclass=self.Profile.GetValue(attrs['class'])
         soid=attrs.get('oid','')
         aoid=-1
         if soid:
            soid=self.Profile.GetEval(soid)
         if soid:
            aoid=int(soid)
         if aoid>=0:
            rclass=aICORDBEngine.Classes['CLASSES_System_Security_OIDRange']
            self.oidfrom=rclass.IDMin.ValuesAsInt(aoid)
            self.oidto=1+rclass.IDMax.ValuesAsInt(aoid)
         elif attrs.get('oidfrom','') and attrs.get('oidto',''):
            self.oidfrom=self.Profile.GetEval(attrs.get('oidfrom',''))
            self.oidto=self.Profile.GetEval(attrs.get('oidto',''))
         else:
            print 'brak zakresu OID w <DELETEOBJECTSINRANGE>: %s'%str(l)
            return
         self.objectclass=aICORDBEngine.Classes[sclass]
         self.classreffields=[]
         self.objectclass.ForEachDerivedClass(self.DeleteObjectsInRange,self.oidfrom,self.oidto)
         if 0:
            for afield in self.classreffields:
               aoid=afield.GetFirstValueID()
               while aoid>=0:
                  arefs=afield.GetRefList(aoid)
                  w=arefs.DelRefsInRange(self.oidfrom,self.oidto)
                  if w:
                     print '   DELREFS:',aoid,afield.ClassItem.ClassPath,'|',afield.Name
                     arefs.Store()
                  aoid=afield.GetNextValueID(aoid)
      elif self.Profile.mode=='undo':
         self.Profile.IsGood=self.IsGood
   def end_DELETEOBJECTSINRANGE(self):
      pass
   def start_EXTERNAL(self,attrs):
      self.ElementInfo(attrs.get('name',''))
      l=self.CheckAttrs(attrs,['name',])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <EXTERNAL>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         aname=self.Profile.GetValue(attrs['name'])
         self.Profile.ParseData(aname=aname)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_EXTERNAL(self):
      pass
   def start_COPYTREE(self,attrs):
      self.ElementInfo(attrs.get('src','')+' -> '+attrs.get('dst',''))
      l=self.CheckAttrs(attrs,['src','dst'])
      if l:
         self.IsGood=0
         print 'nieznane atrybuty w tagu <COPYTREE>: %s'%str(l)
      if self.Profile.mode in ['build','undo']:
         asrc=self.Profile.GetValue(attrs['src'])
         adst=self.Profile.GetValue(attrs['dst'])
         ICORUtil.copytree(asrc,adst,asilent=0)
      elif self.Profile.mode=='check':
         self.Profile.IsGood=self.IsGood
   def end_COPYTREE(self):
      pass

class ProfileParser:
   def __init__(self,auid,amode='build'):
      self.UIDs=[auid,]
      self.mode=amode
      self.IsGood=1
      self.Variables={
         'ICOR':os.path.normpath(aICORDBEngine.Variables['_ICOR_BASE_DIR']),
      }
      self.InputVariables=[]
      self._vardict={}
      self.FileItemsClass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Meta_FileItem']
   def _GetVarValue(self,m):
      sn=s=m.group(1)
      if not s:
         return '%'
      if self._vardict.has_key(sn):
         return ''
      self._vardict[sn]=1
      if not self.Variables.has_key(s):     
         s=self.GetValue(s)
      ret=re.sub('%(.*?)%',self._GetVarValue,self.Variables.get(s,''))
      del self._vardict[sn]
      return ret
   def __getitem__(self,name):
      if self._vardict.has_key(name):
         return ''
      self._vardict[name]=1
      avalue=re.sub('%(.*?)%',self._GetVarValue,self.Variables.get(name,''))
      del self._vardict[name]
      return avalue
   def __setitem__(self,name,value):
      self.Variables[name]=value
   def GetValue(self,avalue):
      if self._vardict.has_key(avalue):
         return ''
      self._vardict[avalue]=1
      ret=re.sub('%(.*?)%',self._GetVarValue,avalue)
      del self._vardict[avalue]
      return ret
   def GetEval(self,avalue,alist=0,acid=-1):
      ovalue=avalue
      avalue=self.GetValue(avalue)
      if avalue:
         avalue=eval(avalue)
      elif ovalue:
         print 'Puste rozwiniecie funkcji eval dla ciagu:',ovalue
      if alist:
         if type(avalue)==type(()):
            avalue=list(avalue)
         elif type(avalue)!=type([]):
            avalue=[avalue,]
         if acid>=MAX_ICOR_SYSTEM_TYPE:
            l=[]
            for aoid in avalue:
               if type(aoid)==type(1) and aoid>=0:
                  l.append([aoid,acid])
               else:
                  print 'Nieprawidlowy OID:',aoid
            avalue=l
      return avalue
   def GetUID(self):
      if not self.UIDs:
         return 0
      return self.UIDs[len(self.UIDs)-1]
   def Impersonate(self,auid):
      self.UIDs.append(auid)
   def RevertToSelf(self):
      if self.UIDs:
         self.UIDs.pop()
   def ParseParameters(self,adata):
      vparser=VariablesParser()
      vparser.Parse(self,adata)
   def ParseData(self,adata='',aname='',adump=0):
      if aname:
         aoid=self.FileItemsClass.Name.Identifiers(aname)
         if aoid<0:
            print '*** Nieznany plik:',aname,'***'
            return ''
         aobj=self.FileItemsClass[aoid]
         kobj=aobj.ItemKind
         if not kobj:
            print 'Plik:',aname,'nie posiada okreslonego typu'
            return
         akind=kobj.Nazwa
         if akind=='XML':
            vparser=DataParser()
            vparser.Parse(self,aobj.FileData)
         elif akind=='Text':
            return aobj.FileData
         elif akind=='PyHTML':
            UID=self.GetUID()
            arepldict={'Variables':self.Variables,'this':self,'UID':UID}
            atext=ICORUtil.GetTextAsHTMLText(aobj.FileData,repldict=arepldict,aengine=aICORDBEngine,aashtmlstring=0,aseparator='$',ascriptname='<PyHTML>')
            return atext
         else:
            print 'Plik:',aname,'posiada nie znany typ:',akind
            return
      else:        
         vparser=DataParser()
         vparser.Parse(self,adata)
      if adump:
         self.Dump()
      return ''
   def Dump(self):
      print '*** variables ***'
      l=self.Variables.keys()
      l.sort()
      for s in l:
         print '  %s="%s"'%(s,self[s])






