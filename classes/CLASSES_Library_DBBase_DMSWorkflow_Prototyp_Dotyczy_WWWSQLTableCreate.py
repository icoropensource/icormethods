# -*- coding: windows-1250 -*-
# saved: 2021/08/03 13:30:20

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import icordbmain.adoutil as ADOLibInit
import icorlib.projekt.sqlrun as SQLRun
import string
import CLASSES_Library_ICORBase_External_MLog as MLog

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Potwierdzenie',adisplayed='Potwierdź zlecenie generowania danych',atype=mt_Bool,avalue='')
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

def SQLCreateTable(tobj,astatus=None,aplaintext=0):
   if not astatus is None:
      astatus.append('')
   #aICORDBEngine.Classes.CacheClear()
   if astatus:
      if not aplaintext:
         astatus.append('<h1>')
      astatus.append('Start tworzenia tabeli w bazie danych.')
      if not aplaintext:
         astatus.append('</h1>')
   if type(tobj)==type(1):
      tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
      tobj=tclass[tobj]
   pobj=tobj.Projekt
   acnt=5
   while not pobj and acnt:
      time.sleep(1)
      acnt=acnt-1
      pobj=tobj.Projekt
   aTableID=tobj.OID
   aTableName=tobj.Nazwa
   try:
      aadoutil=ADOLibInit.ADOUtil(acominitialize=1,dbaccessobj=pobj.DBAccess)
   except:
      astatus.append('Brak dostepu do bazy danych<br>')
      import traceback
      traceback.print_exc()
      return
   try:
      w=0
      wcreate=0
      try:
         rs=aadoutil.GetRS("select Count(*) Ilosc from %sBZR_%d"%(pobj.BaseNameModifier,aTableID))
         w=1
      except Exception,err:
         try:
            if err[2][5]==-2147217865:
               if astatus:
                  if not aplaintext:
                     astatus.append('<h1>')
                  astatus.append('Takiej tabeli nie ma w bazie danych.')
                  if not aplaintext:
                     astatus.append('</h1>')
               wcreate=1
            else:
               if astatus:
                  if not aplaintext:
                     astatus.append('<h1>')
                  astatus.append('Wystapil blad dostepu do bazy danych')
                  if not aplaintext:
                     astatus.append('</h1>')
         except:
            pass
      if w and rs.State!=aadoutil.adoconst.adStateClosed:
         ailosc=ADOLibInit.GetRSValueAsStr(rs,'Ilosc',astype=1)
         if ailosc>0:
            if astatus:
               if not aplaintext:
                  astatus.append('<h1>')
               astatus.append('Tabela posiada już %d rekordów. Tworzenie tabeli anulowane.'%(ailosc,))
               if not aplaintext:
                  astatus.append('</h1>')
         else:
            wcreate=1
         rs=aadoutil.CloseRS(rs)
      if wcreate:
         saveout=MLog.MemorySysOutWrapper()
         try:
            SQLRun.ExecuteGoSplitSQLCommand('',tobj.SQLSource,aprint=1,acominitialize=0,dbaccessobj=pobj.DBAccess)
            if astatus:
               if not aplaintext:
                  astatus.append('<h1><font color=green>')
               astatus.append('Tabela utworzona poprawnie.')
               if not aplaintext:
                  astatus.append('<font></h1><hr>')
         except:
            if astatus:
               if not aplaintext:
                  astatus.append('<h1><font color=red>')
               astatus.append('Wystąpił błąd podczas tworzenia tabeli.')
               if not aplaintext:
                  astatus.append('<font></h1><hr>')
               import traceback
               traceback.print_exc()
               astatus.append('\n'+saveout.read()+'\n')
         saveout.Restore()
   finally:
      aadoutil.Close()
   if astatus:
      if not aplaintext:
         astatus.append('<h1>')
      astatus.append('Koniec tworzenia tabeli w bazie danych.')
      if not aplaintext:
         astatus.append('</h1>')

def SQLDropTable(tobj,astatus=None,aplaintext=0):
   aICORDBEngine.Classes.CacheClear()
   if type(tobj)==type(1):
      tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Dotyczy']
      tobj=tclass[tobj]
   pobj=tobj.Projekt
   aTableID=tobj.OID
   aTableName=tobj.Nazwa
   try:
      aadoutil=ADOLibInit.ADOUtil(acominitialize=1,dbaccessobj=pobj.DBAccess)
   except:
      astatus.append('Brak dostepu do bazy danych.')
      return
   try:
      try:
         aadoutil.Execute("drop table %sBZR_V_%d"%(pobj.BaseNameModifier,aTableID))
      except Exception,err:
         try:
            if err[2][5]==-2147217865:
               if astatus:
                  if not aplaintext:
                     astatus.append('<h1>')
                  astatus.append('Tabeli wersyjnej nie ma w bazie danych.')
                  if not aplaintext:
                     astatus.append('</h1>')
         except:
            pass
      try:
         aadoutil.Execute("drop table %sBZR_%d"%(pobj.BaseNameModifier,aTableID))
      except Exception,err:
         try:
            if err[2][5]==-2147217865:
               if astatus:
                  if not aplaintext:
                     astatus.append('<h1>')
                  astatus.append('Tabeli roboczej nie ma w bazie danych.')
                  if not aplaintext:
                     astatus.append('</h1>')
         except:
            pass
   finally:
      aadoutil.Close()

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      apotwierdzenie=ICORUtil.str2bool(awwweditor['Potwierdzenie'])
      if apotwierdzenie:
         astatus=[]
         SQLCreateTable(aobj,astatus)
         for s in astatus:
            file.write(s)
      awwweditor.WriteObjectView(aobj,asbutton=apotwierdzenie)

