# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

<%
ddict={
   'plugin_oid':Plugin.OID,
   'virtualroot':this.VirtualRoot,
   'chapteroid':this.ThisChapter.OID,
   'ASPBegin':ASPBegin,
   'ASPVarBegin':ASPVarBegin,
   'ASPEnd':ASPEnd,
   'width':int(Plugin.PluginVars.get('width','550')),
   'rowheight':int(Plugin.PluginVars.get('rowheight','26')),
   'widokrekordu_main':Plugin.PluginVars.get('aCSS_widokrekordu_main','widokrekordu_main'),
   'widokrekordu_info':Plugin.PluginVars.get('aCSS_widokrekordu_info','widokrekordu_info'),
   'widokrekordu_pozycja':Plugin.PluginVars.get('aCSS_widokrekordu_pozycja','widokrekordu_pozycja'),
   'widokrekordu_nazwa':Plugin.PluginVars.get('aCSS_widokrekordu_nazwa','widokrekordu_nazwa'),
   'widokrekordu_wartosc':Plugin.PluginVars.get('aCSS_widokrekordu_wartosc','widokrekordu_wartosc'),
   'widokrekordu_link':Plugin.PluginVars.get('aCSS_widokrekordu_link','widokrekordu_link'),
   'widokrekordu_html':Plugin.PluginVars.get('aCSS_widokrekordu_html','widokrekordu_html'),
}

