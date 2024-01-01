# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_DBBase_Query_MultiDimension_Main_Iterators import StringRangeIterator
from CLASSES_Library_DBBase_Query_Driver_FK20_QueryAccess import QueryAccessFK
from CLASSES_Library_NetBase_Utils_XMLUtil import *
import CLASSES_Library_DBBase_Query_MultiDimension_XML_Preprocessor_ReceiveQuery as ReceiveQuery
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import time
import string
import re
import random
import math

ICORMDQueryException = 'ICORMDQuery exception'

VERBOSE=0

# query output types
mdqt_HTML,mdqt_Excel=1,2

op_add,op_sub,op_mul,op_div,op_radd,op_rsub,op_rmul,op_rdiv,op_idiv=1,2,3,4,5,6,7,8,9

class DateSum:
   def __init__(self,amultiplyby=1.0,afromsum=None):
      if afromsum is None:
         self.TotalSum=0.0
         self.DateSums={}
         self.MultiplyBy=amultiplyby
      else:
         self.TotalSum=afromsum.TotalSum
         self.MultiplyBy=afromsum.MultiplyBy
         self.DateSums={}
         for akey,avalue in afromsum.DateSums.items():
            self.DateSums[akey]=avalue
   def __getitem__(self,key):
      if len(key)==3:
         k=(key[0],key[1])
      else:
         k=key
      return self.DateSums.get(k,0.0)
   def __setitem__(self,key,value):
      self.Update(key,value)
   def Update(self,key,value,aop=op_add):
      if len(key)==3:
         k=(key[0],key[1])
      else:
         k=key
      v=self.DateSums.get(k,0.0)
      self.TotalSum=self.TotalSum-v
      mvalue=value*self.MultiplyBy
      if aop==op_add:
         v=v+mvalue
      elif aop==op_sub:
         v=v-mvalue
      elif aop==op_mul:
         v=v*mvalue
      elif aop==op_div:
         try:
            if (mvalue<0.00001) and (mvalue>-0.00001):
               v=0.0
            else:
               v=float(v)/float(mvalue)
         except ZeroDivisionError:
            v=0.0
      elif aop==op_idiv:
         try:
            if (v<0.00001) and (v>-0.00001):
               v=0.0
            else:
               v=float(mvalue)/float(v)
         except ZeroDivisionError:
            v=0.0
      self.TotalSum=self.TotalSum+v
      self.DateSums[k]=v
   def Dodaj(self,value):
      for k in value.DateSums.keys():
         self.Update(k,value.DateSums[k])
      return self
   def Odejmij(self,value):
      for k in value.DateSums.keys():
         self.Update(k,value.DateSums[k],op_sub)
      return self
   def funcAvg(self):
      l=self.DateSums.values()
      al=len(filter(lambda x: x!=0.0,l))
      if al:
         return 1.0*reduce(lambda x,y:x+y,l)/al
      else:
         return 0.0
   def funcMax(self):
      l=self.DateSums.values()
      return 1.0*max(l)
   def funcMin(self):
      l=filter(lambda x: x!=0.0,self.DateSums.values())
      if l:
         return 1.0*min(l)
      else:
         return 0.0
   def __add__ (self, other):
      newsum=DateSum(afromsum=self)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_add)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_add)
      return newsum
   def __sub__ (self, other):
      newsum=DateSum(afromsum=self)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_sub)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_sub)
      return newsum
   def __mul__ (self, other):
      newsum=DateSum(afromsum=self)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_mul)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_mul)
      return newsum
   def __div__ (self, other):
      newsum=DateSum(afromsum=self)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_div)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_div)
      return newsum
   def __radd__ (self, other):
      newsum=DateSum(afromsum=self)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_add)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_add)
      return newsum
   def __rsub__ (self, other):
      newsum=DateSum(afromsum=self)
      for k in self.DateSums.keys():
         newsum.Update(k,-1,op_mul)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_add)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_add)
      return newsum
   def __rmul__ (self, other):
      newsum=DateSum(afromsum=self)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_mul)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_mul)
      return newsum
   def __rdiv__ (self, other):
      newsum=DateSum(afromsum=self)
      for k in self.DateSums.keys():
         newsum.Update(k,1,op_idiv)
      if isinstance(other,self.__class__):
         for k in other.DateSums.keys():
            newsum.Update(k,other.DateSums[k],op_mul)
      else:
         for k in self.DateSums.keys():
            newsum.Update(k,other,op_mul)
      return newsum
   def __neg__ (self):
      newsum=DateSum(afromsum=self)
      for k in self.DateSums.keys():
         newsum.Update(k,-1,op_mul)
      return newsum

   def __repr__(self):
      return str(self.TotalSum)
   def SetDateRange(self,adatefrom,adateto):
      if adatefrom>adateto:
         print 'DateFrom>DateTo:',adatefrom,adateto
         return
      r1,m1=adatefrom[0],adatefrom[1]
      r2,m2=adateto[0],adateto[1]
      while r1<r2:
         while m1<=12:
            if not self.DateSums.has_key((r1,m1)):
               self.DateSums[(r1,m1)]=0.0
            m1=m1+1
         r1,m1=r1+1,1
      while m1<m2:
         if not self.DateSums.has_key((r1,m1)):
            self.DateSums[(r1,m1)]=0.0
         m1=m1+1
   def GetDateRange(self):
      res=self.DateSums.keys()
      res.sort()
      return res
   def LoadFromField(self,adate,afield,aoid):
      v=afield.ValuesAsFloat(aoid)
      self.__setitem__(adate,v)

