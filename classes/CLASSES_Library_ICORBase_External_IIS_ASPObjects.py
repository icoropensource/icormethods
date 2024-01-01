# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import string
import re
from CLASSES_Library_ICORBase_External_MLog import Log,LogException
from CLASSES_Library_ICORBase_Interface_ICORUtil import URLString2NormalString

class ASPCollection:
   def __init__(self,aaspobject,aname,areadonly=0,awriteonly=0):
      self.aspobject=aaspobject
      self.name=aname
      self._ReadOnly=areadonly
      self._WriteOnly=awriteonly
      self.Refresh()
   def Refresh(self):
      reportstring=self.aspobject.communicator.GetCollection(self.aspobject.name,self.name)
      self.formdict={}
      if reportstring=='':
         return
      sl=string.split(reportstring,'&')
      for v in sl:
         i=string.find(v,'=')
         if i>=0:
            self.formdict[v[:i]]=URLString2NormalString(v[i+1:])
   def keys(self):
      ret=self.formdict.keys()
      ret.sort()
      return ret
   def __getattr__(self,name):
      if name in self.formdict.keys():
         return self.formdict[name]
   def __getitem__(self,name):
      if self._WriteOnly:
         return ''
      if name in self.formdict.keys():
         return self.formdict[name]
   def __setitem__(self,name,value):
      if self._ReadOnly:
         return
      self.SetValue(name,value)
   def SetValue(self,name,value):
      self.formdict[name]=value
      self.aspobject.SetCollectionItem(self.name,name,value)
   def AsString(self,adefpost=1):
      if adefpost:
         sep1,sep2='=','&'
      else:
         sep1,sep2=chr(254),chr(255)
      alist=[]
      for key,value in self.formdict.items():
         alist.append(key+sep1+value)
      return string.join(alist,sep2)
   def Dump(self,file=None):
      keys=self.formdict.keys()
      keys.sort()
      for akey in keys:
         print akey,'=',self.formdict[akey]

class ASPObject:
   def __init__(self,aname,acommunicator):
      self.name=aname
      self.communicator=acommunicator
   def CallMethod(self,amethod,avalue=''):
      return self.communicator.CallMethod(self.name,amethod,avalue)
   def GetProperty(self,aname):
      return self.communicator.GetProperty(self.name,aname)
   def SetProperty(self,aname,avalue):
      return self.communicator.SetProperty(self.name,aname,avalue)
   def GetCollection(self,aname,areadonly=0,awriteonly=0):
      ret=ASPCollection(self,aname,areadonly=areadonly,awriteonly=awriteonly)
      return ret
   def SetCollectionItem(self,cname,iname,ivalue):
      return self.communicator.SetCollectionItem(self.name,cname,iname,ivalue)

class Server(ASPObject):
   #Properties: 
   def __getattr__(self,aname):
      if aname=='ScriptTimeout':
         return int(self.GetProperty('SCRIPTTIMEOUT'))
   def __setattr__(self,aname,avalue):
      if aname=='ScriptTimeout':
         return self.SetProperty('SCRIPTTIMEOUT',str(avalue))
      self.__dict__[aname]=avalue
   #Methods:
   #def CreateObject(self): #todo
      #pass
   #def Execute(self): #todo
      #pass
   #def GetLastError(self): #todo
      #pass
   #def Transfer(self): #todo
      #pass
   def HTMLEncode(self,avalue):
      return self.CallMethod('HTMLENCODE',avalue)
   def MapPath(self,avalue):
      return self.CallMethod('MAPPATH',avalue)
   def URLEncode(self,avalue):
      return self.CallMethod('URLENCODE',avalue)

class Session(ASPObject):
   def __init__(self,aname,acommunicator):
      ASPObject.__init__(self,aname,acommunicator)
      self._Contents=None
   #Properties: 
   def __getattr__(self,aname):
      if aname=='CodePage':
         return int(self.GetProperty('CODEPAGE'))
      if aname=='LCID':
         return int(self.GetProperty('LCID'))
      if aname=='SessionID':
         return self.GetProperty('SESSIONID')
      if aname=='Timeout':
         return int(self.GetProperty('TIMEOUT'))
      if aname=='Contents':
         if self._Contents is None:
            self._Contents=self.GetCollection('CONTENTS')
         return self._Contents
   def __setattr__(self,aname,avalue):
      if aname=='CodePage':
         return self.SetProperty('CODEPAGE',str(avalue))
      if aname=='LCID':
         return self.SetProperty('LCID',str(avalue))
      if aname=='Timeout':
         return self.SetProperty('TIMEOUT',str(avalue))
      self.__dict__[aname]=avalue
   #Methods:
   #def Abandon(self): #todo
      #pass

