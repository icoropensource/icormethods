# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

atext="""
class SIUser(SIServiceBase):
   def Login(self,appid,username,passwordhash,salt,headers):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 504 - nieprawidlowe haslo
         status: 505 - wystapil blad podczas pobierania tokena. konieczne ponowne logowanie.
      '''
      d={
         'appid':appid,
         'username':username,
         'passwordhash':passwordhash,
         'salt':salt,
         'headers':headers
      }
      return self.api.CallSI('user.asmx/Login',d)
   def Impersonate(self,appid,username,headers):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 505 - wystapil blad podczas pobierania tokena. konieczne ponowne logowanie.
      '''
      d={
         'appid':appid,
         'username':username,
         'headers':headers
      }
      return self.api.CallSI('user.asmx/Impersonate',d)
   def Logout(self,appid,token):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 505 - wystapil blad podczas pobierania tokena. token nie jest aktywny.
         status: 506 - token nie istnieje lub nie jest aktywny
      '''
      d={
         'appid':appid,
         'token':token
      }
      return self.api.CallSI('user.asmx/Logout',d)
   def GetParam(self,appid,token,paramname):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 507 - brak parametru o podanej nazwie
      '''
      d={
         'appid':appid,
         'token':token,
         'paramname':paramname,
      }
      return self.api.CallSI('user.asmx/GetParam',d)
   def SetParam(self,appid,token,paramname,paramvalue):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 507 - brak parametru o podanej nazwie
         status: 508 - parametr nie zostal zaktualizowany
      '''
      d={
         'appid':appid,
         'token':token,
         'paramname':paramname,
         'paramvalue':paramvalue
      }
      return self.api.CallSI('user.asmx/SetParam',d)
   def CheckRole(self,appid,token,roleid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 505 - wystapil blad podczas pobierania tokena. token nie jest aktywny.
         status: 509 - uzytkownik nie wystepuje w podanej roli
      '''
      d={
         'appid':appid,
         'token':token,
         'roleid':roleid,
      }
      return self.api.CallSI('user.asmx/CheckRole',d)
   def GetRoles(self,appid,token):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 505 - wystapil blad podczas pobierania tokena. token nie jest aktywny.
      '''
      d={
         'appid':appid,
         'token':token,
      }
      return self.api.CallSI('user.asmx/GetRoles',d)
   def AddRole(self,appid,token,roleid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 505 - wystapil blad podczas pobierania tokena. token nie jest aktywny.
         status: 510 - rola o podanym id nie istnieje.
         status: 511 - rola nie zostala przypisana.
      '''
      d={
         'appid':appid,
         'token':token,
         'roleid':roleid,
      }
      return self.api.CallSI('user.asmx/AddRole',d)
   def RemoveRole(self,appid,token,roleid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 505 - wystapil blad podczas pobierania tokena. token nie jest aktywny.
         status: 509 - uzytkownik nie wystepuje w podanej roli
         status: 510 - rola o podanym id nie istnieje.
         status: 512 - rola nie zostala usunieta.
      '''
      d={
         'appid':appid,
         'token':token,
         'roleid':roleid,
      }
      return self.api.CallSI('user.asmx/RemoveRole',d)

class SIUsers(SIServiceBase):
   def Items(self,appid,token,offset,limit):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 514 - brak uzytkownikow
         status: 515 - nieprawidlowy zakres parametrow
      '''
      d={
         'appid':appid,
         'token':token,
         'offset':offset,
         'limit':limit,
      }
      return self.api.CallSI('users.asmx/Items',d)
   def Create(self,appid,token,username,passwordhash,email,status):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 516 - uzytkownik o podanej nazwie juz istnieje
         status: 517 - uzytkownik nie zostal dodany
         status: 529 - nieprawidlowa wartosc parametru status.
      '''
      d={
         'appid':appid,
         'token':token,
         'username':username,
         'passwordhash':passwordhash,
         'email':email,
         'status':status,
      }
      return self.api.CallSI('users.asmx/Create',d)
   def Delete(self,appid,token,username):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 516 - uzytkownik o podanej nazwie juz istnieje
         status: 517 - uzytkownik nie zostal dodany
         status: 518 - status nie zostal zaktualizowany
      '''
      d={
         'appid':appid,
         'token':token,
         'username':username,
      }
      return self.api.CallSI('users.asmx/Delete',d)
   def AddRole(self,appid,token,username,roleid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 510 - rola o podanym id nie istnieje.
         status: 511 - rola nie zostala przypisana.
      '''
      d={
         'appid':appid,
         'token':token,
         'username':username,
         'roleid':roleid,
      }
      return self.api.CallSI('users.asmx/AddRole',d)
   def RemoveRole(self,appid,token,username,roleid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 510 - rola o podanym id nie istnieje.
         status: 512 - rola nie zostala usunieta.
      '''
      d={
         'appid':appid,
         'token':token,
         'username':username,
         'roleid':roleid,
      }
      return self.api.CallSI('users.asmx/RemoveRole',d)
   def CheckRole(self,appid,token,username,roleid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 509 - uzytkownik nie wystepuje w podanej roli
      '''
      d={
         'appid':appid,
         'token':token,
         'username':username,
         'roleid':roleid,
      }
      return self.api.CallSI('users.asmx/CheckRole',d)
   def AssignIdentity(self,appid,token,username,login,providerid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 505 - wystapil blad podczas pobierania tokena. konieczne ponowne logowanie.
         status: 527 - tozsamosc nie jest w stanie zezwalajacym na przypisanie.
         status: 528 - identyfikator uzytkownika nie zostal zaktualizowany.
      '''
      d={
         'appid':appid,
         'token':token,
         'username':username,
         'login':login,
         'providerid':providerid,
      }
      return self.api.CallSI('users.asmx/AssignIdentity',d)

class SIRoles(SIServiceBase):
   def Items(self,appid,token):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 515 - nieprawidlowy zakres parametrow
         status: 519 - brak rol
      '''
      d={
         'appid':appid,
         'token':token,
      }
      return self.api.CallSI('roles.asmx/Items',d)

class SIIdentities(SIServiceBase):
   def Items(self,appid,token,offset,limit):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 520 - brak tozsamosci
         status: 515 - nieprawidlowy zakres parametrow
      '''
      d={
         'appid':appid,
         'token':token,
         'offset':offset,
         'limit':limit,
      }
      return self.api.CallSI('identities.asmx/Items',d)
   def Create(self,appid,token,login,providerid,userid,status):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 521 - tozsamosc o podanej nazwie juz istnieje w rejestrze dostawcy
         status: 522 - tozsamosc nie zostala dodana
         status: 523 - brak zarejestrowanej tozsamosci
         status: 524 - nieprawidlowy kod dostawcy tozsamosci
         status: 529 - nieprawidlowa wartosc parametru status.
      '''
      d={
         'appid':appid,
         'token':token,
         'login':login,
         'providerid':providerid,
         'userid':userid,
         'status':status,
      }
      return self.api.CallSI('identities.asmx/Create',d)
   def Delete(self,appid,token,login,providerid):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 523 - brak zarejestrowanej tozsamosci
         status: 524 - nieprawidlowy kod dostawcy tozsamosci
         status: 518 - status nie zostal zaktualizowany
      '''
      d={
         'appid':appid,
         'token':token,
         'login':login,
         'providerid':providerid,
      }
      return self.api.CallSI('identities.asmx/Delete',d)

class SIIdentity(SIServiceBase):
   def Impersonate(self,appid,login,providerid,headers):
      '''
         status: 0 - OK
         status: 501 - wystapil blad podczas przetwarzania danych. w info jest tresc komunikatu
         status: 502 - nieprawidlowy kod aplikacji, lub aplikacja zablokowana
         status: 503 - brak zarejestrowanego uzytkownika o podanej nazwie
         status: 505 - wystapil blad podczas pobierania tokena. konieczne ponowne logowanie.
         status: 525 - nie mozna impersonifikowac tozsamości bez przypisanego uzytkownika SI. Uzyj metody AssignIdentity.
         status: 526 - tozsamosc nie jest w stanie zezwalajacym na impersonifikacje.
         status: 529 - nieprawidlowa wartosc parametru status.
      '''
      d={
         'appid':appid,
         'login':login,
         'providerid':providerid,
         'headers':headers
      }
      return self.api.CallSI('identity.asmx/Impersonate',d)
"""

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   UID=18500
   rclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
   robj=rclass[35000]

   mclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_API_Method']
   pclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_API_Parameter']
   tclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_API_ParameterType']
   nclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_API_Namespace']
   l=atext.split('\n')
   astate=''
   dtypes={
      'appid':'OID',
      'email':'EMail',
      'headers':'Opis',
      'limit':'Liczba całkowita',
      'login':'Ciąg znaków - 1 linia',
      'offset':'Liczba całkowita',
      'paramname':'Ciąg znaków - 1 linia',
      'paramvalue':'Ciąg znaków - 1 długa linia',
      'passwordhash':'Ciąg znaków - 1 linia',
      'providerid':'OID',
      'roleid':'OID',
      'salt':'Ciąg znaków - 1 linia',
      'status':'Ciąg znaków - 1 linia',
      'token':'OID',
      'userid':'OID',
      'username':'Ciąg znaków - 1 linia',
}
   dparms={}
   for s in l:
      if s[:8]=='class SI':
         l1=s.split('(')
         sclass=l1[0][8:]
         print sclass
         astate='c'
      elif s[:7]=='   def ':
         l1=s.split('(')
         smethod=l1[0][7:]
         print '  ',smethod
         astate='m'
      elif s[:9]=="      '''":
         if astate=='m':
            astate='d'
            ldokumentacja=[]
         else:
            print '     ',ldokumentacja
            astate='de'
      elif s[:9]=='      d={':
         lparms=[]
         astate='p'
      elif s[:7]=='      }':
         print '       ',lparms
         astate='p2'
      elif s[:15]=='      return se':
         l1=s.split("'")
         surl=l1[1]
         l1=surl.split('/')
         surlpath=l1[0]
         surlmethod=l1[1]
         print surl,surlpath,surlmethod
         moid=mclass.AddObject(arefobject=robj)
         mclass.Nazwa[moid]=smethod
         #mclass.Grupa[moid]=sclass
         mclass.DokumentacjaRet[moid]='\n\nWartości pola status:\n'+'\n'.join(ldokumentacja)
         mclass.URLPath[moid]=surlpath
         mclass.URLMethod[moid]=surlmethod
         for aparam in lparms:
            poid=pclass.AddObject(arefobject=robj)
            pclass.Nazwa[poid]=aparam
            tname=dtypes[aparam]
            toid=tclass.Opis.Identifiers(tname)
            pclass.ParameterType.AddRefs(poid,[toid,tclass.CID])
            mclass.Parameters.AddRefs(moid,[poid,pclass.CID])
         noid=nclass.Nazwa.Identifiers(sclass)
         if noid<0:
            noid=nclass.AddObject(arefobject=robj)
            nclass.Nazwa[noid]=sclass
         nclass.Metody.AddRefs(noid,[moid,mclass.CID])
      elif astate=='d':
         ldokumentacja.append(s.strip())
      elif astate=='p':
         l1=s.split("'")
         sparm=l1[1]
         lparms.append(sparm)
         dparms[sparm]=1

   if 0:
      lk=dparms.keys()
      lk.sort()
      for s in lk:
         print "      '%s':'',"%(s,)
#class SIUser(SIServiceBase):
#   def Login(self,appid,username,passwordhash,salt,headers):


   if 0:
      aoid=aclass.AddObject(arefobject=robj)
      print aoid
      aclass.Nazwa[aoid]='testsi1'
   return
