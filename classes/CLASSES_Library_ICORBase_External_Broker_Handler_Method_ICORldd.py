# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import sys
import os
import ihooks
import time
import string
import zlib
import struct
import marshal

magic    = ihooks.imp.get_magic()
stringtr = map(lambda x:chr(x),range(256))
stringtr = reduce(lambda x, y: x+y, stringtr, '')
stringtr = stringtr[:0x0d]+chr(0x0a)+stringtr[0x0e:]

LOADER_MODULE = 128
class m32Loader(ihooks.ModuleLoader):
   def __init__(self, verbose=0):
      ihooks.ModuleLoader.__init__(self,None,verbose)
      self.loaders={}
      self.loaderID=LOADER_MODULE
   def registerLoader(self, loader):
      self.loaders[self.loaderID]=loader
      self.loaderID=self.loaderID+1
   def find_module_in_dir(self, name, dirname, allow_packages=1):
      loaders=self.loaders.keys()
      loaders.sort()
      for loader in loaders:
         result=self.loaders[loader].find_module_in_dir(self, name, dirname, allow_packages, loader)
         if result is not None:
            return result
      return ihooks.ModuleLoader.find_module_in_dir(self, name, dirname, allow_packages)
   def load_module(self, name, stuff):
      file, filename, info = stuff
      (suff, mode, loaderid) = info
      if self.loaders.has_key(loaderid):
         return self.loaders[loaderid].load_module(self, name, stuff)
      return ihooks.ModuleLoader.load_module(self, name, stuff)

class m32BasicLoader:
   def __init__(self,description):
      self.description = description
   def __str__(self):
      return self.description
   __repr__=__str__
   def find_module_in_dir(self, loader, name, dirname, allow_packages,loaderid):
      return None
   def load_module(self, loader, name, stuff):
      file, filename, info = stuff
      (code, ispkg, loaderid) = info
      m = loader.hooks.add_module(name)
      m.__loadtime__=time.localtime(time.time())
      m.__file__ = name
      if ispkg:
         m.__path__ = [name,]
      exec code in m.__dict__
      return m
   def getCode(self,iName,dirName,data):
      iLen = len(data)
      if iLen==0:
         raise ImportError,"No module named \"%s\" " %iName
      needCompiler=1
      if iLen >= 4:
         needCompiler = (data[0:4] != magic)
      if needCompiler:
         data=data[:].translate(stringtr)
         code = compile(data+ "\n", iName, "exec")
      else:
         code = marshal.loads(data[8:])
      return code

def install(loader = None):
   if loader is None:
      ihooks.current_importer = ihooks.ModuleImporter(m32Loader())
      ihooks.current_importer.install()
   else:
      ihooks.current_importer.loader.registerLoader(loader)

class DIRLoader(m32BasicLoader):
   def __init__(self,dirname):
      m32BasicLoader.__init__(self,'DIRLoader(%s)' %dirname)
      self.dirname = dirname
   def find_module_in_dir(self, loader, name, dirname, allow_packages,loaderid):
      if dirname is not None:
         return None
      return ihooks.ModuleLoader.find_module_in_dir(loader, name, self.dirname, allow_packages)

class FUNCLoader(m32BasicLoader):
   def __init__(self,func):
      m32BasicLoader.__init__(self,'FUNCLoader(%s)' %func)
      self.func = func
   def find_module_in_dir(self, loader, name, dirname, allow_packages,loaderid):
      try:
         code = self.LoadFromFunction(name, dirname)
         return None, name, (code, None, loaderid)
      except ImportError:
         pass
      return None
   def LoadFromFuncion(self, iName, dirName):
      data=self.func(iName,dirName)
      return self.getcode(iName,dirName,data)

_MAGIC0 = 'PYLB\0\0\0\0' # python library not compressed
_MAGIC1 = 'PYLB\0\1\0\0' # python library compressed

def writez(output,data,pack):
   if pack:
      data = zlib.compress(data, 9)
      crc32= zlib.adler32(data)
   else:
      crc32=0
   pdata=struct.pack('<ii',len(data),crc32)
   output.write(pdata)
   output.write(data)

def readz(input,pack):
   ldata,lcrc32=struct.unpack('<ii',input.read(8))
   data=input.read(ldata)
   if pack:
      crc32= zlib.adler32(data)
      ok=lcrc32==crc32
      data = zlib.decompress(data)
   else:
      ok=lcrc32==0
   if ok:
      data=marshal.loads(data)
   else:
      data=''
   return ok,data

class PYLLoader(m32BasicLoader):
   def __init__(self, archive_pathname):
      m32BasicLoader.__init__(self,'PYLLoader(%s)' %archive_pathname)
      self.archive_pathname = archive_pathname
      self.library = open(archive_pathname, 'rb')
      magik = self.library.read(len(_MAGIC0))
      if magik==_MAGIC0:
         self.packed=0
      elif magik==_MAGIC1:
         self.packed=1
      else:
         raise NameError,archive_pathname
      offset = struct.unpack('=i', self.library.read(4))[0]
      self.library.seek(offset)
      self.toc = readz(self.library,self.packed)[1]
   def find_module_in_dir(self, loader, name, dirname, allow_packages,loaderid):
      if dirname is None:
         data=self.toc.get(name,None)
      else:
         name=string.join([dirname,name],'.')
         data=self.toc.get(name,None)
      if not data:
         return None
      pos, ispkg = data
      self.library.seek(pos)
      code=readz(self.library,self.packed)[1]
      return None, name, (code, ispkg, loaderid)

def find_in_locals(aname,adefault):
   try:
      raise ZeroDivisionError
   except ZeroDivisionError:
      f=sys.exc_info()[2].tb_frame.f_back
   while f is not None:
      if f.f_locals.has_key(aname):
         return f.f_locals[aname]
      f=f.f_back
   return adefault

def uid():
   return find_in_locals('UID',-1)

class ICORLoader(m32BasicLoader):
   def find_module_in_dir(self, loader, name, dirname, allow_packages,loaderid):
      if (dirname is None) and not string.find(name,'CLASSES'):
         try:
            code = self.ICORLoadFromStream(name)
            return None, name, (code, None, loaderid)
         except ImportError:
            pass
      return None
   def ICORLoadFromStream(self,iName):
      import icorapi
      data=icorapi.ImportModuleAsString(uid(),iName)
      if not data:
         raise ImportError,iName
      return self.getCode(iName,None,data)

def installone(name):
   try:
      if type(name)==type(''):
         if len(name)==0:
            return
         if os.path.isdir(name):
            install(DIRLoader(name))
         else:
            install(PYLLoader(name))
      else:
         install(FUNCLoader(name))
   except:
      pass

def installall(top,modules):
   for i in modules:
      installone('%s/%s' %(top,i))
   install(ICORLoader('ICORLoader'))

install()
installall('c:/icor/python',[])



