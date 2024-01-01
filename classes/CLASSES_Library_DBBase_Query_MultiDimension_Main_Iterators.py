# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import string

class StringRange:
   def __init__(self,afromS,atoS,attrs=None):
      self.FromS=afromS
      self.ToS=atoS
      self.Value=''
      self.Attrs={}
      if not attrs is None:
         if type(attrs)==type({}):
            self.Attrs=attrs
         else:
            self.Value=attrs
   def __cmp__(self,other):
      if self.FromS<other.FromS:
         return -1
      elif self.FromS>other.FromS:
         return 1
      else:
         if self.ToS<other.ToS:
            return -1
         elif self.ToS>other.ToS:
            return 1
         else:
            return 0
   def __repr__(self):
      s=self.FromS+'-'+self.ToS
      if type(self.Value)==type(''):
         s=s+' '+self.Value
      else:
         s=s+' '+str(self.Value)
      return s
   def __getitem__(self,key):
      return self.Attrs.get(key,None)
   def __setitem__(self,key,value):
      self.Attrs[key]=value

class StringRangeIterator:
   def __init__(self):
      self.AttrDict={}
      self.AttrCnt=0
      self.RangeDict={}
      self.Ranges=[]
      self.Values=[]
      self.Result=[]
   def AddRange(self,afrom,ato,attrs=None):
      if ato=='':
         ato=CLASSES_Library_ICORBase_Interface_ICORUtil.IncNumString(afrom)
      self.AttrDict[self.AttrCnt]=attrs
      v=self.RangeDict.get(afrom,[])
      v.append([0,self.AttrCnt])
      self.RangeDict[afrom]=v
      v=self.RangeDict.get(ato,[])
      v.append([1,self.AttrCnt])
      self.RangeDict[ato]=v
      self.AttrCnt=self.AttrCnt+1
#      arange=StringRange(afrom,ato,attrs)
#      self.Ranges.append(arange)
#      return arange
   def Join(self):
      lpoints=self.RangeDict.keys()
      lpoints.sort()
      lfrom=''
      lpts=[]
      w=0
      for apoint in lpoints:
         v=self.RangeDict[apoint]
         if lpts!=[] and w:
#            print lfrom,'-',apoint,':',
            avalues=[]
            for apt in lpts:
               avalues.append(self.AttrDict[apt])
#               print self.AttrDict[apt],
#            print
            avalues.sort()
            self.Result.append([lfrom,apoint,avalues])
         for aaction,acnt in v:
            if aaction:
               lpts.remove(acnt)
            else:
               lpts.append(acnt)
         lfrom,w=apoint,1
      for i in range(len(self.Result)-1,0,-1):
         if self.Result[i][2]==self.Result[i-1][2]:
            self.Result[i-1][1]=self.Result[i][1]
            del self.Result[i]
   def Dump(self):
      for lfrom,apoint,avalues in self.Result:
         print lfrom,'|',apoint,'|'
         for avalue in avalues[:25]:
            print '  ',avalue

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   aclass=aICORDBEngine.Classes[CID]
   sri=StringRangeIterator()
   sri.AddRange('05','10','aaa')
   sri.AddRange('05','10','bbb')
   sri.AddRange('10','20','aaa')
   sri.AddRange('10','20','bbb')
   sri.AddRange('10','20','ccc')
   sri.AddRange('15','17','ddd')
   sri.AddRange('16','30','eee')
   sri.AddRange('20','21','fff')
   sri.AddRange('35','50','fff')
   sri.AddRange('40','45','ggg')

#   sri.AddRange('15','25',5)
#   sri.AddRange('47','60',5)
   sri.Join()
   sri.Dump()
   return