class FKFilter:
   def __init__(self,adimension,aparameters):
      self.Dimension=adimension
      self.Parameters=aparameters
      self.Name=''
      self.MultiplyBy=0.0
      self.DateFrom=ICORUtil.ZERO_DATE_D
      self.DateTo=ICORUtil.ZERO_DATE_D

      if 0:
         robj=self.ClassItem[self.OID].AccountRange
         self.AccountFrom=''
         if robj:
            self.AccountFrom=robj.FromAccount
            self.AccountTo=robj.ToAccount
            self.AccountMask=robj.AccountMask
            self.AccountInheritedMask=robj.AccountInheritedMask
            if self.AccountInheritedMask=='':
               self.AccountInheritedMask=aparameters['AccountInheritedMask']
         if self.AccountFrom=='' or not robj:
            self.AccountFrom=aparameters['AccountFrom']
            self.AccountTo=aparameters['AccountTo']
            self.AccountMask=''
            self.AccountInheritedMask=aparameters['AccountInheritedMask']

      self.AccountFrom=aparameters['AccountFrom']
      self.AccountTo=aparameters['AccountTo']
      self.AccountMask=''
      self.AccountInheritedMask=aparameters['AccountInheritedMask']

      self.ShowWn=aparameters['ShowWn']
      self.ShowMa=aparameters['ShowMa']
      self.ShowBOWn=aparameters['ShowBOWn']
      self.ShowBOMa=aparameters['ShowBOMa']
      self.ShowSaldoWn=aparameters['ShowSaldoWn']
      self.ShowSaldoMa=aparameters['ShowSaldoMa']
      self.ShowSaldoObrotyWn=aparameters['ShowSaldoObrotyWn']
      self.ShowSaldoObrotyMa=aparameters['ShowSaldoObrotyMa']
      self.ShowObrotyWn=aparameters['ShowObrotyWn']
      self.ShowObrotyMa=aparameters['ShowObrotyMa']
      if 0:
         sobj=self.ClassItem[self.OID].ShowWn
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowWn=1
            else:
               self.ShowWn=0
         sobj=self.ClassItem[self.OID].ShowMa
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowMa=1
            else:
               self.ShowMa=0
         sobj=self.ClassItem[self.OID].ShowBOWn
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowBOWn=1
            else:
               self.ShowBOWn=0
         sobj=self.ClassItem[self.OID].ShowBOMa
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowBOMa=1
            else:
               self.ShowBOMa=0
         sobj=self.ClassItem[self.OID].ShowSaldoWn
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowSaldoWn=1
            else:
               self.ShowSaldoWn=0
         sobj=self.ClassItem[self.OID].ShowSaldoMa
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowSaldoMa=1
            else:
               self.ShowSaldoMa=0
         sobj=self.ClassItem[self.OID].ShowSaldoObrotyWn
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowSaldoObrotyWn=1
            else:
               self.ShowSaldoObrotyWn=0
         sobj=self.ClassItem[self.OID].ShowSaldoObrotyMa
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowSaldoObrotyMa=1
            else:
               self.ShowSaldoObrotyMa=0
         sobj=self.ClassItem[self.OID].ShowObrotyWn
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowObrotyWn=1
            else:
               self.ShowObrotyWn=0
         sobj=self.ClassItem[self.OID].ShowObrotyMa
         if sobj:
            if sobj.Name in ['Tak','Yes','1','Show','Enable']:
               self.ShowObrotyMa=1
            else:
               self.ShowObrotyMa=0
   def PostProcess(self):
      if self.MultiplyBy==0.0:
         self.MultiplyBy=1.0
      if self.DateFrom==ICORUtil.ZERO_DATE_D:
         self.DateFrom=self.Parameters['DateFrom']
      if self.DateTo==ICORUtil.ZERO_DATE_D:
         self.DateTo=self.Parameters['DateTo']
      aparameters=self.Parameters
      aparameters['ShowWn']=self.ShowWn
      aparameters['ShowMa']=self.ShowMa
      aparameters['ShowBOWn']=self.ShowBOWn
      aparameters['ShowBOMa']=self.ShowBOMa
      aparameters['ShowSaldoWn']=self.ShowSaldoWn
      aparameters['ShowSaldoMa']=self.ShowSaldoMa
      aparameters['ShowSaldoObrotyWn']=self.ShowSaldoObrotyWn
      aparameters['ShowSaldoObrotyMa']=self.ShowSaldoObrotyMa
      aparameters['ShowObrotyWn']=self.ShowObrotyWn
      aparameters['ShowObrotyMa']=self.ShowObrotyMa

      aparameters['DateFrom']=self.DateFrom
      aparameters['DateTo']=self.DateTo
      aparameters['AccountFrom']=self.AccountFrom
      aparameters['AccountTo']=self.AccountTo
      aparameters['AccountMask']=self.AccountMask
      aparameters['AccountInheritedMask']=self.AccountInheritedMask

      self.SumBOWn=DateSum(amultiplyby=self.MultiplyBy)
      self.SumBOMa=DateSum(amultiplyby=self.MultiplyBy)
      self.SumWn=DateSum(amultiplyby=self.MultiplyBy)
      self.SumMa=DateSum(amultiplyby=self.MultiplyBy)

   def GetShowString(self):
      s=''
      if self.ShowWn:
         s=s+' Wn'
      if self.ShowMa:
         s=s+' Ma'
      if self.ShowBOWn:
         s=s+' BOWn'
      if self.ShowBOMa:
         s=s+' BOMa'
      if self.ShowObrotyWn:
         s=s+' ObrotyWn'
      if self.ShowObrotyMa:
         s=s+' ObrotyMa'
      if self.ShowSaldoWn:
         s=s+' SaldoWn'
      if self.ShowSaldoMa:
         s=s+' SaldoMa'
      if self.ShowSaldoObrotyWn:
         s=s+' SaldoObrotyWn'
      if self.ShowSaldoObrotyMa:
         s=s+' SaldoObrotyMa'
      return s
   def __repr__(self):
      x=(self.Name,)+self.DateFrom+self.DateTo+(self.AccountFrom,self.AccountTo,self.AccountMask,self.AccountInheritedMask,self.GetShowString())
      s='Filter: %s Od: %d/%d/%d Do: %d/%d/%d OdKodu: %s DoKodu: %s Maska: %s MaskaI: %s %s'%x
      return s
   def InitDane(self):
      if self.AccountMask:
         self.rMask=re.compile(self.AccountMask,re.I)
      else:
         self.rMask=None
      if self.AccountInheritedMask:
         self.rMaskI=re.compile(self.AccountInheritedMask,re.I)
      else:
         self.rMaskI=None
      if self.AccountFrom!='' and self.AccountTo=='':
         self.AccountTo=ICORUtil.IncNumString(self.AccountFrom)
   def CheckFK(self,nrkonta,rdata):
      if nrkonta<self.AccountFrom or nrkonta>=self.AccountTo:
         return 0
      if self.rMask:
         if not self.rMask.match(nrkonta):
            return 0
      if self.rMaskI:
         if not self.rMaskI.match(nrkonta):
            return 0
      if rdata<self.DateFrom or rdata>=self.DateTo:
         return 0
      return 1
   def AcceptWn(self,kwota,adata):
      self.SumWn[adata]=kwota
   def AcceptBOWn(self,kwota,adata):
      self.SumBOWn[adata]=kwota
   def AcceptMa(self,kwota,adata):
      self.SumMa[adata]=kwota
   def AcceptBOMa(self,kwota,adata):
      self.SumBOMa[adata]=kwota
   def Dump(self,aindent=0):
      print '%sFilter: %s'%(' '*aindent,self.Name)
      x=(' '*(aindent+3),)+self.DateFrom+self.DateTo+(self.GetShowString(),)
      print '%sOd: %d/%d/%d Do: %d/%d/%d, %s'%x
      print '%sOdKodu: %s DoKodu: %s Maska: %s MaskaI: %s'%(' '*(aindent+3),self.AccountFrom,self.AccountTo,self.AccountMask,self.AccountInheritedMask)

class QueryDimension:
   def __init__(self,aparentdimension,aquery,aparameters,aonecolumnonly=0):
      self.ParentDimension=aparentdimension
      self.Query=aquery
      if self.ParentDimension is None:
         aparentdimension=self.Query
      aparentdimension.Dimensions.append(self)
      self.Parameters=aparameters
      self.Name=''
      self.FormulaName=''
      self.FormulaText=''
      self.OneColumnOnly=aonecolumnonly
      self.TotalName=''
      self.IsFramed=0
      self.IsItalic=0
      self.IsTotalBold=0
      self.IsTotalBiggerFont=0
      self.IsBold=0
      self.IsTotalDoubleFrameAfter=0
      self.FrameSize=''
      self.FirstNDate=0
      self.LastNDate=0
      self.DisableTitle=0
      self.DisableTotal=0
      self.DisableInheritance=0
      self.DisplayValueModifier=0.0
      self.EmptyRowBefore=0
      self.EmptyRowBeforeTotal=0
      self.FramedTotal=0 #UWAGA! Not
      self.FrameBegin=0
      self.FrameEnd=0
      self.RowTotalFunction='sum'
      self.TitleCenteredFramed=0
      self.NumberFormatDecimals=-1
      self.NumberFormatText=''
      if self.ParentDimension:
         self.ShowWn,self.ShowMa,self.ShowBOWn,self.ShowBOMa,self.ShowSaldoWn,self.ShowSaldoMa,self.ShowObrotyWn,self.ShowObrotyMa,self.ShowSaldoObrotyWn,self.ShowSaldoObrotyMa=self.ParentDimension.ShowWn,aparentdimension.ShowMa,aparentdimension.ShowBOWn,aparentdimension.ShowBOMa,aparentdimension.ShowSaldoWn,aparentdimension.ShowSaldoMa,aparentdimension.ShowObrotyWn,aparentdimension.ShowObrotyMa,aparentdimension.ShowSaldoObrotyWn,aparentdimension.ShowSaldoObrotyMa
      else:
         self.ShowWn,self.ShowMa,self.ShowBOWn,self.ShowBOMa,self.ShowSaldoWn,self.ShowSaldoMa,self.ShowObrotyWn,self.ShowObrotyMa,self.ShowSaldoObrotyWn,self.ShowSaldoObrotyMa=0,0,0,0,0,0,0,0,0,0
      self.ShowSubDimensions=aparameters['ShowSubDimensions']

      self.SumBOWn=DateSum()
      self.SumBOMa=DateSum()
      self.SumWn=DateSum()
      self.SumMa=DateSum()

      self.SumSingle=DateSum()
      self.SumFormula=DateSum()

      aparameters.PushAll()
      self.Dimensions=[]
      self.FKFilters=[]
      self.ThisFilter=None
   def PostProcess(self):
      if not self.TotalName:
         self.TotalName=self.Query.TotalColumnName+self.Name
      if not self.FrameSize:
         self.FrameSize='.5pt hairline'
      if self.DisplayValueModifier==0.0:
         self.DisplayValueModifier=1.0
      if self.FrameBegin:
         self.FrameDrawing=1
         self.Query.FrameDrawing=1
      else:
         self.FrameDrawing=self.Query.FrameDrawing
      if self.FrameEnd:
         self.FrameDrawing=0
         self.Query.FrameDrawing=0
      self.Parameters['ShowSubDimensions']=self.ShowSubDimensions

      for adimension in self.Dimensions:
         self.ShowWn=self.ShowWn or adimension.ShowWn
         self.ShowMa=self.ShowMa or adimension.ShowMa
         self.ShowBOWn=self.ShowBOWn or adimension.ShowBOWn
         self.ShowBOMa=self.ShowBOMa or adimension.ShowBOMa
         self.ShowSaldoWn=self.ShowSaldoWn or adimension.ShowSaldoWn
         self.ShowSaldoMa=self.ShowSaldoMa or adimension.ShowSaldoMa
         self.ShowSaldoObrotyWn=self.ShowSaldoObrotyWn or adimension.ShowSaldoObrotyWn
         self.ShowSaldoObrotyMa=self.ShowSaldoObrotyMa or adimension.ShowSaldoObrotyMa
         self.ShowObrotyWn=self.ShowObrotyWn or adimension.ShowObrotyWn
         self.ShowObrotyMa=self.ShowObrotyMa or adimension.ShowObrotyMa

      for afkfilter in self.FKFilters:
         self.ShowWn=self.ShowWn or afkfilter.ShowWn
         self.ShowMa=self.ShowMa or afkfilter.ShowMa
         self.ShowBOWn=self.ShowBOWn or afkfilter.ShowBOWn
         self.ShowBOMa=self.ShowBOMa or afkfilter.ShowBOMa
         self.ShowSaldoWn=self.ShowSaldoWn or afkfilter.ShowSaldoWn
         self.ShowSaldoMa=self.ShowSaldoMa or afkfilter.ShowSaldoMa
         self.ShowSaldoObrotyWn=self.ShowSaldoObrotyWn or afkfilter.ShowSaldoObrotyWn
         self.ShowSaldoObrotyMa=self.ShowSaldoObrotyMa or afkfilter.ShowSaldoObrotyMa
         self.ShowObrotyWn=self.ShowObrotyWn or afkfilter.ShowObrotyWn
         self.ShowObrotyMa=self.ShowObrotyMa or afkfilter.ShowObrotyMa

      if self.Dimensions==[]:
         for afkfilter in self.FKFilters:
            self.Query.SRIterator.AddRange(afkfilter.AccountFrom,afkfilter.AccountTo,afkfilter)
      self.Parameters.PopAll()
      self._depth=0
   def AddFilter(self):
      self.ThisFilter=FKFilter(self,self.Query.Parameters)
      self.FKFilters.append(self.ThisFilter)
   def Depth(self):
      if not self._depth:
         md=0
         if self.ShowSubDimensions:
            for adimension in self.Dimensions:
               md=adimension.Depth()
               if md>self._depth:
                  self._depth=md
         self._depth=self._depth+1
      return self._depth
   def GetNumColsCount(self):
      if self.OneColumnOnly:
         return 1
      return self.CShowWn+self.CShowMa+self.CShowBOWn+self.CShowBOMa+self.CShowSaldoWn+self.CShowSaldoMa+self.CShowSaldoObrotyWn+self.CShowSaldoObrotyMa+self.CShowObrotyWn+self.CShowObrotyMa
   def GetNumDatesList(self):
      l=self.SumBOWn.DateSums.keys()
      l.sort()
      return l
   def CalculateSumAll(self,aobject):
      if aobject.ShowBOWn or aobject.ShowSaldoWn or aobject.ShowSaldoMa or aobject.ShowSaldoObrotyWn or aobject.ShowSaldoObrotyMa:
         self.SumBOWn.Dodaj(aobject.SumBOWn)
      if aobject.ShowBOMa or aobject.ShowSaldoWn or aobject.ShowSaldoMa or aobject.ShowSaldoObrotyWn or aobject.ShowSaldoObrotyMa:
         self.SumBOMa.Dodaj(aobject.SumBOMa)
      if aobject.ShowWn or aobject.ShowObrotyWn or aobject.ShowSaldoWn or aobject.ShowSaldoMa or aobject.ShowSaldoObrotyWn or aobject.ShowSaldoObrotyMa:
         self.SumWn.Dodaj(aobject.SumWn)
      if aobject.ShowMa or aobject.ShowObrotyMa or aobject.ShowSaldoWn or aobject.ShowSaldoMa or aobject.ShowSaldoObrotyWn or aobject.ShowSaldoObrotyMa:
         self.SumMa.Dodaj(aobject.SumMa)
   def CalculateSumSingle(self,aobject):
      if aobject.ShowWn:
         self.SumSingle.Dodaj(aobject.SumWn)
      if aobject.ShowMa:
         self.SumSingle.Dodaj(aobject.SumMa)
      if aobject.ShowBOWn:
         self.SumSingle.Dodaj(aobject.SumBOWn)
      if aobject.ShowBOMa:
         self.SumSingle.Dodaj(aobject.SumBOMa)
      if aobject.ShowObrotyWn:
         self.SumSingle.Dodaj(aobject.SumWn)
         self.SumSingle.Dodaj(aobject.SumBOWn)
      if aobject.ShowObrotyMa:
         self.SumSingle.Dodaj(aobject.SumMa)
         self.SumSingle.Dodaj(aobject.SumBOMa)
      if aobject.ShowSaldoWn:
         self.SumSingle.Dodaj(aobject.SumWn)
         self.SumSingle.Odejmij(aobject.SumMa)
      if aobject.ShowSaldoMa:
         self.SumSingle.Dodaj(aobject.SumMa)
         self.SumSingle.Odejmij(aobject.SumWn)
      if aobject.ShowSaldoObrotyWn:
         self.SumSingle.Dodaj(aobject.SumWn)
         self.SumSingle.Dodaj(aobject.SumBOWn)
         self.SumSingle.Odejmij(aobject.SumMa)
         self.SumSingle.Odejmij(aobject.SumBOMa)
      if aobject.ShowSaldoObrotyMa:
         self.SumSingle.Dodaj(aobject.SumMa)
         self.SumSingle.Dodaj(aobject.SumBOMa)
         self.SumSingle.Odejmij(aobject.SumWn)
         self.SumSingle.Odejmij(aobject.SumBOWn)
   def CalculateSums(self,gmindate,gmaxdate,vdict):
      self.SumBOWn.SetDateRange(gmindate,gmaxdate)
      self.SumBOMa.SetDateRange(gmindate,gmaxdate)
      self.SumWn.SetDateRange(gmindate,gmaxdate)
      self.SumMa.SetDateRange(gmindate,gmaxdate)
      self.SumSingle.SetDateRange(gmindate,gmaxdate)
      for afkfilter in self.FKFilters:
         self.CalculateSumAll(afkfilter)
         self.CalculateSumSingle(afkfilter)
      self.CalculateFormulas(vdict)
      self.SumSingle.Dodaj(self.SumFormula)
      for adimension in self.Dimensions:
         adimension.CalculateSums(gmindate,gmaxdate,vdict)
         if not adimension.DisableInheritance:
            self.CalculateSumAll(adimension)
            if self.OneColumnOnly:
               self.SumSingle.Dodaj(adimension.SumSingle)
            else:
               self.SumFormula.Dodaj(adimension.SumFormula)
               self.SumSingle.Dodaj(adimension.SumFormula)
               self.CalculateSumSingle(adimension)
