# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import *
from CLASSES_Library_NetBase_Utils_MDSpaceUtil import *
from CLASSES_Library_Win32_OLE_ICORExcel import *
from CLASSES_Library_Win32_OLE_MDSpaceUtil import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_Test_ICORBase_ICORAISummaryGenerator import SummaryGenerator
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import ICORDelphi
import random
import string
import math
import re
               
class SummaryDataValue:
   def __init__(self,afield,avalue,astringvalue,aodd,aoid,acid):
      self.Field=afield
      self.DataValue=avalue
      self.StringValue=astringvalue
      self.Odd=aodd
      self.RefOID=aoid
      self.RefCID=acid
   def AlignmentStd(self):
      if self.Field is None:
         return -1
      else:
         return self.Field.AlignmentStd

class SummarySpace2Excel(ICORMDSpace2Excel):
   def OnData(self,arow,acol):
      if self.Value is None:
         return
      s=self.Value.StringValue
      self.excel[acol+1,arow+2]=s

class SummarySpace2CSV(ICORMDSpace2CSV):
   def OnData(self,arow,acol):
      if self.Value is None:
         return
      s=self.GetCSVValue(self.Value.StringValue)
      self.file.write(s)

class SummarySpace2HTML(ICORMDSpace2HTML):
   def OnEndPage(self):
      if self.RowCount==0:
         self.file.write('<H1>Brak danych</H1><BR>\n')
      if self.Page:
         self.file.write('</body></html>\n')
   def OnStartCol(self,arow,acol):
      pass
   def OnData(self,arow,acol):
      if self.Value is None:
         sadd=self.OddS
      else:
         if self.Value.Odd:
            sadd='odd'
         else:
            sadd='even'
         self.OddS=sadd
      s='<TD class=objectsviewdata'+sadd+' NOWRAP>'
      self.file.write(s)
      if self.Value is None:
         self.file.write('&nbsp;')
      else:
         alg=self.Value.AlignmentStd()
         if alg=='0':
            align='Left'
         elif alg=='1':
            align='Right'
         elif alg=='2':
            align='Center'
         else:
            align='Center'
         s=string.replace(self.Value.StringValue,' ','&nbsp;')
         if s=='':
            align='Center'
            s='&nbsp;-&nbsp;'
         if self.Page:              
            s='<DIV align=%s><A CLASS="objectitemasanchor">%s</A></DIV>' % (align,s)
         else:
            s='<DIV align=%s><A CLASS="objectitemasanchor" href="icormain.asp?jobtype=objectedit&CID=%d&OID=%d">%s</A></DIV>' % (align,self.Value.RefCID,self.Value.RefOID,s)
         self.file.write(s)

class SummarySpace2HTMLSimple(ICORMDSpace2HTMLSimple):
   def OnEndPage(self):
      if self.RowCount==0:
         self.file.write('<H1>Brak danych</H1><BR>\n')
      else:
         self.file.write('<BR>\n')
      if self.Page:
         self.file.write('</body></html>\n')
   def OnData(self,arow,acol):
      if self.Value is None:
         self.file.write('&nbsp;')
      else:
         alg=self.Value.AlignmentStd()
         if alg=='0':
            align='Left'
         elif alg=='1':
            align='Right'
         elif alg=='2':
            align='Center'
         else:
            align='Center'
         s=self.Value.StringValue
         if s=='':
            align='Center'
            s='&nbsp;-&nbsp;'
         s='<DIV align=%s>%s</DIV>' % (align,s)
         self.file.write(s)

_indent='   '

#SummaryCondition
scEqual,scDifferent,scGreater,scLess,scGreaterOrEqual,scLessOrEqual=0,1,2,3,4,5
scSimilarToPattern,scSoundexSimilar=6,7
scExisting,scNonExisting=8,9
scModifiedAfter,scModifiedBefore=10,11
scRegExp,scNotRegExp=12,13
scUserFunction=14

#SummaryConditionNames
SummaryConditionsAsString = {scEqual:'równe =',scDifferent:'różne <>',scGreater:'większe >',scLess:'mniejsze <',scGreaterOrEqual:'większe bądź równe >=',scLessOrEqual:'mniejsze bądź równe <=',
scSimilarToPattern:'podobne do wzorca',scSoundexSimilar:'podobne fonetycznie',
scExisting:'każde istniejące w zbiorze',scNonExisting:'każde nieistniejące w zbiorze',
scModifiedAfter:'zmodyfikowane po',scModifiedBefore:'zmodyfikowane przed',
scRegExp:'wyrażenie regularne',scNotRegExp:'wyrażenie regularne, negacja',
scUserFunction:'funkcja użytkownika'}

#SummaryLinkage 
slAnd,slOr,slAndNot,slOrNot=0,1,2,3

#SummaryGroup
sgSum,sgAverage,sgMin,sgMax,sgCount,sgCumulative,sgMul=0,1,2,3,4,5,6
sgOr,sgAnd=7,8
#not implemented
sgXor=9
sgDay,sgWeek,sgMonth,sgYear=10,11,12,13

