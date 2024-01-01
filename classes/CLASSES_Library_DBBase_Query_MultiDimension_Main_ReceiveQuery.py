# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil
import string
from xmllib import XMLParser
import time
import sys
import os

class XMLQueryReceive(XMLParser):
   def __init__(self):
      XMLParser.__init__(self,accept_utf8=1,accept_unquoted_attributes=1,accept_missing_endtag_name=1)
      self.level=0
      self.QueryClass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_Main']
      self.DimensionClass=self.QueryClass.Dimensions.ClassOfType
      self.FilterClass=self.DimensionClass.FKFilters.ClassOfType
      self.AccountRangeClass=self.FilterClass.AccountRange.ClassOfType
      self.ValueClass=self.FilterClass.ShowMa.ClassOfType
      self.KeywordClass=self.QueryClass.Keywords.ClassOfType
      self.QueryRefs=''
   def Indent(self):
      return '   '*len(self.stack)
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
      self.QueryOID=self.QueryClass.AddObject()
      self.QueryRefs=self.QueryRefs+str(self.QueryOID)+':'+str(self.QueryClass.CID)+':'
      self.Dimensions=[]
      self.DimensionOID=-1
      self.ParentDimensionOID=-1
      self.DimensionAttrs={}
      if attrs.get('name',''):
         self.QueryClass.Name[self.QueryOID]=self.translate_references(attrs.get('name',''))
      if attrs.get('caption',''):
         self.QueryClass.Caption[self.QueryOID]=self.translate_references(attrs.get('caption',''))
      if attrs.get('title',''):
         self.QueryClass.Title[self.QueryOID]=self.translate_references(attrs.get('title',''))
      elif self.GlobalTitle:
         self.QueryClass.Title[self.QueryOID]=self.GlobalTitle
      if attrs.get('subtitle',''):
         self.QueryClass.SubTitle[self.QueryOID]=self.translate_references(attrs.get('subtitle',''))
      elif self.GlobalSubTitle:
         self.QueryClass.SubTitle[self.QueryOID]=self.GlobalSubTitle
      if attrs.get('totalcolumnname',''):
         self.QueryClass.TotalColumnName[self.QueryOID]=self.translate_references(attrs.get('totalcolumnname',''))
      if attrs.get('categorycolumnname',''):
         self.QueryClass.CategoryColumnName[self.QueryOID]=self.translate_references(attrs.get('categorycolumnname',''))
      else:
         d=CLASSES_Library_ICORBase_Interface_ICORUtil.tdate()
         self.QueryClass.CategoryColumnName[self.QueryOID]=str(d[0])
      if attrs.get('onecolumnonly',''):
         self.QueryClass.OneColumnOnly[self.QueryOID]=attrs.get('onecolumnonly','')
      else:
         self.QueryClass.OneColumnOnly[self.QueryOID]='1'
      if attrs.get('hideemptydimensions',''):
         self.QueryClass.HideEmptyDimensions[self.QueryOID]=attrs.get('hideemptydimensions','')
      if attrs.get('nozerovalues',''):
         self.QueryClass.NoZeroValues[self.QueryOID]=attrs.get('nozerovalues','')
      else:
         self.QueryClass.NoZeroValues[self.QueryOID]='1'
      if attrs.get('nodecimals',''):
         self.QueryClass.NoDecimals[self.QueryOID]=attrs.get('nodecimals','')
      print '%sQuery: %s'%(self.Indent(),self.translate_references(attrs.get('name','')))
   def end_query(self):
      aobj=self.QueryClass[self.QueryOID]
      dobj=aobj.Dimensions
      if dobj:
         fobj=dobj.FKFilters
         if not fobj:
            fclass=dobj.Class.FKFilters.ClassOfType
            foid=fclass.AddObject()
            fclass.FromDate.SetValuesAsDate(foid,(2000,1,1))
            fclass.ToDate.SetValuesAsDate(foid,(2001,1,1))
            dobj.Class.FKFilters[dobj.OID]=str(foid)+':'+str(fclass.CID)+':'
   def start_dimension(self,attrs):
