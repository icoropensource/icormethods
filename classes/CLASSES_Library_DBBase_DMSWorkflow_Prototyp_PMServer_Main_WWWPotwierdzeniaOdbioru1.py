# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import appplatform.startutil as startutil
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   adate=ICORUtil.tdate2fmtstr(ICORUtil.tdate())
   awwweditor.RegisterField('DataPotwierdzenia',adisplayed='Data potwierdzenia odbioru z listy',atype=mt_DateTime,avalue=adate,adefaultcheck=1)
   awwweditor.RegisterField('PotwierdzeniaOdbioru',adisplayed='Identyfikatory, kody paskowe',atype=mt_Memo,avalue='',acols=15,arows=22)
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
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
      bwwweditor=ICORWWWEditor(aobj.Class,amenu,file,areport)
      adate=ICORUtil.getStrAsDate(awwweditor['DataPotwierdzenia'])
      if adate==ICORUtil.ZERO_DATE_Z:
         file.write('<h3><font color="red">wprowadzono niepoprawn� dat�!</font></h3>\n')
      else:
         sdate=ICORUtil.tdate2fmtstr(adate)
         file.write('<h3><font color="green">Potwierdzenia odbioru z dnia: %s</font></h3>\n'%sdate)
         apreprocessor=MassPaymentsServer(aobj.Nazwa)
         lp=string.split(awwweditor['PotwierdzeniaOdbioru'],'\n')
         lret=[]
         for aid in lp:
            aid=string.strip(aid)
            if not aid:
               continue
            w=apreprocessor.CheckTransID(aid)
            if w:
               lret.append([adate,aid])
            else:
               file.write('<h3>zly kod paskowy: [%s]</h3>\n'%aid)
         if lret:
            apreprocessor.WprowadzPotwierdzeniaOdbioru(lret,file)
      bwwweditor.WriteObjectView(aobj,asbutton=1)



