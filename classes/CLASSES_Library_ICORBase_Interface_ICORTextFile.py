# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

# Text files with automatic (un)compression
#
# Written by: Konrad Hinsen <hinsenk@ere.umontreal.ca>
# Last revision: 1996-11-8
#
# Modified by: Rafal Smotrzyk <rsmotrzyk@mikroplan.com.pl>
# Tested: python 1.5, WinNT 4.0 SP3
# Last revision: 1998-12-16
#  - added .wrz files
#  - standard module gzip
#  - removed file closing from destructor
# Last revision: 1998-12-31
#  - added 'read' method

# This module defines a class TextFile whose instances can be
# accessed like normal file objects (i.e. by calling readline(),
# readlines(), and write()), but can also be used as line iterators
# in for loops.
#
# The class TextFile also handles compression transparently, i.e. it is
# possible to read lines from a compressed text file as if it were not
# compressed.  Compression is deduced from the file name suffixes '.Z'
# (compress/uncompress) and '.gz' (gzip/gunzip).
#
# Finally, TextFile objects accept file names that start with '~' or
# '~user' to indicate a home directory.

import os
import gzip
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

class TextFile:
   def __init__(self,filename,mode='r',aencoding=None):
      adir,afname=os.path.split(filename)
      self.myfileobj=None
      if mode == 'r':
         if not os.path.exists(filename):
            raise IOError, (2, 'No such file or directory')
         if filename[-3:]=='.gz' or filename[-4:]=='.wrz' or filename[-4:]=='.tgz':
            self.myfileobj=open(filename,mode+'b')
            self.file=gzip.GzipFile(afname,mode+'b',9,self.myfileobj)
         else:
            self.file=ICORUtil.OpenText(filename,mode,aencoding=aencoding)
      elif mode == 'w':
         if filename[-3:]=='.gz' or filename[-4:]=='.wrz' or filename[-4:]=='.tgz':
            self.myfileobj=open(filename,mode+'b')
            self.file=gzip.GzipFile(afname,mode+'b',9,self.myfileobj)
         else:
            self.file=ICORUtil.OpenText(filename,mode,aencoding=aencoding)
      else:
         raise IOError, (0, 'Illegal mode')
   def __getitem__(self, item):
      line = self.file.readline()
      if not line:
         raise IndexError
      return line
   def read(self,size=-1):
      return self.file.read(size)
   def readline(self):
      return self.file.readline()
   def readlines(self):
      return self.file.readlines()
   def write(self, data):
      self.file.write(data)
   def writelines(self, list):
      for line in list:
         self.file.write(line)
   def tell(self):
      if not self.myfileobj is None:
         return self.myfileobj.tell()
      return self.file.tell()
   def close(self):
      if not self.file is None:
         self.file.close()
         self.file=None
      if not self.myfileobj is None:
         self.myfileobj.close()
         self.myfileobj=None



