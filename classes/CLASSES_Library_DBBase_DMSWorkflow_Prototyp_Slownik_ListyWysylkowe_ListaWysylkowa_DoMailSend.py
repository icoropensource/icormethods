# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import icordbmain.adoutil as ADOLibInit
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_SMTPUtil as SMTPUtil
import CLASSES_Library_NetBase_WWW_HTML_Util_ConversionsPL as ConversionsPL
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_ListyWysylkowe_ListaWysylkowa_WWWGeneratePage as WWWGeneratePage
import string
import random
import time
import sha
import os
import re
import win32api

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.Header import Header

LOG_FILE=FilePathAsSystemPath('%ICOR%/log/newsletter.txt')
SEND_FIRST_EMAIL=0

def Log(s='',amode='a+',fname=LOG_FILE,aconsole=0):
   if aconsole:
      print string.replace(s,'\n','') 
   try:
      f=open(fname,amode)
      if s[-1:]!='\n':
         s=s+'\n'
      f.write('['+str(os.getpid())+'] '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())+': '+s)
      f.close()
   except:
      pass

def LogException(amode='a+',fname=LOG_FILE,aconsole=0):
   try:
      f=open(fname,amode)
      import traceback
      if aconsole:
         traceback.print_exc()
      f.write('['+str(os.getpid())+'] '+ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())+': Exception!\n')
      traceback.print_exc(file=f)
      f.close()
   except:
      pass

def Main(aproject):
   pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   lclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Slownik_ListyWysylkowe_ListaWysylkowa']
   poid=pclass.Nazwa.Identifiers(aproject)
   if poid<0:
      Log('Nieznany projekt: '+aproject)
      return
   pobj=pclass[poid]
   if pobj['SGIsDisabled']:
      Log('Projekt wylaczony: '+aproject)
      return
   aBaseNameModifier=pobj.BaseNameModifier
   try:
      aadoutil=ADOLibInit.ADOUtil(acominitialize=1,dbaccessobj=pobj.DBAccess)
   except:
      Log('Brak dostepu do db w projekcie: '+aproject)
      return
   try:
      lobj=pobj.ListyWysylkowe
      Log('Potwierdzenia:')
      while lobj:
         sobj=lobj.SMTPServerParameters
         rs1=aadoutil.GetRS("select _OID,NewsletterOID,EMail,Status from %sNEWSLETTERUSERS_0 where (Status='N' or Status='M') and NewsletterOID=%d"%(aBaseNameModifier,lobj.OID))
         while not rs1.EOF and not rs1.BOF:
            ato=ADOLibInit.GetRSValueAsStr(rs1,'EMail')
            aoid=ADOLibInit.GetRSValueAsStr(rs1,'_OID')
            Log('  To: '+ato)
            Log('  Subject: Potwierdzenie listy wysyłkowej: '+lobj.NazwaWidoczna)
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = Header(ConversionsPL.Win2ISO('Potwierdzenie listy wysyłkowej z serwisu ICOR: '+lobj.NazwaWidoczna), 'iso-8859-2')
            msgRoot['From'] = string.strip(sobj.SMTPFrom)