#      self.UpdateSumValues()
   def UpdateSumValues(self):
      dates=self.SumWn.GetDateRange()
      arefs=self.ClassItem.Values.GetRefList(self.OID)
      for adate in dates:
         cdate=adate+(1,0,0,0,0)
         pos,find=arefs.FindRefByValue(self.ValuesClass.FromDate,cdate,asorted=1)
         if not find:
            aoid=self.ValuesClass.AddObject()
            self.ValuesClass.FromDate.SetValuesAsDate(aoid,adate+(1,))
            self.ValuesClass.Dimension[aoid]=str(self.OID)+':'+str(self.ClassItem.CID)+':'
         else:
            aoid=arefs[pos][0]
         self.ValuesClass.SumMa[aoid]=str(self.SumMa[adate])
         self.ValuesClass.SumWn[aoid]=str(self.SumWn[adate])
         self.ValuesClass.SumBOMa[aoid]=str(self.SumBOMa[adate])
         self.ValuesClass.SumBOWn[aoid]=str(self.SumBOWn[adate])
         self.ValuesClass.SumSingle[aoid]=str(self.SumSingle[adate])
         if not find:
            arefs.InsertRefEx(self.ValuesClass.FromDate,aoid,self.ValuesClass.CID)
#      print 'US:',self.OID,arefs.AsString()
      self.ClassItem.Values.SetRefList(self.OID,arefs)
   def CalculateFormulas(self,vdict):
      if self.FormulaName:
         vdict[self.FormulaName]=self.SumSingle
      if self.FormulaText:
         try:
            res=eval(self.FormulaText,vdict)
            if isinstance(res,DateSum):
#               print '   result:',res.DateSums[(2000,1)]
               self.SumFormula=res
            else:
#               print '   result value:',res
               self.SumFormula.__add__(res)