#Footer group
fgNone,fgSum,fgAverage,fgMin,fgMax,fgCount,fgMul=-1,0,1,2,3,4,5
FooterGroupAsText = {fgNone:'',fgSum:'Suma:&nbsp;',fgAverage:'Średnia:&nbsp;',fgMin:'Min:&nbsp;',fgMax:'Max:&nbsp;',fgCount:'Ilość:&nbsp;',fgMul:'Iloczyn:&nbsp;'}

class SummaryRule:
   def __init__(self,aobj,acasesensitive=0,formcondition=-1,formvalue=''):
      if formcondition>=0:
         self.Condition=formcondition
      else:
         self.Condition=aobj.Class.Condition.ValuesAsInt(aobj.OID)
      self.Linkage=aobj.Class.Linkage.ValuesAsInt(aobj.OID)
      self.FieldName=aobj.FieldName
      self.FunctionName=aobj.FunctionName
      if formcondition>=0:
         self.Value=formvalue
      else:
         self.Value=aobj.Value
      self.RuleValue=self.Value
      self.Value2=self.Value
      self.IsValue2Check=0
      self.ParentFieldsList=string.split(aobj.ParentFieldsList,'\\')
      self.ClassItem=None
      if self.Condition in [scRegExp,scSimilarToPattern,scSoundexSimilar,scNotRegExp]:
         if self.Condition==scSimilarToPattern:
            self.Value=string.replace(self.Value,'*','.*')
            self.Value='^'+string.replace(self.Value,'?','.')
         if acasesensitive:
            self.Pattern=re.compile(self.Value)
         else:
            self.Pattern=re.compile(self.Value,re.I)
      else:
         self.Pattern=None
      if self.Condition in [scExisting,scNonExisting]:
         self.ExistingRefs=FieldRefIterator(self.Value)
      else:
         self.ExistingRefs=None
      self.UserFunction=None
   def SetClassItem(self,aclass):
      self.ClassItem=aclass
      self.Field=self.ClassItem.FieldsByName(self.FieldName)
      if self.Condition in [scRegExp,scSimilarToPattern,scSoundexSimilar,scNotRegExp]:
         return
      if self.Condition in [scUserFunction]:
         mname=self.ClassItem.ClassPath+'_'+self.FunctionName
         mname=string.replace(mname,'\\','_')
         mname=string.replace(mname,'/','_')
         self.UserFunctionModule=__import__(mname)
         if not self.UserFunctionModule is None:
            self.UserFunction=getattr(self.UserFunctionModule,'ICORMain')
      ft=self.Field.FieldTID
      avalue=self.Value
      try:
         if ft==mt_Integer:
            self.Value=int(self.Value)
         elif ft==mt_Boolean:
            self.Value=ICORUtil.str2bool(self.Value)
         elif ft==mt_DateTime:
            self.Value,self.Value2,self.IsValue2Check=ICORUtil.GetStringAsDate(self.Value)
         elif ft==mt_Double:
            self.Value=string.atof(self.Value)
      except:
         self.Value=avalue
   def CheckObject(self,aoid):
      w=0
      wobject=0
      if self.Condition==scEqual:
         v=self.Field.ValuesAsComp(aoid)
         if self.IsValue2Check:
            if v>=self.Value and v<=self.Value2:
               w=1
         else:
            if v==self.Value:
               w=1
      elif self.Condition==scDifferent:
         v=self.Field.ValuesAsComp(aoid)
         if v!=self.Value:
            w=1
      elif self.Condition==scGreater:
         v=self.Field.ValuesAsComp(aoid)
         if v>self.Value:
            w=1
      elif self.Condition==scLess:
         v=self.Field.ValuesAsComp(aoid)
         if v<self.Value:
            w=1
      elif self.Condition==scGreaterOrEqual:
         v=self.Field.ValuesAsComp(aoid)
         if v>=self.Value:
            w=1
      elif self.Condition==scLessOrEqual:
         v=self.Field.ValuesAsComp(aoid)
         if v<=self.Value:
            w=1
      elif self.Condition==scExisting:
         arefs=self.Field.GetRefList(aoid)
         w=arefs.RefsExists(self.ExistingRefs)
      elif self.Condition==scNonExisting:
         arefs=self.Field.GetRefList(aoid)
         w=not arefs.RefsExists(self.ExistingRefs)
      elif self.Condition==scModifiedAfter:
         if self.Field.GetValueLastModified(aoid)>=self.Value:
            w=1
      elif self.Condition==scModifiedBefore:
         if self.Field.GetValueLastModified(aoid)<self.Value:
            w=1
      elif self.Condition==scRegExp or self.Condition==scSimilarToPattern or self.Condition==scSoundexSimilar:
         v=self.Field.Values(aoid)
         if self.Pattern.search(v):
            w=1
      elif self.Condition==scNotRegExp:
         v=self.Field.Values(aoid)
         if not self.Pattern.search(v):
            w=1
      elif self.Condition==scUserFunction:
         if not self.UserFunction is None:
            w,wobject=apply(self.UserFunction,(self.ClassItem.CID,self.FieldName,aoid,self.Value))
      if self.Linkage==slAndNot or self.Linkage==slOrNot:
         w=not w
      return w,wobject
   def dump(self,indent=_indent):
      print indent,self.FieldName,self.Value,self.Condition,self.Linkage,self.ParentFieldsList
   def GenerateSrc(self,agenerator,indent=_indent):
      print

