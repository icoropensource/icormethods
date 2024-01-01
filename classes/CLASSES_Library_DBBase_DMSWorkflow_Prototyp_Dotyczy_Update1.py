# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORSecurity as ICORSecurity

def Update1(aobj):
   aclear=1
   dobj=aobj.TabeleZrodlowe
   asourcehtml1="""
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
   asourcehtml2="""
   rs("_DateTime")=getStrAsDateTime(FormFields("InformacjaDataModyfikacji"),"","",0)
"""
   while dobj:
      print dobj.Nazwa
      s=dobj.ASPSourceShowFields
      if s!=asourcehtml1 and s!='':
         print 'Tabela %d ma juz zdefiniowana metode ASPSourceShowFields - zapamietaj i zmodyfikuj recznie'%dobj.OID
      else:
         if aclear: 
            print 'ASPSourceShowFields w tabeli %d was cleaned'%dobj.OID
            dobj.ASPSourceShowFields=''
         else:
            print 'ASPSourceShowFields w tabeli %d was updated'%dobj.OID
            dobj.ASPSourceShowFields=asourcehtml1
      s=dobj.ASPSourceSubmit
      if s!=asourcehtml2 and s!='':
         print 'Tabela %d ma juz zdefiniowana metode ASPSourceSubmit - zapamietaj i zmodyfikuj recznie'%dobj.OID
      else:
         if aclear:
            print 'ASPSourceSubmit w tabeli %d was cleaned'%dobj.OID
            dobj.ASPSourceSubmit=''
         else:
            print 'ASPSourceSubmit w tabeli %d was updated'%dobj.OID
            dobj.ASPSourceSubmit=asourcehtml2
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

def UpdateGroupItemAccL(tobj,afname,acclist,adelete=0):
   arefs=ICORSecurity.GetStringAsAccessLevelRefs(acclist)
   while tobj:
      afield=tobj.Class.FieldsByName(afname)
      if adelete:
         afield.DeleteRefs(tobj.OID,arefs.refs)
      else:
         afield.AddRefs(tobj.OID,arefs.refs,ainsertifnotexists=1)
      tobj.Next()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   print 'CID:',CID
   UID=4150
   aclass=aICORDBEngine.Classes[CID]
   aICORDBEngine.Classes.CacheClear()
   return 1
   
   aoid=aclass.Nazwa.Identifiers('???')
   aobj=aclass[aoid]
   print aobj
   #Update1(aobj)

#   acclist=['Administrator Projekt�w','BIP Admin','BIP Operator']
   acclist=['BIP Operator']
   UpdateGroupItemAccL(aobj.TabeleZrodlowe,'AccessLevelView',acclist,adelete=1)
#   Update2(aobj,'Informacja data wytworzenia','Informacja opis czynno�ci')
   return       



