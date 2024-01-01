# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import os
import re

def ProcessRozdzialy(robj,lrsoids):
   while robj:
      lrsoids.append(robj.OID)
      ProcessRozdzialy(robj.PodRozdzialy,lrsoids)
      robj.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   RENAME=1
   aobj=aclass.GetFirstObject()
   while aobj:
      if not aobj.SGIsDisabled:
         apath=FilePathAsSystemPath(aobj.AppPaths.SciezkaAplikacji)
         print aobj.Nazwa,':',apath
         if RENAME:
            anewdir=apath+'/old'
            if not os.path.exists(anewdir):
               os.makedirs(anewdir)
         lreoids=[]
         l=os.listdir(apath)
         for afname in l:
            m=re.search('chapter_(\d+).asp',afname,re.I)
            if m:
               lreoids.append(int(m.group(1)))
         lrsoids=[]
         ProcessRozdzialy(aobj.Rozdzialy,lrsoids)
         lr=[]
         for roid in lreoids:
            if not roid in lrsoids:
               lr.append(roid)
         lr.sort()
         print lr
         if RENAME:
            for roid in lr:
               os.rename('%s/chapter_%d.asp'%(apath,roid),'%s/chapter_%d.asp'%(anewdir,roid))
               try:
                  os.rename('%s/chapter_%d.xml'%(apath,roid),'%s/chapter_%d.xml'%(anewdir,roid))
               except:
                  pass
               try:
                  os.rename('%s/chapter_%d.xsl'%(apath,roid),'%s/chapter_%d.xsl'%(anewdir,roid))
               except:
                  pass
               try:
                  os.rename('%s/chapter_%d_so.xsl'%(apath,roid),'%s/chapter_%d_so.xsl'%(anewdir,roid))
               except:
                  pass
      aobj.Next()
   return