#      print '%sDimension: %s'%(self.Indent(),self.translate_references(attrs.get('name','')))
      self.Dimensions.append([self.DimensionOID,self.DimensionAttrs])
      self.ParentDimensionOID=self.DimensionOID
      self.DimensionOID=self.DimensionClass.AddObject()
      self.DimensionAttrs={}
      for key,value in attrs.items():
         if key in ['showwn','showma','showbown','showboma','showsaldown','showsaldoma','showobrotywn','showobrotyma','showsaldoobrotywn','showsaldoobrotyma']:
            if CLASSES_Library_ICORBase_Interface_ICORUtil.str2bool(value):
               value='1:'+str(self.ValueClass.CID)+':'
            else:
               value='2:'+str(self.ValueClass.CID)+':'
         self.DimensionAttrs[key]=value
      if self.DimensionAttrs.get('name',''):
         self.DimensionClass.Name[self.DimensionOID]=self.translate_references(self.DimensionAttrs.get('name',''))
      if self.DimensionAttrs.get('formulaname',''):
         self.DimensionClass.FormulaName[self.DimensionOID]=self.translate_references(self.DimensionAttrs.get('formulaname',''))
      if self.DimensionAttrs.get('formulatext',''):
         self.DimensionClass.FormulaText[self.DimensionOID]=self.translate_references(self.DimensionAttrs.get('formulatext',''))
      if self.DimensionAttrs.get('totalname',''):
         self.DimensionClass.TotalName[self.DimensionOID]=self.translate_references(self.DimensionAttrs.get('totalname',''))
      if self.DimensionAttrs.get('visible',''):
         if CLASSES_Library_ICORBase_Interface_ICORUtil.str2bool(self.DimensionAttrs.get('visible','')):
            value='1:'+str(self.ValueClass.CID)+':'
         else:
            value='2:'+str(self.ValueClass.CID)+':'
         self.DimensionClass.ShowSubDimensions[self.DimensionOID]=value
      if self.DimensionAttrs.get('framed',''):
         self.DimensionClass.IsFramed[self.DimensionOID]=self.DimensionAttrs.get('framed','')
      if self.DimensionAttrs.get('framesize',''):
         self.DimensionClass.FrameSize[self.DimensionOID]=self.DimensionAttrs.get('framesize','')
      if self.DimensionAttrs.get('istotalbold',''):
         self.DimensionClass.IsTotalBold[self.DimensionOID]=self.DimensionAttrs.get('istotalbold','')
      if self.DimensionAttrs.get('isbold',''):
         self.DimensionClass.IsBold[self.DimensionOID]=self.DimensionAttrs.get('isbold','')
      if self.DimensionAttrs.get('istotaldoubleframeafter',''):
         self.DimensionClass.IsTotalDoubleFrameAfter[self.DimensionOID]=self.DimensionAttrs.get('istotaldoubleframeafter','')
      if self.DimensionAttrs.get('isitalic',''):
         self.DimensionClass.IsItalic[self.DimensionOID]=self.DimensionAttrs.get('isitalic','')
      if self.DimensionAttrs.get('istotalbiggerfont',''):
         self.DimensionClass.IsTotalBiggerFont[self.DimensionOID]=self.DimensionAttrs.get('istotalbiggerfont','')
      if self.DimensionAttrs.get('framebegin',''):
         self.DimensionClass.FrameBegin[self.DimensionOID]=self.DimensionAttrs.get('framebegin','')
      if self.DimensionAttrs.get('noframedtotal',''):
         self.DimensionClass.FramedTotal[self.DimensionOID]=self.DimensionAttrs.get('noframedtotal','')
      if self.DimensionAttrs.get('frameend',''):
         self.DimensionClass.FrameEnd[self.DimensionOID]=self.DimensionAttrs.get('frameend','')
      if self.DimensionAttrs.get('titlecenteredframed',''):
         self.DimensionClass.TitleCenteredFramed[self.DimensionOID]=self.DimensionAttrs.get('titlecenteredframed','')
      if self.DimensionAttrs.get('emptyrowbefore',''):
         self.DimensionClass.EmptyRowBefore[self.DimensionOID]=self.DimensionAttrs.get('emptyrowbefore','')
      if self.DimensionAttrs.get('emptyrowbeforetotal',''):
         self.DimensionClass.EmptyRowBeforeTotal[self.DimensionOID]=self.DimensionAttrs.get('emptyrowbeforetotal','')
      if self.DimensionAttrs.get('disabletitle',''):
         self.DimensionClass.DisableTitle[self.DimensionOID]=self.DimensionAttrs.get('disabletitle','')
      if self.DimensionAttrs.get('disabletotal',''):
         self.DimensionClass.DisableTotal[self.DimensionOID]=self.DimensionAttrs.get('disabletotal','')
      if self.DimensionAttrs.get('displayvaluemodifier',''):
         self.DimensionClass.DisplayValueModifier[self.DimensionOID]=self.translate_references(self.DimensionAttrs.get('displayvaluemodifier',''))

      if self.ParentDimensionOID<0:
         sref=self.QueryClass.Dimensions[self.QueryOID]
         sref=sref+str(self.DimensionOID)+':'+str(self.DimensionClass.CID)+':'
         self.QueryClass.Dimensions[self.QueryOID]=sref
      else:
         sref=self.DimensionClass.SubDimensions[self.ParentDimensionOID]
         sref=sref+str(self.DimensionOID)+':'+str(self.DimensionClass.CID)+':'
         self.DimensionClass.SubDimensions[self.ParentDimensionOID]=sref
   def start_filters(self,attrs):
      pass
   def start_filter(self,attrs):
      self.FilterOID=self.FilterClass.AddObject()
      if attrs.get('datefrom',''):
         s=attrs.get('datefrom','')
         if s:
            dt=CLASSES_Library_ICORBase_Interface_ICORUtil.getStrAsDate(s)
            self.FilterClass.FromDate.SetValuesAsDate(self.FilterOID,dt)
      if attrs.get('dateto',''):
         s=attrs.get('dateto','')
         if s:
            dt=CLASSES_Library_ICORBase_Interface_ICORUtil.getStrAsDate(s)
            self.FilterClass.ToDate.SetValuesAsDate(self.FilterOID,dt)
      if attrs.get('multiplyby',''): #"1.0"
         self.FilterClass.MultiplyBy[self.FilterOID]=attrs.get('multiplyby','')

      self.showattrs={}
      for key in ['showwn','showma','showbown','showboma','showsaldown','showsaldoma','showobrotywn','showobrotyma','showsaldoobrotywn','showsaldoobrotyma']:
         if self.DimensionAttrs.get(key,''):
            self.showattrs[key]=self.DimensionAttrs.get(key,'')
      for key,value in attrs.items():
         if key in ['showwn','showma','showbown','showboma','showsaldown','showsaldoma','showobrotywn','showobrotyma','showsaldoobrotywn','showsaldoobrotyma']:
            if CLASSES_Library_ICORBase_Interface_ICORUtil.str2bool(value):
               value='1:'+str(self.ValueClass.CID)+':'
            else:
               value='2:'+str(self.ValueClass.CID)+':'
         self.showattrs[key]=value

      if self.showattrs.get('showwn',''):
         self.FilterClass.ShowWn[self.FilterOID]=self.showattrs.get('showwn','')
      if self.showattrs.get('showma',''):
         self.FilterClass.ShowMa[self.FilterOID]=self.showattrs.get('showma','')
      if self.showattrs.get('showbown',''):
         self.FilterClass.ShowBOWn[self.FilterOID]=self.showattrs.get('showbown','')
      if self.showattrs.get('showboma',''):
         self.FilterClass.ShowBOMa[self.FilterOID]=self.showattrs.get('showboma','')
      if self.showattrs.get('showsaldown',''):
         self.FilterClass.ShowSaldoWn[self.FilterOID]=self.showattrs.get('showsaldown','')
      if self.showattrs.get('showsaldoma',''):
         self.FilterClass.ShowSaldoMa[self.FilterOID]=self.showattrs.get('showsaldoma','')
      if self.showattrs.get('showobrotywn',''):
         self.FilterClass.ShowObrotyWn[self.FilterOID]=self.showattrs.get('showobrotywn','')
      if self.showattrs.get('showobrotyma',''):
         self.FilterClass.ShowObrotyMa[self.FilterOID]=self.showattrs.get('showobrotyma','')
      if self.showattrs.get('showsaldoobrotywn',''):
         self.FilterClass.ShowSaldoObrotyWn[self.FilterOID]=self.showattrs.get('showsaldoobrotywn','')
      if self.showattrs.get('showsaldoobrotyma',''):
         self.FilterClass.ShowSaldoObrotyMa[self.FilterOID]=self.showattrs.get('showsaldoobrotyma','')

      sar=attrs.get('accountfrom','')+attrs.get('accountto','')+attrs.get('accountmask','')+attrs.get('inheritedmask','')
      if sar:
         self.AccountRangeOID=self.AccountRangeClass.AddObject()
         if attrs.get('accountfrom',''):
            self.AccountRangeClass.FromAccount[self.AccountRangeOID]=attrs.get('accountfrom','')
         if attrs.get('accountto',''):
            self.AccountRangeClass.ToAccount[self.AccountRangeOID]=attrs.get('accountto','')
         if attrs.get('accountmask',''):
            self.AccountRangeClass.AccountMask[self.AccountRangeOID]=attrs.get('accountmask','')
         if attrs.get('inheritedmask',''):
            self.AccountRangeClass.AccountInheritedMask[self.AccountRangeOID]=attrs.get('inheritedmask','')
         s=self.FilterClass.AccountRange[self.FilterOID]
         s=s+str(self.AccountRangeOID)+':'+str(self.AccountRangeClass.CID)+':'
         self.FilterClass.AccountRange[self.FilterOID]=s

      s=self.DimensionClass.FKFilters[self.DimensionOID]
      s=s+str(self.FilterOID)+':'+str(self.FilterClass.CID)+':'
      self.DimensionClass.FKFilters[self.DimensionOID]=s
   def end_filter(self):
      pass
   def end_filters(self):
      pass
   def start_subdimensions(self,attrs):
      pass
   def end_subdimensions(self):
      pass
   def end_dimension(self):
      self.DimensionOID,self.DimensionAttrs=self.Dimensions.pop()
   def start_keywords(self,attrs):
      self.KeywordRefs=''
   def end_keywords(self):
      if self.KeywordRefs:
         self.QueryClass.Keywords[self.QueryOID]=self.KeywordRefs
   def start_keyword(self,attrs):
      value=self.translate_references(attrs.get('value',''))
      aoid=self.KeywordClass.Name.Identifiers(value)
      if aoid<0:
         aoid=self.KeywordClass.AddObject()
         self.KeywordClass.Name[aoid]=value
      self.KeywordRefs=self.KeywordRefs+str(aoid)+':'+str(self.KeywordClass.CID)+':'
   def Process(self, filename):
      start=time.clock()
      self.feed(open(filename,'r').read())
      self.close()
      finish=time.clock()
      return finish-start