class SummaryField:
   def __init__(self,afi,acol):
      self.Field=afi
      self.IsRuled=0
      self.Col=acol
      self.Row=1
      self.GroupType=-1
      self.GroupUnique=0
      self.IsCharted=0
      self.FooterType=-1
      self.IsFilled=0
      self.FooterValue=0
      self.ValuesCount=0
   def dump(self,indent=_indent):
      sr,sg,su,sc='','','',''
      if self.IsRuled:
         sr='Ruled'
      if self.GroupType>=0:
         sg='Grouped(%d)'%(self.GroupType)
      if self.GroupUnique:
         su='Unique'
      if self.IsCharted:
         sc='Charted'
      print indent,self.Field.Name,sr,sg,su,sc
   def SetFooterType(self,atype):
      self.FooterType=atype
      if atype<0:
         return
      if atype==fgSum:
         self.FooterValue=0
      elif atype==fgAverage:
         self.FooterValue=0
      elif atype==fgMin:
         self.FooterValue=99999999
      elif atype==fgMax:
         self.FooterValue=-99999999
      elif atype==fgCount:
         self.FooterValue=0
      elif atype==fgMul:
         self.FooterValue=1
   def AddFooterValue(self,avalue):
      if not (type(avalue)==type(0) or type(avalue)==type(1.0)):
         return
      self.ValuesCount=self.ValuesCount+1
      atype=self.FooterType
      if atype in [fgSum,fgAverage]:
         self.FooterValue=self.FooterValue+avalue
      elif atype==fgMin:
         if avalue<self.FooterValue:
            self.FooterValue=avalue
      elif atype==fgMax:
         if avalue>self.FooterValue:    
            self.FooterValue=avalue
      elif atype==fgCount:
         self.FooterValue=self.FooterValue+1
      elif atype==fgMul:
         self.FooterValue=self.FooterValue*avalue
   def GetFooterValue(self):
      atype=self.FooterType
      if atype<0:
         return None
      if atype==fgAverage:
         if self.ValuesCount>0:
            self.FooterValue=float(self.FooterValue)/float(self.ValuesCount)
         else:
            self.FooterValue=''
      if type(self.FooterValue)==type(1):
         return FooterGroupAsText[atype]+str(self.FooterValue)
      elif type(self.FooterValue)==type(1.0):
         return FooterGroupAsText[atype]+'%0.2f'%(self.FooterValue)
      else:
         return FooterGroupAsText[atype]+self.FooterValue
   def GetFieldValueGrouped(self,arefs,aaccepted):
      self.Refs=arefs
      lpos=arefs.position            
      self.AcceptedOIDs=aaccepted
      try:
         if self.GroupType==sgCumulative:
            arefs.Last()
            if arefs.position>=0:
               self.avalue=self.Field.ValuesAsComp(arefs.OID)
            else:
               self.avalue=0
            arefs.First()
            if arefs.position>=0:
               self.avalue=self.avalue-self.Field.ValuesAsComp(arefs.OID)
         else:
            self.PreGroup()
            if self.GroupUnique:
               for aoid in aaccepted.keys():
                  self.DoGetFieldValueGrouped(aoid)
            else:
               arefs.First()
               while arefs.position>=0:
                  if aaccepted.has_key(arefs.OID):
                     self.DoGetFieldValueGrouped(arefs.OID)
                  arefs.Next()
            self.PostGroup()
         avalue=self.avalue
      except:
         avalue=''
      arefs.position=lpos
      return avalue
   def PreGroup(self):
      self.avalue=0
      if self.GroupType==sgSum:
         self.avalue=0
      elif self.GroupType==sgAverage:
         self.avalue=0
         self.acnt=0
      elif self.GroupType==sgMin:
         self.avalue=99999999
      elif self.GroupType==sgMax:
         self.avalue=-99999999
      elif self.GroupType==sgCount:
         self.avalue=0
      elif self.GroupType==sgMul:
         self.avalue=1
      elif self.GroupType==sgOr:
         self.avalue=0
      elif self.GroupType==sgAnd:
         self.avalue=1
   def PostGroup(self):
      if self.GroupType==sgAverage:
         self.avalue=self.avalue*1.0/self.acnt
      elif self.GroupType==sgMin:
         if self.avalue==99999999:
            self.avalue=0
      elif self.GroupType==sgMax:
         if self.avalue==-99999999:
            self.avalue=0
   def DoGetFieldValueGrouped(self,aoid):
      if self.GroupType==sgSum:
         self.avalue=self.avalue+self.Field.ValuesAsComp(aoid)
      elif self.GroupType==sgAverage:
         self.avalue=self.avalue+self.Field.ValuesAsComp(aoid)
         self.acnt=self.acnt+1
      elif self.GroupType==sgMin:
         v=self.Field.ValuesAsComp(aoid)
         if v<self.avalue:
            self.avalue=v
      elif self.GroupType==sgMax:
         v=self.Field.ValuesAsComp(aoid)
         if v>self.avalue:
            self.avalue=v
      elif self.GroupType==sgCount:
         self.avalue=self.avalue+1
      elif self.GroupType==sgMul:
         self.avalue=self.avalue*self.Field.ValuesAsComp(aoid)
      elif self.GroupType==sgOr:
         self.avalue=self.avalue or self.Field.ValuesAsComp(aoid)
      elif self.GroupType==sgAnd:
         self.avalue=self.avalue and self.Field.ValuesAsComp(aoid)

