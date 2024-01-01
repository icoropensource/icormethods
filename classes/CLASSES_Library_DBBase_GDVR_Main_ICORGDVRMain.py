# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

class ICORGDVRDateValue:
   def __init__(self,aoid):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Dictionary_DateValue']
      self.OID=aoid
      self._ValueDT,self._ValueF=None,None
   def __getattr__(self,name):
      if name=='ValueDT':
         if self._ValueDT is None:
            self._ValueDT=self.ClassItem.ValueDT.ValuesAsDate(self.OID)
         return self._ValueDT
      elif name=='ValueF':
         if self._ValueF is None:
            self._ValueF=self.ClassItem.ValueF.ValuesAsFloat(self.OID)
         return self._ValueF
   def SetValueF(self,avalue):
      self.ClassItem.ValueF[self.OID]=str(avalue)
      self._ValueF=avalue

class ICORGDVRField:
   def __init__(self,aoid):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Dictionary_ValueField']
      self.DateValueClass=self.ClassItem.DateValues.ClassOfType
      self.OID=aoid
      self.Caption=self.ClassItem.Caption[aoid]
      self._DateValues=None
      self._FormulaText=None
   def __getattr__(self,name):
      if name=='DateValues':
         if self._DateValues is None:
            self._DateValues={}
            aobj=self.ClassItem[self.OID].DateValues
            while aobj.Exists():
               aitem=ICORGDVRDateValue(aobj.OID)
               self.DateValues[aitem.ValueDT]=aitem
               aobj.Next()
         return self._DateValues
      if name=='FormulaText':
         if self._FormulaText is None:
            self._FormulaText=self.ClassItem.FormulaText[self.OID]
         return self._FormulaText
   def __getitem__(self,key):
      if self.DateValues.has_key(key):
         return self.DateValues[key].ValueF
      return 0.0
   def __setitem__(self,key,value):
      if not self.DateValues.has_key(key):
         doid=self.DateValueClass.AddObject()
         self.DateValueClass.ValueDT.SetValuesAsDate(doid,key)
         self.ClassItem.DateValues.AddRefs(self.OID,[doid,self.DateValueClass.CID],asortedreffield=self.DateValueClass.ValueDT)
         aitem=ICORGDVRDateValue(doid)
         self._DateValues[key]=aitem
      else:
         aitem=self._DateValues[key]
      aitem.SetValueF(value)
   def SetFormula(self,avalue):
      self.ClassItem.FormulaText[self.OID]=avalue
      self._FormulaText=avalue
      gdict={
         'setvalue':self.SetValue,
      }
      sl=string.split(avalue,'#!')
      for aline in sl:
         l=string.strip(aline)
         if not l:
            continue
         try:
            res=eval(l,gdict)
         except:
            print 'Błąd podczas obliczania formuły:',l
            raise
   def SetValue(self,ayear,amonth,aday,avalue):
      adate=(ayear,amonth,aday)
      self.__setitem__(adate,avalue)