class XMLQueryStructReceive(XMLParser):
   def __init__(self):
      XMLParser.__init__(self)
      self.level=0
      self.QueryStructClass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_QueryStruct']
      self.QueryClass=aICORDBEngine.Classes['CLASSES_Library_DBBase_Query_MultiDimension_Main']
      self.QueryStructRefs=''
   def Indent(self):
      return '   '*len(self.stack)
   def start_querytree(self,attrs):
      self.QueryTreeOID=self.QueryStructClass.AddObject()
      self.QueryTreeRefs=''
   def end_querytree(self):
      self.QueryStructClass.Query[self.QueryTreeOID]=self.QueryTreeRefs
   def start_querygroup(self,attrs):
      self.QueryGroupName=attrs.get('name','QueryGroup')
      self.QueryOID=self.QueryClass.AddObject()
      self.QueryClass.Name[self.QueryOID]=self.QueryGroupName
      self.QueryTreeRefs=self.QueryTreeRefs+str(self.QueryOID)+':'+str(self.QueryClass.CID)+':'
      self.QueryRefs=''
      print '%sQueryGroup: %s'%(self.Indent(),self.QueryGroupName)
   def end_querygroup(self):
      self.QueryClass.SubQuery[self.QueryOID]=self.QueryRefs
   def start_querylocation(self,attrs):
      self.QueryLocation=self.DirName+attrs.get('file','')
      print '%sQueryLocation: %s'%(self.Indent(),self.QueryLocation)
      xqr = XMLQueryReceive()
      xqr.Process(self.QueryLocation)
      self.QueryRefs=self.QueryRefs+xqr.QueryRefs
   def Process(self, filename):
      self.DirName=os.path.dirname(filename)
      if self.DirName:
         self.DirName=self.DirName+'/'
      start=time.clock()
      self.feed(open(filename,'r').read())
      self.close()
      finish=time.clock()
      return finish-start