#            print '   sumsingle:',self.SumSingle.DateSums[(2000,1)]
         except:
            print 'wyst�pi� b��d podczas obliczania formu�y:',self.FormulaText
            print 'dla warto�ci:'
            for akey,avalue in vdict.items():
               if isinstance(avalue,DateSum):
                  print '  ',akey,avalue.DateSums
            raise
   def SetShowColumns(self,aparentdimension=None):
      if aparentdimension:
         self.CShowWn,self.CShowMa,self.CShowBOWn,self.CShowBOMa,self.CShowSaldoWn,self.CShowSaldoMa,self.CShowObrotyWn,self.CShowObrotyMa,self.CShowSaldoObrotyWn,self.CShowSaldoObrotyMa=aparentdimension.CShowWn,aparentdimension.CShowMa,aparentdimension.CShowBOWn,aparentdimension.CShowBOMa,aparentdimension.CShowSaldoWn,aparentdimension.CShowSaldoMa,aparentdimension.CShowObrotyWn,aparentdimension.CShowObrotyMa,aparentdimension.CShowSaldoObrotyWn,aparentdimension.CShowSaldoObrotyMa
      else:
         self.CShowWn,self.CShowMa,self.CShowBOWn,self.CShowBOMa,self.CShowSaldoWn,self.CShowSaldoMa,self.CShowObrotyWn,self.CShowObrotyMa,self.CShowSaldoObrotyWn,self.CShowSaldoObrotyMa=self.ShowWn,self.ShowMa,self.ShowBOWn,self.ShowBOMa,self.ShowSaldoWn,self.ShowSaldoMa,self.ShowObrotyWn,self.ShowObrotyMa,self.ShowSaldoObrotyWn,self.ShowSaldoObrotyMa
      for adimension in self.Dimensions:
         adimension.SetShowColumns(self)
   def GetShowString(self):
      s=''
      if self.ShowWn:
         s=s+' Wn'
      if self.ShowMa:
         s=s+' Ma'
      if self.ShowBOWn:
         s=s+' BOWn'
      if self.ShowBOMa:
         s=s+' BOMa'
      if self.ShowObrotyWn:
         s=s+' ObrotyWn'
      if self.ShowObrotyMa:
         s=s+' ObrotyMa'
      if self.ShowSaldoWn:
         s=s+' SaldoWn'
      if self.ShowSaldoMa:
         s=s+' SaldoMa'
      if self.ShowSaldoObrotyWn:
         s=s+' SaldoObrotyWn'
      if self.ShowSaldoObrotyMa:
         s=s+' SaldoObrotyMa'
      return s
   def Dump(self,aindent=0):
      if self.ShowSubDimensions:
         sv=' - Visible'
      else:
         sv=' - Not visible'
      print '%sSubDimension: %s%s'%(' '*aindent,self.Name,sv),self.GetShowString()
      for afkfilter in self.FKFilters:
         afkfilter.Dump(aindent+3)
      for adimension in self.Dimensions:
         adimension.Dump(aindent+3)
   def DumpSums(self,aindent=0):
      if self.ShowSubDimensions:
         sv=' - Visible'
      else:
         sv=' - Not visible'
      print '%sSubDimension: %s%s - %d'%(' '*aindent,self.Name,sv,aindent)
      print '%s       WN   |     MA   |   BOWn   |   BOMa   | SaldoWn  | SaldoMa  |  Single  | Formula  |'%(' '*aindent,)
      s='%s  %10.2f|%10.2f|%10.2f|%10.2f|%10.2f|%10.2f|%10.2f|%10.2f|'%(' '*aindent,self.SumWn.TotalSum,self.SumMa.TotalSum,self.SumBOWn.TotalSum,self.SumBOMa.TotalSum,self.SumWn.TotalSum-self.SumMa.TotalSum,self.SumMa.TotalSum-self.SumWn.TotalSum,self.SumSingle.TotalSum,self.SumFormula.TotalSum)
      print s
      for adimension in self.Dimensions:
         adimension.DumpSums(aindent+3)
   def DumpFileXML(self,file,aindent=0):
      file.write('%s<zestawienie>\n'%(' '*aindent,))
      file.write('%s<nazwa>%s</nazwa>\n'%(' '*aindent,GetAsXMLString(self.Name)))
      file.write('%s<sumawn>%s</sumawn>\n'%(' '*aindent,self.SumWn))
      file.write('%s<sumama>%s</sumama>\n'%(' '*aindent,self.SumMa))
      file.write('%s<sumabown>%s</sumabown>\n'%(' '*aindent,self.SumBOWn))
      file.write('%s<sumaboma>%s</sumaboma>\n'%(' '*aindent,self.SumBOMa))
      file.write('%s<zestawienia>\n'%(' '*aindent,))
      if self.ShowSubDimensions:
         for adimension in self.Dimensions:
            adimension.DumpFileXML(file,aindent+3)
      file.write('%s</zestawienia>\n'%(' '*aindent,))
      file.write('%s</zestawienie>\n'%(' '*aindent,))
      return
   def WriteSumsHeader(self,file,sclass='objectsviewheader'):
      if self.OneColumnOnly:
         return
      if self.CShowWn:
         file.write('<td align=center class=%s>Wn</td>\n'%(sclass,))
      if self.CShowMa:
         file.write('<td align=center class=%s>Ma</td>\n'%(sclass,))
      if self.CShowBOWn:
         file.write('<td align=center class=%s>BOWn</td>\n'%(sclass,))
      if self.CShowBOMa:
         file.write('<td align=center class=%s>BOMa</td>\n'%(sclass,))
      if self.CShowObrotyWn:
         file.write('<td align=center class=%s>ObrotyWn</td>\n'%(sclass,))
      if self.CShowObrotyMa:
         file.write('<td align=center class=%s>ObrotyMa</td>\n'%(sclass,))
      if self.CShowSaldoWn:
         file.write('<td align=center class=%s>SaldoWn</td>\n'%(sclass,))
      if self.CShowSaldoMa:
         file.write('<td align=center class=%s>SaldoMa</td>\n'%(sclass,))
      if self.CShowSaldoObrotyWn:
         file.write('<td align=center class=%s>SaldoObrotyWn</td>\n'%(sclass,))
      if self.CShowSaldoObrotyMa:
         file.write('<td align=center class=%s>SaldoObrotyMa</td>\n'%(sclass,))

   def WriteHTMLDataRow(self,file,adate,aclass='objectsviewtabledataeven',abold=0,aitalic=0,afont=0):
      dwidth=77
      sa1,sa2='',''
      if abold:
         sa1='<b>'
         sa2='</b>'
      if aitalic:
         sa1=sa1+'<i>'
         sa2='</i>'+sa2
      if afont>100:
         sa1=sa1+'<font size="+%d">'%(afont)
         sa2='</font>'+sa2

      if self.OneColumnOnly:
         sum=self.SumSingle[adate]
#         sum=0.0
#         if self.ShowWn:
#            sum=sum+self.SumWn[adate]
#         if self.ShowMa:
#            sum=sum+self.SumMa[adate]
#         if self.ShowBOWn:
#            sum=sum+self.SumBOWn[adate]
#         if self.ShowBOMa:
#            sum=sum+self.SumBOMa[adate]
#         if self.ShowObrotyWn:
#            sum=sum+self.SumWn[adate]+self.SumBOWn[adate]
#         if self.ShowObrotyMa:
#            sum=sum+self.SumMa[adate]+self.SumBOMa[adate]
#         if self.ShowSaldoWn:
#            sum=sum+self.SumWn[adate]-self.SumMa[adate]
#         if self.ShowSaldoMa:
#            sum=sum+self.SumMa[adate]-self.SumWn[adate]
#         if self.ShowSaldoObrotyWn:
#            sum=sum+self.SumWn[adate]+self.SumBOWn[adate]-self.SumMa[adate]-self.SumBOMa[adate]
#         if self.ShowSaldoObrotyMa:
#            sum=sum+self.SumMa[adate]+self.SumBOMa[adate]-self.SumWn[adate]-self.SumBOWn[adate]
         file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(sum,self.Query.FNumFormat),sa2))
      else:
         if self.ShowWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn[adate],self.Query.FNumFormat),sa2))
         elif self.CShowWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa[adate],self.Query.FNumFormat),sa2))
         elif self.CShowMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowBOWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumBOWn[adate],self.Query.FNumFormat),sa2))
         elif self.CShowBOWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowBOMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumBOMa[adate],self.Query.FNumFormat),sa2))
         elif self.CShowBOMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowObrotyWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn[adate]+self.SumBOWn[adate],self.Query.FNumFormat),sa2))
         elif self.CShowObrotyWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowObrotyMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa[adate]+self.SumBOMa[adate],self.Query.FNumFormat),sa2))
         elif self.CShowObrotyMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowSaldoWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn[adate]-self.SumMa[adate],self.Query.FNumFormat),sa2))
         elif self.CShowSaldoWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowSaldoMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa[adate]-self.SumWn[adate],self.Query.FNumFormat),sa2))
         elif self.CShowSaldoMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowSaldoObrotyWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn[adate]+self.SumBOWn[adate]-self.SumMa[adate]-self.SumBOMa[adate],self.Query.FNumFormat),sa2))
         elif self.CShowSaldoObrotyWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))
   
         if self.ShowSaldoObrotyMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa[adate]+self.SumBOMa[adate]-self.SumWn[adate]-self.SumBOWn[adate],self.Query.FNumFormat),sa2))
         elif self.CShowSaldoObrotyMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(0.0,self.Query.FNumFormat),sa2))

   def CheckTotalSum(self):
      if self.OneColumnOnly:
         sum=self.SumSingle.TotalSum
      else:
         sum=0.0
         if self.ShowWn:
            sum=sum+self.SumWn.TotalSum
         if self.ShowMa:
            sum=sum+self.SumMa.TotalSum
         if self.ShowBOWn:
            sum=sum+self.SumBOWn.TotalSum
         if self.ShowBOMa:
            sum=sum+self.SumBOMa.TotalSum
         if self.ShowObrotyWn:
            sum=sum+self.SumWn.TotalSum+self.SumBOWn.TotalSum
         if self.ShowObrotyMa:
            sum=sum+self.SumMa.TotalSum+self.SumBOMa.TotalSum
         if self.ShowSaldoWn:
            sum=sum+self.SumWn.TotalSum-self.SumMa.TotalSum
         if self.ShowSaldoMa:
            sum=sum+self.SumMa.TotalSum-self.SumWn.TotalSum
         if self.ShowSaldoObrotyWn:
            sum=sum+self.SumWn.TotalSum+self.SumBOWn.TotalSum-self.SumMa.TotalSum-self.SumBOMa.TotalSum
         if self.ShowSaldoObrotyMa:
            sum=sum+self.SumMa.TotalSum+self.SumBOMa.TotalSum-self.SumWn.TotalSum-self.SumBOWn.TotalSum
      return sum
   def WriteHTMLTotalDataRow(self,file,adate,aclass='objectsviewtabledataeven',abold=0,aitalic=0,afont=0):
      dwidth=88
      sa1,sa2='',''
      if abold:
         sa1='<b>'
         sa2='</b>'
      if aitalic:
         sa1=sa1+'<i>'
         sa2='</i>'+sa2
      if afont>100:
         sa1=sa1+'<font size="+%d">'%(afont)
         sa2='</font>'+sa2
      if self.OneColumnOnly:
         sum=self.SumSingle.TotalSum
