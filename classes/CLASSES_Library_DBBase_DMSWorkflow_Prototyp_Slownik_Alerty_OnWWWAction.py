# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import icordbmain.adoutil as ADOLibInit
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWGetFieldIteratorEvent(afield,aoid,aparamobj):
   if aoid<0 and afield.Name in ['XMLData',]:
      return -1
   elif aparamobj and aoid<0:
      aobj=aparamobj.AsObject()
   elif aoid<0:
      return None
   else:
      rclass=afield.ClassItem
      aobj=rclass[aoid]
   if afield.Name=='XMLData':
      if aobj.CID==afield.ClassItem.CID:
         sobj=aparamobj.Struktura
         tobj=sobj.TabeleZrodlowe
         lrefs=FieldRefIterator()
         d={}
         while tobj:
            sgroup=tobj.Grupa
            sname=tobj.Nazwa
            xobj=tobj.XMLData
            while xobj:
               if not d.has_key(xobj.OID):
                  sxgroup=xobj.Grupa
                  sxname=xobj.Name
                  d[xobj.OID]=[sgroup,sname,sxgroup,sxname]
                  lrefs.AddRef(xobj.OID,xobj.CID)
               xobj.Next()
            tobj.Next()
         if lrefs:
            return lrefs.AsObject(),d,d
         return -1
   return None

