# -*- coding: windows-1250 -*-
# saved: 2023/03/04 14:32:41

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from icorlib.projekt.mcrmwwwmenu import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def Update1(aobj):
   dobj=aobj.TabeleZrodlowe
   while dobj:
      s=dobj.ASPSourceShowFields
      s=''
      if s:
         print 'Tabela %d ma juz zdefiniowana metode ASPSourceShowFields - zapamietaj i zmodyfikuj recznie'%dobj.OID
      else:
         dobj.ASPSourceShowFields="""
   if aoid<>"-1" then
      Response.Write "<TR VALIGN=top class=objectseditrow>"
      Response.Write "<td width='160px' class=objectseditdatafieldnameodd style='BACKGROUND-COLOR: red;'>Informacja data modyfikaji (pole systemowe!):</td><td class=objectseditdatafieldvalueodd style='BACKGROUND-COLOR: red;'>"
      if Year(rs.Fields("_datetime").Value)=1900 then
         sdv1=""
      else
         sdv1="" & Year(now) & "/" & Month(now) & "/" & Day(now)
      end if
      Response.Write "&nbsp;rrrr/mm/dd:<input type=text id='InformacjaDataModyfikacji' name='InformacjaDataModyfikacji' size=10 maxlength=10 value='" & sdv1 & "' FILTER='[0-9/]' DATE='YYYY/M/D' >"
      Response.Write "<IMG alt='wyb�r daty' id=InformacjaDataModyfikacji_ds src='/icormanager/images/icon_calendar2.png' style='cursor:pointer;' onclick='showPopupDT(InformacjaDataModyfikacji,InformacjaDataModyfikacji_ds);'>"
      Response.Write "</td></tr>"
   else
      Response.Write "<TR VALIGN=top class=objectseditrow>"
      Response.Write "<td width='160px' class=objectseditdatafieldnameodd style='BACKGROUND-COLOR: red;'>Informacja data modyfikaji (pole systemowe!):</td><td class=objectseditdatafieldvalueodd style='BACKGROUND-COLOR: red;'>"
      Response.Write "&nbsp;rrrr/mm/dd:<input type=text id='InformacjaDataModyfikacji' name='InformacjaDataModyfikacji' size=10 maxlength=10 value='" & year(now) & "/" & month(now) & "/" & day(now) & "' FILTER='[0-9/]' DATE='YYYY/M/D' >"
      Response.Write "<IMG alt='wyb�r daty' id=InformacjaDataModyfikacji_ds src='/icormanager/images/icon_calendar2.png' style='cursor:pointer;' onclick='showPopupDT(InformacjaDataModyfikacji,InformacjaDataModyfikacji_ds);'>"
      Response.Write "</td></tr>"
   end if      
"""
      s=dobj.ASPSourceSubmit
      s=''
      if s:
         print 'Tabela %d ma juz zdefiniowana metode ASPSourceSubmit - zapamietaj i zmodyfikuj recznie'%dobj.OID
      else:
         dobj.ASPSourceSubmit="""
   rs("_DateTime")=getStrAsDateTime(FormFields("InformacjaDataModyfikacji"),"","",0)
"""
      dobj.Next()

def Update2(sobj,beforefield,newfield):
   aobj=sobj.TabeleZrodlowe
   while aobj:
      atabid=0
      pobj=aobj.Pola
      pclass=pobj.Class
      w=1
      drefs=[]
      while pobj:
         if pobj.Nazwa==beforefield:
            atabid=5+pobj.Class.SGTabIndex.ValuesAsInt(pobj.OID)
         if pobj.Nazwa==newfield:
            drefs.append([pobj.OID,pobj.CID])
         pobj.Next()
      aobj.Class.Pola.DeleteRefs(aobj.OID,drefs,aobjectdelete=1)
      if not atabid:
         w=0
         print 'babol1',aobj
      if w:
         poid=pclass.AddObject()
         print 'ni:',poid
         pclass.Nazwa[poid]=newfield
         pclass.TypPolaDotyczy[poid]=[1,pclass.TypPolaDotyczy.ClassOfType.CID]
         pclass.SGTabIndex[poid]=str(atabid)
         pclass.SGIsAliased[poid]='1'
         pclass.SGIsIndexed[poid]='1'
         pclass.SGIsSearch[poid]='1'
         pclass.SGIsDictViewHidden[poid]='1'
         pclass.SGIsObligatory[poid]='1'
         aobj.Class.Pola.AddRefs(aobj.OID,[poid,pclass.CID],asortedreffield=pclass.SGTabIndex)
      aobj.Next()

def Update3(aobj):
   bparser=ICORBIPTablesXMLParser()
   bparser.StoreXMLSource(aobj)

def Update4(sobj,afields):
   aobj=sobj.TabeleZrodlowe
   while aobj:
      arefs=aobj.Class.Pola.GetRefList(aobj.OID)
      pclass=aobj.Class.Pola.ClassOfType
      for afname in afields:
         apos,afind=arefs.FindRefByValue('Nazwa',afname)
         if afind:
            poid,pcid=arefs[apos]
            print aobj.Nazwa,poid,pclass.Nazwa[poid]
            pclass.SGIsObligatory[poid]='1'
      aobj.Next()