#            msgRoot['To'] = Header(ConversionsPL.Win2ISO(ato), 'iso-8859-2')
            msgRoot['To'] = ConversionsPL.Win2ISO(ato)
            msgRoot.preamble = 'This is a multi-part message in MIME format.'
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)                                           
            msgText = MIMEText(ConversionsPL.Win2ISO('Ten komunikat należy odczytać w postaci HTML.'),'plain','iso-8859-2')
            msgAlternative.attach(msgText)

            ahrefpotwierdzenie='%s?o=%s&m=p'%(sobj.AdresStronyPotwierdzen,aoid)
            ahrefzakonczenie='%s?o=%s&m=u'%(sobj.AdresStronyPotwierdzen,aoid)
            arepldict={'aOID':aoid,'aTo':ato,'aHRefAccept':ahrefpotwierdzenie,'aHRefDecline':ahrefzakonczenie,'aNewsletter':lobj,'aSMTPServerParameters':sobj,'rs':rs1,'re':re,'string':string,'ICORUtil':ICORUtil,'ADOLibInit':ADOLibInit,'aadoutil':aadoutil}
            btext=ICORUtil.GetTextAsHTMLText(lobj.SzablonPotwierdzenia,repldict=arepldict,aengine=aICORDBEngine,aashtmlstring=0,ascriptname='NewsletterAccept '+str(lobj.OID))

            msgText = MIMEText(ConversionsPL.Win2ISO(btext), 'html', 'iso-8859-2')
            msgAlternative.attach(msgText)
            w=0
            Log('  Wysyłanie potwierdzenia')
            astatus='W'
            try:
               asmtp=SMTPUtil.AuthSMTP(sobj.SMTPServer)
               if sobj.SMTPUser!='' and sobj.SMTPPassword!='':
                  asmtp.login(sobj.SMTPUser,sobj.SMTPPassword)
               asmtp.sendmail(string.strip(sobj.SMTPFrom),string.strip(ato),msgRoot.as_string())
               asmtp.quit()
               w=1
            except:
               astatus='E'
               LogException()
            if w:
               rs1.Fields.Item('Status').Value=astatus
               aadoutil.UpdateRS(rs1)
            rs1.MoveNext()
         rs1=aadoutil.CloseRS(rs1)

         lobj.Next()

      Log('Listy:')
      rs=aadoutil.GetRS("select NewsletterOID,OIDRef,TableID,ChapterID,Status,DataWyslania,WyslanyPrzez from %sNEWSLETTERITEMS_0 where Status='G'"%(aBaseNameModifier,))
      if rs.State!=aadoutil.adoconst.adStateClosed:
         while not rs.EOF and not rs.BOF:
            atableid=ADOLibInit.GetRSValueAsStr(rs,'TableID')
            aoidref=ADOLibInit.GetRSValueAsStr(rs,'OIDRef')
            asql="select * from %sBZR_%s where _OID='%s' and GETDATE()>=RozpocznijWysylanieOd"%(aBaseNameModifier,atableid,aoidref)
            w=0
            try:
               rsdata=aadoutil.GetRS(asql)
               w=1
            except:
               print '$$ERROR in DoMailSend: '+asql
            if not w:
               asql="select * from %sBZR_%s where _OID='%s'"%(aBaseNameModifier,atableid,aoidref)
               rsdata=aadoutil.GetRS(asql)
            if rsdata.EOF:
               rsdata=aadoutil.CloseRS(rsdata)
               rs.MoveNext()
               continue
            anewsletteroid=ADOLibInit.GetRSValueAsStr(rs,'NewsletterOID',astype=1)
            lobj=lclass[anewsletteroid]
            sobj=lobj.SMTPServerParameters
            Log('Newsletter Item: '+str(anewsletteroid)+' Table: '+atableid+' OIDRef: '+aoidref)
            rs1=aadoutil.GetRS("select _OID,NewsletterOID,EMail,Status from %sNEWSLETTERUSERS_0 where Status in ('Z','M') and NewsletterOID=%d"%(aBaseNameModifier,anewsletteroid))
            Log('Emails:')
            while not rs1.EOF and not rs1.BOF:
               ato=ADOLibInit.GetRSValueAsStr(rs1,'EMail')
               aemailoid=ADOLibInit.GetRSValueAsStr(rs1,'_OID')
               this={
                  'NewsletterOID':str(anewsletteroid),
                  'OIDRef':aoidref,
                  'TableID':atableid,
                  'MailSubject':lobj.EMailTemat,
                  'ListaKrotkiOpis':lobj.KrotkiOpis,
                  'ListaDlugiOpis':lobj.DlugiOpis,
                  'EMailTo':ato,
                  'EMailOID':aemailoid,
                  'AdresStronyPotwierdzen':sobj.AdresStronyPotwierdzen,
                  'ShowAllCategories':0,
                  'AllowSend':1,
               }
               Log('  To: '+ato)
               Log('  Subject: '+this['MailSubject'])
#               arepldict={'this':this,'rs':rsdata,'re':re,'string':string,'ICORUtil':ICORUtil,'ADOLibInit':ADOLibInit}
               try:
