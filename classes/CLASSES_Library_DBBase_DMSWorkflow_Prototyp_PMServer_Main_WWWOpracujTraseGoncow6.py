# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from ctypes import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import win32api
import string
import os
import random
import math
import time

MAX_TIME=55.0
MAX_ITER=350

LOG_FILE='out.txt'

def Log(s='',amode='a+',fname=LOG_FILE,aconsole=0):
   if type(s)==type([]):
      s=string.join(map(repr,s),' ')
   if aconsole:
      print string.replace(s,'\n','')
   try:
      f=open(fname,amode)
      if s[-1:]!='\n':
         s=s+'\n'
      f.write('['+str(os.getpid())+'] '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())+': '+s)
      f.close()
   except:
      pass

class Goniec:
   def __init__(self):
      pass

class Lista:
   def __init__(self,aid,adane,amindist=0.0):
      self.ID=aid
      self.mindist=amindist
      self.data=adane
      self.routelen=len(self.data)
      self.distmod=0.0
      self.dist=0.0
      for i in range(self.routelen-1):
         ax1,ay1=self.data[i][1],self.data[i][2]
         ax2,ay2=self.data[i+1][1],self.data[i+1][2]
         ad=self.UpdateDist(ax1,ay1,ax2,ay2)
   def AsString(self):
      l=[]
      for aname,ax1,ay1 in self.data:
         l.append(aname+chr(254)+str(ax1)+chr(254)+str(ay1))
      return string.join(l,chr(255))
   def Normalize(self):
      if self.routelen<2:
         return
      l=[]
      adist=0.0
      amaxdist=0.0
      amaxdistpos=0
      aname2,ax2,ay2=None,None,None
      for i in range(len(self.data)-1):
         aname1,ax1,ay1=self.data[i][0],self.data[i][1],self.data[i][2]
         aname2,ax2,ay2=self.data[i+1][0],self.data[i+1][1],self.data[i+1][2]
         ad=math.sqrt((abs(ax1-ax2)**2)+(abs(ay1-ay2)**2))
         l.append([aname1,ax1,ay1])
         adist=adist+ad
         if ad>amaxdist:
            amaxdist=ad
            amaxdistpos=i
      if not aname2 is None:
         l.append([aname2,ax2,ay2])
         aname1,ax1,ay1=self.data[0][0],self.data[0][1],self.data[0][2]
         ad=math.sqrt((abs(ax1-ax2)**2)+(abs(ay1-ay2)**2))
         if ad<amaxdist:
            l=l[amaxdistpos+1:]+l[:amaxdistpos+1]
      self.data=l

      self.distmod=0.0
      self.dist=0.0
      for i in range(len(self.data)-1):
         aname1,ax1,ay1=self.data[i][0],self.data[i][1],self.data[i][2]
         aname2,ax2,ay2=self.data[i+1][0],self.data[i+1][1],self.data[i+1][2]
         self.UpdateDist(ax1,ay1,ax2,ay2)
   def UpdateDist(self,ax1,ay1,ax2,ay2,amod=1):
      ad=math.sqrt((ax1-ax2)*(ax1-ax2)+(ay1-ay2)*(ay1-ay2))
      self.dist=self.dist+amod*ad
      if ad>self.mindist:
         self.distmod=self.distmod+ad
      return ad
   def CheckUpdateDist(self,ax1,ay1,ax2,ay2,amod=1):
      ad=math.sqrt((ax1-ax2)*(ax1-ax2)+(ay1-ay2)*(ay1-ay2))
      dist=self.dist+amod*ad
      distmod=self.distmod
      if ad>self.mindist:
         distmod=distmod+ad
      return ad,dist,distmod
   def AddFirst(self,aitem):
      ad=0.0
      self.data.insert(0,aitem)
      if self.routelen:
         ax1,ay1=self.data[0][1],self.data[0][2]
         ax2,ay2=self.data[1][1],self.data[1][2]
         ad=self.UpdateDist(ax1,ay1,ax2,ay2)
      self.routelen=1+self.routelen
      return ad
   def AddLast(self,aitem):
      ad=0.0
      self.data.append(aitem)
      if self.routelen:
         ax1,ay1=self.data[self.routelen-1][1],self.data[self.routelen-1][2]
         ax2,ay2=self.data[self.routelen][1],self.data[self.routelen][2]
         ad=self.UpdateDist(ax1,ay1,ax2,ay2)
      self.routelen=1+self.routelen
      return ad
   def RemoveFirst(self):
      ret=None
      if self.routelen==1:
         ret=self.data[0]
         self.data=[]
         self.routelen=0
         self.dist=0.0
         return ret
      if self.routelen:
         ax1,ay1=self.data[0][1],self.data[0][2]
         ax2,ay2=self.data[1][1],self.data[1][2]
         ad=self.UpdateDist(ax1,ay1,ax2,ay2,-1)
         ret=self.data[0]
         del self.data[0]
         self.routelen=self.routelen-1
      return ret
   def RemoveLast(self):
      ret=None
      if self.routelen==1:
         ret=self.data[0]
         self.data=[]
         self.routelen=0
         self.dist=0.0
         return ret
      if self.routelen:
         ax1,ay1=self.data[self.routelen-2][1],self.data[self.routelen-2][2]
         ax2,ay2=self.data[self.routelen-1][1],self.data[self.routelen-1][2]
         ad=self.UpdateDist(ax1,ay1,ax2,ay2,-1)
         ret=self.data[self.routelen-1]
         del self.data[self.routelen-1]
         self.routelen=self.routelen-1
      return ret
   def CheckFirst(self,aitem):
      ad=0.0
      if type(aitem)==type([]) or type(aitem)==type(()):
         ax1,ay1=aitem[1],aitem[2]
      else:
         ax1,ay1=aitem.data[aitem.routelen-1][1],aitem.data[aitem.routelen-1][2]
      if self.routelen:
         ax2,ay2=self.data[0][1],self.data[0][2]
         ad=math.sqrt((ax1-ax2)*(ax1-ax2)+(ay1-ay2)*(ay1-ay2))
      return ad,ad+self.dist
   def CheckLast(self,aitem):
      ad=0.0
      if type(aitem)==type([]) or type(aitem)==type(()):
         ax1,ay1=aitem[1],aitem[2]
      else:
         ax1,ay1=aitem.data[0][1],aitem.data[0][2]
      if self.routelen:
         ax2,ay2=self.data[self.routelen-1][1],self.data[self.routelen-1][2]
         ad=math.sqrt((ax1-ax2)*(ax1-ax2)+(ay1-ay2)*(ay1-ay2))
      return ad,ad+self.dist
   def CheckJoinFirst(self,alista):
      dist=self.dist
      distmod=self.distmod
      ad=0.0
      if alista.routelen and self.routelen:
         ax1,ay1=alista.data[alista.routelen-1][1],alista.data[alista.routelen-1][2]
         ax2,ay2=self.data[0][1],self.data[0][2]
         ad,dist,distmod=self.CheckUpdateDist(ax1,ay1,ax2,ay2)
      dist=dist+alista.dist
      distmod=distmod+alista.distmod
      routelen=len(self.data)+len(alista.data)
      return ad,dist,distmod,routelen
   def CheckJoinLast(self,alista):
      dist=self.dist
      distmod=self.distmod
      ad=0.0
      if alista.routelen and self.routelen:
         ax1,ay1=self.data[self.routelen-1][1],self.data[self.routelen-1][2]
         ax2,ay2=alista.data[0][1],alista.data[0][2]
         ad,dist,distmod=self.CheckUpdateDist(ax1,ay1,ax2,ay2)
      dist=dist+alista.dist
      distmod=distmod+alista.distmod
      routelen=len(self.data)+len(alista.data)
      return ad,dist,distmod,routelen
   def JoinFirst(self,alista):
      if alista.routelen and self.routelen:
         ax1,ay1=alista.data[alista.routelen-1][1],alista.data[alista.routelen-1][2]
         ax2,ay2=self.data[0][1],self.data[0][2]
         ad=self.UpdateDist(ax1,ay1,ax2,ay2)
      self.data=alista.data+self.data
      self.dist=self.dist+alista.dist
      self.distmod=self.distmod+alista.distmod
      self.routelen=len(self.data)
   def JoinLast(self,alista):
      if alista.routelen and self.routelen:
         ax1,ay1=self.data[self.routelen-1][1],self.data[self.routelen-1][2]
         ax2,ay2=alista.data[0][1],alista.data[0][2]
         ad=self.UpdateDist(ax1,ay1,ax2,ay2)
      self.data=self.data+alista.data
      self.dist=self.dist+alista.dist
      self.distmod=self.distmod+alista.distmod
      self.routelen=len(self.data)
   def Dump(self):
      Log('%03d %03d %8.4f %8.4f'%(self.ID+1,self.routelen,self.dist,self.distmod))

