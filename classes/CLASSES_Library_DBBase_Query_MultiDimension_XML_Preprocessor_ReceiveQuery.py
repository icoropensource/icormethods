# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
from xmllib import XMLParser
import time
import sys
import os

class XMLQueryReceive(XMLParser):
   def __init__(self,aquery):
      XMLParser.__init__(self,accept_utf8=1,accept_unquoted_attributes=1,accept_missing_endtag_name=1)
      self.level=0
      self.Query=aquery
   def Indent(self):
      return '   '*len(self.stack)
   def Process(self,atext):
      start=time.clock()
      self.feed(atext)
      finish=time.clock()
      return finish-start
   def start_queries(self,attrs):
      print '%sQueries'%(self.Indent(),)
      if attrs.get('title',''):
         self.GlobalTitle=self.translate_references(attrs.get('title',''))
      else:
         self.GlobalTitle=''
      if attrs.get('subtitle',''):
         self.GlobalSubTitle=self.translate_references(attrs.get('subtitle',''))
      else:
         self.GlobalSubTitle=''
   def start_query(self,attrs):
      self.Dimensions=[]
      self.DimensionAttrs={}
      if attrs.get('name',''):
         self.Query.Name=self.translate_references(attrs.get('name',''))
      if attrs.get('caption',''):
         self.Query.Caption=self.translate_references(attrs.get('caption',''))
      if attrs.get('title',''):
         self.Query.Title=self.translate_references(attrs.get('title',''))
      elif self.GlobalTitle:
         self.Query.Title=self.GlobalTitle
      if attrs.get('subtitle',''):
         self.Query.SubTitle=self.translate_references(attrs.get('subtitle',''))
      elif self.GlobalSubTitle:
         self.Query.SubTitle=self.GlobalSubTitle
      if attrs.get('totalcolumnname',''):
         self.Query.TotalColumnName=self.translate_references(attrs.get('totalcolumnname',''))
      if attrs.get('categorycolumnname',''):
         self.Query.CategoryColumnName=self.translate_references(attrs.get('categorycolumnname',''))
      else:
         d=ICORUtil.tdate()
         self.Query.CategoryColumnName=str(d[0])
      if attrs.get('onecolumnonly',''):
         self.Query.OneColumnOnly=int(attrs.get('onecolumnonly',''))
      if attrs.get('hideemptydimensions',''):
         self.Query.HideEmptyDimensions=attrs.get('hideemptydimensions','')
      if attrs.get('nozerovalues',''):
         self.Query.NoZeroValues=int(attrs.get('nozerovalues',''))
      else:
         self.Query.NoZeroValues=1
      if attrs.get('nodecimals',''):
         self.Query.NoDecimals=int(attrs.get('nodecimals',''))
      if attrs.get('descriptioncolumnwidth',''):
         self.Query.DescriptionColumnWidth=int(attrs.get('descriptioncolumnwidth','470'))
      if attrs.get('spacercolumnwidth',''):
         self.Query.SpacerColumnWidth=int(attrs.get('spacercolumnwidth','5'))
      if attrs.get('monthcolumnwidth',''):
         self.Query.MonthColumnWidth=int(attrs.get('monthcolumnwidth','80'))
      if attrs.get('totalcolumnwidth',''):
         self.Query.TotalColumnWidth=int(attrs.get('totalcolumnwidth','130'))

      print '%sQuery: %s'%(self.Indent(),self.translate_references(attrs.get('name','')))
   def end_query(self):
      pass
   def start_dimension(self,attrs):
