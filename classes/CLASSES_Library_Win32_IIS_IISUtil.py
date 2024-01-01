# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

import win32api
from win32com.client import GetObject,gencache,Dispatch
import win32con
import os
import string

import CLASSES_Library_ICORBase_External_MLog as MLog

gencache.EnsureModule('{565783C6-CB41-11D1-8B02-00600806D9B6}', win32con.LANG_NEUTRAL, 1, 1) # Microsoft WMI Scripting Library
if 0:
   gencache.EnsureModule('{E503D000-5C7F-11D2-8B74-00104B2AFB41}', win32con.LANG_NEUTRAL, 1, 0) # WMI ADSI Extension Type Library
gencache.EnsureModule('{5C65924B-E236-11D2-8899-00104B2AFB46}', win32con.LANG_NEUTRAL, 1, 0) # WMICntl Type Library

def IISCreateVirtualDirectory(strVirtualDirectoryName,strVirtualDirectoryPath,appCreate=1,aserviceid='1',ahost='localhost'):
#   pythoncom.CoInitialize()
   try:
      MachineName=win32api.GetComputerName()
      strOwner="IUSR_"+MachineName
      try:
         objVirtualDirectory=GetObject(r"IIS://"+ahost+"/W3SVC/"+aserviceid+r"/Root/"+strVirtualDirectoryName)
         return 1
      except:
         pass
      try:
         objIIS=GetObject(r"IIS://"+ahost+"/W3SVC/"+aserviceid+r"/Root")
         if not os.path.exists(strVirtualDirectoryPath):
            os.makedirs(strVirtualDirectoryPath)
         objVirtualDirectory=objIIS.Create('IISWebVirtualDir',strVirtualDirectoryName)
         avpath=string.replace(strVirtualDirectoryPath,'/','\\')
         print '*** PATH ***',avpath
         objVirtualDirectory.AccessRead=1
         objVirtualDirectory.AccessWrite=0
         objVirtualDirectory.AccessExecute=0
         objVirtualDirectory.DontLog=0
         objVirtualDirectory.ContentIndexed=0
         objVirtualDirectory.EnableDirBrowsing=0
         objVirtualDirectory.EnableDefaultDoc=1
         objVirtualDirectory.DefaultDoc='default.htm,default.asp'
         objVirtualDirectory.AuthAnonymous=1
         objVirtualDirectory.AnonymousUserName=strOwner
         objVirtualDirectory.AnonymousPasswordSync=1
         objVirtualDirectory.Path=avpath
         if appCreate:
            objVirtualDirectory.AppFriendlyName=strVirtualDirectoryName
            objVirtualDirectory.AccessExecute=1
            objVirtualDirectory.AccessScript=1
            objVirtualDirectory.AppCreate(0)
            objVirtualDirectory.AppIsolated=2
            objVirtualDirectory.AspScriptTimeout=900
            objVirtualDirectory.AspSessionTimeout=90
            objVirtualDirectory.AppAllowClientDebug=0
            objVirtualDirectory.AppAllowDebugging=0
         objVirtualDirectory.SetInfo()
      except:
         MLog.LogException()
         return 0
#      strACLCommand='cmd /c echo y| CACLS '+strVirtualDirectoryPath+' /g '+strOwner+':C'
   finally:
      pass
#      pythoncom.CoUninitialize()
   return 1

def IISDeleteVirtualDirectory(strVirtualDirectoryName,aserviceid='1',ahost='localhost'):
#   pythoncom.CoInitialize()
   try:
      try:
         objIIS=GetObject(r'IIS://'+ahost+"/W3SVC/"+aserviceid+r"/Root")
         objIIS.Delete('IISWebVirtualDir',strVirtualDirectoryName)
      except:
#         MLog.LogException()
         return 0
   finally:
      pass
#      pythoncom.CoUninitialize()
   return 1

def ISAddCatalog(acatalog,adir,ascopes=''):
#   pythoncom.CoInitialize()
   try:
      objISAdmin=Dispatch('Microsoft.ISAdm')
      try:
         objISAdmin.AddCatalog(acatalog,adir)
         if objISAdmin.IsRunning:
            objISAdmin.Stop()
         objISAdmin.Start()
         if ascopes:
            myCat=objISAdmin.GetCatalogByName(acatalog)
            if type(ascopes)==type([]):
               for ascope in ascopes:
                  ScopeAdmin=myCat.AddScope(string.replace(ascope,'/','\\'),0)
            else:
               ScopeAdmin=myCat.AddScope(string.replace(ascopes,'/','\\'),0)
      except:
#         MLog.LogException()
         return 0
   finally:
      pass
#      pythoncom.CoUninitialize()
   return 1

def ISAddScope(acatalog,ascopes=''):
#   pythoncom.CoInitialize()
   try:
      objISAdmin=Dispatch('Microsoft.ISAdm')
      try:
         if objISAdmin.IsRunning:
            objISAdmin.Stop()
         objISAdmin.Start()
         if ascopes:
            myCat=objISAdmin.GetCatalogByName(acatalog)
            if type(ascopes)==type([]):
               for ascope in ascopes:
                  ScopeAdmin=myCat.AddScope(string.replace(ascope,'/','\\'),0)
            else:
               ScopeAdmin=myCat.AddScope(string.replace(ascopes,'/','\\'),0)
      except:
#         MLog.LogException()
         return 0
   finally:
      pass
#      pythoncom.CoUninitialize()
   return 1

def ISRemoveScope(acatalog,ascopes=''):
#   pythoncom.CoInitialize()
   try:
      objISAdmin=Dispatch('Microsoft.ISAdm')
      try:
         if objISAdmin.IsRunning:
            objISAdmin.Stop()
         objISAdmin.Start()
         if ascopes:
            myCat=objISAdmin.GetCatalogByName(acatalog)
            if type(ascopes)==type([]):
               for ascope in ascopes:
                  try:
                     ScopeAdmin=myCat.RemoveScope(string.replace(ascope,'/','\\'))
                  except:
                     MLog.LogException()
                     pass
            else:
               try:
                  ScopeAdmin=myCat.RemoveScope(string.replace(ascopes,'/','\\'))
               except:
                  MLog.LogException()
                  pass
      except:
         MLog.LogException()
         return 0
   finally:
      pass
#      pythoncom.CoUninitialize()
   return 1

def ISDeleteCatalog(acatalog):
#   pythoncom.CoInitialize()
   try:
      objISAdmin=Dispatch('Microsoft.ISAdm')
      try:
         if objISAdmin.IsRunning:
            objISAdmin.Stop()
         objISAdmin.RemoveCatalog(acatalog,1)
         objISAdmin.Start()
      except:
#         MLog.LogException()
         return 0
      try:
         if not objISAdmin.IsRunning:
            objISAdmin.Start()
      except:
         pass
   finally:
      pass
#      pythoncom.CoUninitialize()
   return 1