def UpdateGroupItemAccL(tobj,afname,acclist,adelete=0):
   arefs=ICORSecurity.GetStringAsAccessLevelRefs(acclist)
   while tobj:
      afield=tobj.Class.FieldsByName(afname)
      if adelete:
         afield.DeleteRefs(tobj.OID,arefs.refs)
      else:
         afield.AddRefs(tobj.OID,arefs.refs,ainsertifnotexists=1)
      tobj.Next()

def ProcessChapter(robj,securname):
   print 'Nazwa:',robj.Naglowek
   acclist=['UM - Platany - Admin','UM - Platany - User']
   UpdateGroupItemAccL(robj.PodRozdzialy,securname,acclist,adelete=0)
   sobj=robj.PodRozdzialy
   while sobj:
      ProcessChapter(sobj,securname)
      sobj.Next()

def ProcessDupChapters(dd,drozdzialy,robj,pobj,sref):
   while robj:
      if 1 or pobj.CID==robj.CID:
         l=drozdzialy.get(robj.OID,[])
         if not [pobj.CID,pobj.OID] in l:
            l.append([pobj.CID,pobj.OID,sref])
         drozdzialy[robj.OID]=l
      if dd.has_key(robj.OID):
#         print 'DUP:',pobj.CID,pobj.OID,'->',robj.OID
         robj.Next()
         continue
      dd[robj.OID]=1
      ProcessDupChapters(dd,drozdzialy,robj.PodRozdzialy,robj,'rr')
      robj.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   UID=4150

   aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_XMLRozdzialy_Struktura']
   dw={}
   aobj=aclass.GetFirstObject()
   while aobj:
      tobj=aobj.PageTemplate
      while tobj:
         l=dw.get(tobj.OID,[])
         l.append([aobj.OID,aobj.Nazwa,tobj.OID,tobj.Template])
         dw[tobj.OID]=l
         tobj.Next()
      aobj.Next()
   for k,v in dw.items():
      if len(v)>1:
         for l in v:
            print l
         print
   return

   if 0:
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
      sclass=aclass.WWWMenuStruct.ClassOfType
      rclass=sclass.Rozdzialy.ClassOfType
      gclass=sclass.GrupyRozdzialow.ClassOfType
#[86003, [[1879, 86000, 'ss'], [1937, 86001, 'gg'], [1879, 86004, 'uu']], 'Mapa serwisu']
      sobj=sclass[86004]
      uobj=sobj.RozdzialyUsuniete
      while uobj:
         print uobj.OID
         uobj.Next()

   if 1:
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_DMSWorkflow_Prototyp_Projekt']
      sclass=aclass.WWWMenuStruct.ClassOfType
      rclass=sclass.Rozdzialy.ClassOfType
      gclass=sclass.GrupyRozdzialow.ClassOfType
      aoid=aclass.Nazwa.Identifiers('PARP')
      lgcids=[sclass.CID,gclass.CID]
      if aoid<0:
         return
      aobj=aclass[aoid]
      wobj=aobj.WWWMenuStruct
      drozdzialy={}
      dd={}
      while wobj:
#         print wobj.Nazwa
         ProcessDupChapters(dd,drozdzialy,wobj.Rozdzialy,wobj,'ss')
         uobj=wobj.RozdzialyUsuniete
         while uobj:
            ProcessDupChapters(dd,drozdzialy,uobj.Rozdzial,uobj,'uu')
            uobj.Next()
         gobj=wobj.GrupyRozdzialow
         while gobj:
            ProcessDupChapters(dd,drozdzialy,gobj.Rozdzialy,gobj,'gg')
            gobj.Next()
         wobj.Next()
      lroids=drozdzialy.keys()
      lroids.sort()
      for aroid in lroids:
         lp=drozdzialy[aroid]
         if len(lp)>1:
            # 1878 rozdzial
            # 1879 struktura
            # 1935 rozdzialy usuniete
            # 1937 grupy
            if (len(lp)==2) and (lp[0][0] in lgcids) and (lp[1][0] in lgcids):
               pass
            else:
               print [aroid,lp,rclass.Naglowek[aroid]]
               if 1:
                  #reguly czyszczace
                  if (len(lp)==2):
                     aoid1=lp[0][1]
                     aoid2=lp[1][1]
                     if (lp[0][2]=='rr') and (lp[1][2]=='uu'):
                        print '  dousuniecie'
                        rclass.PodRozdzialy.DeleteRefs(aoid1,[aroid,rclass.CID])
                     if (lp[0][2]=='rr') and (lp[1][2]=='gg'):
                        print '  duplikat w grupie'
                        gclass.Rozdzialy.DeleteRefs(aoid2,[aroid,rclass.CID])

#   securname='AccessLevelView'
   if 0:
      robj=aobj.Rozdzialy
      acclist=['UM - Osiedla - Admin']
      UpdateGroupItemAccL(aobj.Rozdzialy,securname,acclist,adelete=0)
      while robj:
         ProcessChapter(robj,securname)
         robj.Next()
   return




