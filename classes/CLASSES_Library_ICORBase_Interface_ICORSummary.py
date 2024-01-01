# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

EXCEL=0
from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import *
from CLASSES_Library_NetBase_Utils_MDSpaceUtil import *
if EXCEL:
   from CLASSES_Library_Win32_OLE_ICORExcel import *
   from CLASSES_Library_Win32_OLE_MDSpaceUtil import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import random
import string
import time
import math
import re

MAX_SUMMARY_ROWS=50000
MAX_DELAY=3 # seconds

class SummaryDataValue:
   def __init__(self,afield,avalue,astringvalue,aodd,aoid,acid):
      self.Field=afield
      self.DataValue=avalue
      self.StringValue=astringvalue
      self.Odd=aodd
      self.RefOID=aoid
      self.RefCID=acid
   def __add__(self,other):
      if (self.Field.FieldTID in [mt_Integer,mt_Double]) and (other.Field.FieldTID in [mt_Integer,mt_Double]):
         d=self.DataValue+other.DataValue
         sv=ICORUtil.FormatFNum(d,self.Field.FieldFormat)
      else:
         d=self.DataValue
         sv=self.StringValue
      return SummaryDataValue(self.Field,d,sv,self.Odd,self.RefOID,self.RefCID)
   def __repr__(self):
      return self.StringValue
   def AlignmentStd(self):
      if self.Field is None:
         return -1
      else:
         return self.Field.AlignmentStd

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
      s='<TD class=objectsviewdata'+sadd+' >'
#      s='<TD class=objectsviewdata'+sadd+' NOWRAP>'
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

#SummaryConditionNames - only WWW conditions
SummaryConditionsAsStringWWW = {scEqual:'=',scDifferent:'&lt;&gt;',scGreater:'&gt;',scLess:'&lt;',scGreaterOrEqual:'&gt;=',scLessOrEqual:'&lt;=',
scRegExp:'wzorzec',scNotRegExp:'bez wzorca'}

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

#Pivot Field Type
pf_none,pf_row,pf_column,pf_data,pf_filter=0,1,2,3,4

#Pivot Field Group
pgf_none,pgf_sum,pgf_count,pgf_min,pgf_max=0,1,2,3,4

