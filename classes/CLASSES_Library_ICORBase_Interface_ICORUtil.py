# -*- coding: windows-1250 -*-
import sys
import locale
locale.setlocale(locale.LC_ALL,'')
if 1:
   try:
      import ICORDelphi
      icorapi=ICORDelphi
      ICOR_EXECUTE_EXTERNAL=0
   except:
      import icorapi
      ICOR_EXECUTE_EXTERNAL=1

import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil

import os
import re
import math
import time
import random
import shutil
import string
import struct
import urllib
import codecs
import binascii
import urlparse
import cStringIO
import traceback
import types

ZERO_DATE = (1899, 12, 30, 0, 0, 0, 0) #Delphi internal epoch
ZERO_DATE_D = (1899, 12, 30) #Delphi internal epoch - date only
ZERO_DATE_T = (0, 0, 0, 0) #Delphi internal epoch - time only
ZERO_DATE_Z = (0, 0, 0) #bad date
ZERO_DATE_TZ = ZERO_DATE_T + ZERO_DATE_Z
ZERO_DATE_MAX = (9999, 99, 99, 99, 99, 99, 99) #Max Datetime
ZERO_DATE_D_MAX = (9999, 99, 99) #Max Date
ZERO_DATE_T_MAX = (99, 99, 99, 99) #Max time
ZERO_DATE_MIN = (-1, -1, -1, -1, -1, -1, -1) #Min Datetime
ZERO_DATE_D_MIN = (-1, -1, -1) #Min Date
ZERO_DATE_T_MIN = (-1, -1, -1, -1) #Min time

monthnames=('styczeń','luty','marzec','kwiecień','maj','czerwiec','lipiec','sierpień','wrzesień','październik','listopad','grudzień')
daynames=('poniedziałek','wtorek','środa','czwartek','piątek','sobota','niedziela')
romanmonthnums=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']

_STRING_PL_ALL='ąćęłńóśźżĄĆĘŁŃÓŚŹŻ'
_STRING_NO_PL_ALL='acelnoszzACELNOSZZ'
_STRING_UPPERCASE_PL='AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
_STRING_LOWERCASE_PL='aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'

_STRING_ASCII_HIGH=''
_STRING_ASCII=''
for i in range(128,256):
   _STRING_ASCII_HIGH=_STRING_ASCII_HIGH+chr(i)
   _STRING_ASCII=_STRING_ASCII+' '

_TransTab_PLWin12502ASCII=string.maketrans(_STRING_PL_ALL,_STRING_NO_PL_ALL)
_TransTab_lowercase_PLWin1250=string.maketrans(_STRING_UPPERCASE_PL,_STRING_LOWERCASE_PL)
_TransTab_uppercase_PLWin1250=string.maketrans(_STRING_LOWERCASE_PL,_STRING_UPPERCASE_PL)
_TransTab_ASCII=string.maketrans(_STRING_ASCII_HIGH,_STRING_ASCII)

_DIGITS='0123456789'
_WHITESPACE='_ '
_GOOD_CHARS_PL=_STRING_UPPERCASE_PL+_STRING_LOWERCASE_PL+_DIGITS+_WHITESPACE

_password_chars=[]
_password_chars.extend(range(ord('0'),ord('9')+1))
_password_chars.extend(range(ord('a'),ord('z')+1))
_password_chars.extend(range(ord('A'),ord('Z')+1))

def find_in_locals(aname,adefault):
   f=sys._getframe().f_back
   while f is not None:
      if f.f_locals.has_key(aname):
         return f.f_locals[aname]
      f=f.f_back
   return adefault

def get_caller_names(adepth=0):
   ret=[]
   f=sys._getframe().f_back
   acnt=0
   while f is not None:
      aname=f.f_code.co_name
      if adepth and acnt==adepth:
         return aname      
      ret.append(aname)
      f=f.f_back
      acnt=acnt+1
   return ret

def GetUID():
#   return 0
   return find_in_locals('UID',-1)

def GetCONNECTION():
#   return 0
   return find_in_locals('CONNECTION',0)

def GetLastExceptionInfo():
   f=cStringIO.StringIO()
   traceback.print_exc(file=f)
   ret=f.getvalue()
   f.close()
   return string.split(ret,'\n')

def trace_string(tb = None, skip = 0):
   return " <- ".join("%s() (%s:%s)"%(m,os.path.split(f)[1],n) for f,n,m,u in reversed(tb or traceback.extract_stack()[:-1-skip]))

def exc_string():
   import win32api
   t,v,tb=sys.exc_info()
   if t is None:
      return ""
   try:
      v=str(v)
   except:
      v=""
   return "[%d] {%s} [%s] %s(\"%s\") in %s"%(os.getpid(),win32api.GetUserName(),tdatetime2fmtstr(tdatetime()),t.__name__,v,trace_string(tb=traceback.extract_tb(tb)))

def dumpstack(aslist=0):
   l=traceback.format_stack()[:-2]
   if aslist:
      return l
   for s in l:
      print s[:-1]

def GetICORModules(g=None):
   import types
   if g is None:
      g=globals()
   icormodules=dict([(x,y) for (x,y) in g.items() if type(y)==types.ModuleType and y.__dict__.get('__name__','<name>')==y.__dict__.get('__file__','<file>')])
   return icormodules

def InputString(acaption,atext,avalue):
   return icorapi.DialogInput(GetUID(),acaption,atext,avalue)
def InputYear(acaption='Wprowadź rok:',atext='yyyy'):
   stime=time.strftime("%Y",time.localtime(time.time()))
   s=icorapi.DialogInput(GetUID(),acaption,atext,stime)
   if s=='':
      return -1
   else:
      try:
         x=int(s)
         if x<1970 or x>2037:
            x=-1
         return x
      except:
         return -1
def InputMonth(acaption='Wprowadź miesiąc:',atext='mm'):
   stime=time.strftime("%m",time.localtime(time.time()))
   s=icorapi.DialogInput(GetUID(),acaption,atext,stime)
   if s=='':
      return -1
   else:
      try:
         x=int(s)
         if x<1 or x>12:
            x=-1
         return x
      except:
         return -1
def InputDateTime(acaption='Wprowadź datę, czas:',atext='dd/mm/yyyy hh:mm:ss'):
   stime=time.strftime("%d/%m/%Y",time.localtime(time.time()))
   s=icorapi.DialogInput(GetUID(),acaption,atext,stime)
   return s

def InputDate(acaption='Wybierz datę'):
   return icorapi.GetStdDialogValue(GetUID(),acaption,'Date','')

def InputDateTuple(acaption='Wybierz datę',atime=0):
   x=icorapi.GetStdDialogValue(GetUID(),acaption,'Date','')
   if x=='':
      return ()
   y=int(x[-4:])
   m=int(x[3:5])
   d=int(x[:2])
   if atime:
      return (y,m,d,0,0,0,0)
   else:
      return (y,m,d)

def tdate(adate=None):
   if adate is None:
      x=time.localtime(time.time())
   else:
      x=time.localtime(adate)
   return (x[0],x[1],x[2])

def tdateztime():
   x=time.localtime(time.time())
   return (x[0],x[1],x[2],0,0,0,0)

def ttime():
   x=time.localtime(time.time())
   return (x[3],x[4],x[5],0)

def tzdatetime():
   x=time.localtime(time.time())
   return (0,0,0,x[3],x[4],x[5],0)

def tdatetime(atime=None):
   if atime is None:
      x=time.localtime(time.time())
   else:
      x=time.localtime(atime)
   return (x[0],x[1],x[2],x[3],x[4],x[5],0)

def tzerodatetime():
   return (0,0,0,0,0,0,0)

def tzerodate():
   return (0,0,0)

def tzerotime():
   return (0,0,0,0)

def tdatetime2gmtdatetime(adt):
   bdt=adt[:6]+(-1,-1,-1)
   asec=time.mktime(bdt)
   x=time.gmtime(asec)
   return (x[0],x[1],x[2],x[3],x[4],x[5],0)

def tdatetime2str(value,delimiter='\t'): #as tuple
   if value==():
      return ''
   if len(value)==7:
      y,m,d,h,mm,s,ms=value
   elif len(value)==3:
      y,m,d=value
      h,mm,s,ms=0,0,0,0
   return '%d%s%d%s%d%s%d%s%d%s%d%s%d' % (y,delimiter,m,delimiter,d,delimiter,h,delimiter,mm,delimiter,s,delimiter,ms)