class SummaryCalculatedField(SummaryField):
   def __init__(self,aname,aformula,afooter):
      SummaryField.__init__(self,None,-1)
      self.Name=aname
      self.Formula=aformula
      try:
         bfooter=int(afooter)
      except:
         bfooter=-1
      self.SetFooterType(bfooter)
   def GetCalculatedValue(self,acols):
      def iif(w,tc,fc):
         if w:
            return tc
         else:
            return fc
      gd={'cols':acols,'math':math,'string':string,'re':re,'random':random,'iif':iif}
      try:
         res=eval(self.Formula,gd)
         self.AddFooterValue(res)
      except:
         res=None
      if type(res)==type(1):
         return res,str(res)
      elif type(res)==type(1.0):
         return res,'%0.2f'%(res)
      else:
         return res,res

class SummaryColsValues:
   def __init__(self,aspace):
      self.space=aspace
      self.Row=-1
      self.Clear()
   def __getitem__(self,key):
      res=self.space[self.Row,key+2]
      if res is None:
         res=self.colcache.get(key+2,0)
      else:
#         res=res.DataValue
         res=res.StringValue
      return res
   def __setitem__(self,key,value):
      self.colcache[key]=value
   def Clear(self):
      self.colcache={}

class SummaryColumn:
   def __init__(self,aid,apath,acaption):
      self.ID=aid
      self.Path=apath
      self.Caption=acaption

class SummaryTree:
   def __init__(self,aclass,apath,afield=None,alevel=0):
      self.ClassItem=aclass
      self.Level=alevel
      self.SubTree={}
      self.Rules=[]
      self.Fields={}
      self.Field=afield
      if not afield is None:
         self.Name=afield.Name
      else:
         self.Name=''
      self.AcceptedOIDs={}
      self.IsGrouped=0
      self.Path=apath
      if not afield is None:
         if self.Path!='':
            self.Path=self.Path+'_'
         self.Path=self.Path+afield.Name
   def GetSubTree(self,aname):
      if aname==[] or aname==[''] or aname==['\\'] or aname==['','']:
         return self
      if self.SubTree.has_key(aname[0]):
         atree=self.SubTree[aname[0]]
      else:
         afi=self.ClassItem.FieldsByName(aname[0])
         atree=SummaryTree(afi.ClassOfType,self.Path,afi,self.Level+1)
         self.SubTree[aname[0]]=atree
      return atree.GetSubTree(aname[1:])
   def DoAddField(self,aclass,afield,pfield,acolumns):
      if afield.IsInteractive=='0':
         return
      if not self.SubTree.has_key(pfield.Name):
         atree=SummaryTree(aclass,self.Path,pfield,self.Level+1)
         self.SubTree[pfield.Name]=atree
      else:
         atree=self.SubTree[pfield.Name]
      self.Recur=atree.AddField([afield.Name],acolumns,self.space,self.Recur)
      return
   def AddField(self,afield,acolumns,aspace,arecur):
