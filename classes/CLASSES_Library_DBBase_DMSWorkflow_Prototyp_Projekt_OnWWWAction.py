# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
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
   acrmpath=aobj.AppPath+'/'

   d={'text':XMLUtil.GetAsXMLStringNoPL('Obsługa projektu'),
      'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
      'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
   }
   xmlfile.TagOpen('tree',d)

   d={'text':XMLUtil.GetAsXMLStringNoPL('ASP Exceptions'),
      'action':acrmpath+'ASPEXCEPTIONS_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Upload plików'),
      'action':acrmpath+'FILEUPLOADS_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Historia zmian'),
      'action':acrmpath+'HISTORIAZMIAN_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Newsletter - pozycje'),
      'action':acrmpath+'NEWSLETTERITEMS_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Newsletter - elementy'),
      'action':acrmpath+'NEWSLETTERELEMENTS_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Newsletter - użytkownicy'),
      'action':acrmpath+'NEWSLETTERUSERS_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Newsletter - użytkownicy i kategorie'),
      'action':acrmpath+'NEWSLETTERUSERCATEGORIES_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Arkusze'),
      'action':acrmpath+'SHEETINFO_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   d={'text':XMLUtil.GetAsXMLStringNoPL('Wizyty WWW'),
      'action':acrmpath+'WWWMENUVISITS_0_sa.asp'
   }
   xmlfile.TagOpen('tree',d,aclosetag=1)

   xmlfile.TagClose('tree')

   # Security
   if 0:
      sobj=aobj.AccessLevelView
      if sobj:
         d={'text':XMLUtil.GetAsXMLStringNoPL('Użytkownicy'),
            'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
            'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
         }
         xmlfile.TagOpen('tree',d)
      
         pobj=sobj.Profile
         gobj=pobj.UserGroups
   
         while gobj:
            d={'text':XMLUtil.GetAsXMLStringNoPL(gobj.Name),
               'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
               'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
            }
            xmlfile.TagOpen('tree',d)
            uobj=gobj.Users
            while uobj:
               d={'text':XMLUtil.GetAsXMLStringNoPL(uobj.UserName),
                  'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
                  'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
               }
               xmlfile.TagOpen('tree',d)
               xmlfile.TagClose('tree')
   
               uobj.Next()
            xmlfile.TagClose('tree')
            gobj.Next()
   
         xmlfile.TagClose('tree')

   # Security
   if 0:
      sobj=aobj.AccessLevelView
      if sobj:
         pobj=sobj.Profile

         d={'text':XMLUtil.GetAsXMLStringNoPL('Profil bezpieczeństwa'),
            'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
            'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
            'src':'icormain.asp?jobtype=menuclassrecur&CID=%d&OID=%d&XMLData=1'%(pobj.CID,pobj.OID)
         }
         xmlfile.TagOpen('tree',d)
      
         if 0:
            gobj=pobj.UserGroups
            while gobj:
               d={'text':XMLUtil.GetAsXMLStringNoPL(gobj.Name),
                  'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
                  'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
               }
               xmlfile.TagOpen('tree',d)
               uobj=gobj.Users
               while uobj:
                  d={'text':XMLUtil.GetAsXMLStringNoPL(uobj.UserName),
                     'icon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
                     'openIcon':'/icormanager/images/icons/silk/icons/folder_wrench.png',
                  }
                  xmlfile.TagOpen('tree',d)
                  xmlfile.TagClose('tree')
      
                  uobj.Next()
               xmlfile.TagClose('tree')
               gobj.Next()
   
         xmlfile.TagClose('tree')

