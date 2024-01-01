# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import sys
#sys.ICOR_SERVER='.'
import icorpipe
if 1:
   import CLASSES_Library_ICORBase_External_ICORldd
   icortop='c:/icor/python'
   for fname in [
      'DAV'
      ]:
      CLASSES_Library_ICORBase_External_ICORldd.installone('%s/%s.pyl' %(icortop,fname))

import urllib
import os
import stat

from DAV.constants import COLLECTION, OBJECT
from DAV.errors import *
from DAV.iface import *
from DAV.davcmd import copyone, copytree, moveone, movetree, delone, deltree
from DAV.davserver import DAVRequestHandler

class dataclassbase(dav_interface):
   BASEURI = None 
   UID = 0
   ROOTOID = 0
   def normpath(self,path):
      comps=filter(lambda x:len(x)>0,path.split("/"))
      if not len(comps):
         return '/'
      i = 0
      while i < len(comps):
         if comps[i] == '.':
            del comps[i]
         elif comps[i] == '..':
            if i==0:
               del comps[i]
            elif i > 0 and comps[i-1] not in ('', '..'):
               del comps[i-1:i+1]
               i = i - 1
         else:
            i = i + 1
      return '/%s' %"/".join(comps)

   def uri2local(self,uri,onlyloc=0):
      uri=urllib.unquote_plus(uri[len(self.BASEURI):])
      try:
         uuri = unicode(uri,'utf-8').encode('cp1250')
         uri = uuri
      except:
         pass
      uri=self.normpath(uri)
      if onlyloc:
         return uri
      rfs = ICORRFSItem(self.UID,self.ROOTOID)
      rfs = rfs.GetRelativeItem(uri,rfs)
      if rfs is None:
         raise DAV_NotFound
      return uri,rfs

   def local2uri(self,filename):
      uri = unicode(filename[1:],'cp1250').encode('utf-8')
      uri=self.BASEURI+urllib.quote(uri)
      return uri

   def newitem(self,uri):
      loc = self.uri2local(uri,1)
      fname = loc.split('/')[1:]
      loc = '/'.join(fname[:-1])
      rfs = ICORRFSItem(self.UID,self.ROOTOID)
      rfs = rfs.GetRelativeItem('/'+loc,rfs)
      rfs.AddItem(fname[-1])
      return self.uri2local(uri)[1]

   def newcollection(self,uri):
      loc = self.uri2local(uri,1)
      fname = loc.split('/')[1:]
      loc = '/'.join(fname[:-1])
      rfs = ICORRFSItem(self.UID,self.ROOTOID)
      rfs = rfs.GetRelativeItem('/'+loc,rfs)
      rfs.AddCollection(fname[-1])
      return self.uri2local(uri)[1]

class dataclass(dataclassbase):
   def get_childs(self,uri):
      fileloc,rfs = self.uri2local(uri)
      if fileloc[-1]!='/':
         fileloc='%s/' %fileloc
      filelist=[]
      if rfs.IsCollection():
         files=rfs.GetSubItems()
         for file in files:
            newloc='%s%s' %(fileloc,file)
            newloc=self.local2uri(newloc)
            filelist.append(newloc)
      return filelist

   def put(self,uri,data,content_type=None):
      try:
         rfs = self.uri2local(uri)[1]
      except DAV_NotFound:
         rfs = self.newitem(uri)
      if not rfs.IsCollection():
         try:
            open(rfs.Location,"wb").write(data)
            return None
         except:
            raise DAV_Error(424)
      raise DAV_NotFound

   def get_data(self,uri):
      rfs = self.uri2local(uri)[1]
      if not rfs.IsCollection():
         try:
            return open(rfs.Location,"rb").read()
         except:
            raise DAV_Error(424)
      raise DAV_NotFound

   def _get_dav_resourcetype(self,uri):
      rfs = self.uri2local(uri)[1]
      if rfs.IsCollection():
         return COLLECTION
      return OBJECT
      
   def _get_dav_displayname(self,uri):
      raise DAV_Secret   # do not show

   def _get_dav_getcontentlength(self,uri):
      """ return the content length of an object """
      rfs = self.uri2local(uri)[1]
      st = rfs.GetStatInfo()
      return st[stat.ST_SIZE]

   def get_lastmodified(self,uri):
      rfs = self.uri2local(uri)[1]
      st = rfs.GetStatInfo()
      return st[stat.ST_MTIME]

   def get_creationdate(self,uri):
      rfs = self.uri2local(uri)[1]
      st = rfs.GetStatInfo()
      return st[stat.ST_CTIME]

   def _get_dav_getcontenttype(self,uri):
      rfs = self.uri2local(uri)[1]
      if rfs.IsCollection():
         return "httpd/unix-directory"
      return "application/octet-stream"

   def exists(self,uri):
      """ test if a resource exists """
      try:
         self.uri2local(uri)
         return 1
      except:
         return None

   def is_collection(self,uri):
      rfs = self.uri2local(uri)[1]
      return rfs.IsCollection()

   def mkcol(self,uri):
      try:
         rfs=self.uri2local(uri)[1]
         raise DAV_Error(405)
      except DAV_NotFound:
         rfs=self.newcollection(uri)
      try:
         os.mkdir(rfs.Location)
         return 201
      except:
         raise DAV_Forbidden

   ### DELETE

   def delone(self,uri):
      return delone(self,uri)

   def deltree(self,uri):
      return deltree(self,uri)

   def rmcol(self,uri):
      rfs = self.uri2local(uri)[1]
      fname = rfs.Location
      rfs.RemoveItem()
      try:
         os.rmdir(fname)
         return 204
      except:
         raise DAV_Forbidden

   def rm(self,uri):
      rfs=self.uri2local(uri)[1]
      fname=rfs.Location
      rfs.RemoveItem()
      try:
         os.unlink(fname)
         return 204
      except:
         raise DAV_Forbidden

   ### MOVE
   def moveone(self,src,dst,overwrite):
      return moveone(self,src,dst,overwrite)

   def movetree(self,src,dst,overwrite):
      return movetree(self,src,dst,overwrite)

   ### COPY

   def copyone(self,src,dst,overwrite):
      return copyone(self,src,dst,overwrite)

   def copytree(self,src,dst,overwrite):
      return copytree(self,src,dst,overwrite)

   ### copy
   def copy(self,src,dst):
      srfs=self.uri2local(src)[1]
      try:
         self.uri2local(dst)
         raise DAV_Error(405)
      except DAV_NotFound:
         drfs=self.newitem(dst)
      try:
         fs=open(srfs.Location,'rb')
         fd=open(drfs.Location,'wb')
         while 1:
            data=fs.read(4096)
            if not data:
               break
            fd.write(data)
      except:
         drfs.RemoveItem()
         try:
            os.unlink(drfs.Location)
         except:
            pass
         raise DAV_Error, Forbidden

   def copycol(self,src,dst):
      return self.mkcol(dst)