#      print 'AF:',self.ClassItem.NameOfClass,afield
      self.Recur=arecur
      self.space=aspace
      fname=afield[0]
      afi=self.ClassItem.FieldsByName(fname)
      if afi is None:
         print 'NONE!',self.ClassItem.NameOfClass,fname
         return self.Recur
      if afi.IsInteractive=='0':
         return self.Recur
      self.Recur.append(self.ClassItem.CID)
      if len(afield)==1:
         if afi.ClassOfType is None:
            if self.Path!='':
               fcolname=self.Path+'_'+fname
            else:
               fcolname=fname
            if acolumns.has_key(fcolname):
               self.Fields[fname]=SummaryField(afi,acolumns[fcolname].ID)
            else:
               aspace.header.Append(afi.FieldNameAsDisplayed)
               self.Fields[fname]=SummaryField(afi,aspace.header.Len())
         else:
            w=1
            if self.Level>0 and afi.ClassOfType.CID in self.Recur:
               w=0
            if w:
               afi.ClassOfType.ForEachField(self.DoAddField,afi,acolumns)
      else:
         w=1
         if self.Level>0 and afi.ClassOfType.CID in self.Recur:
            w=0
         if w:
            if not self.SubTree.has_key(fname):
               atree=SummaryTree(afi.ClassOfType,self.Path,afi,self.Level+1)
               self.SubTree[fname]=atree
            else:
               atree=self.SubTree[fname]
            self.Recur=atree.AddField(afield[1:],acolumns,aspace,self.Recur)
      self.Recur=self.Recur[:-1]
      return self.Recur
   def DoAddGroupField(self,aclass,afield,pfield,agrouptype,aunique,achart,afooter,afill):
      if afield.IsInteractive=='0':
         return
      if not self.SubTree.has_key(pfield.Name):
         atree=SummaryTree(aclass,self.Path,pfield,self.Level+1)
         self.SubTree[pfield.Name]=atree
      else:
         atree=self.SubTree[pfield.Name]
      self.Recur=atree.AddGroupField([afield.Name],self.space,agrouptype,aunique,achart,afooter,afill,self.Recur)
      return
   def AddGroupField(self,afield,aspace,agrouptype,aunique,achart,afooter,afill,arecur):
#      print 'AF:',self.ClassItem.NameOfClass,afield,agrouptype,aunique,achart
      self.Recur=arecur
      self.space=aspace
      fname=afield[0]
      afi=self.ClassItem.FieldsByName(fname)
      if afi is None:
         print 'NONE!',self.ClassItem.NameOfClass,fname
         return self.Recur
      if afi.IsInteractive=='0':
         return self.Recur
      self.Recur.append(self.ClassItem.CID)
      if len(afield)==1:
         if afi.ClassOfType is None:
            if not self.Fields.has_key(fname):
               aspace.header.Append(afi.FieldNameAsDisplayed)
               self.Fields[fname]=SummaryField(afi,aspace.header.Len())
            self.IsGrouped=agrouptype>=0
            self.Fields[fname].GroupType=agrouptype
            self.Fields[fname].GroupUnique=aunique
            self.Fields[fname].IsCharted=achart
            self.Fields[fname].SetFooterType(afooter)
            self.Fields[fname].IsFilled=afill
         else:
            w=1
            if self.Level>0 and afi.ClassOfType.CID in self.Recur:
               w=0
            if w:
               afi.ClassOfType.ForEachField(self.DoAddGroupField,afi,agrouptype,aunique,achart,afooter,afill)
      else:
         w=1
         if self.Level>0 and afi.ClassOfType.CID in self.Recur:
            w=0
         if w:
            if not self.SubTree.has_key(fname):
               atree=SummaryTree(afi.ClassOfType,self.Path,afi,self.Level+1)
               self.SubTree[fname]=atree
            else:
               atree=self.SubTree[fname]
            self.Recur=atree.AddGroupField(afield[1:],aspace,agrouptype,aunique,achart,afooter,afill,self.Recur)
      self.Recur=self.Recur[:-1]
      return self.Recur
   def AddRule(self,arule,pos=0):
      mpfl=len(arule.ParentFieldsList)-1
      if pos>=mpfl:
         arule.SetClassItem(self.ClassItem)
         self.Rules.append(arule)
         if self.Fields.has_key(arule.FieldName):
            self.Fields[arule.FieldName].IsRuled=1
      else:
         fname=arule.ParentFieldsList[pos]
         afi=self.ClassItem.FieldsByName(fname)
         if not self.SubTree.has_key(fname):
            atree=SummaryTree(afi.ClassOfType,self.Path,afi,self.Level+1)
            self.SubTree[fname]=atree
         else:
            atree=self.SubTree[fname]
         atree.AddRule(arule,pos+1)
   def ClearValues(self):
      self.AcceptedOIDs={}
      self.GroupPrinted=0
      sv=self.SubTree.values()
      for atree in sv:
         atree.ClearValues()
   def ClearGroupPrinted(self):
      self.GroupPrinted=0
      sv=self.SubTree.values()
      for atree in sv:
         atree.ClearValues()
   def CheckObject(self,aoid,lev=0):
      wobject=0
      if aoid<0:
         if self.Rules!=[]:
            return 0,0
         wand=1
         sv=self.SubTree.values()
         if sv!=[]:
            wand=1
            for atree in sv:
               w1,w2=atree.CheckObject(-1,lev+1)
               wand=wand and w1
               wobject=wobject or w2
         return wand,wobject
      w=1
      wo=0
      if self.Rules!=[]:
         wo=1
         wor=0
         worexists=0
         wand=1
         for arule in self.Rules:
            wres,wobject1=arule.CheckObject(aoid)
            wobject=wobject or wobject1
            if arule.Linkage==slOr or arule.Linkage==slOrNot:
               worexists=1
               wor=wor or wres
            else:
               wand=wand and wres
         if worexists:
            w=wand and wor
         else:
            w=wand
         if not w:
            return 0,wobject
