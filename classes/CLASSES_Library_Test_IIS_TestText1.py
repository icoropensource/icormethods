# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<%
#
# Strona do potwierdzen i zapamietywania wpisow w ksiedze gosci
#
import wordfilter

aSMTPServerParametersOID=int(Plugin.PluginVars['aSMTPServerParametersOID'])
aTable_KsiegaGosci=aWWWMenuStruct.Project.BaseNameModifier+'BZR_'+Plugin.PluginVars['aTableOID_KsiegaGosci']

#"N","Nowy wpis"
  #"B","Błędne dane"
  #"O","Oczekuje na potwierdzenie"
     #"P","Wpis potwierdzony"
       #"M","Do moderacji"
          #"X","Zablokowany przez moderatora"
             #"X1","Usunięty z listy wpisów"
          #"Z","Zatwierdzony przez moderatora"
             #"Z1","Wpis wyświetlony po moderacji"
       #"Y","Do wyświetlenia"
          #"W","Wpis wyświetlony"
       #"G","Zgłoszenie wpisu do moderacji"

#
# Wyslanie poczty z zadaniem potwierdzenia wpisu
#
asmtpserver=aWWWMenuStruct.Project.GetSMTPServer(aSMTPServerParametersOID)
rs=aadoutil.GetRS("select * from %s where Status='N'"%(aTable_KsiegaGosci,),aclient=1)
if rs.State!=aadoutil.adoconst.adStateClosed:
   while not rs.EOF and not rs.BOF:
      aoid=ADOLibInit.GetRSValueAsStr(rs,'_OID')
      v=rs.Fields.Item('DataWpisu').Value
      adatawpisu=ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime(int(v)))
      atytul=ADOLibInit.GetRSValueAsStr(rs,'Tytul')
      aautor=ADOLibInit.GetRSValueAsStr(rs,'Autor')
      aemail=ADOLibInit.GetRSValueAsStr(rs,'EMail')
      atresc=ADOLibInit.GetRSValueAsStr(rs,'Tresc')
      astatus=ADOLibInit.GetRSValueAsStr(rs,'Status')

      ahrefpotwierdzenie='%s/%s/ksiegagosci_%d.asp?mode=p&wid=%s'%(aWWWMenuStruct.Obj.AppPaths.AdresZewnetrznyWWW,aWWWMenuStruct.Obj.AppPaths.KatalogWirtualny,Plugin.OID,aoid)
      ahrefanulowanie='%s/%s/ksiegagosci_%d.asp?mode=a&wid=%s'%(aWWWMenuStruct.Obj.AppPaths.AdresZewnetrznyWWW,aWWWMenuStruct.Obj.AppPaths.KatalogWirtualny,Plugin.OID,aoid)
      atext="""
Prosimy o sprawdzenie, czy rzeczywiście wprowadzony komentarz jest tym, co powinno się wyświetlić na stronie i być widoczne
przez wszystkich ludzi na calym świecie przez wiele lat:

<div style='background:#c1dcbe;border:solid 2px #CBD79D;margin:10px;padding:5px;'>
<b>Autor:</b> %s<br>
<b>Data wpisu:</b> %s<br>
<b>Tytuł:</b> %s<br>
<hr style='border: dashed 2px green;'><br><i>%s</i>
</div>

Zastrzegamy sobie prawo do moderacji wpisu w przypadku gdy będzie on zawierał treści niezgodne z regulaminem serwisu.
<br><br>
Aby potwierdzić wpis należy wybrać <a href="%s"><font color=green>ten odnośnik</font></a>.<br>
<br>
Aby anulować wpis należy wybrać <a href="%s"><font color=red>ten odnośnik</font></a>.<br>

"""%(aautor,adatawpisu,atytul,atresc,ahrefpotwierdzenie,ahrefanulowanie)
      ret=asmtpserver.Send(aemail,'Potwierdzenie wpisu do księgi gości',atext,alog=aLog)
      if ret:
         rs.Fields.Item('Status').Value='O'
      else:
         rs.Fields.Item('Status').Value='B'
      aadoutil.UpdateRS(rs)
      rs.MoveNext()
   rs=aadoutil.CloseRS(rs)


#
# Sprawdzenie poprawnosci wpisow potwierdzonych i ustawienie status do wyswietlenia lub moderacji
#
rs=aadoutil.GetRS("select * from %s where Status='P'"%(aTable_KsiegaGosci,),aclient=1)
if rs.State!=aadoutil.adoconst.adStateClosed:
   while not rs.EOF and not rs.BOF:
      atytul=ADOLibInit.GetRSValueAsStr(rs,'Tytul')
      atresc=ADOLibInit.GetRSValueAsStr(rs,'Tresc')
      if wordfilter.CheckText(atresc):
         rs.Fields.Item('Status').Value='Y' #do wyswietlenia
      else:
         rs.Fields.Item('Status').Value='M' #do moderacji
      aadoutil.UpdateRS(rs)
      rs.MoveNext()
   rs=aadoutil.CloseRS(rs)