#         sum=0.0
#         if self.ShowWn:
#            sum=sum+self.SumWn.TotalSum
#         if self.ShowMa:
#            sum=sum+self.SumMa.TotalSum
#         if self.ShowBOWn:
#            sum=sum+self.SumBOWn.TotalSum
#         if self.ShowBOMa:
#            sum=sum+self.SumBOMa.TotalSum
#         if self.ShowObrotyWn:
#            sum=sum+self.SumWn.TotalSum+self.SumBOWn.TotalSum
#         if self.ShowObrotyMa:
#            sum=sum+self.SumMa.TotalSum+self.SumBOMa.TotalSum
#         if self.ShowSaldoWn:
#            sum=sum+self.SumWn.TotalSum-self.SumMa.TotalSum
#         if self.ShowSaldoMa:
#            sum=sum+self.SumMa.TotalSum-self.SumWn.TotalSum
#         if self.ShowSaldoObrotyWn:
#            sum=sum+self.SumWn.TotalSum+self.SumBOWn.TotalSum-self.SumMa.TotalSum-self.SumBOMa.TotalSum
#         if self.ShowSaldoObrotyMa:
#            sum=sum+self.SumMa.TotalSum+self.SumBOMa.TotalSum-self.SumWn.TotalSum-self.SumBOWn.TotalSum
         file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(sum,self.Query.FNumFormat),sa2))
      else:
         if self.CShowWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowBOWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumBOWn.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowBOMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumBOMa.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowObrotyWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn.TotalSum+self.SumBOWn.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowObrotyMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa.TotalSum+self.SumBOMa.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowSaldoWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn.TotalSum-self.SumMa.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowSaldoMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa.TotalSum-self.SumWn.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowSaldoObrotyWn:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumWn.TotalSum+self.SumBOWn.TotalSum-self.SumMa.TotalSum-self.SumBOMa.TotalSum,self.Query.FNumFormat),sa2))
         if self.CShowSaldoObrotyMa:
            file.write('<td width="%d" align="right" class=%s NOWRAP>%s%s%s</td>\n'%(dwidth,aclass,sa1,ICORUtil.FormatFNumHTML(self.SumMa.TotalSum+self.SumBOMa.TotalSum-self.SumWn.TotalSum-self.SumBOWn.TotalSum,self.Query.FNumFormat),sa2))

   def DumpFileHTML(self,file,ndates,aindent=0):
      if self.Query.HideEmptyDimensions and self.CheckTotalSum()==0.0:
         return 0
#         file.write('%s\n'%(' '*aindent,))
      file.write('<tr>\n')

      if self.Depth()==1:
         file.write('<td class=objectsviewdataeven NOWRAP>%s%s</td>'%('&nbsp;'*aindent,self.Name,))
         for adate in ndates:
            self.WriteHTMLDataRow(file,adate,'objectsviewtabledataeven')
         self.WriteHTMLTotalDataRow(file,adate,'objectsviewtabledataeven')
      else:
         file.write('<td colspan=%d class=objectsviewdatasubsection NOWRAP align=left>%s%s<td>\n'%(1+(len(ndates)+1)*self.GetNumColsCount(),'&nbsp;'*aindent,self.Name))
      file.write('</tr>\n')
      if self.ShowSubDimensions:
         for adimension in self.Dimensions:
            adimension.DumpFileHTML(file,ndates,aindent+5)
      if self.Depth()>1:
         file.write('<tr>\n')
         if aindent==0:
            sa1,sa2,fs='<font size="+1">','</font>',1
         else:
            sa1,sa2,fs='','',0
         file.write('<td class=objectsviewdatasubsectionsummary NOWRAP>%s<B>%sRAZEM:%s</B></td>'%('&nbsp;'*aindent,sa1,sa2))
         for adate in ndates:
            self.WriteHTMLDataRow(file,adate,'objectsviewdatasubsectionsummary',1,aindent==0,fs)
         self.WriteHTMLTotalDataRow(file,adate,'objectsviewdatasubsectionsummary',1,aindent==0,fs)
         file.write('</tr>\n')
      return 1
   def GetModifiedValueAsString(self,sum):
      adecimalsadd=0
      if self.NumberFormatText=='%':
         adecimalsadd=2
      if sum==0.0:
         if self.Query.NoZeroValues:
            ssum=''
         else:
            if self.Query.NoDecimals:
               ssum=''
            elif self.NumberFormatDecimals<0:
               ssum=''
            else:
               ssum='0.'+'0'*self.NumberFormatDecimals
      elif self.NumberFormatDecimals<0:
         if self.Query.NoDecimals:
            ssum=str(round(sum*self.DisplayValueModifier,0+adecimalsadd))
         else:
            ssum=str(round(sum*self.DisplayValueModifier,2+adecimalsadd))
      else:
         ssum=str(round(sum*self.DisplayValueModifier,self.NumberFormatDecimals+adecimalsadd))
      return ssum
   def GetTitleCellStyle(self):
#      st='border-left:%s windowtext;border-right:%s windowtext;'%(self.FrameSize,self.FrameSize)
      st=''
      if self.FrameBegin:
         st='border-top:%s windowtext;'%(self.FrameSize,)
      if self.FrameEnd:
         st=st+'border-bottom:%s windowtext;'%(self.FrameSize,)
      if self.IsBold:
         st=st+'FONT-WEIGHT: bold;'
      if self.IsItalic:
         st=st+'FONT-STYLE: italic;'
      if st:
         st='style="%s" '%(st,)
      return st
   def GetNumStandard(self):
      sfnum='Standard'
      if self.NumberFormatDecimals<0:
         if self.Query.NoDecimals:
            adecimals=0
         else:
            adecimals=2
      else:
         adecimals=self.NumberFormatDecimals
      aformattext=''
      if self.NumberFormatText:
         aformattext='\\'+self.NumberFormatText
      if adecimals>0:
         sdecimals='0'*adecimals
         sfnum='"\\#\\,\\#\\#0\\.%s%s\\;\\[Red\\]\\-\\#\\,\\#\\#0\\.%s%s"'%(sdecimals,aformattext,sdecimals,aformattext)
      else:
         sfnum='"\\#\\,\\#\\#0%s\\;\\[Red\\]\\-\\#\\,\\#\\#0%s"'%(aformattext,aformattext)
      return sfnum
   def GetNumCellStyle(self):
      st=''
      if self.FrameBegin:
         st='border-top:%s windowtext;'%(self.FrameSize,)
      if self.FrameEnd:
         st=st+'border-bottom:%s windowtext;'%(self.FrameSize,)
      if self.IsBold:
         st=st+'FONT-WEIGHT: bold;'
      if self.IsItalic:
         st=st+'FONT-STYLE: italic;'
      sfnum=self.GetNumStandard()
      if sfnum:
         st=st+'mso-number-format:%s;'%sfnum
      if st:
         st="style='%s' "%(st,)
      return st
   def GetNumFramedTotalStyle(self):
      st=''
      if self.FirstNDate:
         st=st+'border-left:%s windowtext;'%(self.FrameSize,)
      else:
         st=st+'border-left:.5pt hairline windowtext;'
      if self.LastNDate:
         st=st+'border-right:%s windowtext;'%(self.FrameSize,)
      else:
         st=st+'border-right:.5pt hairline windowtext;'
      if not self.FramedTotal:
         st=st+'border-top:%s windowtext;'%(self.FrameSize,)
         if self.IsTotalDoubleFrameAfter:
            st=st+'border-bottom:2.0pt double windowtext;'
         else:
            st=st+'border-bottom:%s windowtext;'%(self.FrameSize,)
      if self.IsBold:
         st=st+'FONT-WEIGHT: bold;'
      if self.IsItalic:
         st=st+'FONT-STYLE: italic;'
      sfnum=self.GetNumStandard()
      if sfnum:
         st=st+'mso-number-format:%s;'%sfnum
      if st:
         st="style='%s' "%(st,)
      return st
   def WriteExcelDataRow(self,file,adate,aclass='xl2506587',astyle=''):
      sum=self.SumSingle[adate]
#      sum=0.0
#      if self.ShowWn:
#         sum=sum+self.SumWn[adate]
#      if self.ShowMa:
#         sum=sum+self.SumMa[adate]
#      if self.ShowBOWn:
#         sum=sum+self.SumBOWn[adate]
#      if self.ShowBOMa:
#         sum=sum+self.SumBOMa[adate]
#      if self.ShowObrotyWn:
#         sum=sum+self.SumWn[adate]+self.SumBOWn[adate]
#      if self.ShowObrotyMa:
#         sum=sum+self.SumMa[adate]+self.SumBOMa[adate]
#      if self.ShowSaldoWn:
#         sum=sum+self.SumWn[adate]-self.SumMa[adate]
#      if self.ShowSaldoMa:
#         sum=sum+self.SumMa[adate]-self.SumWn[adate]
#      if self.ShowSaldoObrotyWn:
#         sum=sum+self.SumWn[adate]+self.SumBOWn[adate]-self.SumMa[adate]-self.SumBOMa[adate]
#      if self.ShowSaldoObrotyMa:
#         sum=sum+self.SumMa[adate]+self.SumBOMa[adate]-self.SumWn[adate]-self.SumBOWn[adate]
      ssum=self.GetModifiedValueAsString(sum)
      file.write("<td class=%s align=right %s x:num >%s</td>\n"%(aclass,astyle,ssum)) #ICORUtil.FormatFNumHTML(sum,self.Query.FNumFormat)

   def WriteExcelTotalDataRow(self,file,adate,aclass='xl2506587',astyle=''):
      dwidth=88
      if self.RowTotalFunction=='sum':
         ssum=self.GetModifiedValueAsString(self.SumSingle.TotalSum)
      elif self.RowTotalFunction=='avg':
         ssum=self.GetModifiedValueAsString(self.SumSingle.funcAvg())
      elif self.RowTotalFunction=='max':
         ssum=self.GetModifiedValueAsString(self.SumSingle.funcMax())
      elif self.RowTotalFunction=='min':
         ssum=self.GetModifiedValueAsString(self.SumSingle.funcMin())
      elif self.RowTotalFunction=='off':
         ssum=''