def tdatetime2fmtstr(value=None,noms=1,longfmt=1,adelimiter='/',asmart=0,atimedelimiter=':',apartdelimiter=' ',amsdelimiter='.'): #as string
   if value is None:
      value=tdatetime()
   if value==():
      return ''
   if len(value)==7:
      y,m,d,h,mm,s,ms=value
      if asmart and value[3:]==ZERO_DATE_T:
         return tdate2fmtstr((y,m,d),adelimiter,longfmt)
   if len(value)==3:
      if asmart:
         return tdate2fmtstr(value,adelimiter,longfmt)
      y,m,d=value
      h,mm,s,ms=0,0,0,0
   if h==0 and mm==0 and s==0 and ms==0:
      if longfmt:
         if noms:
            return '%04d%s%02d%s%02d' % (y,adelimiter,m,adelimiter,d)
         else:
            return '%04d%s%02d%s%02d' % (y,adelimiter,m,adelimiter,d)
      elif noms:
         return '%d%s%d%s%d' % (y,adelimiter,m,adelimiter,d)
      else:
         return '%d%s%d%s%d' % (y,adelimiter,m,adelimiter,d)
   else:
      if longfmt:
         if noms:
            return '%04d%s%02d%s%02d%s%02d%s%02d%s%02d' % (y,adelimiter,m,adelimiter,d,apartdelimiter,h,atimedelimiter,mm,atimedelimiter,s)
         else:
            return '%04d%s%02d%s%02d%s%02d%s%02d%s%02d%s%03d' % (y,adelimiter,m,adelimiter,d,apartdelimiter,h,atimedelimiter,mm,atimedelimiter,s,amsdelimiter,ms)
      elif noms:
         return '%d%s%d%s%d%s%d%s%d%s%d' % (y,adelimiter,m,adelimiter,d,apartdelimiter,h,atimedelimiter,mm,atimedelimiter,s)
      else:
         return '%d%s%d%s%d%s%d%s%d%s%d%s%d' % (y,adelimiter,m,adelimiter,d,apartdelimiter,h,atimedelimiter,mm,atimedelimiter,s,amsdelimiter,ms)

def tdate2fmtstr(value,delimiter='/',longfmt=0):
   if value==():
      return ''
   if len(value)==3:
      y,m,d=value
   else:
      y,m,d,h,mm,s,ms=value
   if longfmt:
      return '%04d%s%02d%s%02d' % (y,delimiter,m,delimiter,d)
   else:
      return '%d%s%d%s%d' % (y,delimiter,m,delimiter,d)

def ttime2fmtstr(value,longfmt=0,delimiter=':'):
   if value==():
      return ''
   if len(value)==4:
      h,mm,s,ms=value
   elif len(value)==3:
      h,mm,s,ms=0,0,0,0
   else:
      y,m,d,h,mm,s,ms=value
   if longfmt:
      return '%02d%s%02d%s%02d' % (h,delimiter,mm,delimiter,s)
   else:
      return '%d%s%d%s%d' % (h,delimiter,mm,delimiter,s)

def tdatetime2RFC822datetime(adt,atz='GMT',agmt=0):
   if not agmt:
      adt=tdatetime2gmtdatetime(adt)
   return "%s, %02d %s %04d %02d:%02d:%02d %s" % (
      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][DayOfWeek(adt[0], adt[1], adt[2])],
      adt[2],
      ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][adt[1]-1],
      adt[0], adt[3], adt[4], adt[5], atz)

def TimeAsString(atime):
   atime=int(atime)
   if not atime:
      return '00s'
   atime,arest=divmod(atime,60)
   ret='%02ds'%arest
   if atime:
      atime,arest=divmod(atime,60)
      ret='%02dm'%arest+ret
   if atime:
      atime,arest=divmod(atime,24)
      ret='%02dh'%arest+ret
   if atime:
      ret='%02dd'%atime+ret
   return ret

def ISODateTime2SQLDateTime(value):
   if value is None:
      return ''
   value=value.replace('T',' ')
   ipos=value.find('.')
   if ipos>0:
      value=value[:ipos]
   return value

def tdate2romanmonthyear(value):
   return romanmonthnums[value[1]-1]+' '+str(value[0])

def tdate2romanmonth(value):
   return romanmonthnums[value[1]-1]

def DayOfWeek(y,m,d):
   if m==1 or m==2:
      m=m+12
      y=y-1
   return (d+2*m+3*(m+1)/5+y+y/4-y/100+y/400)%7

def IsLeapYear(year):
   if year%4!=0:
      return 0
   elif year%100!=0:
      return 1
   elif year%400==0:
      return 1
   else:
      return 0

def DaysInMonth(year,month):
   monthlist=[31,28,31,30,31,30,31,31,30,31,30,31]
   if month==2:
      if IsLeapYear(year):
         return 29
      else:
         return 28
   return monthlist[month-1]

def PrevDay(adate):
   d=list(adate)
   d[2]=d[2]-1
   if d[2]<1:
      d[1]=d[1]-1
      if d[1]<1:
         d[0]=d[0]-1
         d[1]=12
      md=DaysInMonth(d[0],d[1])
      d[2]=md
   return tuple(d)

def NextDay(adate):
   d=list(adate)
   d[2]=d[2]+1
   md=DaysInMonth(d[0],d[1])
   if d[2]>md:
      d[2]=1
      d[1]=d[1]+1
      if d[1]>12:
         d[1]=1
         d[0]=d[0]+1
   return tuple(d)

def StartOfWeek(adate):
   d=list(adate)
   wd=DayOfWeek(d[0],d[1],d[2])
   while wd>0:
      d=PrevDay(d)
      wd=wd-1
   return tuple(d)

def EndOfWeek(adate):
   d=list(adate)
   wd=DayOfWeek(d[0],d[1],d[2])
   while wd<6:
      d=NextDay(d)
      wd=wd+1
   return tuple(d)

def ThisWeek(adate):
   df=StartOfWeek(adate)
   dl=df
   for i in range(6):
      dl=NextDay(dl)
   return df,dl

def LastWeek(adate):
   df=StartOfWeek(adate)
   df=PrevDay(df)
   dl=df
   for i in range(6):
      dl=PrevDay(dl)
   return dl,df

def NextWeek(adate):
   df=EndOfWeek(adate)
   df=NextDay(df)
   dl=df
   for i in range(6):
      dl=NextDay(dl)
   return df,dl

def FromStartOfMonth(adate):
   d=list(adate)
   return (d[0],d[1],1),adate
   
def ThisMonth(adate):
   d=list(adate)
   md=DaysInMonth(d[0],d[1])
   return (d[0],d[1],1),(d[0],d[1],md)
   
def LastMonth(adate):
   d=list(adate)
   d[1]=d[1]-1
   if d[1]<1:
      d[1]=12
   md=DaysInMonth(d[0],d[1])
   return (d[0],d[1],1),(d[0],d[1],md)

def NextMonth(adate):
   d=list(adate)
   d[1]=d[1]+1
   if d[1]>12:
      d[1]=1
   md=DaysInMonth(d[0],d[1])
   return (d[0],d[1],1),(d[0],d[1],md)

def FromStartOfYear(adate):
   d=list(adate)
   return (d[0],1,1),(d[0],d[1],d[2])

def ThisYear(adate):
   d=list(adate)
   return (d[0],1,1),(d[0],12,31)

def LastYear(adate):
   d=list(adate)
   return (d[0]-1,1,1),(d[0]-1,12,31)

def NextYear(adate):
   d=list(adate)
   return (d[0]+1,1,1),(d[0]+1,12,31)
   
def InputFile(acaption='Wybierz plik',afilename=''):
   return icorapi.GetStdDialogValue(GetUID(),acaption,'File',afilename)

def InputDirectory(acaption='Wybierz katalog'):
   return icorapi.GetStdDialogValue(GetUID(),acaption,'Directory','')

def SummaryEdit(asummaryOID):
   return icorapi.SummaryEdit(GetUID(),asummaryOID)

class InputElementDialog:
   def __init__(self,acaption='',ashowfields=0,ashowmethods=0,ashowsummaries=0):
      self.ItemClass=''
      self.ClassPath=''
      self.FieldName=''
      self.MethodName=''
      self.Value=''
      self.Caption=acaption
      self.ShowFields=ashowfields
      self.ShowMethods=ashowmethods
      self.ShowSummaries=ashowsummaries
   def Show(self):
      elms=0
      if self.ShowFields>0:
         elms=elms+2
      if self.ShowMethods>0:
         elms=elms+4
      if self.ShowSummaries>0:
         elms=elms+8
      ret=icorapi.SelectElementDialog(GetUID(),self.Caption,elms)
      self.ItemClass,self.ClassPath,self.FieldName,self.MethodName,self.Value=ret
      return self.ItemClass!=''

def InputPassword(acaption='',auser=''):
   return icorapi.GetStdDialogValue(GetUID(),acaption,'Password',auser)

