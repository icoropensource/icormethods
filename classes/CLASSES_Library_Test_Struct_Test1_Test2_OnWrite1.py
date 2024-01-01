# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<%
#
# Strona do pobierania danych z XMLData
#
aTable_DaneTabelaryczne=this.CRM.BaseNameModifier+'BZR_'+Plugin.PluginVars['aTableOID_DaneTabelaryczne']
aadoutil=ADOLibInit.ADOUtil(this.CRM.ConnectionString,acominitialize=1)
rs=aadoutil.GetRS("select IdZapytaniaXml from %s Group by IdZapytaniaXml"%(aTable_DaneTabelaryczne,),aclient=1)
if rs.State!=aadoutil.adoconst.adStateClosed:
   while not rs.EOF and not rs.BOF:
      axmldataid=int(ADOLibInit.GetRSValueAsStr(rs,"IdZapytaniaXml"))
      axmldata=this.CRM.GetTableXMLDataByID(axmldataid)
      if axmldata is None:
         rs.MoveNext()
         continue
      atext=''
      afname='%sXMLDATA_%d.asp'%(this.WSBaseDirectory,axmldataid)
      fout=open(afname,'w')
      aMainTable_DBName=axmldata.Parser.querysql.TablesList[0].NameSQL
      aMainTable_DBNameID=axmldata.Parser.querysql.TablesList[0].NameSQLID
      try:
         dd={
            'PluginOID':str(Plugin.OID),
            'aTable_DaneTabelaryczne':aTable_DaneTabelaryczne,
            'aMainTable_DBName':aMainTable_DBName,
            'aMainTable_DBNameID':aMainTable_DBNameID,
            'ASPVarBegin':ASPVarBegin,
            'ASPBegin':ASPBegin,
            'ASPEnd':ASPEnd,
            'XMLDataID':axmldataid,
            'ConnectionStringShape':this.ConnectionString,
         }
         atext='''<!-- #include file="all.asp" -->
<!-- #include file="inc/forms/validation.asp" -->
%(ASPBegin)s
Response.Charset = "windows-1250"
'   Response.CodePage = 1250
Response.CacheControl = "Private"
Response.ExpiresAbsolute = #1/1/1999 1:10:00 AM#

amode=ReplaceIllegalCharsLev0Text(mid(Request.QueryString("mode"),1,10))

function GetRSValue(ars,afieldname)
   dim arstype
   GetRSValue=ars.Fields(afieldname).Value
   arsType=ars.Fields(afieldname).Type
   if IsNull(GetRSValue) then
      GetRSValue="-"
   end if
   if (arsType=7) or (arsType=133) or (arsType=134) or (arsType=135) then
      GetRSValue=getDateTimeAsStr(GetRSValue)
   end if
   GetRSValue=trim(CStr(GetRSValue))
   if GetRSValue="" then
      GetRSValue="-"
   end if
end function

function JSONEncode(s)
   JSONEncode=Server.HTMLEncode(s)
   JSONEncode=replace(JSONEncode,chr(13),"&#13;")
   JSONEncode=replace(JSONEncode,chr(10),"&#10;")
end function

Function stripHTMLTags(val)
   dim re
   set re = new RegExp
   re.pattern = "<[\w/]+[^<>]*>"
   re.global=true
   stripHTMLTags = re.replace(val,"")
   set re=Nothing
End Function

function GetTableAbstract(atable,toid,amaxlen)
   dim rs9,m9,i9,f9,n9,s9
   GetTableAbstract=""
   Set rs9 = Server.CreateObject("ADODB.Recordset")
   rs9.ActiveConnection = cn
   rs9.CursorType = 1 'adOpenKeyset
   rs9.LockType = 3 'adLockOptimistic
   rs9.Source = "select * from " & atable & " where _OID='" & toid & "'"
   rs9.Open
   if not rs9.EOF then
      for i9=0 to rs9.Fields.Count-2
         n9=rs9.Fields.Item(i9).Name
         if mid(n9,1,1)<>"_" and TypeName(rs9.Fields(i9).Value)="String" and n9<>"InformacjaPodmiotUdostepniajacy" and n9<>"InformacjaOsobaOdpowiedzialna" and n9<>"InformacjaOpisCzynnosci" then
            s9=CStr(rs9.Fields.Item(i9).Value)
            if (s9<>"") and ((len(s9)<>32) or ((len(s9)=32) and (InStr(s9," ")>0))) then
               GetTableAbstract=GetTableAbstract & " " & s9
            end if
         end if
      next
   end if
   if rs9.State<>adStateClosed then
      rs9.Close
   end if
   set rs9=Nothing
   GetTableAbstract=stripHTMLTags(GetTableAbstract)
   GetTableAbstract=replace(GetTableAbstract,"""","`")
   GetTableAbstract=replace(GetTableAbstract,"'","`")
   GetTableAbstract=replace(GetTableAbstract,chr(10)," ")
   GetTableAbstract=replace(GetTableAbstract,chr(13)," ")
   GetTableAbstract=Left(GetTableAbstract,amaxlen)
end function

if amode="p" then
   ReturnValue=0
   MoreRecords=0
   aPageNumber=CLng(ReplaceIllegalCharsLev0Text(mid(Request.QueryString("page"),1,10)))
   aRecsPerPage=CLng(ReplaceIllegalCharsLev0Text(mid(Request.QueryString("rows"),1,10)))
   asidx=ReplaceIllegalCharsLev0Text(mid(Request.QueryString("sidx"),1,80))
   asord=ReplaceIllegalCharsLev0Text(mid(Request.QueryString("sord"),1,6))
   achapterid=ReplaceIllegalCharsLev0Text(mid(Request.QueryString("chapterid"),1,10))

   Set cn = Server.CreateObject("ADODB.Connection")
   cn.CursorLocation=2 'adUseServer
   cn.CommandTimeout=15
   cn.ConnectionTimeout=15
   cn.Open CONNECTION_STRING
   sp=""
   iandcnt=0
   iorcnt=0
   if achapterid<>"" then
      sp=sp & " (%(aMainTable_DBName)s._ChapterID=" & achapterid & ") "
   end if
   sob=""
'''%dd
         for asearchrule in axmldata.Parser.querysql.LSearchFields:
            atext=atext+"""
if sp<>"" then
   sp=sp & " AND "
end if
sp=sp & " (%s %s %s) "
"""%(asearchrule.Field.NameSQL,asearchrule.TypeOp,asearchrule.Value)

         for afield in axmldata.Parser.querysql.FieldsList:
            if afield.IsIndexed and afield.IsAliased and afield.Type in ['string','numeric','date','datetime','text','integer','money','dict','dict int','bool','float']:
               atext=atext+"""
   if asidx="%s" then
      sob=" %s "
   end if
"""%(afield.UniqueName,afield.NameSQL)
         atext=atext+"""
   if sob<>"" then
      if asord="asc" then
         sob=sob+" ASC "
      end if
      if asord="desc" then
         sob=sob+" DESC "
      end if
   end if
   
   Const adUseClient = 3
   Const adCmdStoredProc = &H0004
   Set cmd1 = Server.CreateObject("ADODB.Command")
   cmd1.CommandTimeout=600
   cmd1.ActiveConnection = cn
   cmd1.ActiveConnection.CursorLocation = adUseClient
   cmd1.CommandType = adCmdStoredProc
   cmd1.CommandText = "sp_%(aMainTable_DBNameID)s_xmldata_BZR_%(XMLDataID)d"
   cmd1.Parameters.Refresh
   Cmd1.Parameters("@Page").Value=aPageNumber
   Cmd1.Parameters("@Size").Value=aRecsPerPage

   Cmd1.Parameters("@sWhere").Value=sp
   Cmd1.Parameters("@sOrder").Value=sob
   Cmd1.Parameters("@UserName").Value=""
   Cmd1.Parameters("@IsPivot").Value=0
   Cmd1.Parameters("@UserRights").Value=""
   
   set rs=cmd1.Execute
   ReturnValue=CLng(cmd1.Parameters.Item(0).Value)
   MoreRecords=CLng(cmd1.Parameters("@MoreRecords").Value)

   if MoreRecords>0 then
      intNumberOfPages=int(MoreRecords/aRecsPerPage)
      if (MoreRecords mod aRecsPerPage)>0 then
         intNumberOfPages=intNumberOfPages+1
      end if

      if (aPageNumber<1) or (aPageNumber>intNumberOfPages) then
         Response.Write "{ total: "+CStr(intNumberOfPages)+", page: "+CStr(aPageNumber)+", records: "+CStr(MoreRecords)+", rows: []}"
         if rs.State<>0 then
            rs.Close
         end if
         cn.Close
         set rs=Nothing
         set cn=Nothing
         Response.End
      end if
      
      Response.Write "{ total: "+CStr(intNumberOfPages)+", page: "+CStr(aPageNumber)+", records: "+CStr(MoreRecords)+", rows: ["
      aLpFirst=rs.Fields("_Row").Value
      wcomma=0
      Do While Not rs.EOF
         if wcomma=1 then
            Response.Write ","
         end if
         aLpLast=rs.Fields("_Row").Value
         aoid=rs.Fields("%(aMainTable_DBNameID)s__OID").Value
         arsValue=rs.Fields("_Row").Value
         Response.Write "{id:'"+JSONEncode(arsValue)+"_"+aoid+"',cell:["
         Response.Write "'"+JSONEncode(arsValue)+"',"
         
"""%dd
         wp=0
         for afield in axmldata.Parser.querysql.FieldsList:
            if afield.IsAliased and afield.Type in ['string','numeric','date','datetime','text','integer','money','dict','dict int','bool','float']:
               if wp:
                  atext=atext+"""
         Response.Write ","
"""
               atext=atext+'''
         arsValue=GetRSValue(rs,"%s")
         Response.Write """"+JSONEncode(arsValue)+""""
'''%(afield.UniqueName,)
               wp=1
         atext=atext+"""
         Response.Write "]}"
         wcomma=1
         rs.MoveNext
      Loop
      Response.Write "]}"
   Else
      Response.Write "{ total: "+CStr(0)+", page: "+CStr(0)+", records: "+CStr(0)+", rows: []}"
   end if
   if rs.State<>0 then
      rs.Close
   end if
   cn.Close
   set rs=Nothing
   set cn=Nothing
end if

if amode="d" then
   aoid=ReplaceIllegalCharsLev0Text(mid(Request.QueryString("soid"),1,80))
   atableid=ReplaceIllegalCharsLev0Text(mid(Request.QueryString("tid"),1,8))
   achapterid=ReplaceIllegalCharsLev0Text(mid(Request.QueryString("chapterid"),1,10))

   Set cn = Server.CreateObject("ADODB.Connection")
   cn.CursorLocation=2 'adUseServer
   cn.CommandTimeout=15
   cn.ConnectionTimeout=15
   cn.Open CONNECTION_STRING
  
   astatus="BAD"
   ainfo=""
   litems="["

"""%dd
         def ProcessTable(aquery,atable,dd,alevel=0,swhere=''):
            lw=[]
            if swhere:
               lw.append(swhere)
            btext=''
            dd['rsModifier']=atable.NameSQLID
            btext=btext+'''
   Set rs%(rsModifier)s = Server.CreateObject("ADODB.Recordset")
   rs%(rsModifier)s.ActiveConnection = cn
   rs%(rsModifier)s.CursorType = 1 'adOpenKeyset
   rs%(rsModifier)s.LockType = 3 'adLockOptimistic
'''%dd
            aselect='SELECT '
            ls=[]
            for afield in atable.FieldsList:
               ls.append(afield.NameSQL)
            aselect=aselect+string.join(ls,',')
            aselect=aselect+' FROM '+atable.NameSQL
            if alevel==0:
               lw.append("""_OID='"+aoid+"'""")
            if lw:
               aselect=aselect+' WHERE '+string.join(lw,' AND ')
            dd['rsSelect']=aselect
            btext=btext+'''
      rs%(rsModifier)s.Open "%(rsSelect)s",cn
      do while not rs%(rsModifier)s.EOF and not rs%(rsModifier)s.BOF
'''%dd

            if alevel==0:
               btext=btext+'''
      astatus="OK"
'''%dd
            else:
               btext=btext+'''
         litems=litems+"["
'''%dd

            lfields=[]
            for afield in atable.FieldsList:
               dd2={'rsModifier':dd['rsModifier']}
               if (afield.IsAliased or afield.IsInteractive) and afield.Type in ['string','numeric','date','datetime','text','integer','money','dict','dict int','external dict','external dict multiple','bool','float']:
                  if afield.Name[:1]!='_' and afield.Name!='InformacjaPodmiotUdostepniajacy' and afield.Name!='InformacjaOsobaOdpowiedzialna' and afield.Name!='InformacjaOpisCzynnosci':
                     dd2['FieldName']=afield.Name
                     dd2['FieldPrettyName']=afield.PrettyName
                     dd2['FieldTypeDescription']=afield.TypeDescription
                     if afield.TypeDescription=='Słownik zewnętrzny' and not afield.ExternalDictTable is None:
                        dd2['FieldDictTable']=afield.ExternalDictTable.NameSQL
                        dd2['TableDictNameAlias']=afield.ExternalDictTable.NameAlias
                        btext=btext+'''
         brsvalue=GetTableAbstract("%(FieldDictTable)s",GetRSValue(rs%(rsModifier)s,"%(FieldName)s"),300)
         litems=litems+"[""%(FieldPrettyName)s"",""%(FieldTypeDescription)s"","""+brsvalue+""","""+JSONEncode(GetRSValue(rs%(rsModifier)s,"%(FieldName)s"))+""",""%(TableDictNameAlias)s""],"
'''%dd2
                     else:
                        btext=btext+'''
         litems=litems+"[""%(FieldPrettyName)s"",""%(FieldTypeDescription)s"","""+JSONEncode(GetRSValue(rs%(rsModifier)s,"%(FieldName)s"))+"""],"
'''%dd2
            for btable in atable.SubTables:
               if btable.LinkFields:
                  dd2={}
                  dd2['FieldName']=btable.NameAlias
                  dd2['FieldPrettyName']=btable.Caption
                  dd2['FieldTypeDescription']='Tabela'
                  btext=btext+'''
         litems=litems+"[""%(FieldPrettyName)s"",""%(FieldTypeDescription)s"",["
'''%dd2
                  srcfield,dstfield,aconstraint=btable.LinkFields
                  bwhere="""%s='"+GetRSValue(rs%s,"%s")+"'"""%(dstfield,atable.NameSQLID,srcfield)
                  brsModifier=dd['rsModifier']
                  btext=btext+ProcessTable(aquery,btable,dd,alevel=alevel+1,swhere=bwhere)
                  dd['rsModifier']=brsModifier
                  btext=btext+'''
                  litems=litems+"["""","""",""""]]],"
'''%dd2
            if alevel>0:
               btext=btext+'''
         litems=litems+"["""","""",""""]],"
'''%dd
            btext=btext+'''
      rs%(rsModifier)s.MoveNext
      Loop
'''%dd

            btext=btext+'''
      if rs%(rsModifier)s.State<>0 then
         rs%(rsModifier)s.Close
      end if
      set rs%(rsModifier)s=Nothing
'''%dd
            return btext

         atext=atext+ProcessTable(axmldata.Parser.querysql,axmldata.Parser.querysql.TablesList[0],dd)
         atext=atext+'''
   litems=litems+"["""","""",""""]]"

   cn.Close
   set cn=Nothing
   Response.Write "{status:"""+astatus+""",info:"""+ainfo+""",dane:"+litems+"}"
end if
%(ASPEnd)s
'''%dd
         fout.write(atext)
      finally:
         fout.close()
      rs.MoveNext()
   rs=aadoutil.CloseRS(rs)                               
aadoutil.Close()
%>                                        
