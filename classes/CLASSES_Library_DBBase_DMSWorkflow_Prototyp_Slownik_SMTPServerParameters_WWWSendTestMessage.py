# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('SMTPTo',adisplayed='EMail adresata',atype=mt_String,avalue='')
   return awwweditor

def RegisterFieldsStep1(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Field1',adisplayed='Pole S',atype=mt_String,avalue='ABC')
   awwweditor.RegisterField('Field2',adisplayed='Pole I',atype=mt_Integer,avalue='123')
   awwweditor.RegisterField('Field3',adisplayed='Pole DT',atype=mt_DateTime,avalue='2002/02/02')
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

def SendMail(sobj,ato,asubject,atext):
   import appplatform.smtpemailutil as smtpemailutil
   import appplatform.storageutil as storageutil
   ret='OK'
   try:
      if type(atext)==type([]):
         atext=string.join(atext,'\n')
      asmtp=smtpemailutil.SMTPServer(sobj.SMTPServer,sobj.SMTPUser,sobj.SMTPPassword,string.strip(sobj.SMTPFrom))
      if type(ato)==type([]):
         lto=ato
      else:
         lto=[ato,]
      for bto in lto:
         asmtp.Send(string.strip(bto),asubject,atext)
   except:
      ret=ICORUtil.GetLastExceptionInfo()
   return ret

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      ato=awwweditor['SMTPTo']
      if ato:
         file.write('Wysylam email do: %s<br>'%awwweditor['SMTPTo'])
         ret=SendMail(aobj,awwweditor['SMTPTo'],'email testowy','tresc testowa')
         if ret=='OK':
            file.write('Wiadomość wysłana pomyślnie<br>')
         else:
            file.write('Wystąpił błąd podczas wysyłania:<br><pre>')
            file.write(string.join(ret,'\n'))
            file.write('</pre>')
      else:
         file.write('Brak adresu docelowego')