def GetRandomPassword(alen=10):
   while 1:
      res=[]
      ws=0
      for i in range(alen):
         c=chr(random.choice(_password_chars))
         if c>='a' and c<='z':
            ws=ws|1
         if c>='A' and c<='Z':
            ws=ws|2
         if c>='0' and c<='9':
            ws=ws|4
         res.append(c)
      if ws==7:
         break
   return ''.join(res)

def GetReadablePassword():
   l1=['b','c','d','f','g','h','j','k','l','m','n','p','r','s','t','w','z'] #'q','v','x','y',
   l2=['a','e','i','o','u','y']
   ret=''
   for i in range(3):
      ret=ret+random.choice(l1)+random.choice(l2)+random.choice(l1)
   return ret

def GetReadablePasswordPL():
   dk={
'a':['ni', 'wi', 'ja', 'pi', 'tu', 'da', 'za', 'ny', 'le', 'cy', 'to', 'ri', 'ru', 'no', 'ce', 'wa', 'la', 'ne'],
'b':['ow', 'yw', 'li', 'ro', 'yc', 'ez', 'ra', 'ed', 'io', 'ej', 'ie', 'yt', 'am', 'je', 'ny', 'an', 'is', 'aw'],
'c':['ze', 'yj', 'zy', 'er', 'io', 'ho', 'za', 'zo', 'yc', 'ie', 'hy', 'eg', 'ia', 'en', 'ni', 'ow', 'iw', 'yz'],
'd':['us', 'zi', 'ok', 'no', 'ni', 'za', 'ze', 'mi', 'ow', 'ep', 'an', 'po', 'aj', 'ac', 'ku', 'aw', 'lu', 'op'],
'e':['ni', 'ze', 'pi', 'ci', 'je', 'mi', 'po', 'si', 'ra', 'go', 'da', 'wi', 'ro', 'za', 'wa', 'pu', 'de', 'bi'],
'f':['un', 'ik', 'or', 'er', 'in', 'iz', 'ir', 'ak', 'ni', 'na', 'ic', 'on', 'al', 'ac'],
'g':['ol', 'od', 'ra', 'lo', 'an', 'ie', 'le', 'ro', 'ul', 'la', 'wa', 'as', 'uj', 'os', 'ru', 'in', 'ni', 'al'],
'h':['od', 'wi', 'yb', 'ow', 'an', 'un', 'ro', 'om', 'yl', 'wa', 'ic', 'or', 'oc', 'ni', 'iw', 'ar', 'ny', 'ko'],
'i':['er', 'en', 'ka', 'az', 'ad', 'es', 'al', 'ed', 'ow', 'ec', 'us', 'el', 'ez', 'on', 'an', 'ko', 'ni', 'ot'],
'j':['ed', 'ny', 'ac', 'ez', 'ne', 'es', 'at', 'ec', 'mu', 'on', 'al', 'et', 'ak', 'mo', 'en', 'em', 'aw', 'ko'],
'k':['to', 'on', 're', 'at', 'om', 'ty', 'ow', 'up', 'la', 'ie', 'ut', 'os', 'az', 'ac', 'ni', 'wi', 'um', 'an'],
'l':['no', 'on', 'ic', 'ac', 'en', 'ez', 'oz', 'ow', 'os', 'ad', 'ok', 'as', 'yw', 'at', 'an', 'ni', 'ik', 'eg'],
'm':['ie', 'is', 'ow', 'in', 'oc', 'io', 'ia', 'ac', 'aj', 'ni', 'it', 'en', 'ag', 'uj', 'oz', 'ar', 'or', 'al'],
'n':['du', 'os', 'ie', 'we', 'yc', 'ic', 'eg', 'no', 'an', 'ik', 'io', 'ac', 'ow', 'al', 'yw', 'ab', 'as', 'fo'],
'o':['wa', 'wi', 'so', 'ko', 'ny', 'wy', 'mi', 'ry', 'bo', 'zy', 'na', 'le', 'su', 're', 'we', 'wo', 'ne', 'mo'],
'p':['ra', 'ow', 'is', 'ie', 'oz', 'od', 'ol', 'os', 'ap', 'la', 'ro', 'ad', 'el', 'ly', 'ub', 'or', 'an', 'oc'],
'r':['ze', 'zy', 'aw', 'es', 'to', 'ty', 'oz', 'za', 'mi', 'an', 'ow', 'od', 'iu', 'yc', 'ej', 'un', 'oc', 'os'],
's':['ta', 'ty', 'ci', 'ob', 'po', 'te', 'ze', 'to', 'lo', 'ie', 'wi', 'za', 'ku', 'uj', 'ad', 'ow', 'ka', 'ia'],
't':['yc', 'or', 'os', 'ow', 'ni', 'aw', 'at', 'er', 'yf', 'yw', 'ar', 'al', 'an', 'ro', 'wo', 'wa', 'ak', 'ko'],
'u':['mo', 'ja', 'pi', 'te', 'me', 'ci', 'zy', 'mi', 'py', 'gi', 'ne', 'za', 'ni', 'gu', 'be', 'wa', 'ra', 'ko'],
'w':['ar', 'es', 'an', 'ia', 'ie', 'ni', 'ol', 'yc', 'yk', 'ym', 'id', 'ne', 'az', 'ny', 'eg', 'la', 'il', 'or'],
'y':['cy', 'wa', 'fi', 'wo', 'ci', 'ta', 'pa', 'tu', 'ko', 'ma', 'ni', 'da', 'la', 'so', 'na', 'wi', 'ku', 'we'],
'z':['en', 'es', 'ys', 'yn', 'an', 'ia', 'el', 'on', 'ec', 'ad', 'ac', 'yt', 'ed', 'ep', 'aw', 'ez', 'as', 'yc'],
}
   ls=['fun','inw','pra','kto','war','jed','ucz','sta','tow','ust','okr','dok','oso','czy','jez','umo','nie','cer','pow','pod','kom','zaw','akt','ter','spo','pap','mie','roz','zas','obo','dzi','wyk','rej','sto','zez','odp','emi','dep','inn','osw','zam','tak','poz','zar',]
   de={
'a':['nia', 'nie', 'tow', 'cji', 'wie', 'niu', 'tut', 'kze', 'dku', 'rty', 'wna', 'zie', 'nej', 'jac', 'cym', 'cje', 'wem', 'nym', 'wne', 'rta', 'rgu', 'low', 'dza', 'dac', 'cej', 'kie', 'zac', 'zku', 'mia', 'lne', 'rze', 'zna', 'zek', 'wcy', 'nem', 'dzi', 'zne', 'zki', 'dem', 'cza', 'cja', 'sie', 'zwe', 'kim'],
'b':['ywa', 'ami', 'yte', 'owe', 'rej', 'oru', 'nym', 'ytu', 'yta', 'yli', 'owi', 'oda', 'nej', 'awy'],
'c':['twa', 'ych', 'ego', 'zen', 'zej', 'zne', 'zyc', 'zna', 'eny', 'zbe', 'zny', 'nik', 'zek', 'zby', 'two', 'iej', 'zyl', 'iem', 'ich', 'zym', 'ony', 'ach', 'zki', 'zas', 'iwy', 'ami', 'zyn', 'zno', 'zac', 'ymi', 'imi', 'hwe', 'emu', 'ane', 'zaj', 'owe', 'ona', 'nym', 'iwe', 'isk', 'iom', 'ilo', 'ila', 'iel'],
'd':['usz', 'nio', 'nie', 'lug', 'aje', 'nak', 'zie', 'zic', 'uje', 'kow', 'zym', 'zac', 'pis', 'owy', 'owe', 'nia', 'nej', 'ami', 'ach', 'yby', 'res', 'aja', 'zaj', 'yty', 'owa', 'nym', 'ali', 'omi', 'miu', 'ana', 'zor', 'zki', 'zil', 'zen', 'ytu', 'ome', 'nim', 'nik', 'nic', 'jal', 'eks', 'dal', 'cow', 'azy'],
'e':['nia', 'nie', 'niu', 'cia', 'sci', 'row', 'sie', 'tto', 'ciu', 'sla', 'pis', 'rac', 'rte', 'dem', 'cie', 'cej', 'bne', 'czy', 'res', 'nty', 'nta', 'den', 'sli', 'rta', 'rty', 'dno', 'zne', 'zna', 'rci', 'ksu', 'sow', 'cza', 'bna', 'wna', 'rze', 'dac', 'cka', 'zen', 'tni', 'sic', 'sem', 'ntu', 'mne', 'low'],
'f':['nac', 'ert', 'onu', 'ach'],
'g':['oda', 'iej', 'ody', 'uje', 'uja', 'ode', 'anu', 'asa', 'nie', 'ana', 'aja', 'aca', 'any', 'oru', 'olu'],
'h':['yba', 'odu', 'ody', 'nie', 'wal', 'ome'],
'i':['sji', 'kow', 'sja', 'ery', 'owe', 'sow', 'nie', 'sje', 'ecy', 'usz', 'ego', 'ety', 'ela', 'any', 'otu', 'ony', 'ana', 'nno', 'one', 'ona', 'wko', 'kat', 'ane', 'alu', 'agu', 'ace', 'aja', 'tej', 'ste', 'ami', 'ala', 'kom', 'aly', 'som', 'rme', 'oty', 'ada', 'aca', 'wym', 'tal', 'owo', 'eta', 'era', 'cow'],
'j':['ace', 'acy', 'nym', 'aca', 'nej', 'sce', 'ete', 'scu', 'ami', 'ach', 'szy', 'sze', 'sza', 'mie', 'lub', 'ety', 'eta', 'ela'],
'k':['aty', 'ach', 'iem', 'owe', 'cji', 'ami', 'ich', 'iej', 'osc', 'res', 'atu', 'cje', 'arb', 'ody', 'owi', 'lad', 'ona', 'cie', 'upu', 'uje', 'owa', 'una', 'uja', 'tow', 'sie', 'ret', 'owy', 'owo', 'oro', 'oda', 'lym', 'alu', 'ali', 'aja'],
'l':['aty', 'one', 'ony', 'ezy', 'ego', 'ega', 'ona', 'nej', 'ska', 'edu', 'nie', 'aja', 'ada', 'ate', 'ski', 'owe', 'oby', 'ita', 'ywu', 'uje', 'uty', 'uja', 'owy', 'owi', 'osc', 'nym', 'kie', 'ywa', 'ych', 'uta', 'osu', 'nia', 'iwe', 'eza', 'ane', 'ami', 'ala', 'ady', 'adu', 'yby', 'ozy', 'owo', 'osy', 'osi'],
'm':['owy', 'owe', 'inu', 'iot', 'uje', 'owa', 'aga', 'iny', 'nej', 'iar', 'ywa', 'ian', 'uja', 'oca', 'arl', 'ych', 'osc', 'nia', 'ila', 'ent', 'emu'],
'n':['ych', 'ego', 'osc', 'iem', 'ika', 'iej', 'ymi', 'iez', 'uje', 'owi', 'kow', 'ana', 'nym', 'nej', 'osi', 'icy', 'ane', 'tow', 'cji', 'ien', 'cie', 'any', 'ach', 'iku', 'ica', 'emu', 'sow', 'iki', 'czy', 'aly', 'owe', 'iec', 'uja', 'tem', 'iom', 'ich', 'ywa', 'ily', 'ila', 'ice', 'ial', 'elo', 'ela', 'cem'],
'o':['sci', 'sob', 'rym', 'rej', 'kat', 'cie', 'tem', 'nej', 'dze', 'wym', 'zna', 'sek', 'row', 'sku', 'nym', 'wac', 'lne', 'ich', 'bie', 'wic', 'rmy', 'wej', 'dzi', 'wie', 'wia', 'bec', 'zyc', 'tow', 'lna', 'dow', 'rzy', 'bom', 'sow', 'lny', 'dne', 'czy', 'wod', 'wna', 'wan', 'tny', 'nie', 'dki', 'zby', 'wil'],
'p':['isy', 'lat', 'uje', 'isu', 'raw', 'nia', 'ekt', 'uja', 'lyw', 'ilo', 'oki', 'nie', 'ily', 'ila', 'ada'],
'r':['zez', 'ych', 'awa', 'min', 'ami', 'ony', 'awo', 'zed', 'otu', 'ona', 'cia', 'mie', 'uga', 'gan', 'ego', 'aku', 'cie', 'owy', 'esu', 'esc', 'cza', 'tej', 'ska', 'oli', 'oby', 'aci', 'zen', 'zec', 'ymi', 'one', 'ofa', 'nie', 'etu', 'emu', 'dzi', 'azy', 'aza', 'awe', 'ane', 'acy', 'ach', 'aca', 'zyc', 'zem'],
's':['twa', 'two', 'tek', 'oby', 'tki', 'tru', 'uje', 'zem', 'cia', 'oba', 'zej', 'owe', 'ami', 'ady', 'zym', 'obe', 'tac', 'cie', 'ach', 'zac', 'tal', 'ciu', 'zlo', 'ter', 'lac', 'zen', 'tka', 'tep', 'mie', 'lic', 'tko', 'nie', 'kow', 'kim', 'iag', 'cem', 'zyc', 'zuw', 'tke', 'obu', 'mem', 'lug', 'iec', 'iat'],
't':['ore', 'awy', 'osc', 'ego', 'awa', 'kow', 'utu', 'ulu', 'ora', 'ych', 'ala', 'aje', 'uje', 'wem', 'ami', 'alo', 'ywa', 'wie', 'aja', 'row', 'szy', 'ron', 'ory', 'edy', 'aly', 'yki', 'nik', 'nej', 'anu', 'ach', 'uly', 'uja', 'nim', 'arg', 'api', 'ale', 'uty', 'roj', 'nie', 'nia', 'ery', 'ele', 'alu', 'ymi'],
'u':['szu', 'szy', 'sza', 'cie', 'nku', 'nki', 'nek', 'sze', 'tem', 'tki', 'tek', 'cje', 'tku', 'ntu', 'pic', 'nty', 'low', 'zyc', 'rsu', 'pie', 'mie', 'mer', 'kty', 'dzy', 'cji'],
'w':['ych', 'ego', 'nej', 'ane', 'ymi', 'ili', 'ila', 'osc', 'och', 'nym', 'iek', 'ach', 'ote', 'aza', 'any', 'ami', 'ala', 'oty', 'ana', 'owe', 'oju', 'nia', 'uje', 'odu', 'ile', 'ien', 'arl', 'aly', 'ale', 'szy', 'owy', 'oje', 'oim', 'iac', 'alo', 'aja', 'sze', 'sza', 'owo', 'ota', 'oli', 'ody', 'nik', 'nic'],
'y':['jny', 'wow', 'jne', 'cie', 'cia', 'wac', 'wem', 'wie', 'lko', 'zji', 'nku', 'tul', 'jna', 'zje', 'wny', 'tym', 'nie', 'czy', 'tow', 'tku', 'tki', 'tac', 'lic', 'ciu', 'bia', 'zja', 'sta', 'nki', 'mal', 'lby', 'dac', 'cza', 'cje', 'bie', 'tem', 'sku', 'sci', 'pis', 'nna', 'nil', 'nik', 'nic', 'nal', 'mac'],
'z':['eli', 'nie', 'one', 'any', 'ona', 'ial', 'ach', 'nym', 'kow', 'ych', 'nej', 'ane', 'ony', 'ego', 'esc', 'adu', 'ibe', 'ace', 'aju', 'iej', 'yna', 'uje', 'sze', 'ech', 'owi', 'ecz', 'dej', 'iba', 'dym', 'dan', 'aje', 'ywa', 'yny', 'ono', 'edu', 'bie', 'ana', 'aja', 'ylo', 'yka', 'tow', 'szy', 'sza', 'owo'],
}
   apass=random.choice(ls)
   apass=apass+random.choice(dk[apass[-1:]])
   apass=apass+random.choice(de[apass[-1:]])
   return apass