#      if self.Field is None:
#         print '%s%s[%d]'%(_indent*lev,self.ClassItem.NameOfClass,aoid)
#      else:
#         print '%s%s : %s'%(_indent*lev,self.Field.Name,self.ClassItem.NameOfClass)
      sv=self.SubTree.values()
      if sv!=[]:
         wand=1
         for atree in sv:
            arefs=atree.Field.GetRefList(aoid)
            if arefs.position>=0:
               wor=0
            else:
               wor,wobject1=atree.CheckObject(-1,lev+1)
               wobject=wobject or wobject1
            while arefs.position>=0:
               wres,wobject1=atree.CheckObject(arefs.OID,lev+1)
               wobject=wobject or wobject1
               wor=wor or wres
               arefs.Next()
            wand=wand and wor
         w=wand
      if w:
         self.AcceptedOIDs[aoid]=1
#         for afield in self.Fields.values():
#            print '%s%s = %s'%(_indent*(lev+1),afield.Field.Name,afield.Field[aoid])
      return w,wobject
   def PrintObject(self,aprefs,acolsvalues,space,aodd,arefoid,arefcid,lev=0):
      self.RefOID=arefoid
      self.RefCID=arefcid
      max=0
      if type(aprefs)==type(1):
         aoid=aprefs
         aprefs=FieldRefIterator(str(aoid)+':'+str(self.ClassItem.CID)+':')
      else:
         if aprefs.position>=0:
            aoid=aprefs.OID
         else:
            aoid=-1
      if not self.IsGrouped and not self.AcceptedOIDs.has_key(aoid):
         return max
#      if self.Field is None:
#         print '%s%s[%d]'%(_indent*lev,self.ClassItem.NameOfClass,aoid)
#      else:           
#         print '%s%s : %s'%(_indent*lev,self.Field.Name,self.ClassItem.NameOfClass)
      if not self.GroupPrinted:
         for afield in self.Fields.values():
#            print '%s%s = %s'%(_indent*(lev+1),afield.Field.Name,afield.Field[aoid])
            if afield.GroupType>=0:
               avalue=afield.GetFieldValueGrouped(aprefs,self.AcceptedOIDs)
               sdv=SummaryDataValue(afield.Field,avalue,str(avalue),aodd,self.RefOID,self.RefCID)
               space[afield.Row,afield.Col]=sdv
               acolsvalues[afield.Col]=avalue
               if afield.FooterType>=0:
                  afield.AddFooterValue(avalue)
               if not afield.GroupUnique:
                  r=afield.Row+1
                  afield.Row=r
                  if r>max:
                     max=r
            else:
               avalue=afield.Field.ValuesAsComp(aoid)
               sdv=SummaryDataValue(afield.Field,avalue,afield.Field.ValuesFmt(aoid),aodd,self.RefOID,self.RefCID)
               space[afield.Row,afield.Col]=sdv
               acolsvalues[afield.Col]=avalue
               if afield.FooterType>=0:
                  afield.AddFooterValue(avalue)
               r=afield.Row+1
               afield.Row=r
               if r>max:
                  max=r
#         if self.IsGrouped:
#            self.GroupPrinted=1
      sv=self.SubTree.values()
      if sv!=[]:
         for atree in sv:
            arefs=atree.Field.GetRefList(aoid)
            if atree.IsGrouped:
               r=atree.PrintObject(arefs,acolsvalues,space,aodd,arefoid,arefcid,lev+1)
               if r>max:
                  max=r
                  atree.SetMaxFieldRow(max,space)
            else:
               while arefs.position>=0:
                  r=atree.PrintObject(arefs,acolsvalues,space,aodd,arefoid,arefcid,lev+1)
                  if r>max:
                     max=r
                     atree.SetMaxFieldRow(max,space)
                  arefs.Next()
      if max>0:
         self.SetMaxFieldRow(max,space)
      return max
   def SetMaxFieldRow(self,max,space):
      for afield in self.Fields.values():
         if afield.IsFilled:
            for i in range(afield.Row,max):
               if space[i,afield.Col] is None:
                  space[i,afield.Col]=space[i-1,afield.Col]
         afield.Row=max
      for atree in self.SubTree.values():
         atree.SetMaxFieldRow(max,space)
   def ForEachField(self,afunc,parms):
      for afield in self.Fields.values():
         apply(afunc,(afield,parms))
      for atree in self.SubTree.values():
         atree.ForEachField(afunc,parms)
   def dump(self,lev=0):
      if self.IsGrouped:
         s='Grouped'
      else:
         s=''
      print '%sTree: %s : [%s] %s'%(_indent*lev,self.Name,self.ClassItem.NameOfClass,s)
      if self.Rules!=[]:
         print '%sRules:'%(_indent*(lev+1))
         for arule in self.Rules:
            arule.dump(_indent*(lev+2))
      if self.Fields.keys()!=[]:
         print '%sFields:'%(_indent*(lev+1))
         for afield in self.Fields.values():
            afield.dump(_indent*(lev+2))
      for arules in self.SubTree.values():
         arules.dump(lev+1)
   def GenerateSrc(self,agenerator,lev=0):
      if self.Rules!=[]:
         for arule in self.Rules:
            arule.GenerateSrc(agenerator,_indent*lev+2)

