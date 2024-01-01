# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Naglowek',aoid=aoid)
   awwweditor.RegisterField('NaglowekMenu',aoid=aoid)
   awwweditor.RegisterField('TabelaZrodlowa',aoid=aoid,adisabledefaultvalue=1)
#   awwweditor.RegisterField('ZrodloDanychWzorca',aoid=aoid)
#   awwweditor.RegisterField('PageTemplate',aoid=aoid)
#   awwweditor.RegisterField('GrupaRozdzialow',aoid=aoid)
   awwweditor.RegisterField('SGIsTableView',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('SGShowAsTable',aoid=aoid,adisabledefaultvalue=1)
#   awwweditor.RegisterField('Galeria',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('SGHref',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('SGHrefParams',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('SGHrefApp',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('SGTarget',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('RodzajZaglebienia',aoid=aoid)
   awwweditor.RegisterField('SGIsMenuDisabled',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('RSSDisabled',aoid=aoid)
   awwweditor.RegisterField('RSSOpis',aoid=aoid)
   awwweditor.RegisterField('IsAutoGenerate',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('ScheduledGenerate',aoid=aoid)
   awwweditor.RegisterField('IsGenerateDisabled',aoid=aoid,adisabledefaultvalue=1)
   awwweditor.RegisterField('Priorytet',aoid=aoid)
   awwweditor.RegisterField('ChapterParams',aoid=aoid)
#   awwweditor.RegisterField('SGInsertBefore',adisplayed='Wstaw przed wybraną pozycję',atype=mt_Boolean)
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

def UpdateSGTabID(dobj):
   atabid=10
   while dobj:
      dobj.SGTabID=atabid
      atabid=atabid+10
      dobj.Next()

def OnWWWActionSubmit(aobj,amenu,areport,file):
   amenu.SetAction('ObjectAdd')
   try:
      bobj=aobj.AsObject()
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
#      ainsertbeforeoid=ICORUtil.str2bool(awwweditor['SGInsertBefore'])
#      awwweditor.WWWActionSubmit(anoobjectview=1,ainsertbeforeoid=ainsertbeforeoid,abaseoid=aobj.OID)
      awwweditor.WWWActionSubmit(anoobjectview=1)
      UpdateSGTabID(bobj.PodRozdzialy)
   finally:
      amenu.RestoreAction()
   file.write('<h3><font color="green">Dane zostały zmienione. Pamiętaj o odświeżeniu odpowiedniej pozycji w menu</font</h3>')