def GetSafeString(s):
   s=string.replace(s,'\\','\\\\')
   s=string.replace(s,'\'','\\\'')
   s=string.replace(s,'\"','\\\"')
   return s

def GetNameAsGoodNamePL(s):
   s1=''
   for c in s:
      if c in _GOOD_CHARS_PL:
         s1=s1+c
      else:
         s1=s1+' '
   return s1

def GetUniqueStringInContainer(s,adata,amaxlen=0,aadd=0,adefvalue=0,aonlychars=0,alower=0):
   if alower:
      s=strLowerPL(s)
   if amaxlen:
      s=s[:amaxlen]
   if aonlychars:
      s=GetNameAsGoodNamePL(s)
   s1=s
   cnt=1
   if type(adata)==type([]):
      while s1 in adata:
         s1=s+str(cnt)
         if amaxlen and len(s1)>amaxlen:
            s1=s[:2*amaxlen-len(s)-len(str(cnt))-1]+str(cnt)
            if not s1:
               s1=str(cnt)[:amaxlen]
         cnt=cnt+1
         if cnt>777:
            raise SystemError
      if aadd:
         adata.append(s1)
   else:
      while adata.has_key(s1):
         s1=s+str(cnt)
         if amaxlen and len(s1)>amaxlen:
            s1=s[:2*amaxlen-len(s)-len(str(cnt))-1]+str(cnt)
            if not s1:
               s1=str(cnt)[:amaxlen]
         cnt=cnt+1
         if cnt>777:
            raise SystemError
      if aadd:
         adata[s1]=adefvalue
   return s1