#      sum=0.0
#      if self.ShowWn:
#         sum=sum+self.SumWn.TotalSum
#      if self.ShowMa:
#         sum=sum+self.SumMa.TotalSum
#      if self.ShowBOWn:
#         sum=sum+self.SumBOWn.TotalSum
#      if self.ShowBOMa:
#         sum=sum+self.SumBOMa.TotalSum
#      if self.ShowObrotyWn:
#         sum=sum+self.SumWn.TotalSum+self.SumBOWn.TotalSum
#      if self.ShowObrotyMa:
#         sum=sum+self.SumMa.TotalSum+self.SumBOMa.TotalSum
#      if self.ShowSaldoWn:
#         sum=sum+self.SumWn.TotalSum-self.SumMa.TotalSum
#      if self.ShowSaldoMa:
#         sum=sum+self.SumMa.TotalSum-self.SumWn.TotalSum
#      if self.ShowSaldoObrotyWn:
#         sum=sum+self.SumWn.TotalSum+self.SumBOWn.TotalSum-self.SumMa.TotalSum-self.SumBOMa.TotalSum
#      if self.ShowSaldoObrotyMa:
#         sum=sum+self.SumMa.TotalSum+self.SumBOMa.TotalSum-self.SumWn.TotalSum-self.SumBOWn.TotalSum
      file.write("<td class=%s align=right %s x:num>%s</td>\n"%(aclass,astyle,ssum)) #ICORUtil.FormatFNumHTML(sum,self.Query.FNumFormat)

   def DumpFileExcel(self,file,ndates,aindent=0):
      if self.Query.HideEmptyDimensions and self.CheckTotalSum()==0.0:
         return 0

#      self.DisplayValueModifier=self.ClassItem.DisplayValueModifier.ValuesAsFloat(self.OID)
#      self.FrameBegin=self.ClassItem.FrameBegin.ValuesAsInt(self.OID)
#      self.FrameEnd=self.ClassItem.FrameEnd.ValuesAsInt(self.OID)

      emptycellclass='xl3110957'
      emptyboldcellclass='xl3110957b'
      emptyboldbiggercellclass='xl3110957bb'

      emptycellclasstotal='xl3110957t'
      emptyboldcellclasstotal='xl3110957tb'
      emptyboldbiggercellclasstotal='xl3110957tbb'

      emptyitaliccellclass='xl3110957i'
      nobordercellclass='xl3110958'
      if self.Depth()==1: #ostatni poziom
         file.write('<tr>\n')
         file.write('<td class=%s %sNOWRAP>%s</td>'%(emptycellclass,self.GetTitleCellStyle(),self.Name,)) #bylo '&nbsp;'*aindent
         file.write('<td class=%s NOWRAP></td>'%(emptycellclass,))
         for adate in ndates:
            self.WriteExcelDataRow(file,adate,emptycellclass,self.GetNumCellStyle())
         file.write('<td class=%s NOWRAP></td>'%(emptycellclass,))
         self.WriteExcelTotalDataRow(file,adate,emptycellclass,self.GetNumCellStyle())
         file.write('</tr>\n')
      else: # dimension na wyzszym pietrze
         if not self.DisableTitle:
            if self.EmptyRowBefore:
               file.write('<tr><td colspan=%d class=xl2356587 NOWRAP align=left></td></tr>\n'%(3+(len(ndates)+1)*self.GetNumColsCount(),))
            file.write('<tr>\n')
            if self.TitleCenteredFramed:
               maxcols=(len(ndates)+1)*self.GetNumColsCount()-1
               file.write('<td class=xl2356587></td><td class=xl2356587></td><td class=xl347287>&nbsp;</td>')
               dcol=maxcols/2
               for i in range(dcol-1):
                  file.write('<td class=xl397287></td>')
               file.write('<td class=xl397287 align=center>%s</td>\n'%(self.Name,))
               for i in range(dcol-2):
                  file.write('<td class=xl397287></td>')
               file.write('<td class=xl387287>&nbsp;</td><td class=xl2356587></td><td class=xl2356587></td>')
            else:
               if self.IsItalic:
                  si='i'
                  if self.IsBold:
                     si='ib'
               else:
                  si=''
               file.write('<td colspan=%d class=xl2346587%s %sNOWRAP align=left>%s</td>\n'%(3+(len(ndates)+1)*self.GetNumColsCount(),si,self.GetTitleCellStyle(),self.Name))
            file.write('</tr>\n')

      if self.ShowSubDimensions:
         for adimension in self.Dimensions:
            adimension.DumpFileExcel(file,ndates,aindent+5)

      if self.Depth()>1:
         if not self.DisableTotal:
            if self.EmptyRowBeforeTotal:
               file.write('<tr><td colspan=%d class=xl2356587 NOWRAP align=left></td></tr>\n'%(3+(len(ndates)+1)*self.GetNumColsCount(),))
            file.write('<tr>\n')
            if self.IsTotalBold:
               tclass=emptyboldcellclasstotal
            else:
               tclass=emptycellclasstotal
            if self.IsTotalBiggerFont:
               tclass=emptyboldbiggercellclasstotal
            self.FirstNDate=1
            self.LastNDate=1
            file.write('<td class=%s %sNOWRAP>%s</td>'%(tclass,self.GetNumFramedTotalStyle(),self.TotalName))
            file.write('<td class=%s NOWRAP></td>'%(tclass,))
            for i in range(len(ndates)):
               adate=ndates[i]
               self.FirstNDate=0
               self.LastNDate=0
               if i==0:
                  self.FirstNDate=1
               if i==len(ndates)-1:
                  self.LastNDate=1
               self.WriteExcelDataRow(file,adate,tclass,self.GetNumFramedTotalStyle())
            self.FirstNDate=1
            self.LastNDate=1
            file.write('<td class=%s NOWRAP></td>'%(tclass,))
            self.WriteExcelTotalDataRow(file,adate,tclass,self.GetNumFramedTotalStyle())
            file.write('</tr>\n')
            self.FirstNDate=0
            self.LastNDate=0
      return 1


class QueryScenario:
   def __init__(self,aoid):
      self.OID=aoid         

class ICORMultiDimensionQuery:
   def __init__(self,aid,asriterator=None):