#Pivot Field Group as Text
pes_fieldgroup=['','sum','count','min','max']

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
      self.RuleDisabled=0
      self.Value2=self.Value
      self.IsValue2Check=0
      self.RuleFieldPath=''
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
         mname=mname.replace('\\','_')
         mname=mname.replace('/','_')
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
      if self.RuleDisabled:
         return 1,0
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
      self.RowGroup=-1
      self.ValuesCount=0
      self.PivotFieldType=-1
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
         avalue=self.avalue # str()
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
      self.RowGroup=-1
      self.PivotFieldType=pf_none
      self.PivotFieldGroupType=pgf_sum
   def __repr__(self):
      return '%d:%s - %d'%(self.ID,self.Caption,self.RowGroup)

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
      self.AccessLevelViewMethod=self.ClassItem.MethodsByName('AccessLevelView')
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
   def DoAddGroupField(self,aclass,afield,pfield,agrouptype,aunique,achart,afooter,afill,arowgroup):
      if afield.IsInteractive=='0':
         return
      if not self.SubTree.has_key(pfield.Name):
         atree=SummaryTree(aclass,self.Path,pfield,self.Level+1)
         self.SubTree[pfield.Name]=atree
      else:
         atree=self.SubTree[pfield.Name]
      self.Recur=atree.AddGroupField([afield.Name],self.space,agrouptype,aunique,achart,afooter,afill,arowgroup,self.Recur)
      return
   def AddGroupField(self,afield,aspace,agrouptype,aunique,achart,afooter,afill,arowgroup,arecur):
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
            self.Fields[fname].RowGroup=arowgroup
         else:
            w=1
            if self.Level>0 and afi.ClassOfType.CID in self.Recur:
               w=0
            if w:
               afi.ClassOfType.ForEachField(self.DoAddGroupField,afi,agrouptype,aunique,achart,afooter,afill,arowgroup)
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
            self.Recur=atree.AddGroupField(afield[1:],aspace,agrouptype,aunique,achart,afooter,afill,arowgroup,self.Recur)
      self.Recur=self.Recur[:-1]
      return self.Recur
   def AddRule(self,arule,pos=0,rulepath=''):
      mpfl=len(arule.ParentFieldsList)-1
      if pos>=mpfl:
         arule.SetClassItem(self.ClassItem)
         afi=self.ClassItem.FieldsByName(arule.FieldName)
         if rulepath:
            rulepath=rulepath+'/'+afi.FieldNameAsDisplayed
         else:
            rulepath=afi.FieldNameAsDisplayed
         arule.RuleFieldPath=rulepath
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
         if rulepath:
            rulepath=rulepath+'/'+afi.FieldNameAsDisplayed
         else:
            rulepath=afi.FieldNameAsDisplayed
         atree.AddRule(arule,pos+1,rulepath)
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
      ### 0 and  - UWAGA - pokazywanie danych z klas systemowych
      if self.AccessLevelViewMethod:
         if self.AccessLevelViewMethod('',aoid,'')!='1':
            return 0,0
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
      adelay=0
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
         return max,adelay
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
               stime=time.time()
               r,adelay=atree.PrintObject(arefs,acolsvalues,space,aodd,arefoid,arefcid,lev+1)
               if not adelay and time.time()-stime>MAX_DELAY:
                  DoEvents()
                  adelay=1
               if r>max:
                  max=r
                  atree.SetMaxFieldRow(max,space)
            else:
               while arefs.position>=0:
                  stime=time.time()
                  r,adelay=atree.PrintObject(arefs,acolsvalues,space,aodd,arefoid,arefcid,lev+1)
                  if not adelay and time.time()-stime>MAX_DELAY:
                     DoEvents()
                     adelay=1
                  if r>max:
                     max=r
                     atree.SetMaxFieldRow(max,space)
                  arefs.Next()
      if max>0:
         self.SetMaxFieldRow(max,space)
      return max,adelay
   def SetMaxFieldRow(self,max,space):
      for afield in self.Fields.values():
         if afield.IsFilled:
            for i in range(afield.Row,max):
               if space[i,afield.Col] is None:
                  space[i,afield.Col]=space[i-1,afield.Col]
         afield.Row=max
      for atree in self.SubTree.values():
         atree.SetMaxFieldRow(max,space)
   def ForEachField(self,afunc,*parms):
      for afield in self.Fields.values():
         apply(afunc,(afield,)+parms)
      for atree in self.SubTree.values():
         apply(atree.ForEachField,(afunc,)+parms)
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
      self.IsRowGroup=0
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
      self.ChartInfo=self.SummaryClass.ChartInfo[sumoid]
      self.ChartType=-1
      if self.ChartInfo:
         self.ChartType=int(self.ChartInfo)-1
         if self.ChartType<0:
            self.ChartType=-1
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
      self.ColumnsID=[]
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
            acolumn=SummaryColumn(i,sl1[0],sl1[1])
            self.Columns[sl1[0]]=acolumn
            self.ColumnsID.append(acolumn)
            self.space.header.Append(sl1[1])
            i=i+1
         for acf in self.CalculatedFields:
            acolumn=SummaryColumn(i,'',acf.Name)
            acolumn.RowGroup=1 #automatyczne sumowanie kolumn przeliczalnych
            self.ColumnsID.append(acolumn)
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
         if len(formdict.keys())>0:
            r1=int(formdict.get('condselect'+str(i),'-1'))
            if r1 in [scExisting,scNonExisting]:
               r1max=int(formdict.get('rulevalue%d_max'%i,'0'))
               r2=''
               for j in range(r1max):
                  s=formdict.get('rulevalue%d_%d'%(i,j),'')
                  if s:
                     r2=r2+s
            else:
               r2=formdict.get('rulevalue'+str(i),'')
         else:
            r1=-1
            r2=''
         arule=SummaryRule(aobj,self.IsCaseSensitive,r1,r2)
         if formdict.get('rulehidden%d'%i,'0')=='1':
            arule.RuleDisabled=1
         self.RulesList.append(arule)
         self.Tree.AddRule(arule)
         i=i+1
         aobj.Next()
      self.PivotRowCol,self.PivotColumnCol,self.PivotDataCol,self.PivotFilterCol=-1,-1,-1,-1
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
               if len(sl1)<8:
                  sl1.append('-1')
               if len(sl1)<9:
                  sl1.append('0')
               if len(sl1)<10:
                  sl1.append('0')
               sfp=string.split(sl1[0],'\\')
#               print sl1[0],sfp
               if sl1[5]!='-1':
                  self.IsFooter=1
               if sl1[7]!='-1':
                  self.IsRowGroup=1
               self.ColumnsID[i-2].RowGroup=int(sl1[7])
               if sl1[8]!='0':
                  self.IsPivot=1
               ipft=1+int(sl1[8])
               self.ColumnsID[i-2].PivotFieldType=ipft
               if ipft==pf_row:
                  self.PivotRowCol=i-2
               elif ipft==pf_column:
                  self.PivotColumnCol=i-2
               elif ipft==pf_data:
                  self.PivotDataCol=i-2
               elif ipft==pf_filter:
                  self.PivotFilterCol=i-2
               self.ColumnsID[i-2].PivotFieldGroupType=1+int(sl1[9])
               if sfp!=[]:        
                  self.Tree.AddGroupField(sfp,self.space,int(sl1[2]),int(sl1[3]),int(sl1[4]),int(sl1[5]),int(sl1[6]),int(sl1[7]),[])
            i=i+1
      self.IsPivot=self.PivotRowCol>=0 and self.PivotColumnCol>=0 and self.PivotDataCol>=0
      self.ShowProgress=1
#      self.dump()
   def dump(self):
      print self.Name,self.Description
      self.Tree.dump()
   def ProcessAll(self,bobj=None):
#      print 'process all',self.Name
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
      stime=time.time()
      while aobj.Exists():
         if not self.AllDataToCheck:
            if max>=self.NumDataToCheck:
               break
         self.Tree.ClearValues()
         accepted,wobject=self.Tree.CheckObject(aobj.OID)
         ntime=time.time()
         if ntime-stime>MAX_DELAY:
            DoEvents()
            stime=ntime
         if accepted or wobject:
            lrow=arow
            sdv=SummaryDataValue(None,cnt,str(cnt),aodd,aobj.OID,aobj.Class.CID)
            self.space[arow,1]=sdv
            self.ColsValues.Clear()
            arow,adelay=self.Tree.PrintObject(aobj.OID,self.ColsValues,self.space,aodd,aobj.OID,aobj.Class.CID)
            ntime=time.time()
            if ntime-stime>MAX_DELAY:
               DoEvents()
               stime=ntime
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
            if cnt>MAX_SUMMARY_ROWS:
               break