def GetSafeRepositoryPath(s):
   s=string.replace(s,'\\','_')
   s=string.replace(s,'/','_')
   return s

def str2ProperID(s,aunderscore=0):
   s=strPL2ASCII(s)
   ret=''
   s1=''
   for c in s:
      if (c>='0' and c<='9') or (c>='a' and c<='z') or (c>='A' and c<='Z'):
         s1=s1+c
      elif aunderscore and c=='_':
         s1=s1+c
      elif s1:
         ret=ret+s1.capitalize()
         s1=''
   if s1:
      ret=ret+s1.capitalize()
   if (ret[:1]>='0' and ret[:1]<='9'):
      ret='a'+ret
   return ret

def do_exec(f,g,l=None,n=''):
   if l is None:
      l=g
   if isinstance(f,types.StringTypes):
      f=string.replace(f,chr(13),'\n')
      f=f+'\n'
   c=compile(f,n,'exec')
   exec(c,g,l)

def str2value(s):
   return eval(s, {'__builtins__': {}})

def str2bool(s):
   if isinstance(s,types.StringTypes):
      if s.lower() in ['true','1','on','yes','prawda','tak','t','y']:
         return 1
   try:
      i=int(s)
      if i>0:
         return 1
   except:
      return 0
   return 0

def normalizeDate(y,m,d,adumb=1):
   if d>31:
      y,m,d=d,m,y
   if not y and not m and not d:
      y,m,d=1900,1,1
   if y<0:
      y=1900
   if m<=0:
      m=1
   if d<=0:
      d=1
   if y<30:
      y=y+2000
   elif y>=30 and y<100:
      y=y+1900
   elif y<1900:
      y=1900
   if m<1 or m>12:
      m=1
   if d<1 or d>31:
      d=1
   if adumb:
      while y>=3000:
         y=y-1000
      while y>=2030:
         y=y-100
   return y,m,d

def DateDiff(adt1,adt2=None):
   if adt2 is None:
      adt2=tdatetime()
   if len(adt1)==7:
      y,m,d,h,mm,s,ms=adt1
   if len(adt1)==3:
      y,m,d=adt1
      h,mm,s,ms=0,0,0,0
   y,m,d=normalizeDate(y,m,d)
   if y<1970:
      y=1971
   bdt1=time.mktime((y,m,d,h,mm,s,0,0,-1))
   if len(adt2)==7:
      y,m,d,h,mm,s,ms=adt2
   if len(adt2)==3:
      y,m,d=adt2
      h,mm,s,ms=0,0,0,0
   y,m,d=normalizeDate(y,m,d)
   if y<1970:
      y=1971
   bdt2=time.mktime((y,m,d,h,mm,s,0,0,-1))
   return int((bdt2-bdt1)/86400)

def getStrAsDate(s):
   s=string.strip(s)
   patt=re.compile('(\d+)\D(\d+)\D(\d+)',re.I)
   m=patt.search(s)
   if m:
      y,m,d=normalizeDate(int(m.group(1)),int(m.group(2)),int(m.group(3)))
      alastday=DaysInMonth(y,m)
      if d<1 or d>alastday:
         return ZERO_DATE_Z
      return (y,m,d)
   return ZERO_DATE_Z

def getStrAsTime(s):
   s=string.strip(s)
   patt=re.compile('(\d+)\D(\d+)\D(\d+)',re.I)
   m=patt.search(s)
   if m:
      h,m,s=int(m.group(1)),int(m.group(2)),int(m.group(3))
      return (h,m,s,0)
   return ZERO_DATE_T

def getStrAsDateTime(s):
   if type(s)==type(()):
      return s
   s=string.strip(s)
   ld=map(int,re.findall('(\d+)',s))
   if len(ld)==3 and ':' in s:
      return (0,0,0)+getStrAsTime(s)
   if len(ld)>=3:
      y,mt,d=normalizeDate(ld[0],ld[1],ld[2])
      alastday=DaysInMonth(y,mt)
      if d<1 or d>alastday:
         return getStrAsDate(s)+(0,0,0,0)
      h,mm,ss=0,0,0
      if len(ld)>=5:
         h,mm=ld[3],ld[4]
      if len(ld)>=6:
         ss=ld[5]
      return (y,mt,d,h,mm,ss,0)
   return getStrAsDate(s)+(0,0,0,0)
str2DateTime=getStrAsDateTime

def strPL2ASCII(s,t=_TransTab_PLWin12502ASCII):
   return s[:].translate(t)

def str2ASCII(s,t=_TransTab_ASCII):
   return s[:].translate(t)

def strUpperPL(s):
   return s[:].translate(_TransTab_uppercase_PLWin1250)
ICORUpperCase=strUpperPL

def strLowerPL(s):
   return s[:].translate(_TransTab_lowercase_PLWin1250)
ICORLowerCase=strLowerPL

def strCapitalizePL(s):
   return s[:1].translate(_TransTab_uppercase_PLWin1250)+s[1:].translate(_TransTab_lowercase_PLWin1250)

def ICORCompareText(s1,s2):
   return cmp(strLowerPL(s1.strip()),strLowerPL(s2.strip()))

def hex2int(anum):
   if len(anum)<8:
      anum='0'*(8-len(anum))+anum
   elif len(anum)>8:
      anum=anum[-8:]
   return struct.unpack('>i',binascii.unhexlify(anum))[0]

def KwotaSlownie(anum):
   ld=['ZER*','JED*','DWA*','TRZ*','CZT*','PIE*','SZE*','SIE*','OSI*','DZI*']
   s='%0.2f'%anum
   s1,s2=s[:-3],s[-2:]
   ret=[]
   for c in s1:
      ret.append(ld[int(c)])
   ret.append(' ZŁ* ')
   if s2!='00' or type(anum)==type(0.0):
      ret.append(ld[int(s2[0])])
      ret.append(ld[int(s2[1])])
      ret.append(' GR*')
   return string.join(ret,'')

def str2HTMLstr(s):
   return re.sub(r'\\u([a-f0-9][a-f0-9][a-f0-9][a-f0-9])',lambda x:'&#'+str(int(x.group(1),16))+';',unicode(s,'cp1250','ignore').encode('raw_unicode_escape','xmlcharrefreplace'))

def SetClipboard(s):
   return icorapi.ICORSetClipboard(s)

def GetCurrentEditorText():
   return icorapi.RepositoryChange(GetUID(),'GetEditorText',-1,-1,'','','')

def SetCurrentEditorText(atext):
   return icorapi.RepositoryChange(GetUID(),'SetEditorText',-1,-1,'',atext,'')

def GetCurrentHTMLEditorText():
   return icorapi.RepositoryChange(GetUID(),'GetHTMLEditorText',-1,-1,'','','')

def SetCurrentHTMLEditorText(atext):
   return icorapi.RepositoryChange(GetUID(),'SetHTMLEditorText',-1,-1,'',atext,'')

def URLString2NormalString(s):
   s=XMLUtil.URL_UTF2Win(s)
   return urllib.unquote_plus(s)

def URLAddParam(aurl,aparams):
   if type(aparams)==type([]):
      aparams=string.join(aparams,'&')
   elif type(aparams)==type({}):
      aparams=string.join(map(lambda (x,y):x+'='+y,d.items()),'&')
   aaddressingscheme,anetworklocation,apath,aparameters,aquery,afragmentidentifier=urlparse.urlparse(aurl)
   if aquery:
      aquery=aquery+'&'+aparams
   else:
      aquery=aparams
   return urlparse.urlunparse((aaddressingscheme,anetworklocation,apath,aparameters,aquery,afragmentidentifier))

def GetProperPath(apath,aslashatend=1):
   if apath:
      apath=apath.replace('\\','/')
      if aslashatend:
         if apath[-1:]!='/':
            apath=apath+'/'
      else:
         if apath[-1:]=='/':
            apath=apath[:-1]
   return apath

def GetStringAsSafeScriptString(s):
   s=s.replace(chr(13),'')
   s=s.replace(chr(10),'\\n')
   s=s.replace('"','&#34;')
   s=s.replace("'",'&#39;')
   s=s.replace("%",'&#37;')
   return s

def GetStringAsSafeFileName(s):
   s=strPL2ASCII(s)
   s=re.sub(r'([^ a-zA-Z0-9\`\#\$\^\(\)\-\_\=\+\[\]\{\}\,\.\|])','_',s)
   s=string.strip(s)
   return s

_dformats={'':'%14.2f'}
_patt_formats=re.compile('(\d+?\.\d+?)',re.I)
def FormatFNum(n,sf=''):
   if not _dformats.has_key(sf):
      m=_patt_formats.search(sf)
      if m:
         _dformats[sf]='%'+m.group(1)+'f'
      else:
         sf=''
   sfp=_dformats[sf]
   return locale.format(sfp,n,1,1)