class ICORSummary:
   def __init__(self,sumoid,aspace,formdict=None,aIsInteractive=1,asummaryuid=''):
      if formdict is None:
         formdict={}
      self.SummaryClass=aICORDBEngine.Classes.MetaClass.aSummaries.ClassOfType
      self.summoid=sumoid
      self.SUID=asummaryuid+'_'+str(sumoid)
      self.space=aspace
      self.IsInteractive=aIsInteractive
      self.IsFooter=0
      self.ClassItem=aICORDBEngine.Classes[self.SummaryClass.OwnerCID.ValuesAsInt(sumoid)]
      self.AllDataToCheck=self.SummaryClass.AllDataToCheck.ValuesAsInt(sumoid)>0
      self.NumDataToCheck=self.SummaryClass.NumDataToCheck.ValuesAsInt(sumoid)
      self.InitialObjectsSet=self.SummaryClass.InitialObjectsSet[sumoid]
      s=self.SummaryClass.CheckedList[sumoid]
      self.CheckedList=string.split(s,':')
      self.ColsValues=SummaryColsValues(self.space)
      for i in range(len(self.CheckedList)):
         sl=string.split(self.CheckedList[i],'\\')
         self.CheckedList[i]=sl
      self.Name=self.SummaryClass.Name[sumoid]
      self.Description=self.SummaryClass.Description[sumoid]
      self.ShowAllRefs=self.SummaryClass.ShowAllRefs.ValuesAsInt(sumoid)>0
      self.ShowFieldLinks=self.SummaryClass.ShowFieldLinks.ValuesAsInt(sumoid)>0
      self.UseLastModification=self.SummaryClass.UseLastModification.ValuesAsInt(sumoid)>0
      self.IsCaseSensitive=self.SummaryClass.IsCaseSensitive.ValuesAsInt(sumoid)>0
      self.SortDescending=self.SummaryClass.SortDescending.ValuesAsInt(sumoid)>0
      self.RecurField=self.SummaryClass.RecurField[sumoid]
      self.RecurSummOID=self.SummaryClass.RecurSummOID.ValuesAsInt(sumoid)
      self.LastCreated=self.SummaryClass.LastCreated.ValuesAsDateTime(sumoid)
      self.SortByField=self.SummaryClass.SortByField[sumoid]
      self.CalculatedFields=[]
      s=self.SummaryClass.CalcFields[sumoid]
      sl=string.split(s,chr(255))
      for s1 in sl[:-1]:
         sl1=string.split(s1,chr(254))
         sc1,sc2,sc3='','',''
         if len(sl1)>0:
            sc1=sl1[0]
         if len(sl1)>1:
            sc2=sl1[1]
         if len(sl1)>2:
            sc3=sl1[2]
         acf=SummaryCalculatedField(sc1,sc2,sc3)
         self.CalculatedFields.append(acf)
         if acf.FooterType>=0:
            self.IsFooter=1
      self.ColID=-1
      self.ColOID=-1
      self.Columns={}
      s=self.SummaryClass.ColumnsPos[sumoid]
      if s!='':
         acolumn=SummaryColumn(1,'','l.p.')
         self.space.header.Append('l.p.')
         self.Columns['']=acolumn
         sl=string.split(s,':')
         i=2
         for s in sl[:-1]:
            sl1=string.split(s,',')
            sl1[0]=string.replace(sl1[0],'\\','_')
            self.Columns[sl1[0]]=SummaryColumn(i,sl1[0],sl1[1])
            self.space.header.Append(sl1[1])
            i=i+1
         for acf in self.CalculatedFields:
            self.space.header.Append(acf.Name)
            acf.Col=i
            i=i+1
         if self.IsInteractive:
            self.space.header.Append('RowID')
            self.space.header.Append('OID')
            self.ColID=i
            self.ColOID=i+1
      else:
         self.space.header.Append('l.p.')
      self.Tree=SummaryTree(self.ClassItem,'',None,0)
      for afield in self.CheckedList[:-1]:
         self.Tree.AddField(afield,self.Columns,self.space,[])
      self.RulesList=[]
      aobj=self.SummaryClass.Rules.GetRefObject(sumoid)
      i=0
      while aobj.Exists():
         if formdict!={}:
            r1=int(formdict.get('condselect'+str(i),'-1'))
            r2=formdict.get('rulevalue'+str(i),'')
         else:
            r1=-1
            r2=''
         arule=SummaryRule(aobj,self.IsCaseSensitive,r1,r2)
         self.RulesList.append(arule)
         self.Tree.AddRule(arule)
         i=i+1
         aobj.Next()
      s=self.SummaryClass.ColumnsPos[sumoid]
      if s!='':
         sl=string.split(s,':')
         i=2
         for s in sl[:-1]:
            sl1=string.split(s,',')
            if len(sl1)>=5:
               if len(sl1)<6:
                  sl1.append('-1')
               if len(sl1)<7:
                  sl1.append('0')
               sfp=string.split(sl1[0],'\\')