#            print 'ACCEPTED!'
#         print '___________________________________________________________________'
         if self.SortDescending:
            aobj.Prev(self.SortField)
         else:
            aobj.Next(self.SortField)
         max=max+1
         if not max%20:
            if self.ShowProgress:
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
      if self.IsRowGroup:
         self.DoGroupRows()
      if self.ShowProgress:
         SetProgress(0,0)
      self.SummaryClass.LastCreated.SetValuesAsDateTime(self.summoid,ICORUtil.tdatetime())
      return cnt-1
   def DoGroupRows(self):
      wcols=[]
      scols=[]
      wrdict={}
      for acolumn in self.ColumnsID:
         if acolumn.RowGroup==0: #w/g wartosci
            wcols.append(acolumn.ID)
         elif acolumn.RowGroup==1: # suma
            scols.append(acolumn.ID)
      fc=self.ColumnsID[0].ID
      lc=self.ColumnsID[len(self.ColumnsID)-1].ID
      arow=1
      loid,lcid=-1,-1
      k,v=self.space._items.GetFirst()
      while k>=0:
         kn,vn=self.space._items.GetNext(k)
         if v is None:
            k,v=kn,vn
            continue
         rid=(0,)
         for acol in wcols:
            v1=v._items[acol]
            if not v1 is None:
               rid=rid+(v1.Value.StringValue,)
            else:
               rid=rid+(None,)
         if wrdict.has_key(rid):
            srow=wrdict[rid]
            for i in scols:
               v1=self.space[srow,i]
               v2=self.space[k,i]
               if (not v1 is None) and (not v2 is None):
                  self.space[srow,i]=v1+v2
               elif v1 is None:
                  self.space[srow,i]=v2
               elif v2 is None:
                  self.space[srow,i]=v1
               else:
                  print 'None'
                  pass
            self.space.Remove(k)
         else:
            wrdict[rid]=k
            arow=arow+1
         k,v=kn,vn
      for i in range(len(self.space._items.keys)):
         self.space._items.keys[i]=i+1
      tslist=self.space._items.keys[:]
      def myfunc(a,b,aspace=self.space,wcols=wcols):
         for acol in wcols:
            v1=aspace[a,acol]
            if v1 is None:
               return -1
            v2=aspace[b,acol]
            if v2 is None:
               return 1
            if v1.DataValue<v2.DataValue:
               return -1
            elif v1.DataValue>v2.DataValue:
               return 1
         return 0
      tslist.sort(myfunc)
      k,v=[],[]
      for i in range(len(tslist)):
         k.append(i+1)
         v.append(self.space._items.values[tslist[i]-1])
      self.space._items.keys=k
      self.space._items.values=v
      lastv=map(lambda x: '',self.ColumnsID)
      for i in range(len(tslist)):
         self.space[i+1,1]=SummaryDataValue(None,i+1,str(i+1),0,-1,-1)
         for acol in wcols:
            sdv=self.space[i+1,acol]
            if not sdv:
               continue
            if sdv.StringValue==lastv[acol-2]:
               self.space[i+1,acol]=SummaryDataValue(sdv.Field,'','',0,sdv.RefOID,sdv.RefCID)
            else:
               lastv[acol-2]=sdv.StringValue
#      print 'po'
#      self.space.Dump()

def GenerateAsHTML(asummary,aspace,fname,aspage=1,aoutputdir='',asimple=0):
   if asimple:
      siterator=SummarySpace2HTMLSimple(aspace,fname,aspage,'',askiplastcolumns=2)
   else:
      siterator=SummarySpace2HTML(aspace,fname,aspage,'',askiplastcolumns=0)
   solist=[]
   siterator.ForEachNotEmptyRow()
   del siterator

#**************************************
def GenerateAsHTML_TDC(asummary,aspace,fname,aspage=1,aoutputdir='',acount=-1):
   csvfname='sd_%d.csv'%(asummary.summoid)
   if aoutputdir=='':
      csvpath=aICORWWWServerInterface.AppOutputPath+csvfname
   else:
      csvpath=aoutputdir+csvfname
   csvpath=FilePathAsSystemPath(csvpath)
   siterator=SummarySpace2CSV(aspace,csvpath,1,1,1)
   siterator.FieldDelimiter=','
   siterator.HeaderTypes[0]='INT'
   def FuncCol(afield,aiterator):
      if afield.Field.FieldTID==mt_String:
         aiterator.HeaderTypes[afield.Col-1]='STRING'
      elif afield.Field.FieldTID==mt_Integer:
         aiterator.HeaderTypes[afield.Col-1]='INT'
      elif afield.Field.FieldTID==mt_Boolean:
         aiterator.HeaderTypes[afield.Col-1]='BOOLEAN'
      elif afield.Field.FieldTID==mt_DateTime:
         aiterator.HeaderTypes[afield.Col-1]='DATE YMD'
      elif afield.Field.FieldTID==mt_Double:
         aiterator.HeaderTypes[afield.Col-1]='FLOAT'
      else:
         aiterator.HeaderTypes[afield.Col-1]='STRING'