#
# Przygotowanie listy rozdzialow do wygenerowania w/g ostatnich zmian
#
rs=aadoutil.GetRS("select IDRozdzialu from %s where Status in ('X','Z','Y') group by IDRozdzialu"%(aTable_KsiegaGosci,),aclient=1)
lrozdzialy=[]
if rs.State!=aadoutil.adoconst.adStateClosed:
   while not rs.EOF and not rs.BOF:
      aidrozdzialu=ADOLibInit.GetRSValueAsStr(rs,'IDRozdzialu')
      lrozdzialy.append(aidrozdzialu)
      rs.MoveNext()
   rs=aadoutil.CloseRS(rs)
Response.write('Rozdzialy do zmiany: %s\n'%(str(lrozdzialy),))

aadoutil.Execute("update %s set Status='W' where Status='Y'"%(aTable_KsiegaGosci,))
aadoutil.Execute("update %s set Status='X1' where Status='X'"%(aTable_KsiegaGosci,))
aadoutil.Execute("update %s set Status='Z1' where Status='Z'"%(aTable_KsiegaGosci,))

for aidrozdzialu in lrozdzialy:
   arssobj=aWWWMenuStruct.Obj.RSSInfo
   arsscontext=None
   if arssobj:
      arsscontext=RSSInterface.RSSContext({},alog=aLog,astructobj=aWWWMenuStruct.Obj,aguidparamname='gboid')
   rs=aadoutil.GetRS("select top 200 * from %s where Status in ('Z1','W','G') and IDRozdzialu=%s order by DataWpisu DESC"%(aTable_KsiegaGosci,aidrozdzialu),aclient=1)
   if rs.State!=aadoutil.adoconst.adStateClosed:
      if not arsscontext is None:
         arsscontext.OpenFile(int(aidrozdzialu),'','',acustom=1,adir='/guestbook/',abasename='guestbook_')
      robj=aWWWMenuStruct.GetChapterByID(int(aidrozdzialu))
      djschannel={}
      djschannel['title']=robj.Obj.Naglowek
      djschannel['pubDate']=ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime())
      djschannel['lastBuildDate']=djschannel['pubDate']
      djschannel['generator']='ICOR'
      ljsitems=[]
      dd={'channel':djschannel,'items':ljsitems}
      Response.write('ID Rozdzialu %s\n'%aidrozdzialu)
      while not rs.EOF and not rs.BOF:
         adatawpisu=ADOLibInit.GetRSValueAsStr(rs,'DataWpisu')
         atytul=ADOLibInit.GetRSValueAsStr(rs,'Tytul')
         aautor=ADOLibInit.GetRSValueAsStr(rs,'Autor')
         atresc=ADOLibInit.GetRSValueAsStr(rs,'Tresc')
         astatus=ADOLibInit.GetRSValueAsStr(rs,'Status')

         Response.write('datawpisu %s\n'%str(adatawpisu))
         Response.write('tytul %s\n'%str(atytul))
         Response.write('autor %s\n'%str(aautor))
         Response.write('tresc %s\n'%str(atresc))
         Response.write('status %s\n'%str(astatus))

         if not arsscontext is None:
            arsscontext.ItemAuthor=aautor
            arsscontext.ItemGUID=ADOLibInit.GetRSValueAsStr(rs,'_OID')
            arsscontext.ItemTitle.append(atytul)
            v=rs.Fields.Item('DataWpisu').Value
            arsscontext.ItemPubDate=ICORUtil.tdatetime2RFC822datetime(ICORUtil.tdatetime(int(v)))
            arsscontext.ItemDescription.append(atresc)
            arsscontext.WriteLink()
            arsscontext.NewLink()
         di={}
         di['title']=atytul
         di['description']=atresc
         di['author']=aautor
         di['pubDate']=ICORUtil.tdatetime2fmtstr(ICORUtil.tdatetime(int(v)))
         ljsitems.append(di)
         rs.MoveNext()
      apath=FilePathAsSystemPath(aWWWMenuStruct.Obj.AppPaths.SciezkaAplikacji)
      fout=open(apath+'/guestbook/guestbook_%s.asp'%(aidrozdzialu,),'w')
      fout.write(ASPBegin+"""
Response.Charset = "windows-1250"
Response.CacheControl = "Private"
Response.ExpiresAbsolute = #1/1/1999 1:10:00 AM#
"""+ASPEnd+'\n')
      atext=JSONUtil.write(dd)
      fout.write(atext)
      fout.close()
      if not arsscontext is None:
         arsscontext.CloseFile()
      rs=aadoutil.CloseRS(rs)
%>
