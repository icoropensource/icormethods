# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_Win32_OLE_ICORExcel import *
from CLASSES_Library_DBBase_GDVR_Main_ICORGDVRMain import aICORGDVR
import string

def UpdateFromExcel(aclass,astructname,adictname):
   agvrdict=aICORGDVR[astructname,adictname]
   print 'Updating:',agvrdict
   excel=ICORExcel(0)
   SKOD,SNAZWA,SOPIS,SZRODLO,SWIEKSZE,SMNIEJSZE,SMASKA="Kod","Nazwa","Opis","Źródło","większe lub równe od konta od Konta z FK","mniejsze od Konta z FK","maska konta"
   arow,acol=1,1
   stdcols={SKOD:0,SNAZWA:0,SOPIS:0,SZRODLO:0,SWIEKSZE:0,SMNIEJSZE:0,SMASKA:0}
   coldict,vcoldict={},{}
   maxcol=1
   s=excel[maxcol,arow]
   while s:
      if stdcols.has_key(s):
         coldict[maxcol]=s
         stdcols[s]=maxcol
      else:
         s1=excel[maxcol,arow+1]
         if not s1:
            print 'Kolumna wartości "%s" nie posiada nazwy'%s
            return
         vcoldict[maxcol]=s,s1
      maxcol=maxcol+1
      s=excel[maxcol,arow]
   maxcol,arow=maxcol-1,arow+2

   waccounts=stdcols[SWIEKSZE] and stdcols[SMNIEJSZE] and stdcols[SMASKA]

   s=excel[acol,arow]
   cnt=1
   while s:
      InfoStatus('Wiersz: '+str(cnt))
      if s!='-':
         sl=['',]
         for i in range(maxcol):
            sl.append(excel[i+1,arow])
         aitem=agvrdict.AddItem(sl[stdcols[SKOD]])
         aitem.SetName(sl[stdcols[SNAZWA]])
         aitem.SetSource(sl[stdcols[SZRODLO]])
         aitem.SetDescription(sl[stdcols[SOPIS]])
         if waccounts:
            s1,s2,s3=string.strip(sl[stdcols[SWIEKSZE]]),string.strip(sl[stdcols[SMNIEJSZE]]),string.strip(sl[stdcols[SMASKA]])
            if s1 or s2 or s3:
               aitem.SetAccounts(s1,s2,s3)
         for vcol,vvalue in vcoldict.items():
            fdesc,fname=vvalue
            aitem.SetFieldValue(fname,fdesc,sl[vcol])
      arow=arow+1
      s=excel[acol,arow]
      cnt=cnt+1
   InfoStatus('')

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      print 'Slownik nie został wybrany'
      return
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass[OID]
   UpdateFromExcel(aclass,aobj.QueryStruct.StructName,aobj.DictName)
   print 'Koniec'
   return