#      print afield.Field.Name,afield.Col,aiterator.HeaderTypes[afield.Col-1]
   asummary.Tree.ForEachField(FuncCol,siterator)
   i=len(siterator.HeaderTypes.keys())
   for acf in asummary.CalculatedFields:
      siterator.HeaderTypes[i]='FLOAT' #Calculated fields
      i=i+1
   siterator.HeaderTypes[i]='INT' #RowID
   siterator.HeaderTypes[i+1]='INT' #OID

   if acount<=0:
      siterator.ForEachNotEmptyRow()
      del siterator
      return
   if type(fname)==type(''):
      isfile=0
      file=open(fname,'w')
   else:
      isfile=1
      file=fname

   solist=[]

   try:
      file.write("""
<OBJECT id=tdcICORData_%(SUID)s CLASSID="clsid:333C7BC4-460F-11D0-BC04-0080C7055A83">
   <PARAM NAME="DataURL" VALUE="output/%(csvfname)s?fparam=%(fparam)d">
   <PARAM NAME="UseHeader" VALUE="True">
   <PARAM NAME="CaseSensitive" VALUE="False">
   <PARAM NAME="FieldDelim" VALUE="%(fielddelim)s">
   <PARAM NAME="Charset" VALUE="windows-1250">
</OBJECT>
<!-- <BR>
<TABLE><TR>
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' ID=cmdpreviousPage_%(SUID)s onclick="aICORDataTable_%(SUID)s.previousPage()">Poprzednia strona</BUTTON></TD>
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' ID=cmdnextPage_%(SUID)s onclick="aICORDataTable_%(SUID)s.nextPage()">Następna strona</BUTTON></TD>
</TR></TABLE><BR> -->"""%{'SUID':asummary.SUID,'csvfname':csvfname,'fparam':random.randint(1,100000),'fielddelim':','})

      s="""
<SCRIPT LANGUAGE=javascript FOR=aICORDataTable_%(SUID)s EVENT=onclick>
   var aelem=window.event.srcElement;
   if (aelem.tagName=="DIV") {
      aelem=aelem.parentElement;
      } else {
      return;
      }
   if (aelem.tagName=="TD") {
      var ri=aelem.parentElement.rowIndex;
      var s=this.rows(ri).cells(%(param1)d).innerText;
      window.location="icormain.asp?jobtype=objectedit&CID=%(param2)d&OID="+s;
      }
   window.event.cancelBubble = true;
</SCRIPT>
<SCRIPT LANGUAGE=javascript>
var lastcolclicked_%(SUID)s=-1;
var lastsorttype_%(SUID)s='-';
function headerClick_%(SUID)s(acolid) {
   if (lastcolclicked_%(SUID)s!=acolid) {
      lastsorttype_%(SUID)s='-';
      }
   if (lastsorttype_%(SUID)s=='-') {
      lastsorttype_%(SUID)s='+';
      } else {
      lastsorttype_%(SUID)s='-';
      }
   tdcICORData_%(SUID)s.Sort = lastsorttype_%(SUID)s+tdcICORData_%(SUID)s.recordset.fields(acolid).name;
   tdcICORData_%(SUID)s.Reset();
   lastcolclicked_%(SUID)s=acolid;
}
</SCRIPT>
<TABLE id=aICORDataTable_%(SUID)s class=objectsviewtable datasrc=#tdcICORData_%(SUID)s DATAPAGESIZE=0>
<caption class=objectsviewcaption>%(param3)s</caption>
<THEAD>
"""%{'SUID':asummary.SUID,'param1':len(siterator.HeaderTypes)-1,'param2':asummary.ClassItem.CID,'param3':asummary.Name}
      file.write(s)
      for i in range(len(aspace.header)-2):
         if i==0:
            k=len(aspace.header)-2
         else:
            k=i
         file.write('<TH onclick="headerClick_%(SUID)s(%(param1)d);" style="cursor=hand;" class=objectsviewheader>%(param2)s</TH>\n'%{'SUID':asummary.SUID,'param1':k,'param2':aspace.header[i]})
      s="""                        
</THEAD>
<TBODY>
<TR class=objectsviewrow>
"""
      file.write(s)
      for i in range(len(aspace.header)-2):
         try:
            if siterator.HeaderTypes[i]=='STRING':
               s='left'
            else:
               s='right'
         except:
            s='right'
