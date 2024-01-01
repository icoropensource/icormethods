# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import sys
import time
import os

MODULES={}
MODULE_LINES={}
LAST_TIME=0.0

LIB_MODULES=1

def LineProfiler(frame,event,arg):
   global LAST_TIME
   atime=time.clock()
   if event=='line':
      amodule=frame.f_code.co_filename
      if amodule!='CLASSES_Library_ICORBase_External_MProfile':
         dtime=atime-LAST_TIME
         d=MODULE_LINES.get(amodule,{})
         l=d.get(frame.f_lineno,[0,0.0])
         l[0]=l[0]+1
         l[1]=l[1]+dtime
         d[frame.f_lineno]=l
         MODULE_LINES[amodule]=d
         d=MODULES.get(amodule,{})
         d['cnt']=d.get('cnt',0)+1
         d['time']=d.get('time',0.0)+dtime
         MODULES[amodule]=d
   LAST_TIME=time.clock()
   return LineProfiler

def Start():
   LAST_TIME=time.clock()
   sys.settrace(LineProfiler)

def Stop(afname='!!!profile.py'):
   sys.settrace(None)
   fout=open(afname,'w')
   try:
      l1,l2=[],[]
      for amodule,d in MODULES.items():
         l1.append([d.get('time',0.0),d.get('cnt',0),amodule])
         l2.append([d.get('cnt',0),d.get('time',0.0),amodule])
      l1.sort()
      l1.reverse()
      l2.sort()
      l2.reverse()
      fout.write('##### MODULES BY TIME ####\n')
      for atime,acnt,amodule in l1:
         fout.write('%20.12f : %12d | %s\n'%(atime,acnt,amodule))
      fout.write('##### MODULES BY CNT ####\n')
      for acnt,atime,amodule in l2:
         fout.write('%12d : %20.12f | %s\n'%(acnt,atime,amodule))
      amodules=MODULE_LINES.keys()
      amodules.sort()
      for amodule in amodules:
         fout.write('\n####################################################################\n### ')
         fout.write(amodule)
         fout.write('\n####################################################################\n')
         astats=MODULE_LINES[amodule]
         atext=''
         if string.find(amodule,'CLASSES_')==0:
            fin=open(FilePathAsSystemPath('%ICOR%/python/methods/'+amodule+'.py'),'r')
            atext=fin.read()
            fin.close()
         elif os.path.exists(amodule):
            if LIB_MODULES:
               fin=open(amodule,'r')
               atext=fin.read()
               fin.close()
         else:
            fout.write('Not Found Module: "%s"'%amodule)
         if atext:
            llines=string.split(atext,'\n')
            acnt=1
            for l in llines:
               if astats.has_key(acnt):
                  ls=astats[acnt]
                  fout.write('%8d : %8d : %20.12f : %12.10f | %s\n'%(acnt,ls[0],ls[1],ls[1]/ls[0],l))
               else:
                  fout.write('%8d : %8s : %20s : %12s | %s\n'%(acnt,'','','',l))
               acnt=acnt+1
   finally:
      fout.close()

