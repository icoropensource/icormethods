# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
   pobj=aobj.Projekt
   acrmpath=pobj.AppPath+'/'
   asufix=aobj['InfoTablesSufix',mt_Integer]

   d={'text':'Obsługa struktury',
      'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
      'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
   }
   xmlfile.TagOpen('tree',d)

   d={'text':'Rozdziały',
      'action':acrmpath+'CHAPTERS_%d_sa.asp'%asufix
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':'Rozdziały w menu',
      'action':acrmpath+'MENUCHAPTERS_%d_sa.asp'%asufix
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':'Rejestr zmian',
      'action':acrmpath+'REJESTRZMIAN_%d_sa.asp'%asufix
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':'Wizyty w rozdziałach',
      'action':acrmpath+'WWWMENUHITS_%d_sa.asp'%asufix
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   xmlfile.TagClose('tree')

def OnWWWGetMenuFieldRecurIteratorEvent(afield,aoid):
   if afield.Name=='Rozdzialy':
      arefs=afield.GetRefList(aoid)
      brefs=arefs.AsRefs()
      while arefs:
         if arefs.Class.GrupaRozdzialow[arefs.OID]:
            brefs.DelRef(arefs.OID)
         arefs.Next()
      if brefs:
         return brefs.AsObject()
   return None

