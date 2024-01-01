# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('edtLoginName',adisplayed='Użytkownik',atype=mt_String,avalue='')
   awwweditor.RegisterField('edtPassword1',adisplayed='Hasło',atype=mt_String,avalue='')
   awwweditor.RegisterField('edtFirstName',adisplayed='Imię',atype=mt_String,avalue='')
   awwweditor.RegisterField('edtLastName',adisplayed='Nazwisko',atype=mt_String,avalue='')
   awwweditor.RegisterField('edtEMail',adisplayed='EMail',atype=mt_String,avalue='')
   awwweditor.RegisterField('edtPhone',adisplayed='Telefon',atype=mt_String,avalue='')
   awwweditor.RegisterField('edtOpis',adisplayed='Opis',atype=mt_String,avalue='')
   gclass=aclass.UserGroups.ClassOfType            
   awwweditor.RegisterField('edtGrupy',adisplayed='Grupy dostępu',atype=gclass.CID,avalue='')
   return awwweditor

def RegisterFieldsDefaults(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('edtLoginName',adisplayed='Użytkownik',atype=mt_String,avalue=areport['edtLoginName'])
   awwweditor.RegisterField('edtPassword1',adisplayed='Hasło',atype=mt_String,avalue=areport['edtPassword1'])
   awwweditor.RegisterField('edtFirstName',adisplayed='Imię',atype=mt_String,avalue=areport['edtFirstName'])
   awwweditor.RegisterField('edtLastName',adisplayed='Nazwisko',atype=mt_String,avalue=areport['edtLastName'])
   awwweditor.RegisterField('edtEMail',adisplayed='EMail',atype=mt_String,avalue=areport['edtEMail'])
   awwweditor.RegisterField('edtPhone',adisplayed='Telefon',atype=mt_String,avalue=areport['edtPhone'])
   awwweditor.RegisterField('edtOpis',adisplayed='Opis',atype=mt_String,avalue=areport['edtOpis'])
   gclass=aclass.UserGroups.ClassOfType            
   awwweditor.RegisterField('edtGrupy',adisplayed='Grupy dostępu',atype=gclass.CID,avalue='')
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

def OnWWWActionGetLink(aobj,amenu):
   return ''

def OnWWWAction(aobj,amenu,file):
   awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   if amenu.Action=='ObjectApplyMethods':
      awwweditor.Write()
   return 0 # show back reference to main object (1-link, 2-button)

def OnWWWActionSubmit(aobj,amenu,areport,file):
   auser,apassword,afirstname,alastname,aemail,aphone,adescription=areport['edtLoginName'],areport['edtPassword1'],areport['edtFirstName'],areport['edtLastName'],areport['edtEMail'],areport['edtPhone'],areport['edtOpis']
   agroups=areport.AsListFromField('edtGrupy',asint=1)
   asecprofile=ICORSecurity.ICORSecurityProfile()
   asecprofile.SetByUser(amenu.uid)
   asecprofile.GetUsers()
   if asecprofile.UserClass.UserName.Identifiers(auser)>=0:
      file.write('<h1><font color="red">Użytkownik o takiej nazwie już istnieje</font></h1>')
      awwweditor=RegisterFieldsDefaults(aobj.Class,amenu,file,aobj.OID,areport)
      awwweditor.Write()
      return
   grefs=''
   for agroup in agroups:
      grefs=grefs+str(agroup)+':'+str(asecprofile.UserGroupClass.CID)+':'
   if grefs=='':
      file.write('<h1><font color="red">Proszę wybrać co najmniej jedną grupę dostępu</font></h1>')
      awwweditor=RegisterFieldsDefaults(aobj.Class,amenu,file,aobj.OID,areport)
      awwweditor.Write()
      return
   ret=asecprofile.AddUser(auser,apassword,grefs,afirstname=afirstname,alastname=alastname,aemail=aemail,aphone=aphone,adescription=adescription)
   if ret:
      file.write('<h1><font color="green">Użytkownik został pomyślnie dodany</font></h1>')
   else:
      file.write('<h1><font color="red">Użytkownik nie został dodany</font></h1>')
      awwweditor=RegisterFieldsDefaults(aobj.Class,amenu,file,aobj.OID,areport)
      awwweditor.Write()
   return

