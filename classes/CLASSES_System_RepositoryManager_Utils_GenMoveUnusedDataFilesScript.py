# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import os
import string

class DirectoryWalker:
   def __init__(self):
      self.BaseDir=aICORDBEngine.Variables._ICOR_REPOSITORY_DIR
      self.IClass=aICORDBEngine.Classes['CLASSES_System_ICORClass']
      self.FClass=aICORDBEngine.Classes['CLASSES_System_ICORField']
   def Walk(self):
      os.path.walk(self.BaseDir+'/MIID',self.IFileFunc,0)
      os.path.walk(self.BaseDir+'/MIDD',self.FFileFunc,0)
   def IFileFunc(self,arg,d,files):
      if d in ['.','..']:
         return
      for aname in files:
         sl=string.split(aname,'.')
         aid=int(sl[0])
         if not self.IClass.ObjectExists(aid):
            print 'move',aname,'dd'
   def FFileFunc(self,arg,d,files):
      if d in ['.','..']:
         return
      for aname in files:
         sl=string.split(aname,'.')
         aid=int(sl[0])
         if not self.FClass.ObjectExists(aid):
            print 'move',aname,'dd'

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   awalker=DirectoryWalker()
   awalker.Walk()                     
   return