#         file.write('<TD class=objectsviewdataeven NOWRAP><DIV align="%s" style="cursor=hand;" datafld="Column%d"></DIV></TD>\n'%(s,i+1))
         file.write('<TD class=objectsviewdataeven ><DIV align="%s" style="cursor=hand;" datafld="Column%d"></DIV></TD>\n'%(s,i+1))
      file.write('<TD width=0 style="visibility:hidden;display:none;"><DIV style="visibility:hidden;display:none;" datafld="Column%d"></DIV></TD>\n'%(i+2))
      file.write('<TD width=0 style="visibility:hidden;display:none;"><DIV style="visibility:hidden;display:none;" datafld="Column%d"></DIV></TD>\n'%(i+3))
      file.write('<TD></TD></TR></TBODY>')
      if len(aspace.footer)>0:
         file.write('<TFOOT><TR>')
         for x in range(len(aspace.footer)-2):
            avalue=aspace.footer.values[x]
            if avalue is None:
               file.write('<TD class=objectsviewfooter>&nbsp;</TD>')
               continue
            if type(avalue)!=type(''):
               avalue=str(avalue)
            file.write('<TD class=objectsviewfooter>'+avalue+'</TD>')
         file.write('</TR></TFOOT>')
      file.write('</TABLE>')
      s="""
<BR>

<!--
<TABLE><TR>
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' ID=cmdpreviousPage_%(SUID)s onclick="aICORDataTable_%(SUID)s.previousPage()">Poprzednia strona</BUTTON></TD>
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' ID=cmdnextPage_%(SUID)s onclick="aICORDataTable_%(SUID)s.nextPage()">Następna strona</BUTTON></TD>
</TR></TABLE>
<BR>
<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick='if (document.getElementById("setTableRowsCountDiv1_%(SUID)s").style.display!="") {document.getElementById("setTableRowsCountDiv1_%(SUID)s").style.display="";}else{document.getElementById("setTableRowsCountDiv1_%(SUID)s").style.display="none";};'>Ilość wierszy</BUTTON>
<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick='if (document.getElementById("setTableFilterDiv1_%(SUID)s").style.display!="") {document.getElementById("setTableFilterDiv1_%(SUID)s").style.display="";}else{document.getElementById("setTableFilterDiv1_%(SUID)s").style.display="none";};'>Filtrowanie danych</BUTTON>
<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick='if (document.getElementById("setTableSortDiv1_%(SUID)s").style.display!="") {document.getElementById("setTableSortDiv1_%(SUID)s").style.display="";}else{document.getElementById("setTableSortDiv1_%(SUID)s").style.display="none";};'>Sortowanie danych</BUTTON>
-->

<SCRIPT LANGUAGE=javascript>
function aDataPageSizeSelect_%(SUID)s_onchange() {
   var si=document.getElementById("aDataPageSizeSelect_%(SUID)s").selectedIndex;
   aICORDataTable_%(SUID)s.dataPageSize = document.getElementById("aDataPageSizeSelect_%(SUID)s").options(si).value;
   document.getElementById("setTableRowsCountDiv1_%(SUID)s").style.display='none';
//   document.getElementById("cmdpreviousPage_%(SUID)s").scrollIntoView(1);
}
</SCRIPT>

<!--
<BR>
<TABLE bgcolor="silver" cellspacing=0 cellpadding=0>
<TR>
<TD bgcolor="ACTIVECAPTION"><FONT face="Arial" size="-2" color="white"><b>&nbsp;&nbsp;Ustaw ilość wierszy&nbsp;&nbsp;</b><font></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="ukryj" style="cursor:pointer" src="images/caption_button_minimize.gif" onclick="document.getElementById("setTableRowsCountDiv1_%(SUID)s").style.display='none';"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="pokaż" style="cursor:pointer" src="images/caption_button_maximize.gif" onclick="document.getElementById("setTableRowsCountDiv1_%(SUID)s").style.display='';/*document.getElementById("setTableRowsCountDiv1_%(SUID)s.scrollIntoView(0);*/"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG src="images/caption_button_close.gif"></TD>
</TR>
<TR><TD>

<DIV ID=setTableRowsCountDiv1_%(SUID)s STYLE="display:none">
<TABLE bgcolor="BUTTONFACE" cellspacing=10>
<TR>
<TD>Ilość&nbsp;wierszy&nbsp;w&nbsp;tabeli:</TD><TD><SELECT ID=aDataPageSizeSelect_%(SUID)s name=aDataPageSizeSelect_%(SUID)s LANGUAGE=javascript onchange="return aDataPageSizeSelect_%(SUID)s_onchange()">
<OPTION value=5>5</OPTION>
<OPTION value=10>10</OPTION>
<OPTION value=15 Selected>15</OPTION>
<OPTION value=20>20</OPTION>
<OPTION value=25>25</OPTION>
<OPTION value=50>50</OPTION>
<OPTION value=75>75</OPTION>
<OPTION value=100>100</OPTION>
<OPTION value=200>200</OPTION>
<OPTION value=500>500</OPTION>
<OPTION value=1000>1000</OPTION>
<OPTION value=0>wszystkie</OPTION>
</SELECT></TD>

</TR></TABLE>
</DIV>
</TD></TR></TABLE>
<BR>
-->

<SCRIPT LANGUAGE=javascript>
function ReplaceChar_%(SUID)s(s,ch,rc) {
   var r="",i;
   for (i=0;i<s.length;i++) {
      c=s.substr(i,1)
      if (c==ch) {
         r=r+rc;
         } else {
         r=r+c;
         }
      }
   return(r);
}
function aFielNameSelect_%(SUID)s_onchange() {
   var sv;
   var va;
   var sf = "";
   
   va=document.getElementById("aFielNameSelect1_%(SUID)s").options(document.getElementById("aFielNameSelect1_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
//      va=tdcICORData_%(SUID)s.recordset.fields(parseInt(va)).name;
//      if (va.indexOf(" ",0)>=0)
//         va=ReplaceChar_%(SUID)s(va," ","\\ ");
      sv=document.getElementById("aFieldValue1_%(SUID)s").value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.getElementById("aFieldConditionSelect1_%(SUID)s").options(document.getElementById("aFieldConditionSelect1_%(SUID)s").selectedIndex).value+sv;
      }

   va=document.getElementById("aFielNameSelect2_%(SUID)s").options(document.getElementById("aFielNameSelect2_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.getElementById("aFieldValue2_%(SUID)s").value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.getElementById("aFieldConditionSelect2_%(SUID)s").options(document.getElementById("aFieldConditionSelect2_%(SUID)s").selectedIndex).value+sv;
      }

   va=document.getElementById("aFielNameSelect3_%(SUID)s").options(document.getElementById("aFielNameSelect3_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.getElementById("aFieldValue3_%(SUID)s").value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.getElementById("aFieldConditionSelect3_%(SUID)s").options(document.getElementById("aFieldConditionSelect3_%(SUID)s").selectedIndex).value+sv;
      }

   va=document.getElementById("aFielNameSelect4_%(SUID)s").options(document.getElementById("aFielNameSelect4_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.getElementById("aFieldValue4_%(SUID)s").value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.getElementById("aFieldConditionSelect4_%(SUID)s").options(document.getElementById("aFieldConditionSelect4_%(SUID)s").selectedIndex).value+sv;
      }

   va=document.getElementById("aFielNameSelect5_%(SUID)s").options(document.getElementById("aFielNameSelect5_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va="Column"+va;
      sv=document.getElementById("aFieldValue5_%(SUID)s").value;
      if (sv.indexOf(" ",0)>=0 || sv=="")
         sv='"'+sv+'"';
      if (sf!="")
         sf=sf+" & ";
      sf=sf+va+document.getElementById("aFieldConditionSelect5_%(SUID)s").options(document.getElementById("aFieldConditionSelect5_%(SUID)s").selectedIndex).value+sv;
      }
   tdcICORData_%(SUID)s.object.Filter = sf;
   tdcICORData_%(SUID)s.Reset();
   document.getElementById("setTableFilterDiv1_%(SUID)s").style.display='none';
//   document.getElementById('cmdpreviousPage_%(SUID)s').scrollIntoView(1);
}
function aClearAllConditions_%(SUID)s() {
   document.getElementById("aFielNameSelect1_%(SUID)s").selectedIndex=0;
   document.getElementById("aFielNameSelect2_%(SUID)s").selectedIndex=0;
   document.getElementById("aFielNameSelect3_%(SUID)s").selectedIndex=0;
   document.getElementById("aFielNameSelect4_%(SUID)s").selectedIndex=0;
   document.getElementById("aFielNameSelect5_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldValue1_%(SUID)s").value="";
   document.getElementById("aFieldValue2_%(SUID)s").value="";
   document.getElementById("aFieldValue3_%(SUID)s").value="";
   document.getElementById("aFieldValue4_%(SUID)s").value="";
   document.getElementById("aFieldValue5_%(SUID)s").value="";
   document.getElementById("aFieldConditionSelect1_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldConditionSelect2_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldConditionSelect3_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldConditionSelect4_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldConditionSelect5_%(SUID)s").selectedIndex=0;
   tdcICORData_%(SUID)s.object.Filter = "";
   tdcICORData_%(SUID)s.Reset();
}
function aSortButtonClick_%(SUID)s(){
   var va;
   var sf = "";
   
   va=document.getElementById("aFieldSortSelect1_%(SUID)s").options(document.getElementById("aFieldSortSelect1_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va=tdcICORData_%(SUID)s.recordset.fields(parseInt(va)).name;
      if (sf!="")
         sf=sf+"; ";
      sf=sf+document.getElementById("aFieldSortCond1_%(SUID)s").options(document.getElementById("aFieldSortCond1_%(SUID)s").selectedIndex).value+va;
      }
   va=document.getElementById("aFieldSortSelect2_%(SUID)s").options(document.getElementById("aFieldSortSelect2_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va=tdcICORData_%(SUID)s.recordset.fields(parseInt(va)).name;
      if (sf!="")
         sf=sf+"; ";
      sf=sf+document.getElementById("aFieldSortCond2_%(SUID)s").options(document.getElementById("aFieldSortCond2_%(SUID)s").selectedIndex).value+va;
      }
   va=document.getElementById("aFieldSortSelect3_%(SUID)s").options(document.getElementById("aFieldSortSelect3_%(SUID)s").selectedIndex).value;
   if (va!="-1") {
      va=tdcICORData_%(SUID)s.recordset.fields(parseInt(va)).name;
      if (sf!="")
         sf=sf+"; ";
      sf=sf+document.getElementById("aFieldSortCond3_%(SUID)s").options(document.getElementById("aFieldSortCond3_%(SUID)s").selectedIndex).value+va;
      }
   tdcICORData_%(SUID)s.object.Sort = sf;
   tdcICORData_%(SUID)s.Reset();
   document.getElementById("setTableSortDiv1_%(SUID)s").style.display='none';
//   document.getElementById("cmdpreviousPage_%(SUID)s").scrollIntoView(1);
}
function aClearSortClick_%(SUID)s(){
   document.getElementById("aFieldSortSelect1_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldSortCond1_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldSortSelect2_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldSortCond2_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldSortSelect3_%(SUID)s").selectedIndex=0;
   document.getElementById("aFieldSortCond3_%(SUID)s").selectedIndex=0;
   tdcICORData_%(SUID)s.object.Sort = "";
   tdcICORData_%(SUID)s.Reset();
}
</SCRIPT>

<!--
<TABLE bgcolor="silver" cellspacing=0 cellpadding=0>
<TR>
<TD bgcolor="ACTIVECAPTION"><FONT face="Arial" size="-2" color="white"><b>&nbsp;&nbsp;Parametry filtrowania&nbsp;&nbsp;</b><font></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="ukryj" style="cursor:pointer" src="images/caption_button_minimize.gif" onclick="document.getElementById('setTableFilterDiv1_%(SUID)s').style.display='none';"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="pokaż" style="cursor:pointer" src="images/caption_button_maximize.gif" onclick="document.getElementById('setTableFilterDiv1_%(SUID)s').style.display='';/*document.getElementById('setTableFilterDiv1_%(SUID)s').scrollIntoView(0);*/"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG src="images/caption_button_close.gif"></TD>
</TR>
<TR><TD>
<DIV ID=setTableFilterDiv1_%(SUID)s STYLE="display:none">
<TABLE bgcolor="BUTTONFACE" cellspacing=10>
<TR>
<TD>
Poniżej możesz wybrać warunki, którymi ograniczysz wyświetlane dane. Dla pól tekstowych możesz napisać
na końcu znak '*' aby znaleźć wszystkie wartości rozpoczynające się od wpisanego słowa np. 'b*' uwzględni
tylko 'Biłgoraj','Bydgoszcz' itd. Jeśli chcesz pozbyć się pustych komórek możesz ograniczyć widok stosując
operator '<' np. pole 'Ilość' ma być mniejsze od 100000. Wynika to z faktu, że puste komórki są traktowane podczas
porównań jako większe od dowolnych komórek wypełnionych wartością.
</TD></TR>
<TR>
"""%{'SUID':asummary.SUID}
      file.write(s)
      s="""
<TABLE>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect1_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i+1,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect1_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue1_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect2_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i+1,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect2_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue2_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect3_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i+1,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect3_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue3_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect4_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i+1,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect4_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue4_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
<TR><TD>Kolumna:</TD><TD><SELECT ID=aFielNameSelect5_%(SUID)s>
<OPTION SELECTED value="-1">brak warunku</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i+1,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldConditionSelect5_%(SUID)s>
<OPTION value=" = " SELECTED> = </OPTION><OPTION value=" > "> > </OPTION><OPTION value=" >= "> >= </OPTION><OPTION value=" < "> < </OPTION><OPTION value=" <= "> <= </OPTION><OPTION value=" <> "> <> </OPTION>
</SELECT></TD><TD>
<INPUT ID=aFieldValue5_%(SUID)s TYPE=TEXT VALUE=""></TD></TR>
</TABLE>
<br>
<TABLE><TR>
<TD>&nbsp;&nbsp;<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="return aFielNameSelect_%(SUID)s_onchange()">Uwzględnij warunki</BUTTON></TD>
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="return aClearAllConditions_%(SUID)s()">Skasuj warunki</BUTTON></TD>
</TR></TABLE>
"""%{'SUID':asummary.SUID}
      file.write(s)