aTable_DaneTabelaryczne=this.CRM.BaseNameModifier+'BZR_'+Plugin.PluginVars['aTableOID_DaneTabelaryczne']
aadoutil=ADOLibInit.ADOUtil(this.CRM.ConnectionString,acominitialize=1)
rs=aadoutil.GetRS("select * from %s where _ChapterID=%d"%(aTable_DaneTabelaryczne,this.ThisChapter.OID,),aclient=1)
if rs.State!=aadoutil.adoconst.adStateClosed:
   while not rs.EOF and not rs.BOF:
      atext=''
      axmldataid=int(ADOLibInit.GetRSValueAsStr(rs,"IdZapytaniaXml"))
      axmldata=this.CRM.GetTableXMLDataByID(axmldataid)
      if axmldata is None:
         rs.MoveNext()
         continue
      lp,lu=[],[]
      for afield in axmldata.Parser.querysql.FieldsList:
         if afield.IsAliased and afield.Type in ['string','numeric','date','datetime','text','integer','money','dict','dict int','bool','float']:
            aalign='left'
            awidth=92
            if afield.Type in ['numeric','date','datetime','integer','money','dict int','bool','float']:
               aalign='right'
               awidth=62
            if afield.ColumnWidth:
               awidth=afield.ColumnWidth
            lp.append("'%s'"%(afield.PrettyName,))
            asortable='false'
            if afield.IsIndexed:
               asortable='true'
            lu.append("{name:'%s',index:'%s', width: %d, align:'%s', sortable: %s}"%(afield.UniqueName,afield.UniqueName,awidth,aalign,asortable))
      ddict["FieldsPrettyNames"]=string.join(lp,',')
      ddict["FieldsUniqueNames"]=string.join(lu,','+chr(13)+chr(10))
      ddict["XMLDataID"]=axmldataid
      atext=atext+"""
<style>
   table.scroll {
   table-layout: fixed;
   background-color: white;
   }

   table.scroll tr.over td {
   background: #E1DCF4;
   }

   table.scroll tr.alt {
   background: #F9F9F9;
   }

   table.scroll tr.selected td {
   background: #FFFFB9;
   color: Black;
   }

   table.scroll tbody td  {
   padding: 2px;
   text-align: left;
   border-bottom: 1px solid #D4D0C8;
   border-left: 1px solid #D4D0C8;
   text-overflow: ellipsis;
   overflow: hidden;
   white-space: nowrap;
   }

   table.scroll th  {
   padding: 2px;
   /* background-color: #ebf3fd; */
   border-bottom: 1px solid #CBC7B8;
   border-left: 1px solid #D4D0C8;
   text-align: left;
   font-weight: normal;
   overflow: hidden;
   background-image: url(/icorlib/jquery/plugins/jqGrid/grid-blue-hd.gif);
   }

   table.scroll th div {
   overflow: hidden;
   white-space: nowrap;
   }

   table.scroll th span {
   cursor: e-resize;
   /* border-right: 1px solid #D6D2C2;  */
   width: 10px;
   float: right;
   display: block;
   margin: -2px -1px -2px 0px;
   height: 18px;
   overflow: hidden;
   }

   table.scroll thead {
   }

div.loading {
   position: absolute;
   padding: 3px;
   text-align: center;
   font-weight: bold;
   background: red;
   color: white;
   display: none;
   }
   div.scroll {
/* padding: 0px; */
   background-color: #ADD8E6;
   /* border-bottom: 1px solid #ADD8E6; */
/* font-weight: normal; */
   background: url(/icorlib/jquery/plugins/jqGrid/grid-blue-ft.gif);
   }
.selbox {
   font-size: x-small;
   }
.cbox {
   height: 10px;
   width: 10px;
   /*border:1px solid #999;*/
}

img.jsHover {
       border: 1px solid #99CCFF;
   }
.tablediv {
   display: table;
   background-color: White;
   border-spacing: 1px;
   /*cellspacing:poor IE support for  this*/
   border-collapse: separate;
   width:100%%;
   /* FF hack poor when scroling subgrid */
}
.celldiv {
   float: left;
   display: table-cell;
   border: 1px dotted #CCCCCC;
   overflow: auto;
   }
.celldivth {
   float: left;
   /*fix for  buggy browsers*/
   border: 1px solid #CCCCCC;
   background-color: #99CCFF;
   border-bottom: 1px solid #CBC7B8;
   text-align: left;
   overflow: auto;
   }
.rowdiv  {
   display: table-row;
   background: #F9F9F9 none;
   color: #000000;
   width: 100%%;
   overflow:auto;
   }
.subgrid {
   overflow:  auto;
   }
</style>
"""%ddict

      if not Plugin.PluginVars.get('aCSS_wpisypamiatkowe_main',''):
         atext=atext+"""
<style>
.%(widokrekordu_main)s {border:dashed 2px #8CA5CA;margin:5px;padding:5px;}
.%(widokrekordu_info)s {margin:2px;padding:4px;width:95%%;text-align:left;font-weight:bold;font-style:italic;font-size:12pt;}
.%(widokrekordu_pozycja)s {margin:2px;padding:4px;width:97%%;text-align:left;}
.%(widokrekordu_nazwa)s {margin:2px;padding:4px;width:22%%;text-align:right;font-weight:bold;float:left;}
.%(widokrekordu_wartosc)s {margin:2px;padding:4px;font-size:7pt;width:72%%;float:left;}
.%(widokrekordu_link)s {margin:2px;padding:4px;font-size:7pt;cursor:pointer;width:72%%;float:left;text-decoration:underline;}
.%(widokrekordu_html)s {overflow:scroll; width:100%%; height:200px; border: 1px dotted black;}
</style>
"""%ddict

      atext=atext+"""
<table id="list%(XMLDataID)d" class="scroll" cellpadding="0" cellspacing="0"></table>
<div id="pager%(XMLDataID)d" class="scroll" style="text-align:center;"></div>

<script language="javascript">
function grid_load_%(XMLDataID)d () {
   jQuery("#list%(XMLDataID)d").jqGrid({
      url:'xmldata_%(XMLDataID)d.asp?mode=p&nd='+new Date().getTime(),
      page:1,
      width:%(width)d,
//      fixedwidth:true,
      rowheight: %(rowheight)d,
      datatype: "json",
      colNames:['l.p.',%(FieldsPrettyNames)s],
      colModel:[
         {name:'l.p.',index:'l.p.', width:22,align:'right'},
         %(FieldsUniqueNames)s
      ],
      altRows:true,
      rowNum:5,
      rowList:[5,10,20,30],
      imgpath: '/icorlib/jquery/plugins/jqGrid',
      recordtext: "Pozycji",
      loadtext: "Ładowanie...",
      pager: jQuery('#pager%(XMLDataID)d'),
      sortname: 'id',
      viewrecords: true,
      sortorder: "asc",
      onSelectRow: function(aid) {
         if(aid==null) {
//            detail_%(XMLDataID)d("T1","");
         } else {
            detail_%(XMLDataID)d("T1",aid);
         }
      }
//$$>
   });
}
function xmlDecode(s) {
   s=s.replace(/&#13;/g, '');
   s=s.replace(/&#10;/g, '\\n');
   s=s.replace(/&quot;/g, '"');
   s=s.replace(/&apos;/g, "'");
   s=s.replace(/&lt;/g, "<");
   s=s.replace(/&gt;/g, ">");
   s=s.replace(/&amp;/g, "&");
   return s;
}
function detail_%(XMLDataID)d_load(json,atid) {
   if (json.status=="OK") {
      var amax=1;
      $("#detail_"+atid).append("<div class=%(widokrekordu_info)s>"+json.info+"</div>");
      var w=0;
      $.each(json.dane,
         function(i,aitem) {
            var s="";
            function processItem(aitem) {
               if ((aitem[2]!="") && (aitem[2]!="-")) {
                  w=1;
                  if (aitem[1]=="Słownik zewnętrzny_") {
                     s+="<div class=%(widokrekordu_pozycja)s><span class=%(widokrekordu_nazwa)s>"+aitem[0]+":</span><span class=%(widokrekordu_link)s onclick='javascript:detail_%(XMLDataID)d(\\""+aitem[4]+"\\",\\"0_"+aitem[3]+"\\");'>"+aitem[2]+"</span><div><div style='clear:both;'></div>";
                  } else if (aitem[1]=="Tabela") {
                     bitems=aitem[2];
                     if (bitems.length>1) {
                        s+="<div class=%(widokrekordu_pozycja)s><div class=%(widokrekordu_nazwa)s>"+aitem[0]+":</div><div style='clear:both;'></div><div>";
                        s+="<table class=scroll>";
                        s+="<tr>";
                        ditems=bitems[0];
                        for (var j=0;j<ditems.length;j++){
                           citem=ditems[j];
                           if (citem[1]=="Tabela") {
                           } else if (citem[1]!="") {
                              s+="<th>"+citem[0]+"</th>";
                           }
                        }
                        s+="</tr>";
                        for (var k=0;k<bitems.length;k++){
                           ditems=bitems[k];
                           if (ditems[0]!="") {
                              s+="<tr>";
                              for (var j=0;j<ditems.length;j++){
                                 citem=ditems[j];
                                 if (citem[1]=="Słownik zewnętrzny_") {
                                    s+="<td>"+citem[2]+"</td>";
                                 } else if (citem[1]=="Tabela") {
                                    processItem(citem);
                                 } else if (citem[1]=="HTML") {
                                    s+="<td>"+xmlDecode(citem[2])+"</td>";
                                 } else if (citem[1]!="") {
                                    s+="<td>"+citem[2]+"</td>";
                                 }
                              }
                              s+="</tr>";
                           }
                        }
                        s+="</table>";
                        s+="</div><div style='clear:both;'></div>";
                     }
                  } else if (aitem[1]=="HTML") {
                     s+="<div class=%(widokrekordu_pozycja)s><div class=%(widokrekordu_nazwa)s>"+aitem[0]+":</div><div style='clear:both;'></div><div class=%(widokrekordu_html)s>"+xmlDecode(aitem[2])+"</div><div style='clear:both;'></div>";
                  } else {
                     s+="<div class=%(widokrekordu_pozycja)s><span class=%(widokrekordu_nazwa)s>"+aitem[0]+":</span><span class=%(widokrekordu_wartosc)s>"+aitem[2]+"</span></div><div style='clear:both;'></div>";
                  }
               }
            }
            processItem(aitem);
            $("#detail_"+atid).append(s);
         }
      )
      if (w==1) {
         detail_show(atid);
      } else {
         alert("brak danych");
      }
   } else {
      alert(json.status+' - '+atid);
   }
}
function detail_hide(atid) {
"""%ddict
      for atable in axmldata.Parser.querysql.TablesList:
         atext=atext+"""
   if (atid=="%s") {
      $("#detail_%s").empty();
      $("#detail_%s").hide();
"""%(atable.NameAlias,atable.NameAlias,atable.NameAlias,)
         for btable in atable.SubTables:
            atext=atext+"""
      detail_hide("%s");
"""%(btable.NameAlias,)
         atext=atext+"""
   }
"""
      atext=atext+"""
}
function detail_show(atid) {
"""%ddict
      for atable in axmldata.Parser.querysql.TablesList:
         atext=atext+"""
   if (atid=="%s") {
      $("#detail_%s").show();
   }
"""%(atable.NameAlias,atable.NameAlias,)
      atext=atext+"""
}
function detail_%(XMLDataID)d(atid,aid) {
   detail_hide(atid);
   if (aid=="") {
      return
   }
   var l=aid.toString().split("_");
   var arow=l[0];
   var aoid=l[1];
   $.getJSON("xmldata_%(XMLDataID)d.asp?mode=d&soid="+aoid+"&tid="+atid+"&rv="+Math.random(),function(json){
      detail_%(XMLDataID)d_load(json,atid);
      }
   );
}
$(grid_load_%(XMLDataID)d);
</script>
<br>
"""%ddict
      for atable in axmldata.Parser.querysql.TablesList:
         atext=atext+"""
<div class=%s style="display:none;" id="detail_%s"></div>
"""%(ddict['widokrekordu_main'],atable.NameAlias,)
      Response.write(atext)
      rs.MoveNext()
   rs=aadoutil.CloseRS(rs)
aadoutil.Close()
%>
