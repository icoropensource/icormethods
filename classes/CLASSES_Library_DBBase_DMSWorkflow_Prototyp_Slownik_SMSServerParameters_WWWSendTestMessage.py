# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
try:
   import simplejson as json
except:
   import json

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Telefon',adisplayed='Nr telefonu',atype=mt_String,avalue='')
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

def SendSMS(sobj,ato,atext):
   ret='OK'
   try:
      if sobj.Dostawca.Nazwa=='serwersms.pl':
         import appplatform.serwersms as serwersms
         api=serwersms.SerwerSMS(sobj.SMSUser,sobj.SMSPassword)
         params = {
            'details': 'true',
         }
         response=api.message.send_sms(ato,atext,sobj.SMSFrom,params)
         result=json.loads(response)
         if result.has_key('error'):
            ret=response
         if result.has_key('success'):
            ret='OK'
      else:
         ret='BAD'
   except:
      ret=ICORUtil.GetLastExceptionInfo()
   return ret

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      ato=awwweditor['Telefon']
      if ato:
         file.write('Wysylam SMS do: %s<br>'%ato)
         ret=SendSMS(aobj,ato,'tresc testowa')
         if ret=='OK':
            file.write('Wiadomość wysłana pomyślnie<br>')
         elif type(ret)==type([]):
            file.write('Wystąpił błąd podczas wysyłania:<br><pre>')
            file.write(string.join(ret,'\n'))
            file.write('</pre>')
         else:
            file.write('Błąd serwera:<br><pre>')
            file.write(ret)
            file.write('</pre>')
      else:
         file.write('Brak adresu docelowego')