# sort
      s="""
</TR></TABLE>
</DIV>

</TD></TR></TABLE>
<BR>
<TABLE bgcolor="silver" cellspacing=0 cellpadding=0>
<TR>
<TD bgcolor="ACTIVECAPTION"><FONT face="Arial" size="-2" color="white"><b>&nbsp;&nbsp;Parametry sortowania&nbsp;&nbsp;</b><font></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="ukryj" style="cursor:pointer" src="images/caption_button_minimize.gif" onclick="document.getElementById('setTableSortDiv1_%(SUID)s').style.display='none';"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG alt="pokaż" style="cursor:pointer" src="images/caption_button_maximize.gif" onclick="document.getElementById('setTableSortDiv1_%(SUID)s').style.display='';/*document.getElementById('setTableSortDiv1_%(SUID)s').scrollIntoView(0);*/"></TD>
<TD bgcolor="ACTIVECAPTION"><IMG src="images/caption_button_close.gif"></TD>
</TR>
<TR><TD>
<DIV ID=setTableSortDiv1_%(SUID)s STYLE="display:none">
<TABLE bgcolor="BUTTONFACE" cellspacing=10>
<TR>

<TD>Poniżej możesz wybrać kolumny, według których chcesz sortować dane. Kliknięcie na nagłówek
kolumny także powoduje sortowanie tej kolumny, klikając ponownie zmieni się sposób sortowania z
rosnącego na malejący. Sortując według pierwszej kolumny (l.p.) wrócisz do pierwotnego ułożenia danych.
</TD></TR>
<TR>
"""%{'SUID':asummary.SUID}
      file.write(s)
      s="""
<TABLE>
<TR><TD align=right>I&nbsp;sortowanie&nbsp;w/g:</TD><TD><SELECT ID=aFieldSortSelect1_%(SUID)s>
<OPTION SELECTED value="-1">nie sortuj</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldSortCond1_%(SUID)s>
<OPTION value="+" SELECTED> rosnąco </OPTION><OPTION value="-"> malejąco </OPTION>
</SELECT></TD></TR>
"""%{'SUID':asummary.SUID}
      file.write(s)
      s="""
<TR><TD align=right>II&nbsp;sortowanie&nbsp;w/g:</TD><TD><SELECT ID=aFieldSortSelect2_%(SUID)s>
<OPTION SELECTED value="-1">nie sortuj</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldSortCond2_%(SUID)s>
<OPTION value="+" SELECTED> rosnąco </OPTION><OPTION value="-"> malejąco </OPTION>
</SELECT></TD></TR>
"""%{'SUID':asummary.SUID}
      file.write(s)
      s="""
<TR><TD align=right>III&nbsp;sortowanie&nbsp;w/g:</TD><TD><SELECT ID=aFieldSortSelect3_%(SUID)s>
<OPTION SELECTED value="-1">nie sortuj</OPTION>
"""%{'SUID':asummary.SUID}
      file.write(s)
      for i in range(1,len(aspace.header)-2):
         file.write('<OPTION value="%d">%s</OPTION>'%(i,aspace.header[i]))
      s="""
</SELECT></TD><TD>
<SELECT ID=aFieldSortCond3_%(SUID)s>
<OPTION value="+" SELECTED> rosnąco </OPTION><OPTION value="-"> malejąco </OPTION>
</SELECT></TD></TR>
</TABLE>
<BR>
<TABLE><TR>
<TD>&nbsp;&nbsp;<BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="return aSortButtonClick_%(SUID)s()">Sortuj</BUTTON></TD>
<TD><BUTTON class='fg-button-single ui-state-default ui-corner-all uihover' onclick="return aClearSortClick_%(SUID)s()">Skasuj sortowanie</BUTTON></TD>
</TR></TABLE>         
</TR></TABLE>
</DIV>
</TD></TR></TABLE>
-->
"""%{'SUID':asummary.SUID}
      file.write(s)
      siterator.ForEachNotEmptyRow()
   finally:
      del siterator
      if not isfile:
         file.close()