from CLASSES_Library_ICORBase_Interface_ICORInterface import FilePathAsSystemPath
from CLASSES_Library_NetBase_RemoteFileSystem_Item_RFSInterface import ICORRFSItem
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_ICORBase_Interface_ICORSecurity import GetUIDByUserPassword
from CLASSES_Library_ICORBase_External_MLog import Log
from CLASSES_Library_ICORBase_Interface_ICORUtil import tdatetime,tdatetime2fmtstr
import CLASSES_Library_ICORBase_External_Broker_Communicator
brokercommunicator=CLASSES_Library_ICORBase_External_Broker_Communicator

LOG_FILE=FilePathAsSystemPath(r'%ICOR%\\log\\isapidav.log')

class mydavHandler(DAVRequestHandler):
   debuglevel=0
   server_realm = 'icor-dav'
   def get_userinfo(self,user,pw):
      uid=GetUIDByUserPassword(user,pw,awwwuser=0)
      if uid<0:
         self.IFACE_CLASS=None
         return 0
      rfs=aICORWWWServerInterface.GetUserDefaultRFSItem(uid)
      path=FilePathAsSystemPath(rfs.CollectionLocation)
      path=path.replace('\\','/')
      self.IFACE_CLASS=dataclass()
      self.IFACE_CLASS.UID=uid
      self.IFACE_CLASS.ROOTOID=rfs.oid
      if aICORWWWServerInterface.RFSDAVServerPort!='80':
         sport=':%s' %aICORWWWServerInterface.RFSDAVServerPort
      else:
         sport=''
      self.IFACE_CLASS.BASEURI="http://%s%s%s" %(
         aICORWWWServerInterface.RFSDAVServer,
         sport,
         aICORWWWServerInterface.RFSDAVServerUrl)
      return 1

errorstr='''
<html><head><title>Error 403</title><meta name="robots" content="noindex">
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1"></head>
<body><h2>HTTP Error 403</h2>
<p><strong>403 Forbidden: Execute Access Forbidden</strong></p>
<p>This error can be caused if you try to execute a CGI, ISAPI, or other executable program from a directory that does not allow programs to be executed.</p>
<p>Please contact the Web server's administrator if the problem persists.</p>
</body></html>
'''
def demo(channel):
   env = channel.Input()
   env = env.split('\0')
   dct = {}
   for i in env:
      i=i.strip()
      if i:
         k,v=i.split('=',1)
         v=v.strip()
         if v:
            dct[k]=v
   command = dct['REQUEST_METHOD']
   where = dct['PATH_INFO']
   what = urllib.unquote_plus(dct.get('QUERY_STRING','/'))
   s=tdatetime2fmtstr(tdatetime(),longfmt=1)

   if where=='/dav.icor':
      body = channel.Input()
      Log('%s - dav %s %s\n' %(s,command,where),fname=LOG_FILE)
      s=mydavHandler(channel,dct,body)
      s.handle()
      channel.Output('',last=0)
   else:
      body = channel.Input()
      Log('%s - error %s %s\n' %(s,command,where),fname=LOG_FILE)
      channel.Output(errorstr,last=1)

def main(pname):
   s=brokercommunicator.CommunicatorServer(pname)
   while 1:
      try:
         demo(s)
         brokercommunicator.SendCmd('DONE %s' %pname,withrecv=0)
      except:
#         import traceback; traceback.print_exc(); raw_input('enter!')
         s.Close()
         brokercommunicator.SendCmd('DONE %s' %pname,withrecv=0)
         sys.exit(1)

#if __name__ == '__main__':
#      main(sys.argv[1])
