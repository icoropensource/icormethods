# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
from ctypes import *
import win32api
import string
import os
import random
import math
import time

class TSPSolver:
   def __init__(self):
      self.data=[]
   def LinKernighan(self,aprint=0):
      if len(self.data)<=1:
         return 0.0,self.data
      elif len(self.data)<=3:
         return 0.0,self.data
      ICOR_DIR=aICORDBEngine.Variables['_ICOR_BASE_DIR']
      atspfilename=ICOR_DIR+'/wwwroot/output/'+ICORUtil.GetRandomFileName(ICOR_DIR+'/wwwroot/output','lk_','.tsp')
      aoutfilename=atspfilename[:-3]+'out'
      fout=open(atspfilename,'w')
      try:
         fout.write("""NAME : temp_file
TYPE : TSP
DIMENSION : %d
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_TYPE : TWOD_COORDS
NODE_COORD_SECTION
"""%(len(self.data),))
         for i in range(len(self.data)):
            fout.write('%d %f %f\n'%(i,self.data[i][1],self.data[i][2]))
         fout.write('EOF\n')
      finally:
         fout.close()

      if not aprint:
         std_in=win32api.GetStdHandle(win32api.STD_INPUT_HANDLE)
         std_out=win32api.GetStdHandle(win32api.STD_OUTPUT_HANDLE)
         std_err=win32api.GetStdHandle(win32api.STD_ERROR_HANDLE)
         win32api.SetStdHandle(win32api.STD_INPUT_HANDLE,0)
         win32api.SetStdHandle(win32api.STD_OUTPUT_HANDLE,0)
         win32api.SetStdHandle(win32api.STD_ERROR_HANDLE,0)
      import linkern25c
      linkern=linkern25c

      dat=linkern.CCdatagroup()
      ret=linkern.CCutil_init_datagroup(byref(dat))
      
      rstate=linkern.CCrandstate()
      linkern.CCutil_sprand(1126908213,byref(rstate))
      
      ncount=c_int(0)
      ret=linkern.CCutil_gettsplib(atspfilename,byref(ncount),byref(dat))
      
      val=c_double(0.0)
      best=1e30
      tempcount=c_int(0)
      itemplist=c_int(0)
      templist=pointer(itemplist)
      tincycle=c_int*int(ncount.value)
      incycle=tincycle()
      toutcycle=c_int*int(ncount.value)
      outcycle=toutcycle()
      
      ret=linkern.CCedgegen_x_quadrant_k_nearest(ncount,3,byref(dat),None,1,byref(tempcount),byref(templist),1)
      v1=int(linkern.CCutil_lprand(byref(rstate)))
      linkern.CCedgegen_x_nearest_neighbor_tour(ncount,v1%int(ncount.value),byref(dat),incycle,byref(val))
      
      lret=[]
      abestcnt=0
      t1=time.time()
      for i in range(500):
         ret=linkern.CClinkern_tour(ncount,byref(dat),tempcount,templist,100000000,-1,incycle,outcycle,byref(val),1,c_double(-1.0),c_double(-1.0),None,2,byref(rstate))
         if val.value<best:
            best=val.value
            lret=[]
            v0=v1=outcycle[0]
            j=1
            while j<(ncount.value):
               v2=outcycle[j]
               lret.append([v1,v2])
               v1=v2
               j=j+1
            lret.append([v2,v0])
            abestcnt=0
         else:
            abestcnt=abestcnt+1
            if abestcnt>44:
               break
         if not (i%4):
            dt=time.time()-t1
            if dt>44:
               break
   
      if not aprint:
         win32api.SetStdHandle(win32api.STD_INPUT_HANDLE,std_in)
         win32api.SetStdHandle(win32api.STD_OUTPUT_HANDLE,std_out)
         win32api.SetStdHandle(win32api.STD_ERROR_HANDLE,std_err)
   
#      print 'route len:',best
#      fout=open(OUTPUT_FILE,'w')
#      fout.write('%d %d\n'%(ncount.value,len(lret)))
#      for i in range(ncount.value):
#         fout.write('%f %f\n'%(dat.x[i],dat.y[i]))
      lids=[]
      for x,y in lret:
         lids.append(x)
#         fout.write('%d %d 0\n'%(x,y))
#      fout.close()
      del linkern

      l=[]
      adist=0.0
      amaxdist=0.0
      amaxdistpos=0
      aname2,ax2,ay2=None,None,None
      for i in range(len(lids)-1):
         j1,j2=lids[i],lids[i+1]
         aname1,ax1,ay1=self.data[j1][0],self.data[j1][1],self.data[j1][2]
         aname2,ax2,ay2=self.data[j2][0],self.data[j2][1],self.data[j2][2]
         ad=math.sqrt((abs(ax1-ax2)**2)+(abs(ay1-ay2)**2))
         l.append([aname1,ax1,ay1])
         adist=adist+ad
         if ad>amaxdist:
#            print i,ad,aname1,ax1,ay1
            amaxdist=ad
            amaxdistpos=i
#         print 'point:',i,aname1,ax1,ay1,ad
      if not aname2 is None:
         l.append([aname2,ax2,ay2])
         j1=lids[0]
         aname1,ax1,ay1=self.data[j1][0],self.data[j1][1],self.data[j1][2]
         ad=math.sqrt((abs(ax1-ax2)**2)+(abs(ay1-ay2)**2))
         if ad<amaxdist:
#         print 'fpint:',0,aname1,ax1,ay1,ad,amaxdistpos
            l=l[amaxdistpos+1:]+l[:amaxdistpos+1]
#      print 'DIST:',adist,amaxdist,amaxdistpos
      return 0.0,l


def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   Test()
#   return
   l1=string.split(Value,chr(255))
   apoints=[]
   for s in l1:
      l2=string.split(s,chr(254))
      l2[1]=float(l2[1])
      l2[2]=float(l2[2])
      apoints.append(l2)
   atspsolver=TSPSolver()
   atspsolver.data=apoints
   adist,ret=atspsolver.LinKernighan()
   l=[]
   for aname,ax1,ay1 in ret:
      l.append(aname+chr(254)+str(ax1)+chr(254)+str(ay1))
   return string.join(l,chr(255))



