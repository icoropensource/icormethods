# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
from CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_AppServer import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import appplatform.startutil as startutil
import string
import pythoncom

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   adate=ICORUtil.tdate2fmtstr(ICORUtil.tdate())
   awwweditor.RegisterField('DataPotwierdzenia',adisplayed='Data potwierdzenia odbioru z listy',atype=mt_DateTime,avalue=adate,adefaultcheck=1)
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
      file.write('<h1>Krok 1/4 - ustalenie daty bazowej</h1>')
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

class PlatnikInfo:
   def __init__(self,acnt,aid,adescription,aerror=0,adatapotwierdzenia='',astatusakceptacji=''):
      self.Cnt=acnt
      self.ID=aid
      self.Description=adescription
      self.Error=aerror
      self.DataPotwierdzenia=adatapotwierdzenia
      self.StatusAkceptacji=astatusakceptacji
   def __repr__(self):
      return str(self.Cnt)+' '+self.ID+' '+self.Description
   def __str__(self):
      return str(self.Cnt)+' '+self.ID+' '+self.Description

def OnWWWActionSubmit(aobj,amenu,areport,file):
   pythoncom.CoInitialize()
   try:
      if not areport['refMode']:
         file.write('<h1>Krok 2/4 - wprowadzenie kod�w paskowych</h1>')
         awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
         bwwweditor=ICORWWWEditor(aobj.Class,amenu,file,areport)
         bwwweditor.RegisterField('PotwierdzeniaOdbioru',adisplayed='Identyfikatory, kody paskowe',atype=mt_Memo,avalue='',acols=15,arows=22)
         bwwweditor.RegisterField('DataPotwierdzenia',atype=mt_String,avalue=awwweditor['DataPotwierdzenia'],adefaultcheck=1,ahidden=1)
         bwwweditor.Write(arefMode='step1')
      elif areport['refMode']=='step1':
         awwweditor=ICORWWWEditor(aobj.Class,amenu,file,areport)
         awwweditor.RegisterField('DataPotwierdzenia',atype=mt_DateTime,adefaultcheck=1)
         awwweditor.RegisterField('PotwierdzeniaOdbioru',atype=mt_Memo)
         file.write('<h1>Krok 3/4 - ustalenie dat</h1>')
         bwwweditor=ICORWWWEditor(aobj.Class,amenu,file,areport)
         adate=awwweditor['DataPotwierdzenia']
         apreprocessor=MassPaymentsServer(aobj.Nazwa)
         lp=string.split(awwweditor['PotwierdzeniaOdbioru'],'\n')
         apreprocessor.OpenConnection()
         dv={'acnt':1}
         dp={}
         lp2=[]
         aerror=0
         try:
            acnt=0
            did={}
            for aid in lp:
               aid=string.strip(aid)
               if not aid or did.has_key(aid):
                  continue
               did[aid]=1
               try:
                  w=apreprocessor.CheckTransID(aid)
               except:
                  w=0
               if w:
                  apname,adatapotwierdzenia,astatusakceptacji=apreprocessor.PobierzInformacjeOPotwierdzeniuOdbioru(aid)
                  if apname:
                     aplatnik=PlatnikInfo(acnt,aid,apname,adatapotwierdzenia=adatapotwierdzenia,astatusakceptacji=astatusakceptacji)
                     svalue='1'
                     if astatusakceptacji=='A2':
                        svalue=''
                     bwwweditor.RegisterField('CzyAkceptowac%d'%acnt,adisplayed=None,atype=mt_Bool,avalue=svalue,ano_td2=1,ano_tr2=1,atag=aid)
                     bwwweditor.RegisterField('PotwierdzenieOdbioru%d'%acnt,adisplayed=None,atype=mt_String,avalue=aid,ahidden=1,ano_td1=1,ano_tr1=1,ano_td2=1,ano_tr2=1)
                     bwwweditor.RegisterField('DataPotwierdzenia%d'%acnt,adisplayed=None,atype=mt_DateTime,avalue=adate,adefaultcheck=1,ano_td1=1,ano_tr1=1)
                     acnt=acnt+1
                  else:
                     aplatnik=PlatnikInfo(acnt,aid,'pozycja nie jest zarejestrowana w SPM',aerror=1)
                     aerror=1
               else:
                  aplatnik=PlatnikInfo(acnt,aid,'b��dny kod paskowy',aerror=1)
                  aerror=1
               dp[aid]=aplatnik
               lp2.append(aplatnik)
            bwwweditor.RegisterField('PotwierdzeniaCnt',adisplayed=None,atype=mt_String,avalue=str(acnt),ahidden=1)
         finally:
            apreprocessor.CloseConnection()
         def FOnFieldRowBeginAfter(afield,dp=dp,lp=lp2,dv=dv):
            if afield.Tag:
               aplatnik=dp[afield.Tag]
               s=string.replace(aplatnik.Description,'\n','<br>')
               if aplatnik.StatusAkceptacji=='A2':
                  s='<font color="red"><b>Potwierdzono dnia %s</b></font><br>'%aplatnik.DataPotwierdzenia+s
               ret='<td class=objectsviewdata><b>'+str(dv['acnt'])+'.</b>&nbsp;<font color="green"><b>'+aplatnik.ID+'</b></font></td><td class=objectsviewdata>'+s+'</td>'
               dv['acnt']=1+dv['acnt']
               return ret
         def FOnFieldRowEndAfter(afield,dp=dp,lp=lp2):
            pass
         bwwweditor.OnFieldRowBeginAfter=FOnFieldRowBeginAfter
         bwwweditor.OnFieldRowEndAfter=FOnFieldRowEndAfter
         if aerror:
            file.write('<h3><font color="red">Niepoprawne identyfikatory:</font></h3>')
            for aplatnik in lp2:
               if aplatnik.Error:
                  file.write('<font color="green"><b>%s</b></font>&nbsp;&nbsp;-&nbsp;%s<br>'%(aplatnik.ID,aplatnik.Description))
         file.write('<h3><font color="green">Poprawne identyfikatory:</font></h3>')
         bwwweditor.Write(arefMode='step2')
      elif areport['refMode']=='step2':
         awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
         awwweditor.RegisterField('PotwierdzeniaCnt',atype=mt_String)
         acnt=int(awwweditor['PotwierdzeniaCnt'])
         file.write('<h1>Krok 4/4 - rejestracja potwierdze�</h1>')
         lret=[]
         for i in range(acnt):
            awwweditor.RegisterField('CzyAkceptowac%d'%i,adisplayed=None,atype=mt_Bool)
            awwweditor.RegisterField('PotwierdzenieOdbioru%d'%i,adisplayed=None,atype=mt_String)
            awwweditor.RegisterField('DataPotwierdzenia%d'%i,adisplayed=None,atype=mt_DateTime)
            aczyakceptowac=ICORUtil.str2bool(awwweditor['CzyAkceptowac%d'%i])
            if aczyakceptowac:
               adate=ICORUtil.getStrAsDate(awwweditor['DataPotwierdzenia%d'%i])
               if adate==ICORUtil.ZERO_DATE_Z:
                  file.write('<h3><font color="red">wprowadzono niepoprawn� dat� (%s) dla identyfikatora: %s</font></h3>\n'%(awwweditor['DataPotwierdzenia%d'%i],awwweditor['PotwierdzenieOdbioru%d'%i]))
               else:
                  sdate=ICORUtil.tdate2fmtstr(adate,delimiter='-',longfmt=1)
                  lret.append([adate,awwweditor['PotwierdzenieOdbioru%d'%i]])
                  file.write('<h3><font color="green">rejestracja wpisu dla identyfikatora: %s</font></h3>\n'%awwweditor['PotwierdzenieOdbioru%d'%i])
            else:
               file.write('<h3><font color="black">pomini�to wpis dla identyfikatora: %s</font></h3>\n'%awwweditor['PotwierdzenieOdbioru%d'%i])
         if lret:
            apreprocessor=MassPaymentsServer(aobj.Nazwa)
            apreprocessor.WprowadzPotwierdzeniaOdbioru(lret,file)
         awwweditor.WriteObjectView(aobj,asbutton=1)
   finally:
      pythoncom.CoUninitialize()