def FormatFNumHTML(n,sf=''):
   if not sf:
      sf='%14.2n'
   ret='<code>'+FormatFNum(n,sf)+'</code>'
   return ret.replace(' ','&nbsp;')

_num2bin_d={'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111','8':'1000','9':'1001','a':'1010','b':'1011','c':'1100','d':'1101','e':'1110','f':'1111'}
def num2bin(x):
   return string.join(map(_num2bin_d.get,'%x'%x),'')

def GetRandomFileName(adir,aprefix,aext):
   ldirs=[]
   if type(adir)==type([]):
      ldirs.extend(adir)
   else:
      ldirs.append(adir)
   while 1:
      anum=random.randrange(0,1000000000)
      afname='%s%010d%s'%(aprefix,anum,aext)
      w=1
      for bdir in ldirs:
         if os.path.exists(bdir+'/'+afname):
            w=0
            break
      if w:
         return afname

def FileExists(afpath):
   try:
      f=open(afpath,'rb')
   except:
      return 0
   f.close()
   return 1

def GetKBSize(asize):
   bsize=int(asize/1024.0)
   ng,nk=divmod(bsize,1024)
   if not ng:
      if not nk:
         return '1 KB'
      return str(nk)+' KB'
   return '%0.2f MB'%(ng+nk/1024.0)

def IncNumString(astr):
   sl=map(int,astr)
   sl.reverse()
   for i in range(len(sl)):
      d=1+sl[i]
      if d<=9:
         sl[i]=d
         break
      sl[i]=0
   else:
      sl.append(1)
   sl.reverse()
   sl=map(repr,sl)
   return string.join(sl,'')

def DecNumString(astr):
   sl=map(int,astr)
   sl.reverse()
   for i in range(len(sl)):
      d=sl[i]-1
      if d>=0:
         sl[i]=d
         break
      sl[i]=9
   sl.reverse()
   sl=map(repr,sl)
   return string.join(sl,'')

def OrNumString(astr1,astr2): # str == binary string
   m=len(astr1)-len(astr2)
   if m>0:
      astr2='0'*m+astr2
   elif m<0:
      astr1='0'*(-m)+astr1
   return string.join(map(str,map(lambda x,y: int(x) or int(y) ,astr1,astr2)),'')

def AndNumString(astr1,astr2): # str == binary string
   m=len(astr1)-len(astr2)
   if m>0:
      astr2='0'*m+astr2
   elif m<0:
      astr1='0'*(-m)+astr1
   return string.join(map(str,map(lambda x,y: int(x) and int(y) ,astr1,astr2)),'')

def XorNumString(astr1,astr2): # str == binary string
   m=len(astr1)-len(astr2)
   if m>0:
      astr2='0'*m+astr2
   elif m<0:
      astr1='0'*(-m)+astr1
   return string.join(map(str,map(lambda x,y: int(x) ^ int(y) ,astr1,astr2)),'')