class Application(ASPObject):
   def __init__(self,aname,acommunicator):
      ASPObject.__init__(self,aname,acommunicator)
      self._Contents=None
   #Properties: 
   def __getattr__(self,aname):
      if aname=='Contents':
         if self._Contents is None:
            self._Contents=self.GetCollection('CONTENTS')
         return self._Contents
   #methods
   def Lock(self):
      return self.CallMethod('LOCK')
   def Unlock(self):
      return self.CallMethod('UNLOCK')

class Request(ASPObject):
   def __init__(self,aname,acommunicator):
      ASPObject.__init__(self,aname,acommunicator)
      self._Form=None
      self._QueryString=None
      self._ServerVariables=None
      self._Cookies=None
   def __getattr__(self,aname):
      if aname=='Form':
         if self._Form is None:
            self._Form=self.GetCollection('FORM')
         return self._Form
      if aname=='QueryString':
         if self._QueryString is None:
            self._QueryString=self.GetCollection('QUERYSTRING')
         return self._QueryString
      if aname=='Cookies':
         if self._Cookies is None:
            self._Cookies=self.GetCollection('COOKIES',areadonly=1)
         return self._Cookies
      if aname=='ServerVariables':
         if self._ServerVariables is None:
            self._ServerVariables=self.GetCollection('SERVERVARIABLES')
         return self._ServerVariables
   #collections
#ClientCertificate
   #Properties:
#TotalBytes
   #Methods:
   #def BinaryRead(self): #todo
      #pass

class Response(ASPObject):
   def __init__(self,aname,acommunicator):
      ASPObject.__init__(self,aname,acommunicator)
      self._Cookies=None
   #Properties:
   def __getattr__(self,aname):
      if aname=='Buffer':
         return int(self.GetProperty('BUFFER'))
      if aname=='CacheControl':
         return self.GetProperty('CACHECONTROL')
      if aname=='Charset':
         return self.GetProperty('CHARSET')
      if aname=='ContentType':
         return self.GetProperty('CONTENTTYPE')
#      if aname=='ExpiresAbsolute':
#         return self.GetProperty('EXPIRESABSOLUTE') #???
      if aname=='IsClientConnected':
         return int(self.GetProperty('ISCLIENTCONNECTED')) #RO
      if aname=='Status':
         return self.GetProperty('STATUS')
      if aname=='Cookies':
         if self._Cookies is None:
            self._Cookies=self.GetCollection('COOKIES',awriteonly=1)
         return self._Cookies
   def __setattr__(self,aname,avalue):
      if aname=='Buffer':
         return self.SetProperty('BUFFER',str(avalue))
      if aname=='CacheControl':
         return self.SetProperty('CACHECONTROL',avalue)
      if aname=='Charset':
         return self.SetProperty('CHARSET',avalue)
      if aname=='ContentType':
         return self.SetProperty('CONTENTTYPE',avalue)
      if aname=='Expires':
         return self.SetProperty('EXPIRES',avalue)
      if aname=='ExpiresAbsolute':
         return self.SetProperty('EXPIRESABSOLUTE',avalue) #???
      if aname=='PICS':
         return self.SetProperty('PICS',avalue)
      if aname=='Status':
         return self.SetProperty('STATUS',avalue)
      self.__dict__[aname]=avalue
   #Methods: 
   def AddHeader(self,aname,avalue):
      return self.CallMethod('ADDHEADER',(aname,avalue))
   def AppendToLog(self,avalue):
      return self.CallMethod('APPENDTOLOG',avalue)
   def BinaryWrite(self,avalue):
      return self.CallMethod('BINARYWRITE',avalue)
   def Clear(self):
      return self.CallMethod('CLEAR','')
   def End(self):
      return self.CallMethod('END','')
   def Flush(self):
      return self.CallMethod('FLUSH','')
   def Redirect(self,avalue):
      return self.CallMethod('REDIRECT',avalue)
   def Write(self,avalue):
      return self.CallMethod('WRITE',avalue)



