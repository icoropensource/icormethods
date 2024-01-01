# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_DBBase_Util_Excel_HTMLXLSTable as HTMLXLSTable

class ICORXMLImporter:
   def __init__(self,axmldata,axlsdata):
      self._MaxCol,self._MaxRow=None,None
      self._XLSTable=None
      self._Cells={}
      self._xmldata=axmldata
      self._xlsdata=axlsdata
   def __getattr__(self,name):
      if name=='XLSTable':
         if self._XLSTable is None:
            amhtmltableparser=HTMLXLSTable.MHTMLXLSTableParser()
            amhtmltableparser.Process(self._xlsdata)
            self._XLSTable=amhtmltableparser.Table
         return self._XLSTable
      if name=='MaxCol':
         if self._MaxCol is None:
            self._MaxCol=self.XLSTable.MaxCol
         return self._MaxCol
      if name=='MaxRow':
         if self._MaxRow is None:
            self._MaxRow=self.XLSTable.MaxRow
         return self._MaxRow
   def __getitem__(self,akey):
      acol,arow=akey
      if self._Cells.has_key(akey):
         return self._Cells[akey].ValueAsString
      acell=self.XLSTable[acol,arow]
      ret=acell.ValueAsString
      self._Cells[akey]=ret
      return ret

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Dane',atype=mt_Memo,afieldeditor='Worksheet')
   return awwweditor

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 0</h1>')
      file.write('<h2>Field : %s</h2>'%awwweditor['Dane'])
      aimporter=ICORXMLImporter(aobj.XMLSource,awwweditor['Dane'])