def GetStringAsDate(avalue):
   IsValue2Check=0
   if avalue=='':
      avalue,avalue2=tdateztime(),tzerodatetime()
   elif avalue in ['dzisiaj','today']:
      IsValue2Check=1
      avalue,avalue2=tdateztime(),tdate()+(23,59,59,0)
   elif avalue in ['wczoraj','yesterday']:
      IsValue2Check=1
      avalue,avalue2=PrevDay(tdate())+(0,0,0,0),PrevDay(tdate())+(23,59,59,0)
   elif avalue in ['jutro','tomorrow']:
      IsValue2Check=1
      avalue,avalue2=NextDay(tdate())+(0,0,0,0),NextDay(tdate())+(23,59,59,0)
   elif avalue in ['od początku tygodnia','od poczatku tygodnia','from the start of the week','from start of week','from the start of week','from start of the week']:
      avalue,avalue2=StartOfWeek(tdate()),tdate()
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['ten tydzień','ten tydzien','this week']:
      avalue,avalue2=ThisWeek(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['ostatni tydzień','ostatni tydzien','last week']:
      avalue,avalue2=LastWeek(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['następny tydzień','nastepny tydzien','next week']:
      avalue,avalue2=NextWeek(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['od początku miesiąca','od poczatku miesiaca','from the start of the month','from start of month','from the start of month','from start of the month']:
      avalue,avalue2=FromStartOfMonth(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['ten miesiąc','ten miesiac','this month']:
      avalue,avalue2=ThisMonth(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['ostatni miesiąc','ostatni miesiac','last month']:
      avalue,avalue2=LastMonth(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['następny miesiąc','nastepny miesiac','next month']:
      avalue,avalue2=NextMonth(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['od początku roku','od poczatku roku','from the start of the year','from start of year','from the start of year','from start of the year']:
      avalue,avalue2=FromStartOfYear(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['ten rok','this year']:
      avalue,avalue2=ThisYear(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['ostatni rok','last year']:
      avalue,avalue2=LastYear(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   elif avalue in ['następny rok','nastepny rok','next year']:
      avalue,avalue2=NextYear(tdate())
      avalue,avalue2=avalue+(0,0,0,0),avalue2+(23,59,59,0)
      IsValue2Check=1
   else:
      avalue,avalue2=str2DateTime(avalue),tzerodatetime()
   return avalue,avalue2,IsValue2Check

def copytree(src,dst,asilent=1):
   names=[]
   try:
      names=os.listdir(src)
      os.makedirs(dst)
   except (IOError, os.error), why:
      if not asilent:
         print "nie moge utworzyc katalogu %s: %s" % (str(dst), str(why))
   for name in names:
      srcname=os.path.join(src,name)
      dstname=os.path.join(dst,name)
      try:
         if os.path.isdir(srcname):
            copytree(srcname,dstname)
         else:
            shutil.copy2(srcname,dstname)
      except (IOError, os.error), why:
         if not asilent:
            print "nie moge skopiowac pliku %s do %s: %s" % (str(srcname), str(dstname), str(why))

def IsIdentifier(avalue,asimple=0,anospecials=0):
   if anospecials:
      sspecials=''
   else:
      sspecials='_'
   if asimple:
      apatt=re.compile('^[A-Za-z'+sspecials+'0-9]+$')
   else:
      apatt=re.compile('^[A-Z][A-Za-z'+sspecials+'0-9]+$')
   m=apatt.match(avalue)
   if m:
      return 1
   return 0

def MakeIdentifier(avalue,asimple=0,adefault='ABC',adefaultprefix='a'):
   apatt=re.compile(' +')
   ret=apatt.sub('_',avalue)
   apatt=re.compile('[^A-Za-z_0-9]')
   ret=apatt.sub('',ret)
   if not ret:
      ret=adefault
   c=ret[:1]
   if not asimple:
      if c>='a' and c<='z':
         ret=c.upper()+ret[1:]
   if not ((c>='A' and c<='Z') or (c>='a' and c<='z')):
      ret=adefaultprefix+ret
   return ret

def GetProperCaption(acaption,amaxcaptionlen=40):
   if len(acaption)>amaxcaptionlen:
      l1=string.split(acaption)
      l2=[]
      amaxcaptionlen2=amaxcaptionlen/2
      i1=0
      while i1<amaxcaptionlen2 and l1:
         s=l1.pop()
         i1=i1+len(s)
         l2.append(s)
      l1.reverse()
      l2.reverse()
      l3=[]
      i1=0
      while i1<amaxcaptionlen2 and l1:
         s=l1.pop()
         i1=i1+len(s)
         l3.append(s)
      l3.append('...')
      acaption=string.join(l3+l2,' ')
   return acaption

class DummyParameters:
   def __init__(self,adict=None):
      if not adict is None:
         self.__dict__.update(adict)
      self.__dict__['__dict']=adict
   def __getattr__(self,name):
      return self.__dict__.get(name,'{'+name+'}')
   def __setattr__(self,name,value):
      self.__dict__[name]=value
      if not self.__dict__['__dict'] is None:
         self.__dict__['__dict'][name]=value
   def __getitem__(self,name):
      return self.__dict__.get(name,'{'+name+'}')
   def __setitem__(self,name,value):
      self.__dict__[name]=value
      if not self.__dict__['__dict'] is None:
         self.__dict__['__dict'][name]=value

class VarDict(dict):
   def deleteItem(self,key):
      if self.has_key(key):
         del self[key]
         return 1
      return 0
   def popItem(self,key,adefault=''):
      v=self.get(key,adefault)
      self.deleteItem(key)
      return v
   def getint(self,akey,adefault=0):
      v=self.get(akey,adefault)
      if type(v)!=type(1):
         if v=='':
            v=adefault
         else:
            v=int(v)
      return v
   def getlist(self,akey,asplit=','):
      s=self.get(akey,'')
      ret=[x.strip() for x in s.split(asplit) if x]
      return ret
   def getlistint(self,akey,asplit=','):
      s=self.get(akey,'')
      ret=[int(x.strip()) for x in s.split(asplit) if x]
      return ret
   def getlistintpairs(self,akey,asplit=','):
      ret=self.getlistint(akey,asplit)
      return zip(ret[0::2],ret[1::2])
   def AsString(self,asplit1='\n',asplit2='=',asorted=1):
      l=[]
      for k,v in self.items():
         if not isinstance(v,types.StringTypes):
            v=str(v)
         l.append(k+asplit2+v)
      if asorted:
         l.sort()
      return asplit1.join(l)

def ParseVars(avalue,d=None,asplit1='\n',asplit2='=',areplace1=chr(13),alowerkey=0):
   if d is None:
      dd=VarDict()
   else:
      dd=VarDict()
      dd.update(d)
   if avalue is None:
      return dd
   if areplace1:
      avalue=string.replace(avalue,areplace1,'')
   l=string.split(avalue,asplit1)
   for s in l:
      s=string.strip(s)
      apos=string.find(s,asplit2)
      if s[:1]=='#' or apos<1:
         continue
      if alowerkey:
         akn=strLowerPL(s[:apos])
      else:
         akn=s[:apos]
      bpos=string.find(akn,'[')
      wlist=0
      if akn[-1:]=='+':
         wlist=1
         akn=akn[:-1]
      if bpos>0 and akn[-1:]==']':
         akn2=akn[bpos+1:-1]
         akn=akn[:bpos]
         d2=dd.get(akn,{})
         if wlist:
            l2=d2.get(akn2,[])
            l2.append(s[apos+1:])
            d2[akn2]=l2
            dd[akn]=d2
         else:
            d2[akn2]=s[apos+1:]
            dd[akn]=d2
      elif wlist:
         l2=dd.get(akn,[])
         l2.append(s[apos+1:])
         dd[akn]=l2
      else:
         dd[akn]=s[apos+1:]
   return dd

class ResponseEndException(Exception):
   def __init__(self,errmsg=''):
      Exception.__init__(self,errmsg)

class ResponseStopException(Exception):
   def __init__(self,errmsg=''):
      Exception.__init__(self,errmsg)

class Response:
   def __init__(self):
      self.HTMLDocument=[]
      self.closed=0
   def end(self):
      self.closed=1
      raise ResponseEndException()
   End=end
   def stop(self):
      self.closed=1
      raise ResponseStopException()
   Stop=stop
   def write(self,*adata):
      if self.closed:
         return
      if type(adata)==type(()):
         for i in adata:
            self.HTMLDocument.append(str(i))
      else:
         self.HTMLDocument.append(str(adata))
   Write=write
   def ASPBegin(self,anl=0):
      if self.closed:
         return
      if anl:
         self.HTMLDocument.append('\n')
      self.HTMLDocument.append('<%')
      if anl:
         self.HTMLDocument.append('\n')
   def ASPVarBegin(self):
      if self.closed:
         return
      self.HTMLDocument.append('<%=')
   def ASPEnd(self,anl=0):
      if self.closed:
         return
      if anl:
         self.HTMLDocument.append('\n')
      self.HTMLDocument.append('%>')
      if anl:
         self.HTMLDocument.append('\n')
   def NL(self):
      if self.closed:
         return
      self.HTMLDocument.append('\n')
   def AsText(self,aashtmlstring=1):
      if aashtmlstring:
         return str2HTMLstr(string.join(self.HTMLDocument,''))
      return string.join(self.HTMLDocument,'')
   def AsXMLText(self,anoplconversion=1):
      if anoplconversion:
         return XMLUtil.GetAsXMLStringNoPL(string.join(self.HTMLDocument,''))
      else:
         return XMLUtil.GetAsXMLString(string.join(self.HTMLDocument,'')) #str2HTMLstr()

def GetTextAsHTMLText(data,repldict=None,aengine=None,aashtmlstring=1,aseparator='%',aglobaldict=0,ascriptname='<icor code>'):
   data=string.replace(data,chr(13),'')
   reg=re.compile('(<'+re.escape(aseparator)+'=?)|('+re.escape(aseparator)+'>)')
   fields=reg.split(data)
   fields=filter(lambda x: x and len(x)!=0,fields)
   inside_pmz=inside_pmzvar=0
#   print fields
   if aglobaldict:
      oldresponse=response=repldict.get('Response',None)
      if response is None:
         response=Response()
         repldict['Response']=response
      gdict=repldict
   else:
      response=Response()
      gdict={}
      if not repldict is None:
         oldresponse=repldict.get('Response',None)
         for key,value in repldict.items():
            gdict[key]=value
         repldict['Response']=response
      gdict['Response']=response
   gdict['aICORDBEngine']=aengine
   gdict['ASPBegin']='<'+aseparator
   gdict['ASPEnd']=aseparator+'>'
   gdict['ASPVarBegin']='<'+aseparator+'='
   gdict['re']=re
   gdict['os']=os
   gdict['string']=string
   gdict['XMLUtil']=XMLUtil
   for f in fields:
      if response.closed:
         break
      if f=='<'+aseparator+'=':
         inside_pmzvar=1
      elif f=='<'+aseparator:
         inside_pmz=1
      elif f==aseparator+'>':
         if inside_pmz:
            inside_pmz=0
         elif inside_pmzvar:
            inside_pmzvar=0
      else:
         if inside_pmz==1:
            try:
               do_exec(f,gdict,gdict,ascriptname)
            except ResponseEndException:
               pass
            except ResponseStopException:
               print 'Exec STOP:'
               sl=string.split(f,'\n')
               il=1
               for s in sl:
                  print '## %04d %s'%(il,XMLUtil.GetAsXMLStringNoPL(s))
                  il=il+1
               traceback.print_exc()
               print 'Exec STOP-INFO:'
               raise ResponseStopException
            except:
               print 'Exec:'
               sl=string.split(f,'\n')
               il=1
               for s in sl:
                  print '## %04d %s'%(il,XMLUtil.GetAsXMLStringNoPL(s))
                  il=il+1
               traceback.print_exc()
         elif inside_pmzvar==1:
            try:
               r=eval(f,gdict,gdict)
               response.write(r)
            except ResponseEndException:
               pass
            except:
               print 'eval: '+str(f)
               traceback.print_exc()
         else:
            response.write(f)
   if not repldict is None:
      if oldresponse is None:
         repldict['Response']=None
         del repldict['Response']
      else:
         repldict['Response']=oldresponse
   return response.AsText(aashtmlstring)

def StripHTMLTags(atext):
   apatt=re.compile('\<[\w\?\!/]+[^\<\>]*\>',re.I)
   bpatt=re.compile(' +',re.I)
   btext=apatt.sub(' ',atext)
   btext=string.replace(btext,'&nbsp;',' ')
   btext=string.replace(btext,chr(13),'')
   btext=string.replace(btext,chr(10),' ')
   btext=string.strip(bpatt.sub(' ',btext))
   return btext

class RecursiveParameters:
   def __init__(self):
      self.parameters={}
      self.registerednames=[]
   def __getitem__(self,name):
      plist=self.parameters.get(name,[])
      if plist==[]:
         return None
      return plist[len(plist)-1]
   def __setitem__(self,name,value):
      plist=self.parameters.get(name,[value])
      plist[len(plist)-1]=value
      self.parameters[name]=plist
   def RegisterParameters(self,value):
      if isinstance(value,types.StringTypes):
         self.registerednames.append(value)
      else:
         for aname,avalue in value:
            self.registerednames.append(aname)
            self.Push(aname,avalue)
   def Push(self,name,value):
      plist=self.parameters.get(name,[])
      plist.append(value)
      self.parameters[name]=plist
   def Pop(self,name):
      plist=self.parameters.get(name,[])
      return plist.pop()
   def PopAll(self):
      for aname in self.registerednames:
         self.Pop(aname)
   def PushAll(self):
      for aname in self.registerednames:
         avalue=self.__getitem__(aname)
         self.Push(aname,avalue)

def ClassFactory(aname,*abaseclasses):
    class Anonymous:
       pass
    Anonymous.__bases__=tuple(abaseclasses)
    Anonymous.__name__=aname
    return Anonymous

def ExtendClass(acls,*bclss):
   for bcls in bclss:
      for k,v in bcls.__dict__.items():
         if k=='__module__':
            continue
         acls.__dict__[k]=v

class BitVector:
   def __init__(self,adata=0L):
      if isinstance(adata,types.StringTypes):
         if adata[:2] in ['0x','0X']:
            adata=self.b2n(adata[2:])
         self._data=long(adata,16)
      elif type(adata)==type(self):
         self._data=adata._data
      else:
         self._data=long(adata)
      self._list=None
   def __repr__(self):
      return '%x'%self._data
   def __hex__(self):
      return '%x'%self._data
   def __nonzero__(self):
      return self._data!=0L
   def __getitem__(self,key):
      return int(self._data&(1L<<key)!=0)
   def __setitem__(self,key,value):
      self._list=None
      if value:
         self._data=self._data|(1L<<key)
      else:
         self._data=self._data&~(1L<<key)
   def __and__(self,other):
      if type(other)!=type(self):
         avalue=other
      else:
         avalue=other._data
      return BitVector(self._data&avalue)
   def __xor__(self,other,*rest):
      if type(other)!=type(self):
         avalue=other
      else:
         avalue=other._data
      return BitVector(self._data^avalue)
   def __or__(self,other,*rest):
      if type(other)!=type(self):
         avalue=other
      else:
         avalue=other._data
      return BitVector(self._data|avalue)
   def __invert__(self):
      return BitVector(~self._data&((1L<<self.__len__())-1))
   def __int__(self):
      return long(self._data)
   def __long__(self):
      return long(self._data)
   def __float__(self):
      return float(self._data)
   def __len__(self):
      mant,l=math.frexp(float(self._data))
      bitmask=1L<<l
      if bitmask<=self._data:
         return 0
      while l:
         bitmask=bitmask>>1
         if self._data&bitmask:
            break
         l=l-1
      return l
   def b2n(self,s):
      if not s:
         return '00'
      ret=''
      while s:
         if len(s)==1:
            s=s+'0'
         ret=s[:2]+ret
         s=s[2:]
      return ret
   def n2b(self,s):
      if not s:
         return '00'
      ret=''
      while s:
         if len(s)==1:
            s='0'+s
         ret=ret+s[-2:]
         s=s[:-2]
      return ret
   def keys(self):
      if not self._list is None:
         return self._list
      self._list=[]
      apos,acnt=1L,0
      while apos<=self._data:
         if apos&self._data:
            self._list.append(acnt)
         acnt=acnt+1
         apos<<=1
      return self._list
   def AsString(self):
      return self.n2b('%x'%self._data)
   def AsBinary(self,asarray=0):
      if asarray:
         snum=self.n2b('%x'%self._data)
      else:
         snum='%x'%self._data
      string.join(map(_num2bin_d.get,snum),'')

class TimeProgressEstimator:
   def __init__(self,amax):
      self.Max=amax
      self.TStart=time.time()
      self.Elapsed=0.0
      self.Estimated=0.0
      self.Remaining=0.0
      self.Value=0
   def __repr__(self):
      return '%d %s %s %s'%(self.Max-self.Value,self.Elapsed,self.Estimated,self.Remaining)
   def SetProgress(self,avalue=-1,asstring=0,amod=0):
      if not avalue:
         return '00s','00s','00s'
      if avalue<0:
         self.Value=self.Value+1
      else:
         self.Value=avalue
      if amod and self.Value%amod:
         return None
      self.Elapsed=time.time()-self.TStart
      self.Estimated=1.0*(self.Elapsed*self.Max)/self.Value
      self.Remaining=self.Estimated-self.Elapsed
      if asstring:
         return '%s %s %s'%(TimeAsString(self.Elapsed),TimeAsString(self.Estimated),TimeAsString(self.Remaining))+' ['+str(self.Value)+'/'+str(self.Max)+']'
      return TimeAsString(self.Elapsed),TimeAsString(self.Estimated),TimeAsString(self.Remaining)

class SafeStreamReaderWriter(codecs.StreamReaderWriter):
   def write(self,atext):
      if isinstance(atext,str):
         atext=unicode(atext,'cp1250','ignore')
      codecs.StreamReaderWriter.write(self,atext)

def OpenText(afilename,amode='rb',aencoding=None,aerrors='xmlcharrefreplace',abuffering=1,pathpriority=None):
   if aencoding is not None and 'b' not in amode:
      amode=amode+'b'
   acnt=5
   atime=0.2
   while acnt:
      try:
         acnt=acnt-1
         if amode[:1]=='w':
            import icorsyncfile
            afile=icorsyncfile.syncopen(afilename,amode,pathpriority=pathpriority)
         else:
            afile=open(afilename,amode,abuffering)
         break
      except IOError,e:
         if e.errno==13: #Permission denied
            time.sleep(atime)
            atime=atime+atime
         else:
            raise
   if aencoding is None:
      return afile
   ainfo=codecs.lookup(aencoding)
   asrw=SafeStreamReaderWriter(afile,ainfo.streamreader,ainfo.streamwriter,aerrors)
   asrw.encoding=aencoding
   return asrw

def GetFileExtIcon(afilename):
   aname,aext=os.path.splitext(afilename)
   dext={
"exe":"exe","cmd":"exe",
"htm":"htm","asp":"htm",
"mp3":"wav","mp4":"wav","ogg":"wav","wav":"wav","snd":"wav","mid":"wav","s3m":"wav","au":"wav",
"avi":"avi","mpg":"avi","mov":"avi","ra":"avi","mpeg":"avi","flv":"avi",
"bmp":"bmp","jpg":"bmp","jpeg":"bmp","gif":"bmp","tga":"bmp","jfif":"bmp","tif":"bmp","tiff":"bmp","png":"bmp","pcx":"bmp","xbm":"bmp","rle":"bmp","dib":"bmp",
"cer":"cer","p4m":"cer",
"chm":"chm",
"doc":"doc","rtf":"doc","wri":"doc","dot":"doc","sxw":"doc","docx":"doc",
"eml":"eml",
"fon":"fon","ttf":"fon",
"hlp":"hlp",
"img":"img","ico":"img","wmf":"img",
"ini":"ini",
"mpp":"mpp",
"msi":"msi",
"pdf":"pdf","pdx":"pdf",
"pps":"pps","ppt":"pps","ppsx":"pps","pptx":"pps",
"ps":"ps","eps":"ps",
"reg":"reg",
"txt":"txt","dat":"txt","me":"txt","diz":"txt","nfo":"txt","to":"txt",
"vss":"vss",
"win":"win",
"xls":"xls","csv":"xls","xla":"xls","xlsx":"xls",
"xml":"xml",
"xsl":"xsl",
"zip":"zip","arj":"zip","rar":"zip","lha":"zip","bz2":"zip","tar":"zip","gz":"zip","tgz":"zip","ace":"zip",
}
   aext=aext.lower().strip()
   aicon="/icorimg/filetypes/"+dext.get(aext[1:],"empty")+".png"
   return aicon

def deepsplit(s,sep=None,*subsep):
   if not subsep:
      return s.split(sep)
   return [deepsplit(fragment,*subsep) for fragment in s.split(sep)]

def hyphen_range(s):
   """ yield each integer from a complex range string like "1-9,12, 15-20,23"

   >>> list(hyphen_range('1-9,12, 15-20,23'))
   [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 15, 16, 17, 18, 19, 20, 23]

   >>> list(hyphen_range('1-9,12, 15-20,2-3-4'))
   Traceback (most recent call last):
        ...
   ValueError: format error in 2-3-4
   """
   for elem in deepsplit(s,',','-'):
      if len(elem)==1: # a number
         yield int(elem[0])
      elif len(elem)==2: # a range inclusive
         start,end=map(int,elem)
         for i in xrange(start,end+1):
            yield i
      else: # more than one hyphen
         raise ValueError('format error in %s'%x)

def SplitByN(s,n=4,j=''):
   if j:
      return j.join([s[k:k+n] for k in xrange(0,len(s),n)])
   return [s[k:k+n] for k in xrange(0,len(s),n)]

def SafeSplit(s, sc=','):
   l=filter(lambda x:len(x),map(lambda x:x.strip(),s.split(sc)))
   return l

def SafeSplitInt(s, sc=','):
   l = map(int, SafeSplit(s, sc))
   return l

patt1_removeSQLComments=re.compile(r'(\-\-.*?)$',re.M+re.S)
patt2_removeSQLComments=re.compile(r'(\/\*.*?\*\/)',re.M+re.S)
def removeSQLComments(asql):
   bsql=patt1_removeSQLComments.sub('',asql)
   bsql=patt2_removeSQLComments.sub(' ',bsql)
   return bsql

def formatSQLAsASP(asql,varname='asql',aindent=3):
   sindent=' '*aindent
   ret=sindent+'%s=""\n'%(varname,)
   asql=removeSQLComments(asql)
   for s in asql.split('\n'):
      if s.find('$$$')>=0:
         s=s.replace('$$$','')
         ret+=s+'\n'
      else:
         ret+=sindent+'%s=%s+"%s "\n'%(varname,varname,s.replace('"','""'))
   return ret