#      print '%sDimension: %s'%(self.Indent(),self.translate_references(attrs.get('name','')))
      self.Query.AddDimension()
      self.Query.ThisDimension.ShowWn=ICORUtil.str2bool(attrs.get('showwn','0'))
      self.Query.ThisDimension.ShowMa=ICORUtil.str2bool(attrs.get('showma','0'))
      self.Query.ThisDimension.ShowBOWn=ICORUtil.str2bool(attrs.get('showbown','0'))
      self.Query.ThisDimension.ShowBOMa=ICORUtil.str2bool(attrs.get('showboma','0'))
      self.Query.ThisDimension.ShowSaldoWn=ICORUtil.str2bool(attrs.get('showsaldown','0'))
      self.Query.ThisDimension.ShowSaldoMa=ICORUtil.str2bool(attrs.get('showsaldoma','0'))
      self.Query.ThisDimension.ShowObrotyWn=ICORUtil.str2bool(attrs.get('showobrotywn','0'))
      self.Query.ThisDimension.ShowObrotyMa=ICORUtil.str2bool(attrs.get('showobrotyma','0'))
      self.Query.ThisDimension.ShowSaldoObrotyWn=ICORUtil.str2bool(attrs.get('showsaldoobrotywn','0'))
      self.Query.ThisDimension.ShowSaldoObrotyMa=ICORUtil.str2bool(attrs.get('showsaldoobrotyma','0'))
      if attrs.get('name',''):
         self.Query.ThisDimension.Name=self.translate_references(attrs.get('name',''))
      if attrs.get('formulaname',''):
         self.Query.ThisDimension.FormulaName=self.translate_references(attrs.get('formulaname',''))
      if attrs.get('formulatext',''):
         self.Query.ThisDimension.FormulaText=self.translate_references(attrs.get('formulatext',''))
      if attrs.get('rowtotalfunction',''):
         self.Query.ThisDimension.RowTotalFunction=self.translate_references(attrs.get('rowtotalfunction',''))
      if attrs.get('totalname',''):
         self.Query.ThisDimension.TotalName=self.translate_references(attrs.get('totalname',''))
      if attrs.get('numberformatdecimals',''):
         self.Query.ThisDimension.NumberFormatDecimals=int(attrs.get('numberformatdecimals','-1'))
      if attrs.get('numberformattext',''):
         self.Query.ThisDimension.NumberFormatText=attrs.get('numberformattext','')
      if attrs.get('visible',''):
         self.Query.ThisDimension.ShowSubDimensions=ICORUtil.str2bool(attrs.get('visible',''))
      if attrs.get('disableinheritance',''):
         self.Query.ThisDimension.DisableInheritance=ICORUtil.str2bool(attrs.get('disableinheritance',''))
      if attrs.get('framed',''):
         self.Query.ThisDimension.IsFramed=int(attrs.get('framed',''))
      if attrs.get('framesize',''):
         self.Query.ThisDimension.FrameSize=attrs.get('framesize','')
      if attrs.get('istotalbold',''):
         self.Query.ThisDimension.IsTotalBold=int(attrs.get('istotalbold',''))
      if attrs.get('isbold',''):
         self.Query.ThisDimension.IsBold=int(attrs.get('isbold',''))
      if attrs.get('istotaldoubleframeafter',''):
         self.Query.ThisDimension.IsTotalDoubleFrameAfter=int(attrs.get('istotaldoubleframeafter',''))
      if attrs.get('isitalic',''):
         self.Query.ThisDimension.IsItalic=int(attrs.get('isitalic',''))
      if attrs.get('istotalbiggerfont',''):
         self.Query.ThisDimension.IsTotalBiggerFont=int(attrs.get('istotalbiggerfont',''))
      if attrs.get('framebegin',''):
         self.Query.ThisDimension.FrameBegin=int(attrs.get('framebegin',''))
      if attrs.get('noframedtotal',''):
         self.Query.ThisDimension.FramedTotal=int(attrs.get('noframedtotal',''))
      if attrs.get('frameend',''):
         self.Query.ThisDimension.FrameEnd=int(attrs.get('frameend',''))
      if attrs.get('titlecenteredframed',''):
         self.Query.ThisDimension.TitleCenteredFramed=int(attrs.get('titlecenteredframed',''))
      if attrs.get('emptyrowbefore',''):
         self.Query.ThisDimension.EmptyRowBefore=int(attrs.get('emptyrowbefore',''))
      if attrs.get('emptyrowbeforetotal',''):
         self.Query.ThisDimension.EmptyRowBeforeTotal=int(attrs.get('emptyrowbeforetotal',''))
      if attrs.get('disabletitle',''):
         self.Query.ThisDimension.DisableTitle=int(attrs.get('disabletitle',''))
      if attrs.get('disabletotal',''):
         self.Query.ThisDimension.DisableTotal=int(attrs.get('disabletotal',''))
      if attrs.get('displayvaluemodifier',''):
         self.Query.ThisDimension.DisplayValueModifier=float(self.translate_references(attrs.get('displayvaluemodifier','')))
   def start_filters(self,attrs):
      pass
   def start_filter(self,attrs):
      self.Query.ThisDimension.AddFilter()
      if attrs.get('datefrom',''):
         s=attrs.get('datefrom','')
         if s:
            self.Query.ThisDimension.ThisFilter.DateFrom=ICORUtil.getStrAsDate(s)
      if attrs.get('dateto',''):
         s=attrs.get('dateto','')
         if s:
            self.Query.ThisDimension.ThisFilter.DateTo=ICORUtil.getStrAsDate(s)
      if attrs.get('multiplyby',''): #"1.0"
         self.Query.ThisDimension.ThisFilter.MultiplyBy=float(attrs.get('multiplyby',''))

      self.showattrs={
         'showwn':self.Query.ThisDimension.ShowWn,
         'showma':self.Query.ThisDimension.ShowMa,
         'showbown':self.Query.ThisDimension.ShowBOWn,
         'showboma':self.Query.ThisDimension.ShowBOMa,
         'showsaldown':self.Query.ThisDimension.ShowSaldoWn,
         'showsaldoma':self.Query.ThisDimension.ShowSaldoMa,
         'showobrotywn':self.Query.ThisDimension.ShowObrotyWn,
         'showobrotyma':self.Query.ThisDimension.ShowObrotyMa,
         'showsaldoobrotywn':self.Query.ThisDimension.ShowSaldoObrotyWn,
         'showsaldoobrotyma':self.Query.ThisDimension.ShowSaldoObrotyMa
      }
      for key,value in attrs.items():
         if key in ['showwn','showma','showbown','showboma','showsaldown','showsaldoma','showobrotywn','showobrotyma','showsaldoobrotywn','showsaldoobrotyma']:
            self.showattrs[key]=ICORUtil.str2bool(value)

      if self.showattrs.get('showwn',''):
         self.Query.ThisDimension.ThisFilter.ShowWn=self.showattrs.get('showwn','')
      if self.showattrs.get('showma',''):
         self.Query.ThisDimension.ThisFilter.ShowMa=self.showattrs.get('showma','')
      if self.showattrs.get('showbown',''):
         self.Query.ThisDimension.ThisFilter.ShowBOWn=self.showattrs.get('showbown','')
      if self.showattrs.get('showboma',''):
         self.Query.ThisDimension.ThisFilter.ShowBOMa=self.showattrs.get('showboma','')
      if self.showattrs.get('showsaldown',''):
         self.Query.ThisDimension.ThisFilter.ShowSaldoWn=self.showattrs.get('showsaldown','')
      if self.showattrs.get('showsaldoma',''):
         self.Query.ThisDimension.ThisFilter.ShowSaldoMa=self.showattrs.get('showsaldoma','')
      if self.showattrs.get('showobrotywn',''):
         self.Query.ThisDimension.ThisFilter.ShowObrotyWn=self.showattrs.get('showobrotywn','')
      if self.showattrs.get('showobrotyma',''):
         self.Query.ThisDimension.ThisFilter.ShowObrotyMa=self.showattrs.get('showobrotyma','')
      if self.showattrs.get('showsaldoobrotywn',''):
         self.Query.ThisDimension.ThisFilter.ShowSaldoObrotyWn=self.showattrs.get('showsaldoobrotywn','')
      if self.showattrs.get('showsaldoobrotyma',''):
         self.Query.ThisDimension.ThisFilter.ShowSaldoObrotyMa=self.showattrs.get('showsaldoobrotyma','')

      sar=attrs.get('accountfrom','')+attrs.get('accountto','')+attrs.get('accountmask','')+attrs.get('inheritedmask','')
      if sar:
         if attrs.get('accountfrom',''):
            self.Query.ThisDimension.ThisFilter.AccountFrom=attrs.get('accountfrom','')
         if attrs.get('accountto',''):
            self.Query.ThisDimension.ThisFilter.AccountTo=attrs.get('accountto','')
         if attrs.get('accountmask',''):
            self.Query.ThisDimension.ThisFilter.AccountMask=attrs.get('accountmask','')
         if attrs.get('inheritedmask',''):
            self.Query.ThisDimension.ThisFilter.AccountInheritedMask=attrs.get('inheritedmask','')
   def end_filter(self):
      self.Query.ThisDimension.ThisFilter.PostProcess()
      pass
   def end_filters(self):
      pass
   def start_subdimensions(self,attrs):
      pass
   def end_subdimensions(self):
      pass
   def end_dimension(self):
      self.Query.ThisDimension.PostProcess()
      self.Query.PopDimension()
   def start_keywords(self,attrs):
      pass
   def end_keywords(self):
      pass
   def start_keyword(self,attrs):
      pass