def DoSummarySave(OID):
   s='SUMM0001'+chr(252)
   sclass=aICORDBEngine.Classes['CLASSES_System_SummaryItem']
   sfields=["AllDataToCheck", "CheckedList", "Description", "Name",
      "NumDataToCheck", "ShowAllRefs", "ShowFieldLinks",
      "Summaries", "UseLastModification", "OwnerCID", "SumFields",
      "RecurField", "RecurSummOID", "ColumnsPos", "WWWDisabled",
      "IsCaseSensitive", "ChartFields", "ChartInfo", "SummaryData1",
      "GroupNoRecur", "LastCreated", "SortByField", "CalcFields","InitialObjectsSet",
      "SortDescending"]
   for fname in sfields:
      afi=sclass.FieldsByName(fname)
      s=s+fname+chr(252)+afi[OID]+chr(252)
   rclass=sclass.Rules.ClassOfType
   rfields=["Condition", "FieldName", "Linkage", "ParentFieldsList", "Value", "FunctionName"]
   arefs=sclass.Rules.GetRefList(OID)
   while arefs:
      s=s+'Rules'+chr(252)+chr(252)
      for fname in rfields:
         afi=rclass.FieldsByName(fname)
         s=s+fname+chr(252)+afi[arefs.OID]+chr(252)
      arefs.Next()
   return s