#                  atext=ICORUtil.GetTextAsHTMLText(lobj.SzablonListu,repldict=arepldict,aengine=aICORDBEngine,aashtmlstring=0)
                  atext=WWWGeneratePage.GetNewsletterText(aadoutil,anewsletteroid,aoidref,this=this)
                  if not this['AllowSend']:
                     Log('    ALLOW_SEND: 0')
                     atext=''
               except:
                  LogException()
                  atext=''
               if atext:
                  # Create the root message and fill in the from, to, and subject headers
                  msgRoot = MIMEMultipart('related')
                  msgRoot['Subject'] = Header(ConversionsPL.Win2ISO(this['MailSubject']), 'iso-8859-2')
                  msgRoot['From'] = string.strip(sobj.SMTPFrom)
#                  msgRoot['To'] = Header(ConversionsPL.Win2ISO(ato), 'iso-8859-2')
                  msgRoot['To'] = ConversionsPL.Win2ISO(ato)
                  msgRoot.preamble = 'This is a multi-part message in MIME format.'
                  
                  # Encapsulate the plain and HTML versions of the message body in an
                  # 'alternative' part, so message agents can decide which they want to display.
                  msgAlternative = MIMEMultipart('alternative')
                  msgRoot.attach(msgAlternative)
                  
                  msgText = MIMEText(ConversionsPL.Win2ISO('Ten komunikat należy odczytać w postaci HTML.'),'plain','iso-8859-2')
                  msgAlternative.attach(msgText)
                  
                  # We reference the image in the IMG SRC attribute by the ID we give it below
   #               msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
                  msgText = MIMEText(ConversionsPL.Win2ISO(atext), 'html', 'iso-8859-2')
                  msgAlternative.attach(msgText)
                  
                  # This example assumes the image is in the current directory
   #               fp = open('test.jpg', 'rb')
   #               msgImage = MIMEImage(fp.read())
   #               fp.close()
                  
                  # Define the image's ID as referenced above
   #               msgImage.add_header('Content-ID', '<image1>')
   #               msgRoot.attach(msgImage)
                  
                  try:                        
                     asmtp=SMTPUtil.AuthSMTP(sobj.SMTPServer)
                     if sobj.SMTPUser!='' and sobj.SMTPPassword!='':
                        asmtp.login(sobj.SMTPUser,sobj.SMTPPassword)
                     asmtp.sendmail(string.strip(sobj.SMTPFrom),string.strip(ato),msgRoot.as_string())
                     asmtp.quit()
                  except:                                                                                   
                     LogException()
               rs1.MoveNext()
            rs1=aadoutil.CloseRS(rs1)     
            rs.Fields.Item('Status').Value='S'
            aadoutil.UpdateRS(rs)
            rsdata=aadoutil.CloseRS(rsdata)
            rs.MoveNext()
