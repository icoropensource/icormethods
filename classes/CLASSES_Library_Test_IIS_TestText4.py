# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<%
#
# Ewentualne, codzienne informowania moderatora o nowych wpisach
#
aSMTPServerParametersOID=int(Plugin.PluginVars['aSMTPServerParametersOID'])
aGuestBookModeratorEmail=Plugin.PluginVars['aGuestBookModeratorEmail']

if aGuestBookModeratorEmail:
   aTable_KsiegaGosci=aWWWMenuStruct.Project.BaseNameModifier+'BZR_'+Plugin.PluginVars['aTableOID_KsiegaGosci']
   asmtpserver=aWWWMenuStruct.Project.GetSMTPServer(aSMTPServerParametersOID)
   rs=aadoutil.GetRS("select * from %s where Status in ('M','G')"%(aTable_KsiegaGosci,),aclient=1)
   if rs.State!=aadoutil.adoconst.adStateClosed:
      if rs.RecordCount>0:
         atext="""
Księga gości: %s<br>
Ilość wpisów: %d
"""%(Plugin.Obj.Nazwa,rs.RecordCount)
         l=string.split(aGuestBookModeratorEmail,',')
         for aemail in l:
            ret=asmtpserver.Send(string.strip(aemail),'Wpisy do moderacji',atext,alog=aLog)
   rs=aadoutil.CloseRS(rs)
%>
