# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import string

def CleanCSS(atext):
   apos=string.find(atext,'TD.TabelaWartoscPolaMain')
   if apos<0:
      return None
   apos=string.find(atext,'TD.TabelaWartoscPolaMain0')
   if apos>=0:
      return ''
   bpos=string.find(atext,'}',apos)
   if bpos<0:
      return ''
   s1=atext[apos:bpos+1]
   s2=string.replace(s1,'TD.TabelaWartoscPolaMain','TD.TabelaWartoscPolaMain0')
   atext=atext+'\n'+s2+'\n'
   s2=string.replace(s1,'TD.TabelaWartoscPolaMain','TD.TabelaWartoscPolaMain1')
   atext=atext+'\n'+s2+'\n'
   return atext

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   aobj=aclass.GetFirstObject()
   while aobj:
      aobj.CSSProcesor=[35000,2067]
      aobj.Next()
   
   return
   aobj=aclass.GetFirstObject()
   while aobj:
      atext=CleanCSS(aobj.CSSSystem)
      if atext is None:
         print 'bad CSS:',aobj.OID,aobj.CSSName
      elif not atext:
         pass
      else:
         aobj.CSSSystem=atext
      aobj.Next()
   return