#         aadoutil.UpdateRS(rs)
         rs=aadoutil.CloseRS(rs)


      Log('Ostatni newsletter po potwierdzeniu:')
      rs1=aadoutil.GetRS("select _OID,NewsletterOID,EMail,Status from %sNEWSLETTERUSERS_0 where Status='Z1'"%(aBaseNameModifier,))
      Log('Emails:')
      while not rs1.EOF and not rs1.BOF:
         if SEND_FIRST_EMAIL:
            ato=ADOLibInit.GetRSValueAsStr(rs1,'EMail')
            aemailoid=ADOLibInit.GetRSValueAsStr(rs1,'_OID')
            anewsletteroid=ADOLibInit.GetRSValueAsStr(rs1,'NewsletterOID',astype=1)
            rs=aadoutil.GetRS("select top 1 * from %sNEWSLETTERITEMS_0 where Status='S' and NewsletterOID=%d order by DataWyslania desc"%(aBaseNameModifier,anewsletteroid))
            if rs.State!=aadoutil.adoconst.adStateClosed:
               atableid=ADOLibInit.GetRSValueAsStr(rs,'TableID')
               aoidref=ADOLibInit.GetRSValueAsStr(rs,'OIDRef')
               w=0
               asql="select * from %sBZR_%s where _OID='%s' and GETDATE()>=RozpocznijWysylanieOd"%(aBaseNameModifier,atableid,aoidref)
               try:
                  rsdata=aadoutil.GetRS(asql)
                  w=1
               except:
                  print '$$ ERROR IN SQL 2 Newsletter: '+asql
               if not w:
                  asql="select * from %sBZR_%s where _OID='%s'"%(aBaseNameModifier,atableid,aoidref)
                  rsdata=aadoutil.GetRS(asql)
               if rsdata.EOF:
                  rsdata=aadoutil.CloseRS(rsdata)
                  rs1.MoveNext()
                  continue
               lobj=lclass[anewsletteroid]
               sobj=lobj.SMTPServerParameters
               Log('Newsletter Item: '+str(anewsletteroid)+' Table: '+atableid+' OIDRef: '+aoidref)
               if 1:
                  this={
                     'NewsletterOID':str(anewsletteroid),
                     'OIDRef':aoidref,
                     'TableID':atableid,
                     'MailSubject':lobj.EMailTemat,
                     'ListaKrotkiOpis':lobj.KrotkiOpis,
                     'ListaDlugiOpis':lobj.DlugiOpis,
                     'EMailTo':ato,
                     'EMailOID':aemailoid,
                     'AdresStronyPotwierdzen':sobj.AdresStronyPotwierdzen,
                     'ShowAllCategories':0,
                     'AllowSend':1,
                  }
                  Log('  To: '+ato)
                  Log('  Subject: '+this['MailSubject'])
   #               arepldict={'this':this,'rs':rsdata,'re':re,'string':string,'ICORUtil':ICORUtil,'ADOLibInit':ADOLibInit}
                  try:
   #                  atext=ICORUtil.GetTextAsHTMLText(lobj.SzablonListu,repldict=arepldict,aengine=aICORDBEngine,aashtmlstring=0)
                     atext=WWWGeneratePage.GetNewsletterText(aadoutil,anewsletteroid,aoidref,this=this)
                     if not this['AllowSend']:
                        Log('    ALLOW_SEND: 0')
                        atext=''
                  except:
                     LogException()
                     atext=''
                  if atext:
                     # Create the root message and fill in the from, to, and subject headers
                     msgRoot = MIMEMultipart('related')
                     msgRoot['Subject'] = Header(ConversionsPL.Win2ISO(this['MailSubject']), 'iso-8859-2')
                     msgRoot['From'] = string.strip(sobj.SMTPFrom)
   #                  msgRoot['To'] = Header(ConversionsPL.Win2ISO(ato), 'iso-8859-2')
                     msgRoot['To'] = ConversionsPL.Win2ISO(ato)
                     msgRoot.preamble = 'This is a multi-part message in MIME format.'
                     
                     # Encapsulate the plain and HTML versions of the message body in an
                     # 'alternative' part, so message agents can decide which they want to display.
                     msgAlternative = MIMEMultipart('alternative')
                     msgRoot.attach(msgAlternative)
                     
                     msgText = MIMEText(ConversionsPL.Win2ISO('Ten komunikat należy odczytać w postaci HTML.'),'plain','iso-8859-2')
                     msgAlternative.attach(msgText)
                     
                     # We reference the image in the IMG SRC attribute by the ID we give it below
      #               msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
                     msgText = MIMEText(ConversionsPL.Win2ISO(atext), 'html', 'iso-8859-2')
                     msgAlternative.attach(msgText)
                     
                     # This example assumes the image is in the current directory
      #               fp = open('test.jpg', 'rb')
      #               msgImage = MIMEImage(fp.read())
      #               fp.close()
                     
                     # Define the image's ID as referenced above
      #               msgImage.add_header('Content-ID', '<image1>')
      #               msgRoot.attach(msgImage)
                     
                     try:                        
                        asmtp=SMTPUtil.AuthSMTP(sobj.SMTPServer)
                        if sobj.SMTPUser!='' and sobj.SMTPPassword!='':
                           asmtp.login(sobj.SMTPUser,sobj.SMTPPassword)
                        asmtp.sendmail(string.strip(sobj.SMTPFrom),string.strip(ato),msgRoot.as_string())
                        asmtp.quit()
                     except:                                                                                   
                        LogException()
         rs1.Fields.Item('Status').Value='Z'
         aadoutil.UpdateRS(rs1)
         if SEND_FIRST_EMAIL:
            rs=aadoutil.CloseRS(rs)
            rsdata=aadoutil.CloseRS(rsdata)
         rs1.MoveNext()
      rs1=aadoutil.CloseRS(rs1)
   finally:
      aadoutil.Close()
   try:
      win32api.Beep(4000,150)
      win32api.Beep(2000,100)
   except:
      pass


                          