class Metoda:
   def __init__(self,atrasa):
      self.trasa=atrasa
      self.listy=[]
      self.name=''
   def Dump(self):
      Log()
      Log('Method: '+self.name)
      for alista in self.listy:
         alista.Dump()
   def Dist(self,ax1,ay1,ax2,ay2):
      return math.sqrt((ax1-ax2)*(ax1-ax2)+(ay1-ay2)*(ay1-ay2))

class MetodaCutByN(Metoda):
   def __init__(self,atrasa,n):
      Metoda.__init__(self,atrasa)
      self.n=n
      self.name='Cut By N, n='+str(n)
   def Process(self):
      l=self.trasa.lroute[:]
      i=0
      while l:
         alista=Lista(i,l[:self.n])
         self.listy.append(alista)
         l=l[self.n:]
         i=i+1

class MetodaCutByDist(Metoda):
   def __init__(self,atrasa,amaxdist):
      Metoda.__init__(self,atrasa)
      self.maxdist=amaxdist
      self.name='Cut By Dist, d='+str(amaxdist)
   def Process(self):
      l=self.trasa.lroute[:]
      aid=0
      i=0
      alista=[]
      adist=0.0
      while i<len(l)-1:
         bdist=self.Dist(l[i][1],l[i][2],l[i+1][1],l[i+1][2])
         if adist+bdist>self.maxdist:
            olista=Lista(aid,alista)
            self.listy.append(olista)
            aid=aid+1
            alista=[l[i],]
            adist=0.0
         else:
            alista.append(l[i])
            adist=adist+bdist
            i=i+1
      alista.append(l[i])
      olista=Lista(aid,alista)
      self.listy.append(olista)

