# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_Services_DNS_SimpleCache_SimpleDNSCache import HostByAddressCache
import sys
import os
import re
import string
import types

revoke_c_ip_list = [
   '195.117.158.24',
   ]

class LogBuilder:
   def __init__(self,afoutname,abasedir,aregexp=''):
      self.OutputFile=afoutname
      self.BaseDir=abasedir
      if aregexp:
         self.Pattern=re.compile(aregexp,re.I)
      else:
         self.Pattern=None
      self.Fields=['date','time','c-ip','c-host','cs-username','s-sitename',
         's-computername','s-ip','cs-method','cs-uri-stem','cs-uri-query',
         'sc-status','sc-win32-status','sc-bytes','cs-bytes','time-taken',
         's-port','cs-version','cs(User-Agent)','cs(Cookie)','cs(Referer)',
         ]
      self.FieldsMap={}
      self.HostCache=HostByAddressCache()
   def Process(self):
      if isinstance(self.OutputFile,types.StringTypes):
         self.file=open(self.OutputFile,'w')
      else:
         self.file=self.OutputFile
      try:
         self.file.write('<table class=objectsviewtable>')
         self.file.write('<caption class=objectsviewcaption>%s</caption>' % (self.BaseDir,))
         for afname in self.Fields:
            self.file.write('<th class=objectsviewheader>'+afname+'</th>')
         os.path.walk(self.BaseDir,self.FileFunc,0)
         self.file.write('</table>')
      finally:
         if isinstance(self.OutputFile,types.StringTypes):
            self.file.close()
   def FileFunc(self,arg,d,files):
      files.sort()
      for aname in files:
         if not os.path.isdir(d+'/'+aname):
            if self.Pattern:
               if self.Pattern.search(aname):
#                  print aname
                  self.ProcessFile(aname)
   def ProcessFile(self,fname):
      fin=open(self.BaseDir+'/'+fname,'r')
      try:
         l=fin.readline()
         while l:
            self.ProcessLine(l[:-1])
            l=fin.readline()
      finally:
         fin.close()
   def ProcessLine(self,aline):
      sl=string.split(aline,' ')
      if not sl:
         return
      if sl[0]=='#Fields:':
         self.FieldsMap={}
         for i in range(1,len(sl)):
            self.FieldsMap[sl[i]]=i
         return
      if sl[0]=='#Date:':
         self.Date=sl[1]
      if sl[0][0] in ['#',chr(0)]:
         return
      ret=[]
      for afield in self.Fields:
         if afield=='c-host':
            continue
         acol=self.FieldsMap.get(afield,0)
         if acol:
            ret.append(sl[acol-1])
            if afield=='c-ip':
               cip=sl[acol-1]
               if cip in revoke_c_ip_list:
                  return
               ret.append(self.HostCache[cip])
         else:
            if afield=='date':
               ret.append(self.Date)
            else:
                ret.append('-')
      self.file.write('<tr class=objectsviewrow>')
      for s in ret:
         self.file.write('<td class=objectsviewdataeven NOWRAP>'+s+'</td>')
      self.file.write('</tr>')

def OnWWWAction(aobj,amenu,file):
   if amenu.Action=='ObjectApplyMethods':
      abuilder=LogBuilder(file,aobj.LogBaseDirPath,aobj.LogFileMask)
      abuilder.Process()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]



