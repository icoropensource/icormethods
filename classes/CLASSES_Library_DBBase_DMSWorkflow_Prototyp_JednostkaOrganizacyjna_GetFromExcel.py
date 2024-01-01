# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_Win32_OLE_ICORExcel import *
import string

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   excel=ICORExcel(0)
   arow=1
   while 1:
      ajednostka=excel[1,arow]
      adokument=excel[2,arow]
      aczynnosc=excel[4,arow]
      if not ajednostka and not adokument and not aczynnosc:
         break
      if ajednostka:
         joid=aclass.Nazwa.Identifiers(ajednostka)
         jobj=aclass[joid]
         print 'Jednostka:',jobj.Nazwa
         arow=arow+1
         continue    
      if adokument:
         if adokument=='Dokumenty tworzone:':
            procedura='T'
            arow=arow+1
            continue
         elif adokument=='Dokumenty otrzymywane:':
            procedura=''
            arow=arow+1
            continue
         else:
            sl=string.split(adokument,' ')
            asymbol=sl[0]
            pobj=jobj.Procedury
            while pobj:
               if procedura=='T' and pobj.Symbol=='T':
                  if pobj.Dokument.Symbol==asymbol:
                     break
               elif pobj.Dokument.Symbol==asymbol:
                  break
               pobj.Next()
            print '  ',pobj.Symbol,pobj.Dokument.Symbol
      if aczynnosc:
         aczynnosc=aczynnosc[3:]
         print '    ',aczynnosc
         coid=pobj.Class.Czynnosci.ClassOfType.AddObject()
         pobj.Class.Czynnosci.ClassOfType.Nazwa[coid]=aczynnosc
         pobj.Czynnosci=pobj.Class.Czynnosci[pobj.OID]+str(coid)+':'+str(pobj.Class.Czynnosci.ClassOfType.CID)+':'
      arow=arow+1



