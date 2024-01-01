# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:57

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *

LIB_START='''&lt;%%
function GetHeaders
   GetHeaders=""
   For Each Key In Request.ServerVariables
      GetHeaders=GetHeaders &amp; Key &amp; "=" &amp; Server.URLEncode(Request.ServerVariables(Key)) &amp; chr(10)
   Next
end function

class %sAPI
   public xmldom
   private abaseurl,aappid,averbose
   private amessagetype
   private aresponsetext
   
   Private Sub Class_Initialize
      abaseurl=BASE_URL
      aappid=APP_ID
      averbose=VERBOSE
      aresponsetext=""
   End Sub

   Private Sub Class_Terminate
      Set xmldom = Nothing
   End Sub

   Public Property Get BaseURL
      BaseURL=abaseurl
   End Property

   Public Property Let BaseURL(avalue)
      abaseurl = avalue
   End Property
   
   Public Property Get AppID
      AppID=aappid
   End Property

   Public Property Let AppID(avalue)
      aappid = avalue
   End Property
   
   Public Property Get Verbose
      Verbose=averbose
   End Property

   Public Property Let Verbose(avalue)
      averbose = avalue
   End Property

   Public Property Get ResponseText
      ResponseText=aresponsetext
   End Property

   Public Property Let ResponseText(avalue)
      aresponsetext = avalue
   End Property
   
   private function Call%s(aurl,aparams)
      dim xmlHttp
      aurl=abaseurl + aurl
      Call%s=false
      Set xmldom = Nothing
      amessagetype=""
      set xmlHttp=server.createobject("MSXML2.ServerXMLHTTP")
      xmlHttp.open "POST",aurl,false
      xmlhttp.setRequestHeader "Content-Type","application/x-www-form-urlencoded"
      xmlHttp.send aparams
      if xmlHttp.ReadyState=4 then
         if xmlHttp.Status=200 then
            me.ResponseText=xmlHttp.responseText
            set xmldom = Server.CreateObject("MSXML2.DOMDocument")
            xmldom.async=false
            Call%s=xmldom.loadxml(me.ResponseText)
            if Call%s then
               set anode=xmldom.selectSingleNode("//type")
               amessagetype=anode.text
               set anode=nothing
            else
               xmldom=Nothing
            end if
         else
            xmlHttp.Abort
         end if
      else
         xmlHttp.Abort
      end if
      set xmlHttp=nothing
   end function

   Public Property Get MessageType
      MessageType=amessagetype
   End Property

   function GetMessageParam(aparamname)
      set anode=xmldom.selectSingleNode("/" &amp; amessagetype &amp; "/" &amp; aparamname)
      GetMessageParam=anode.text
      set anode=nothing
   end function

   Public Property Get Status
      Status=GetMessageParam("status")
   End Property

   Public Property Get Info
      Info=GetMessageParam("info")
   End Property
   
   Public Property Get tokenid
      tokenid=GetMessageParam("tokenid")
   End Property

   Public Property Get userid
      userid=GetMessageParam("userid")
   End Property

'''

LIB_PARAM_0='''      d="%s=" &amp; Server.HTMLEncode(%s)
'''
LIB_PARAM_1='''      d=d &amp; "&amp;%s=" &amp; Server.HTMLEncode(%s)
'''

LIB_METHOD_0='''   function %s_%s(%s)
%s      %s_%s=CallSI("%s/%s",d)
   end function

'''

LIB_FINISH_0='''end class
%&gt;
'''

def RegisterFields(aclass,amenu,file,aoid=-1,areport=None):
   awwweditor=ICORWWWEditor(aclass,amenu,file,areport)
   awwweditor.RegisterField('Nazwa',aoid=aoid)
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

def OnWWWActionGetLink(aobj,amenu):
   return ''

def GetDoc(s):
   if not s:
      s='&nbsp;-&nbsp;'
   s=s.replace('\n','<br>\n')
   return s

def OnWWWAction(aobj,amenu,file):
   #awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,None)
   #if amenu.Action=='ObjectApplyMethods':
      #awwweditor.Write()

   file.write('<pre>\n')
   file.write(LIB_START%(aobj.LibraryPrefix,aobj.LibraryPrefix,aobj.LibraryPrefix,aobj.LibraryPrefix,aobj.LibraryPrefix,))

   lnamespaces=[]
   nobj=aobj.Namespaces
   while nobj:
      lnamespaces.append(nobj.Nazwa)
      #file.write(LIB_CLASS_0%(aobj.LibraryPrefix,nobj.Nazwa,aobj.LibraryPrefix))
      #file.write('<tr><td>URL:</td><td colspan=2><a href="%s">%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,aobj.URLBase+nobj.URLPath,))
      #file.write('<tr><td>WSDL:</td><td colspan=2><a href="%s?WSDL">%s?WSDL</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,aobj.URLBase+nobj.URLPath,))
      mobj=nobj.Metody
      while mobj:
         lparams=[]
         pobj=mobj.Parameters
         while pobj:
            lparams.append(pobj.Nazwa)
            pobj.Next()
         sparams=','.join(lparams)
         sdparams=''
         if lparams:
            sdparams=LIB_PARAM_0%(lparams[0],lparams[0])+''.join([LIB_PARAM_1%(x,x) for x in lparams[1:]])
         file.write(LIB_METHOD_0%(nobj.Nazwa,mobj.Nazwa,sparams,sdparams,nobj.Nazwa,mobj.Nazwa,nobj.URLPath,mobj.URLMethod))
         #file.write('<tr><td>Dokumentacja:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(mobj.Dokumentacja),))
         #file.write('<tr><td>Dokumentacja wyniku:</td><td colspan=2>%s</td></tr>\n'%(GetDoc(mobj.DokumentacjaRet),))
         #file.write('<tr><td>URL - opis, parametry, wyniki:</td><td colspan=2><a href="%s?op=%s">%s?op=%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,mobj.URLMethod,aobj.URLBase+nobj.URLPath,mobj.URLMethod))
         #file.write('<tr><td>URL do wywołania:</td><td colspan=2><a href="%s/%s">%s/%s</a></td></tr>\n'%(aobj.URLBase+nobj.URLPath,mobj.URLMethod,aobj.URLBase+nobj.URLPath,mobj.URLMethod))
         mobj.Next()
      nobj.Next()
   file.write(LIB_FINISH_0)
   file.write('</pre>\n')
   return 0

def OnWWWActionSubmit(aobj,amenu,areport,file):
   if not areport['refMode']:
      awwweditor=RegisterFields(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 0</h1>')
      file.write('<h2>Field : %s</h2>'%awwweditor['Nazwa'])
      bwwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,None)
      bwwweditor.Write(arefMode='step1')
   elif areport['refMode']=='step1':
      awwweditor=RegisterFieldsStep1(aobj.Class,amenu,file,aobj.OID,areport)
      file.write('<h1>Step 1</h1>')
      file.write('<h2>Field 1: %s</h2>'%awwweditor['Field1'])
      file.write('<h2>Field 2: %s</h2>'%awwweditor['Field2'])
      file.write('<h2>Field 3: %s</h2>'%awwweditor['Field3'])

