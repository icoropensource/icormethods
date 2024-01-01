# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_ICORBase_Interface_ICORIterators import FieldRefIterator
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
import string

def OnBeforeWWWAction(aobj,amenu,file):
   return 1

def OnWWWAction(aclass,amenu,file):
   awwweditor=RegisterFields(aclass,amenu,file)
   awwweditor.WWWAction()

def OnWWWGetFieldIteratorEvent(afield,aoid,aparamobj):
   if aoid<0 and afield.Name in ['PolaczeniaDoTabel',]:
      return -1
   if aparamobj and aoid<0:
      aobj=aparamobj.AsObject()
   elif aoid<0:
      return None
   else:
      rclass=afield.ClassItem
      aobj=rclass[aoid]
   if afield.Name=='Dotyczy':
      if aobj.CID==afield.ClassItem.CID:
         return aobj.Projekt.BazyZrodlowe
      pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
      if aobj.CID==pclass.CID:
         return aobj.BazyZrodlowe
   if afield.Name=='PolaczeniaDoTabel':
      return aobj.PolaczeniaDoTabel
   return None

def OnWWWGetFieldAutoCompleteValues(aobj,afield):
   if afield.Name:
      if aobj.OID<0:
         pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
         arefs=FieldRefIterator()
         auid=GetUID()
         pobj=pclass.GetFirstObject()
         while pobj:
            if ICORSecurity.CheckRecursiveAccessLevelForUser(pobj,'AccessLevelView',auid):
               tobj=pobj.BazyZrodlowe
               while tobj:
                  arefs.AddRef(tobj.OID,tobj.CID)
                  tobj.Next()
            pobj.Next()
         return arefs.AsObject()
      else:
         ret=aobj.Projekt.BazyZrodlowe
      return ret
   return 1

def OnWWWActionSubmit(aclass,amenu,areport,file):
   awwweditor=RegisterFields(aclass,amenu,file,-1,areport)
   awwweditor.WWWActionSubmit()

def OnWWWMenuObjRecur(xmlfile,aobj,UID):
#   print 'T:',aobj.Class.CID,aobj.Class.NameOfClass,'o:',aobj.OID,'u:',UID
   pobj=aobj.Projekt
   acrmpath=pobj.AppPath+'/'

   d={'text':XMLUtil.GetAsXMLStringNoPL('Obsługa tabeli'),
      'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
      'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
   }
   xmlfile.TagOpen('tree',d)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Nowa pozycja'),
      'action':acrmpath+'BZR_%d_au.asp'%(aobj.OID,)
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Wyszukiwarka'),
      'action':acrmpath+'BZR_%d_sv.asp'%(aobj.OID,)
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   xmlfile.TagClose('tree')