class ICORGDVRItem:
   def __init__(self,aoid):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Dictionary_Item']
      self.AccountRangeClass=self.ClassItem.AccountRange.ClassOfType
      self.ValueFieldsClass=self.ClassItem.ValueFields.ClassOfType
      self.OID=aoid
      self.Code=self.ClassItem.ItemCode[aoid]
      self._ValueFields=None
      self._Name,self._Source,self._Description=None,None,None
      self._AccountObj,self._AccountFrom,self._AccountTo,self._AccountMask=None,None,None,None
   def __getattr__(self,name):
      if name=='ValueFields':
         if self._ValueFields is None:
            self._ValueFields={}
            aobj=self.ClassItem[self.OID].ValueFields
            while aobj.Exists():
               aitem=ICORGDVRField(aobj.OID)
               self._ValueFields[aitem.Caption]=aitem
               aobj.Next()
         return self._ValueFields
      if name=='Name':
         if self._Name is None:
            self._Name=self.ClassItem.ItemName[self.OID]
         return self._Name
      if name=='Source':
         if self._Source is None:
            self._Source=self.ClassItem.ItemSource[self.OID]
         return self._Source
      if name=='Description':
         if self._Description is None:
            self._Description=self.ClassItem.Description[self.OID]
         return self._Description
      if name=='AccountObj':
         if self._AccountObj is None:
            if self.ClassItem.AccountRange[self.OID]=='':
               roid=self.AccountRangeClass.AddObject()
               self.ClassItem.AccountRange[self.OID]=[roid,self.AccountRangeClass.CID]
            self._AccountObj=self.ClassItem[self.OID].AccountRange
         return self._AccountObj
      if name=='AccountFrom':
         if self._AccountFrom is None:
            self._AccountFrom=self.AccountObj.AccountFrom
         return self._AccountFrom
      if name=='AccountTo':
         if self._AccountTo is None:
            self._AccountTo=self.AccountObj.AccountTo
         return self._AccountTo
      if name=='AccountMask':
         if self._AccountMask is None:
            self._AccountMask=self.AccountObj.AccountMask
         return self._AccountMask
   def __getitem__(self,key):
      return self.ValueFields[key]
   def SetName(self,aname):
      self.ClassItem.ItemName[self.OID]=aname
      self._Name=aname
   def SetSource(self,asource):
      self.ClassItem.ItemSource[self.OID]=asource
      self._Source=asource
   def SetDescription(self,adescription):
      self.ClassItem.Description[self.OID]=adescription
      self._Description=adescription
   def SetAccounts(self,afrom,ato,amask):
      self.AccountObj.AccountFrom=afrom
      self.AccountObj.AccountTo=ato
      self.AccountObj.AccountMask=amask
   def AddField(self,aname,adesc):
      foid=self.ValueFieldsClass.AddObject()
      self.ValueFieldsClass.Caption[foid]=aname
      self.ValueFieldsClass.Description[foid]=adesc
      self.ClassItem.ValueFields.AddRefs(self.OID,[foid,self.ValueFieldsClass.CID],asortedreffield=self.ValueFieldsClass.Caption)
      aitem=ICORGDVRField(foid)
      self._ValueFields[aname]=aitem
      return aitem
   def SetFieldValue(self,aname,adesc,avalue):
      if not self.ValueFields.has_key(aname):
         self.AddField(aname,adesc)
      self.ValueFields[aname].SetFormula(avalue)

class ICORGDVRDict:
   def __init__(self,aoid):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Main']
      self.ItemsClass=self.ClassItem.Items.ClassOfType
      self.OID=aoid
      self.Name=self.ClassItem.DictName[aoid]
      self._Items=None
      self._ItemsNames=None
   def __repr__(self):
      return self.Name
   def __str__(self):
      return self.Name
   def __getattr__(self,name):
      if name=='Items':
         if self._Items is None:
            self._Items={}
            aobj=self.ClassItem[self.OID].Items
            while aobj.Exists():
               aitem=ICORGDVRItem(aobj.OID)
               self._Items[aitem.Code]=aitem
               aobj.Next()
         return self._Items
   def __getitem__(self,key):
      if type(key)!=type('') and (len(key)==3):
         return self.Items[key[0]][key[1]][key[2]]
      return self.Items[key]
   def has_key(self,name):
      return self.Items.has_key(name)
   def AddItem(self,acode):
      if self.Items.has_key(acode):
         return self.Items[acode]
      ioid=self.ItemsClass.AddObject()
      self.ItemsClass.ItemCode[ioid]=acode
      self.ClassItem.Items.AddRefs(self.OID,[ioid,self.ItemsClass.CID],asortedreffield=self.ItemsClass.ItemCode)
      aitem=ICORGDVRItem(ioid)
      self._Items[acode]=aitem
      return aitem

class ICORGDVR:
   def __init__(self):
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_QueryStruct']
      self.Dicts={}
      aobj=self.ClassItem.GetFirstObject()
      while aobj.Exists():
         qobj=aobj.Query
         while qobj:
            aitem=ICORGDVRDict(qobj.OID)
            self.Dicts[(aobj.StructName,aitem.Name)]=aitem
            qobj.Next()
         aobj.Next()
   def __getitem__(self,key):
      return self.Dicts[key]

aICORGDVR=ICORGDVR()