class MetodaCutByDistAndN(Metoda):
   def __init__(self,atrasa,amaxdist,n):
      Metoda.__init__(self,atrasa)
      self.maxdist=amaxdist
      self.n=n
      self.name='Cut By Dist, d='+str(amaxdist)+' n='+str(n)
   def Process(self):
      l=self.trasa.lroute[:]
      aid=0
      i=0
      alista=[]
      adist=0.0
      while i<len(l)-1:
         bdist=self.Dist(l[i][1],l[i][2],l[i+1][1],l[i+1][2])
#         print i,aid,adist,bdist,adist+bdist,
         if ((adist+bdist)>=self.maxdist) or (len(alista)>=self.n):
            if alista:
               olista=Lista(aid,alista)
               self.listy.append(olista)
               aid=aid+1
            alista=[l[i],]
            adist=0.0
#            print ' *** cut ***'
         else:
            alista.append(l[i])
            adist=adist+bdist
#            print 'non cut'
         i=i+1
      alista.append(l[i])
      olista=Lista(aid,alista)
      self.listy.append(olista)

class MetodaCutByDistAndNMin(Metoda):
   def __init__(self,atrasa,amaxdist,amindist,n,aminodleglosc):
      Metoda.__init__(self,atrasa)
      self.maxdist=amaxdist
      self.mindist=amindist
      self.n=n
      self.minodleglosc=aminodleglosc
      self.name='Cut By Dist&Min, d='+str(amaxdist)+' m='+str(amindist)+' n='+str(n)+' o='+str(aminodleglosc)
   def Process(self):
      l=self.trasa.lroute[:]
      aid=0
      olista=Lista(aid,[],self.mindist)
      aid=aid+1
      self.listy=[olista,]
      for aitem in l:
         ad,atd=olista.CheckLast(aitem)
         if ad<=self.mindist:
            olista.AddLast(aitem)
         else:
            olista=Lista(aid,[aitem,],self.mindist)
            aid=aid+1
            self.listy.append(olista)

#      Log()
#      Log('Pierwsze przyblizenie')
#      self.Dump()

      icnt=0
      while 1:
         wswitch=0
         apos=1
         while apos<len(self.listy)-1:
#            Log([' while',apos])
            blista=self.listy[apos]
            ad1,dist1,distmod1,routelen1=blista.CheckJoinFirst(self.listy[apos-1])
            ad2,dist2,distmod2,routelen2=blista.CheckJoinLast(self.listy[apos+1])
            wn,w1,w2=1,1,1
            if routelen1>self.n or distmod1>self.maxdist or ad1>self.minodleglosc:
               w1=0
            if routelen2>self.n or distmod2>self.maxdist or ad2>self.minodleglosc:
               w2=0
#            Log([' w1',w1,'w2',w2,routelen1,distmod1,routelen2,distmod2])
            if w1 and w2:
               wswitch=1
               if distmod1<distmod2:
                  blista.JoinFirst(self.listy[apos-1])
                  del self.listy[apos-1]
                  apos=apos-1
                  if apos<1:
                     apos=1