#      self.QueryClass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_QueryStruct']
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_Main']
      if type(aid)==type(''):
         self.OID=self.ClassItem.Name.Identifiers(aid)
      else:
         self.OID=aid
      if self.OID<0:
         raise ICORMDQueryException,'No such query - '+aid
      aobj=self.ClassItem[self.OID]
      self.FrameDrawing=0
      self.Parameters=ICORUtil.RecursiveParameters()
      self.Parameters.RegisterParameters([
         ['DateFrom',ICORUtil.ZERO_DATE_D],
         ['DateTo',ICORUtil.ZERO_DATE_D],
         ['AccountFrom',''],
         ['AccountTo',''],
         ['AccountMask',''],
         ['AccountInheritedMask',''],
         ['ShowWn',0],
         ['ShowMa',0],
         ['ShowBOWn',0],
         ['ShowBOMa',0],
         ['ShowObrotyWn',0],
         ['ShowObrotyMa',0],
         ['ShowSaldoWn',0],
         ['ShowSaldoMa',0],
         ['ShowSaldoObrotyWn',0],
         ['ShowSaldoObrotyMa',0],

         ['ShowSubDimensions','1'],
         ])
      self.Dimensions=[]
      self.ThisDimension=None
      self.Name=self.ClassItem.Name[self.OID]
      self.Caption=self.ClassItem.Caption[self.OID]
      if asriterator is None:
         self.SRIterator=StringRangeIterator()
      else:
         self.SRIterator=asriterator
      self.Title=''
      self.SubTitle=''
      self.TotalColumnName=''
      self.CategoryColumnName=''
      self.OneColumnOnly=1
      self.HideEmptyDimensions=0
      self.NoZeroValues=1
      self.NoDecimals=1
      self.DescriptionColumnWidth=470
      self.SpacerColumnWidth=5
      self.MonthColumnWidth=80
      self.TotalColumnWidth=130
      aparser=ReceiveQuery.XMLQueryReceive(self)
      aparser.Process(aobj.SourceXML)
      if not self.TotalColumnName:
         self.TotalColumnName='Razem '
      if self.NoDecimals:
         self.FNumFormat='%13.0n'
      else:
         self.FNumFormat='%13.2n'
      self.ThisDimension=None
      if 0:
         qobj=aobj.QueryStruct
         self.FKDataFileLocation=qobj.FKDataPath.DataPath
         if self.FKDataFileLocation is None:   
            print 'Brak ustawienia �cie�ki dost�pu do FK'
            self.FKDataFileLocation='d:/icor/tmp/fk/dat/'
         self.FKDataFileLocation=FilePathAsSystemPath(self.FKDataFileLocation)
         arefs=self.ClassItem.Dimensions.GetRefList(self.OID)
         while arefs:
            adimension=QueryDimension(arefs.OID,None,self,aparameters,aonecolumnonly=self.OneColumnOnly)
            self.Dimensions.append(adimension)
            arefs.Next()
   def __zero__(self):
      return len(self.Dimensions)>=0
   def AddDimension(self):
      self.ThisDimension=QueryDimension(self.ThisDimension,self,self.Parameters,aonecolumnonly=self.OneColumnOnly)
   def PopDimension(self):
      if not self.ThisDimension is None:
         self.ThisDimension=self.ThisDimension.ParentDimension
   def Depth(self):
      d=0
      for adimension in self.Dimensions:
         td=adimension.Depth()
         if td>d:
            d=td
      return d
   def Process(self):
      ret=0
      if VERBOSE:
         print '\nProcess:'
      self.SRIterator.Join()
      gmindate=ICORUtil.ZERO_DATE_D_MAX
      gmaxdate=ICORUtil.ZERO_DATE_D
      ranges=[]
      for afrom,ato,afilters in self.SRIterator.Result:
         if VERBOSE:
            print 'Range:',afrom,ato
         mindate=ICORUtil.ZERO_DATE_D_MAX
         maxdate=ICORUtil.ZERO_DATE_D
         for afilter in afilters:
            afilter.InitDane()
            if afilter.DateTo>maxdate:
               maxdate=afilter.DateTo
            if afilter.DateFrom<mindate:
               mindate=afilter.DateFrom
            if VERBOSE:
               print '  ',afilter
         if maxdate>gmaxdate:
            gmaxdate=maxdate
         if mindate<gmindate:
            gmindate=mindate
         ranges.append([afrom,ato,mindate,maxdate,afilters])
         if VERBOSE:
            print 'FromDate:',mindate,'ToDate:',maxdate
      aqaccess=QueryAccessFK(self.FKDataFileLocation)
      tstart=time.time()
      try:
         ret,n=aqaccess.Process(ranges,gmindate,gmaxdate)
      finally:
         del aqaccess
      tfinish=time.time()
      print 'Process time:',tfinish-tstart
      if VERBOSE:
         print
         print '===================================================================='
         for afrom,ato,mindate,maxdate,afilters in ranges:
            print afrom,ato,mindate,maxdate
            print '       WN   |     MA   |   BOWn   |   BOMa   | SaldoWn  | SaldoMa  |'
            for afilter in afilters:
               s='  %12s|%12s|%12s|%12s|%12s|%12s|%s'%(afilter.SumWn,afilter.SumMa,afilter.SumBOWn,afilter.SumBOMa,afilter.SumWn.TotalSum+afilter.SumBOWn.TotalSum,afilter.SumMa.TotalSum+afilter.SumBOMa.TotalSum,afilter)
               print s
            print
         print '===================================================================='
      self.PostProcess(gmindate,gmaxdate)
      return ret
   def PostProcess(self,gmindate,gmaxdate):
      vdict={}
      def iif(w,tc,fc):
         if w:
            return tc
         else:
            return fc
      vdict['math']=math
      vdict['string']=string
      vdict['re']=re
      vdict['random']=random
      vdict['iif']=iif
      for adimension in self.Dimensions:
         adimension.CalculateSums(gmindate,gmaxdate,vdict)
         if VERBOSE:
            adimension.DumpSums()
   def Dump(self):
      print 'MDQuery:',self.Name
      for adimension in self.Dimensions:
         adimension.Dump()
   def DumpFileXML(self,fname):
      file=open(fname,'w')
      try:
         file.write('<?xml version="1.0" encoding="Windows-1250"?>\n')
         file.write('<zestawienia>\n')
         for adimension in self.Dimensions:
            adimension.DumpFileXML(file)
         file.write('</zestawienia>\n')
      finally:
         file.close()
   def DumpFileHTML(self,fname):
      if len(self.Dimensions)<1:
         print 'Query nie posiada zdefiniowanych wymiar�w'
         return 0
      if len(self.Dimensions)>1:
         print 'Wymiar bazowy dla Query jest wi�kszy od jedno�ci'
         return 0
      fdimension=self.Dimensions[0]
      ndates=fdimension.GetNumDatesList()
      fdimension.SetShowColumns()
      ncols=fdimension.GetNumColsCount()
      if len(ndates)==0:
         print 'Query nie posiada zakres�w dat!'
         return 0
      if type(fname)==type(''):
         file=open(fname,'w')
         fclose=1
      else:
         file=fname
         fclose=0
      try:
         file.write('''<html>
<head>
<link rel=STYLESHEET type="text/css" href="icor.css" title="SOI">
<meta http-equiv="Content-Type" content="text/html; charset=windows-1250">
<title>%s</title>
</head>
<body>
'''%(self.Name,))
         file.write('<table class=objectsviewtable><caption class=objectsviewcaption>%s</caption>\n'%(self.Name,))
         if self.OneColumnOnly:
            file.write('<th class=objectsviewheader>Nazwa</th>\n')
         else:
            file.write('<th rowspan=2 class=objectsviewheader>Nazwa</th>\n')
         for ndate in ndates:
            sd=ICORUtil.tdate2romanmonthyear(ndate)
            sd=string.replace(sd,' ','&nbsp;')
            file.write('<th colspan=%d class=objectsviewheader>%s</th>\n'%(ncols,sd))
         file.write('<th colspan=%d class=objectsviewheader>RAZEM</th>\n'%(ncols,))
         if not self.OneColumnOnly:
            file.write('<tr class=objectsviewrow>\n')
            for ndate in ndates:
               fdimension.WriteSumsHeader(file)
            fdimension.WriteSumsHeader(file)
            file.write('</tr>\n')
         dret=0
         for adimension in self.Dimensions:
            dret=dret+adimension.DumpFileHTML(file,ndates)
         if not dret and self.NoZeroValues:
            file.write('<tr>\n')
            sa1,sa2,fs='<font size="+1">','</font>',1
            file.write('<td class=objectsviewdatasubsectionsummary NOWRAP>%s<B>%sRAZEM:%s</B></td>'%('',sa1,sa2))
            for adate in ndates:
               adimension.WriteHTMLDataRow(file,adate,'objectsviewdatasubsectionsummary',1,1,fs)
            adimension.WriteHTMLTotalDataRow(file,adate,'objectsviewdatasubsectionsummary',1,1,fs)
            file.write('</tr>\n')
         file.write('</table>\n')
         adt=ICORUtil.tdatetime()
         fsize=file.tell()
         self.ClassItem.LastGenerated.SetValuesAsDateTime(self.OID,adt)
         self.ClassItem.OutputFileSize[self.OID]=str(fsize)
         file.write('<hr><small><i>Data utworzenia: %s, rozmiar: %s</i></small>'%(ICORUtil.tdatetime2fmtstr(adt),ICORUtil.GetKBSize(fsize)))
         file.write('</body></html>\n')
      finally:
         if fclose:
            file.close()
      return 1
   def DumpFileExcel(self,fname):
      if len(self.Dimensions)<1:
         print 'Query nie posiada zdefiniowanych wymiar�w'
         return 0
      if len(self.Dimensions)>1:
         print 'Wymiar bazowy dla Query jest wi�kszy od jedno�ci'
         raise 'aaa'
         return 0
      fdimension=self.Dimensions[0]
      ndates=fdimension.GetNumDatesList()
      fdimension.SetShowColumns()
      ncols=fdimension.GetNumColsCount()
      if len(ndates)==0:
         print 'Query nie posiada zakres�w dat!'
         return 0
      if type(fname)==type(''):
         file=open(fname,'w')
         fclose=1
      else:
         file=fname
         fclose=0
      try:
         file.write("""
<html xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:x="urn:schemas-microsoft-com:office:excel"
xmlns="http://www.w3.org/TR/REC-html40" xmlns:tool>

<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1250">
<meta name=ProgId content=Excel.Sheet>
<meta name=Generator content="Microsoft Excel 9">
<title>%(nazwa)s</title>
<link rel=File-List href="./Page_files/filelist.xml">
<style id="Bil99bia_6587_Styles">
<!--table
   {mso-displayed-decimal-separator:"\.";
   mso-displayed-thousand-separator:" ";}
.xl2346587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2346587i
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:400;
   font-style:italic;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2346587ib
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:700;
   font-style:italic;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2356587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl347287
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:center;
   vertical-align:middle;
   border-top:.5pt hairline windowtext;
   border-right:none;
   border-bottom:.5pt hairline windowtext;
   border-left:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl397287
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:center;
   vertical-align:middle;
   border-top:.5pt hairline windowtext;
   border-right:none;
   border-bottom:.5pt hairline windowtext;
   border-left:none;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl387287
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:middle;
   border-top:.5pt hairline windowtext;
   border-right:.5pt hairline windowtext;
   border-bottom:.5pt hairline windowtext;
   border-left:none;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2366587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2376587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl3110957
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:10.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-right:.5pt hairline windowtext;
   border-bottom:none;
   border-left:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl3110957i
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:10.0pt;
   font-weight:400;
   font-style:italic;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-right:.5pt hairline windowtext;
   border-bottom:none;
   border-left:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl3110957b
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:10.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-right:.5pt hairline windowtext;
   border-bottom:none;
   border-left:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl3110957bb
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:12.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-right:.5pt hairline windowtext;
   border-bottom:none;
   border-left:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}

.xl3110957t
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:10.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-bottom:none;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl3110957tb
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:10.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-bottom:none;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl3110957tbb
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:12.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-bottom:none;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl3110958
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:10.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:general;
   vertical-align:middle;
   border-top:none;
   border-right:none;
   border-bottom:none;
   border-left:none;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2386587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:bottom;
   mso-background-source:auto;
   mso-pattern:auto;
   white-space:nowrap;}
.xl2396587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:center;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2406587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:700;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:center;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2416587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:bottom;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2426587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:center;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2436587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:"\#\,\#\#0"; */
   text-align:center;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2446587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:underline;
   text-underline-style:single;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2456587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:underline;
   text-underline-style:single;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:general;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2466587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:left;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2476587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:General; */
   text-align:left;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2486587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:Standard; */
   text-align:center;
   vertical-align:middle;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2496587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:0; */
   text-align:center;
   vertical-align:middle;
   border:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2506587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:windowtext;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:Standard; */
   text-align:center;
   vertical-align:middle;
   border:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
.xl2516587
   {padding-top:1px;
   padding-right:1px;
   padding-left:1px;
   mso-ignore:padding;
   color:black;
   font-size:9.0pt;
   font-weight:400;
   font-style:normal;
   text-decoration:none;
   font-family:"Arial CE", sans-serif;
   mso-font-charset:238;
/*   mso-number-format:Standard; */
   text-align:center;
   vertical-align:middle;
   border:.5pt hairline windowtext;
   background:white;
   mso-pattern:auto none;
   white-space:nowrap;}
-->
</style>
</head>

<body>                  
<!--[if !excel]>&nbsp;&nbsp;<![endif]-->
<!--The following information was generated by Microsoft Excel's Publish as Web
Page wizard.-->
<!--If the same item is republished from Excel, all information between the DIV
tags will be replaced.-->
<!----------------------------->
<!--START OF OUTPUT FROM EXCEL PUBLISH AS WEB PAGE WIZARD -->
<!----------------------------->

<div id="ICORReport_6587" align=center x:publishsource="Excel">
<table x:str border=0 cellpadding=0 cellspacing=0 class=xl2386587 style='border-collapse:collapse;table-layout:fixed;'>
"""%{'nazwa':self.Name,'tytul':self.Title,'podtytul':self.SubTitle,'kolumnaglowna':self.CategoryColumnName})

         file.write("<col class=xl2386587 width=%d ><col class=xl2386587 width=%d >"%(self.DescriptionColumnWidth,self.SpacerColumnWidth)) #style='mso-width-source:userset;mso-width-alt: 16952;width:358pt'       style='mso-width-source:userset;mso-width-alt: 1393;width:14pt'
         for ndate in ndates:
            file.write("<col class=xl2386587 width=%d >"%self.MonthColumnWidth) #style='mso-width-source:userset; mso-width-alt:2588;width:55pt'
         file.write("<col class=xl2386587 width=%d >"%self.SpacerColumnWidth) #style='mso-width-source:userset;mso-width-alt: 1393;width:14pt'
         file.write("<col class=xl2386587 width=%d >"%self.TotalColumnWidth) #style='mso-width-source:userset; mso-width-alt:3400;width:100pt'
         file.write("""
 <tr height=16 style='height:12.0pt'>
  <td height=16 class=xl2346587 colspan=3 style='height:12.0pt;'>%(tytul)s</td>
  <td class=xl2356587 >&nbsp;</td>
  <td class=xl2356587 >&nbsp;</td>
  <td class=xl2356587 >&nbsp;</td>
  <td class=xl2366587 >&nbsp;</td>
  <td class=xl2366587 >&nbsp;</td>
  <td class=xl2376587 >&nbsp;</td>
  <td class=xl2376587 >&nbsp;</td>
  <td class=xl2376587 >&nbsp;</td>
  <td class=xl2356587 >&nbsp;</td>
  <td class=xl2356587 >&nbsp;</td>
  <td class=xl2356587 >&nbsp;</td>
  <td class=xl2356587 >&nbsp;</td>
  <td class=xl2356587 >&nbsp;</td>
 </tr>
 <tr height=16 style='height:12.0pt'>
  <td height=16 class=xl2376587 style='height:12.0pt'>%(podtytul)s</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2396587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2366587>&nbsp;</td>
  <td class=xl2406587>%(nazwa)s</td>
  <td class=xl2376587>&nbsp;</td>
  <td class=xl2376587>&nbsp;</td>
  <td class=xl2376587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
 </tr>
 <tr height=15 style='height:11.4pt'>
  <td height=15 class=xl2356587 style='height:11.4pt'>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2416587>&nbsp;</td>
  <td class=xl2416587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2416587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2426587>&nbsp;</td>
  <td class=xl2436587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
 </tr>
 <tr height=15 style='height:11.4pt'>
  <td height=15 class=xl2356587 style='height:11.4pt'>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2446587><u style='visibility:hidden;mso-ignore:visibility'>&nbsp;</u></td>
  <td class=xl2446587><u style='visibility:hidden;mso-ignore:visibility'>&nbsp;</u></td>
  <td class=xl2446587><u style='visibility:hidden;mso-ignore:visibility'>&nbsp;</u></td>
  <td class=xl2446587><u style='visibility:hidden;mso-ignore:visibility'>&nbsp;</u></td>
  <td class=xl2456587><u style='visibility:hidden;mso-ignore:visibility'>&nbsp;</u></td>
  <td class=xl2466587>&nbsp;</td>
  <td class=xl2476587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
  <td class=xl2356587>&nbsp;</td>
 </tr>
 <tr height=15 style='height:11.4pt'>
  <td class=xl2496587>%(kolumnaglowna)s</td>
  <td class=xl2356587>&nbsp;</td>
"""%{'nazwa':self.Name,'tytul':self.Title,'podtytul':self.SubTitle,'kolumnaglowna':self.CategoryColumnName})

         for ndate in ndates:
            sd=ICORUtil.tdate2romanmonth(ndate)
            sd=string.replace(sd,' ','&nbsp;')
            file.write('<td class=xl2506587>%s</td>\n'%(sd,))
