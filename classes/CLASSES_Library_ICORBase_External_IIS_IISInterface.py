# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

#from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def Test1(Log):
   teststring='>ten ciag znaków służy do testowania ciągów znaków<'
   Log('  *** Server ***\n')
   Log('     ScriptTimeout = %s\n'%Server.ScriptTimeout)
   Log('     HTMLEncode = %s\n'%Server.HTMLEncode(teststring))
   Log('     MapPath = %s\n'%Server.MapPath(teststring))
   Log('     URLEncode = %s\n'%Server.URLEncode(teststring))

   Log('  *** Session ***\n')
   Log('     CodePage = %s\n'%Session.CodePage)
   Log('     LCID = %s\n'%Session.LCID)
   Log('     SessionID = %s\n'%Session.SessionID)
   Log('     Timeout = %s\n'%Session.Timeout)

   Log('  *** Request ***\n')
   Log('     Cookies = %s\n'%Request.Cookies.item1)
   Log('     Form = %s\n'%Request.Form.item1)
   Log('     QueryString = %s\n'%Request.QueryString.item1)
   Log('     ServerVariables = %s\n'%Request.ServerVariables.item1)

   Log('  *** Response ***\n')
   Log('     Buffer = %d\n'%Response.Buffer)
   Log('     CacheControl = %s\n'%Response.CacheControl)
   Log('     Charset = %s\n'%Response.Charset)
   Log('     ContentType = %s\n'%Response.ContentType)
   Log('     Expires = %s\n'%Response.Expires)
   Log('     ExpiresAbsolute = %s\n'%Response.ExpiresAbsolute)
   Log('     IsClientConnected = %d\n'%Response.IsClientConnected)
   Log('     Status = %s\n'%Response.Status)

def DumpValue(astring,avalue):
   if type(avalue)!=type(''):
      avalue=str(avalue)
   Response.Write('<font color="green" size="+2"><b>%s:</b> = %s</font><br><br>\n'%(astring,avalue))

def DumpCollection(astring,acollection):
   skl=acollection.keys()
   Response.Write('<font color="green" size="+2"><b>%s: </b></font><br>\n'%astring)
   for sk in skl:
      s='   <b><i>%s</i></b> = %s<br>\n'%(sk,acollection[sk])
      Response.Write(s)
   Response.Write('<br>')

def Test2(Log):
   Response.Write('<h1>Działa znowu i znowu!!!</h1>')

   DumpValue('SessionID',Session.SessionID)
   DumpCollection('QueryString',Request.QueryString)
   DumpCollection('Form',Request.Form)
   DumpCollection('ServerVariables',Request.ServerVariables)

   DumpValue('Response.Buffer',Response.Buffer)
   DumpValue('Response.CacheControl',Response.CacheControl)
   DumpValue('Response.Charset',Response.Charset)
   DumpValue('Response.ContentType',Response.ContentType)
   DumpValue('Response.IsClientConnected',Response.IsClientConnected)
   DumpValue('Response.Status',Response.Status)

   Session.Contents['UP1']='UParam1'
   Session.Contents['UP2']='UParam1'

   Application.Contents['UP1']='UParam1'
   Application.Contents['UP2']='UParam1'

   DumpCollection('Application.Contents',Application.Contents)
   DumpCollection('Session.Contents',Session.Contents)

#   Response.Write('<br>')
#   s=Request.Cookies.AsString()
#   print 'Cookies:',s[:80]
#   Response.Write('<b>Cookies: </b>'+s+'<hr>')

def DoStart(Log,aiid):
   Log("Method: %s\n"%aiid)
   Test2(Log)