#                  Log([' switch 1'])
               else:
#                  Log([' switch 2'])
                  blista.JoinLast(self.listy[apos+1])
                  del self.listy[apos+1]
            elif w1:
#               Log([' switch 3'])
               wswitch=1
               blista.JoinFirst(self.listy[apos-1])
               del self.listy[apos-1]
               apos=apos-1
               if apos<1:
                  apos=1
            elif w2:
#               Log([' switch 4'])
               wswitch=1
               blista.JoinLast(self.listy[apos+1])
               del self.listy[apos+1]
            else:
#               Log([' no switch'])
               apos=apos+1
         if not wswitch:
            break
         else:
#            Log()
#            Log(['Iteracja:',icnt])
#            self.Dump()
            icnt=icnt+1

class Trasa:
   def __init__(self):
      pass
   def Open(self,atspfilename='',adata=None,aprint=0):
      self.odata=adata
      self.ddata={}
      if not adata is None:
         if len(adata)<=1:
            return 0.0,adata
         elif len(adata)<=3:
            return 0.0,adata
         self.ddist={}
         for i in range(len(adata)):
            self.ddist[(i,i)]=0.0
            for j in range(i+1,len(adata)):
               ad=math.sqrt((abs(adata[i][1]-adata[j][1])**2)+(abs(adata[i][2]-adata[j][2])**2))
               self.ddist[(i,j)]=ad
               self.ddist[(j,i)]=ad
         ICOR_DIR=aICORDBEngine.Variables['_ICOR_BASE_DIR']
         atspfilename=ICOR_DIR+'/wwwroot/output/'+ICORUtil.GetRandomFileName(ICOR_DIR+'/wwwroot/output','lk_','.tsp')
         aoutfilename=atspfilename[:-3]+'out'
         fout=open(atspfilename,'w')
         try:
            fout.write("""NAME: temp_file
TYPE: TSP
DIMENSION: %d
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: FULL_MATRIX
DISPLAY_DATA_TYPE: NO_DISPLAY
EDGE_WEIGHT_SECTION
"""%(len(adata),))
            for i in range(len(adata)):
               akey='%0.5f %0.5f'%(adata[i][1],adata[i][2])
               lvalue=self.ddata.get(akey,[])
               lvalue.append(adata[i][0])
               self.ddata[akey]=lvalue     
               for j in range(len(adata)):
                  fout.write(' %d'%(int(self.ddist[(i,j)]*10000.0)))
               fout.write('\n')
            fout.write('EOF\n')
         finally:
            fout.close()

         try:
            aparms=[ICOR_DIR+'/bin/linkern.exe','-Q','-t','120','-K','0','-I','1','-o',aoutfilename,atspfilename]
            os.spawnv(os.P_WAIT,aparms[0],aparms)
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

      self.data=[]
      for i in range(ncount.value):
         ax,ay=dat.x[i],dat.y[i]
         akey='%0.5f %0.5f'%(ax,ay)
         lvalue=self.ddata.get(akey,None)
         if lvalue is None:
            print '**** NO POINT ****',ax,ay
            spname=''
         else:
            spname=lvalue.pop()
         self.data.append([spname,ax,ay])
      lids=[]
      for x,y in lret:
         lids.append(x)

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
            amaxdist=ad
            amaxdistpos=i
      if not aname2 is None:
         l.append([aname2,ax2,ay2])
         j1=lids[0]
         aname1,ax1,ay1=self.data[j1][0],self.data[j1][1],self.data[j1][2]
         ad=math.sqrt((abs(ax1-ax2)**2)+(abs(ay1-ay2)**2))
         if ad<amaxdist:
            l=l[amaxdistpos+1:]+l[:amaxdistpos+1]

      if 1:
         aqsfilename=atspfilename+'.qs'
         fout=open(aqsfilename,'w')
         try:
            fout.write('%d %d\n'%(len(l),len(l)-1))
            for s,ax,ay in l:
               fout.write('%f %f\n'%(ax,ay))
            for i in range(len(l)-1):
               aname1,ax1,ay1=l[i][0],l[i][1],l[i][2]
               aname2,ax2,ay2=l[i+1][0],l[i+1][1],l[i+1][2]
               ad=math.sqrt((abs(ax1-ax2)**2)+(abs(ay1-ay2)**2))
               fout.write('%d %d %d\n'%(i,i+1,int(ad)))
         finally:
            fout.close()

      self.lroute=l
   def Process(self,stv_iloscgoncow,stv_mindist,stv_maxdist,stv_minodleglosc,stv_iloscprzesylek):
      if len(self.odata)<4:
         if not self.odata:
            return ''
         s=str(len(self.odata))+chr(253)+str(0.0)+chr(253)
         l=[]
         for aname,ax1,ay1 in self.odata:
            l.append(aname+chr(254)+str(ax1)+chr(254)+str(ay1))
         s=s+string.join(l,chr(255))
         return s
      amethod=MetodaCutByDistAndNMin(self,stv_maxdist,stv_mindist,stv_iloscprzesylek,stv_minodleglosc)
      amethod.Process()