#  <td class=xl2506587 style='border-left:none'>II</td>

         file.write('<td class=xl2486587>&nbsp;</td><td class=xl2506587>Total</td></tr>')

         dret=0
         for adimension in self.Dimensions:
            dret=dret+adimension.DumpFileExcel(file,ndates)
         if 0: #not dret and self.NoZeroValues:
            file.write('<tr>\n')
            sa1,sa2,fs='<font size="+1">','</font>',1
            file.write('<td class=objectsviewdatasubsectionsummary NOWRAP>%s<B>%sRAZEM:%s</B></td>'%('',sa1,sa2))
            for adate in ndates:
               adimension.WriteHTMLDataRow(file,adate,'objectsviewdatasubsectionsummary',1,1,fs)
            adimension.WriteHTMLTotalDataRow(file,adate,'objectsviewdatasubsectionsummary',1,1,fs)
            file.write('</tr>\n')

         file.write("""
</table>
</div>
<!----------------------------->
<!--END OF OUTPUT FROM EXCEL PUBLISH AS WEB PAGE WIZARD-->
<!----------------------------->
</body>
</html>
""")

         adt=ICORUtil.tdatetime()
         fsize=file.tell()
         self.ClassItem.LastGenerated.SetValuesAsDateTime(self.OID,adt)
         self.ClassItem.OutputFileSize[self.OID]=str(fsize)
         file.write('<hr><small><i>Data utworzenia: %s, rozmiar: %s</i></small>'%(ICORUtil.tdatetime2fmtstr(adt),ICORUtil.GetKBSize(fsize)))
         file.write('</body></html>\n')
      finally:
         if fclose:
            file.close()
      return 1

def GenerateMDQuery(afile,aoid,atype=mdqt_HTML,logfile=None):
   if not logfile is None:
      start=time.time()
      logfile.write('\ninicjalizacja zestawienia: %d\n'%(aoid,))
   amdquery=ICORMultiDimensionQuery(aoid)
   if not logfile is None:
      finish=time.time()
      logfile.write('   inicjalizacja zestawienia zako�czona, czas: %s\n'%(str(finish-start),))
      logfile.write('   pocz�tek generowania zestawienia: name="%s", title="%s", subtitle="%s", caption="%s"\n'%(amdquery.Name,amdquery.Title,amdquery.SubTitle,amdquery.Caption))
      start=time.time()
   ret=amdquery.Process()
   if not logfile is None:
      finish=time.time()
      logfile.write('   koniec generowania zestawienia, czas: %s, status=%d\n'%(str(finish-start),ret))
   if ret!=0:
      afile.write('<h1><font color="red">Wyst�pi� b��d podczas komunikacji z maszyna BTrieve. Status: %d</font></h1>'%(ret,))
      return 0
   if atype==mdqt_HTML:
      ret=amdquery.DumpFileHTML(afile)
   elif atype==mdqt_Excel:
      ret=amdquery.DumpFileExcel(afile)
   else:
      afile.write('<h1><font color="red">Nieznany format wyj�ciowy dla zestawienia. Skontaktuj si� z administratorem.</font></h1>')
      ret=0
#   amdquery.Dump()
   return ret

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   aclass=aICORDBEngine.Classes[CID]

#   aoid=aclass.FirstObject()
#   while aoid>=0:
#      aclass.NoZeroValues[aoid]='1'
#      aoid=aclass.NextObject(aoid)
#   return

#   OID='FirstMDQuery'
#   OID=14

   OID=296
   amdquery=ICORMultiDimensionQuery(OID)
   if VERBOSE:
      amdquery.Dump()
   amdquery.Process()
   afile='d:/icor/html/output/ICORMDQuery.html'
   if amdquery.DumpFileExcel(afile):
      ExecuteShellCommand(afile)
   print 'Koniec'
   return