def DoReceive(afilename):
   xqr = XMLQueryReceive()
   atimeelapsed=xqr.Process(afilename)
   return atimeelapsed

def DoReceiveStruct(afilename):
  xqr = XMLQueryStructReceive()
  atimeelapsed=xqr.Process(afilename)
  return atimeelapsed

def Main():
   if len(sys.argv)<2:
      print 'Usage:'
      print '  ',sys.argv[0],'groupfile.xml'
      return
   t=DoReceiveStruct(sys.argv[1])
   print 'czas importu:',t
   print 'Zakończono pobieranie definicji zestawień.\nPamiętaj o ustaleniu katalogu bazowego dla danych z FK.'

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   aclass=aICORDBEngine.Classes[CID]
   ret=MessageDialog('Naciśnięcie "Tak", pobranie struktury zestawień,\nnaciśnięcie "Nie" spowoduje pobranie definicji jednego zestawienia.',mtConfirmation,mbYesNoCancel)
   if ret==mrCancel:
      return
   fname=FilePathAsSystemPath(CLASSES_Library_ICORBase_Interface_ICORUtil.InputFile())
#   fname='c:/icor/tmp/queries.xml'
   if fname:
      if ret==mrYes:
         t=DoReceiveStruct(fname)
      else:
         t=DoReceive(fname)
      print 'Time elapsed:',t
      MessageDialog('Zakończono pobieranie definicji zestawień.\nPamiętaj o ustaleniu katalogu bazowego dla danych z FK.',mtInformation,mbOK)
   return



