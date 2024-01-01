# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
import os
import random
import math
import time

class TSPSolver:
   def __init__(self):
      self.data=[]
   def __len__(self):
      return len(self.data)
   def open(self,afname):
      fin=open(afname,'r')
      try:
         astate=0
         while 1:
            s=fin.readline()
            if s[:3]=='EOF' or not s:
               break
            if astate==1:
               l=string.split(s[:-1],' ')
               self.data.append([l[0],float(l[1]),float(l[2])])
            if astate==0:
               if s[:18]=='NODE_COORD_SECTION':
                  astate=1
      finally:
         fin.close()
   def LinKernighan(self):
      if len(self.data)<=1:
         return 0.0,self.data
      elif len(self.data)>3:
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
         try:
            acommand=string.join([ICOR_DIR+'/bin/linkern.exe','-Q','-o',aoutfilename,atspfilename],' ')
            ExecuteShellCommand(acommand,amode='ProcessNoWindow',await=1)
         except:
            return 0.0,[]
         i=120
         while i:
            try:
               fin=open(aoutfilename,'r')
               break
            except:
               i=i-1
               time.sleep(0.5)
         try:
            fin.readline()
            lids=[]
            while 1:
               s=fin.readline()
               if not s:
                  break
               sl=string.split(s,' ')
               if len(sl)==3:
                  lids.append(int(sl[0]))
         finally:
            fin.close()
      else:
         lids=range(len(self.data))
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
      if 1:
         try:
            os.unlink(atspfilename)
            os.unlink(aoutfilename)
         except:
            pass
      if 0:
         adist=0.0
         for i in range(len(l)-1):
            ax1,ay1=l[i][1],l[i][2]
            ax2,ay2=l[i+1][1],l[i+1][2]
            ad=math.sqrt((ax1-ax2)*(ax1-ax2)+(ay1-ay2)*(ay1-ay2))
            adist=adist+ad
         aqsfilename=atspfilename[:-3]+'qs'
         fout=open(aqsfilename,'w')
         try:
            fout.write('%d %d\n'%(len(l),len(l)-1))
            for s,ax,ay in l:
               fout.write('%f %f\n'%(ax,ay))
            for i in range(len(l)-1):
               ax1,ay1=l[i][1],l[i][2]
               ax2,ay2=l[i+1][1],l[i+1][2]
               ad=math.sqrt((abs(ax1-ax2)**2)+(abs(ay1-ay2)**2))
               fout.write('%d %d %d\n'%(i,i+1,int(ad)))
         finally:
            fout.close()
         return adist,l
      return 0.0,l

def Test():
   apoints=[
      ['p01',87949.97978,36755.19044],
      ['p02',88701.21825,37392.03632],
      ['p03',88845.84944,35893.92856],
      ['p04',88871.49062,36404.10249],
      ['p05',89117.55453,36383.07165],
      ['p06',87214.91034,37336.49837],
      ['p07',86708.12152,38041.29555],
      ['p08',89694.69392,37579.54889],
      ['p09',86993.05047,37827.36145],
      ['p10',86930.45138,36676.71232],
      ['p11',88121.90249,35771.00723],
      ['p12',89702.91416,38346.51245],
      ['p13',86500.77026,36102.57022],
      ['p14',89505.49929,36457.47884],
      ['p15',87324.90701,38460.52454],
      ['p16',89810.90278,37051.28489],
      ['p17',89551.82287,37610.27222],
      ['p18',90088.39826,36131.53437],
      ['p19',87728.49583,38518.09019],
      ['p20',87585.57214,35743.34511],
      ['p21',87526.48025,36594.01949],
      ['p22',87770.23608,38172.44375],
      ['p23',86227.41614,36600.02369],
      ['p24',88521.35764,38332.83292],
      ['p25',89368.80654,38521.48853],
      ['p26',86818.26233,37275.64477],
   ]
   bpoints=[]
   for s,x,y in apoints:
      bpoints.append([s,x,y])
      bpoints.append([s+'1',x+333,y+337])
      bpoints.append([s+'2',x+127,y+238])
      bpoints.append([s+'3',x-2008,y+398])
      bpoints.append([s+'4',x-1078,y-67])
   apoints=bpoints

   atspsolver=TSPSolver()
   atspsolver.data=apoints
#   atspsolver.open('qa194.tsp')
#   atspsolver.open('zi929.tsp')
   adist,ret=atspsolver.LinKernighan()
   print 'TSP'
   print 'dist:',adist
#   for s,x,y in ret:
#      print s,x,y

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

                               