def DoSummaryLoad(s,OID=-1,ainteractive=1,ownerClass=None):
   sl=string.split(s,chr(252))
   if sl==[]:
      if ainteractive:
         MessageDialog('Plik nie zawiera informacji o zestawieniu',mtError,mbOK)
      return OID
   if sl[0]!='SUMM0001':
      if ainteractive:
         MessageDialog('Plik nie zawiera informacji o zestawieniu',mtError,mbOK)
      return OID
   sclass=aICORDBEngine.Classes['CLASSES_System_SummaryItem']
   if OID<0:
      OID=sclass.AddObject()
      if not ownerClass is None:
         oclass=aICORDBEngine.Classes[ownerClass]
         sclass.OwnerCID[OID]=str(oclass.CID)
         sclass.AllDataToCheck[OID]='1'
         aICORDBEngine.Classes.MetaClass.aSummaries.AddRefs(oclass.CID,[OID,sclass.CID],ainsertifnotexists=1)
   rclass=sclass.Rules.ClassOfType
   max=len(sl)
   i=1
   while i<max-1:
      s1,s2=sl[i],sl[i+1]
      if s1=='Rules':
         break
      afi=sclass.FieldsByName(s1)
      if s1=='OwnerCID':
         if ownerClass is None:
            aICORDBEngine.Classes.MetaClass.aSummaries.AddRefs(int(s2),[OID,sclass.CID],ainsertifnotexists=1)
            afi[OID]=s2
      else:
         afi[OID]=s2
      i=i+2
   sr=''
   while i<max-1:
      s1,s2=sl[i],sl[i+1]
      i=i+2
      if s1=='Rules':
         roid=rclass.AddObject()
         sr=sr+str(roid)+':'+str(rclass.CID)+':'
         continue
      afi=rclass.FieldsByName(s1)
      afi[roid]=s2
   sclass.Rules[OID]=sr
   return OID

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aspace=ICORMDSpace()
   asummary=ICORSummary(305,aspace,aIsInteractive=0)
   asummary.ProcessAll()
   fname=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath+'output.html')
   fdir=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath)
   GenerateAsHTML(asummary,aspace,fname,1,fdir)

   ExecuteShellCommand(fname)
   print 'Koniec'
   return