#      amethod.Dump()
      l=[]
      i=0
      olista=None
      for alista in amethod.listy:
         if alista.routelen:
            alista.Normalize()
            s=alista.AsString()
            l.append(str(alista.routelen)+chr(253)+str(alista.distmod)+chr(253)+s)
#            if olista:
#               print '  ',alista.CheckJoinFirst(olista)
#            print i,len(alista.data),alista.routelen,alista.distmod,'-->',s
            i=i+1
            olista=alista
      return string.join(l,chr(252))
      amethods=[
#         [MetodaCutByN,(30,)],
         [MetodaCutByN,(40,)],
#         [MetodaCutByN,(70,)],
#         [MetodaCutByDist,(1000.0,)],
#         [MetodaCutByDist,(2000.0,)],
#         [MetodaCutByDist,(3500.0,)],
#         [MetodaCutByDistAndN,(2000.0,60)],
#         [MetodaCutByDistAndN,(2000.0,80)],
#         [MetodaCutByDistAndN,(2000.0,90)],
#         [MetodaCutByDistAndNMin,(5000.0,20.0,70)],
         [MetodaCutByDistAndNMin,(8000.0,30.0,80)],
#         [MetodaCutByDistAndNMin,(5000.0,40.0,90)],
      ]
      lmethods=[]
      for amethodclass,aparams in amethods:
         amethod=apply(amethodclass,(self,)+aparams)
         amethod.Process()
         amethod.Dump()
         lmethods.append(amethod)

def Main():
   afnamein='data/lk_0105653883.tsp' #742
   afnamein='data/lk_0067048010.tsp' #385
   afnamein='data/lk_0115368212.tsp' #54

#if __name__=='__main__':
#   Log('',amode='w')
#   Main()

def Test():
   stv_iloscgoncow=60
   stv_mindist=35.0
   stv_maxdist=8000.0
   stv_minodleglosc=1750.0
   stv_iloscprzesylek=60

   apoints=[
['aa',10.0,10.0],
['bb',20.0,20.0],
['cc',30.0,30.0],
['dd',10.0,30.0],
['ee',10.0,20.0],
['ff',30.0,10.0],
['gg',30.0,20.0],
['hh',20.0,30.0],
]
   atrasa=Trasa()
   atrasa.Open(adata=apoints)
   ret=atrasa.Process(stv_iloscgoncow,stv_mindist,stv_maxdist,stv_minodleglosc,stv_iloscprzesylek)
   return ret

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
#   s=Test()
#   print s
#   return                    
   l0=string.split(Value,chr(253))
   lparms=string.split(l0[0],chr(252))
   stv_iloscgoncow=int(lparms[0])
   stv_mindist=float(lparms[1])
   stv_maxdist=float(lparms[2])
   stv_minodleglosc=float(lparms[3])
   stv_iloscprzesylek=int(lparms[4])

   l1=string.split(l0[1],chr(255))
   apoints=[]
   for s in l1:
      l2=string.split(s,chr(254))
      l2[1]=float(l2[1])
      l2[2]=float(l2[2])
      apoints.append(l2)

#   print 'parms:',stv_iloscgoncow,stv_mindist,stv_maxdist,stv_minodleglosc,stv_iloscprzesylek
   atrasa=Trasa()
   atrasa.Open(adata=apoints)
   ret=atrasa.Process(stv_iloscgoncow,stv_mindist,stv_maxdist,stv_minodleglosc,stv_iloscprzesylek)
   return ret
#   atspsolver=TSPSolver()
#   atspsolver.data=apoints
#   adist,ret=atspsolver.LinKernighan()
#   l=[]
#   for aname,ax1,ay1 in ret:
#      l.append(aname+chr(254)+str(ax1)+chr(254)+str(ay1))
#   return string.join(l,chr(255))
                              