#               print sl1[0],sfp
               if sl1[5]!='-1':
                  self.IsFooter=1
               if sfp!=[]:
                  self.Tree.AddGroupField(sfp,self.space,int(sl1[2]),int(sl1[3]),int(sl1[4]),int(sl1[5]),int(sl1[6]),[])
      self.ShowProgress=1
#      self.dump()
   def ProcessAll(self,bobj=None):
      if self.ClassItem is None:
         return 0
#      return
      self.SortField=None
      if bobj is None:
         if self.SortByField!='' and self.ClassItem.IsFieldInClass(self.SortByField):
            self.SortField=self.ClassItem.FieldsByName(self.SortByField)
            byfield=1
         else:
            byfield=0
         if self.InitialObjectsSet:
            arefs=FieldRefIterator(self.InitialObjectsSet)
            if not self.SortField is None:
               arefs.sort(self.SortField)
            aobj=arefs.AsObject()
         else:
            if self.SortDescending:
               aobj=self.ClassItem.GetLastObject(self.SortField)
            else:
               aobj=self.ClassItem.GetFirstObject(self.SortField)
      else:
         aobj=bobj
         byfield=0
      self.space.Caption=self.Name
      max=0
      aodd=0
      arow=1
      cnt=1
      if not self.AllDataToCheck:
         progressmax=self.NumDataToCheck
      else:
         if not aobj.Class is None:
            progressmax=aobj.Class.ObjectsCount()
         else:
            progressmax=0
      rrow=len(self.space.header)+1
      orow=rrow+1
      while aobj.Exists():
         if not self.AllDataToCheck:
            if max>=self.NumDataToCheck:
               break
         self.Tree.ClearValues()
         accepted,wobject=self.Tree.CheckObject(aobj.OID)
         if accepted or wobject:
            lrow=arow
            sdv=SummaryDataValue(None,cnt,str(cnt),aodd,aobj.OID,aobj.Class.CID)
            self.space[arow,1]=sdv
            self.ColsValues.Clear()
            arow=self.Tree.PrintObject(aobj.OID,self.ColsValues,self.space,aodd,aobj.OID,aobj.Class.CID)
            if self.CalculatedFields!=[]:
               crow=lrow
               while crow<arow:
                  self.ColsValues.Row=crow
                  for acf in self.CalculatedFields:
                     v,vs=acf.GetCalculatedValue(self.ColsValues)
                     if not v is None:
                        sdv=SummaryDataValue(None,v,vs,aodd,aobj.OID,aobj.Class.CID)
                        self.space[crow,acf.Col]=sdv
                  crow=crow+1
            self.Tree.SetMaxFieldRow(arow,self.space)
            if self.ColID>=0 and self.IsInteractive:
               while lrow<arow:
                  self.space[lrow,self.ColID]=SummaryDataValue(None,lrow,str(lrow),aodd,aobj.OID,aobj.Class.CID)
                  self.space[lrow,self.ColOID]=SummaryDataValue(None,aobj.OID,str(aobj.OID),aodd,aobj.OID,aobj.Class.CID)
                  lrow=lrow+1
            aodd=1-aodd
            cnt=cnt+1
#            print 'ACCEPTED!'
#         print '___________________________________________________________________'
         if self.SortDescending:
            aobj.Prev(self.SortField)
         else:
            aobj.Next(self.SortField)
         max=max+1
         if self.ShowProgress:
            if max%20==0:
               SetProgress(max,progressmax)
      if self.IsFooter:
         def FooterFunc(afield,aspace):
            v=afield.GetFooterValue()
            if not v is None:
               aspace.footer[afield.Col-1]=v
         for i in range(len(self.space.header)):
            self.space.footer.Append(None)
         self.Tree.ForEachField(FooterFunc,self.space)
         for acf in self.CalculatedFields:
            FooterFunc(acf,self.space)
      if self.ShowProgress:
         SetProgress(0,0)
      self.SummaryClass.LastCreated.SetValuesAsDateTime(self.summoid,ICORUtil.tdatetime())
      return cnt-1
   def dump(self):
      print self.Name,self.Description
      self.Tree.dump()
   def GenerateSrc(self):
      agenerator=SummaryGenerator(self)
      self.Tree.GenerateSrc(agenerator)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aspace=ICORMDSpace()
   asummary=ICORSummary(292,aspace,aIsInteractive=0)
   asummary.dump()
   print '*** SOURCE: ***'
   asummary.GenerateSrc()
#   asummary.ProcessAll()
#   fname=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath+'output.html')
#   fdir=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath)
#   GenerateAsHTML(asummary,aspace,fname,1,fdir)
#   ExecuteShellCommand(fname)
   print 'Koniec'
   return
