# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      return
   boid=aclass.AddObject(arefobject=OID)
   for afname in ['Adresat','Cel','DataModyfikacji','Dotyczy','IloscDokumentowNaOkres','InneCzynnosci','Nazwa','OsobyOdpowiedzialne','PrzewidywanaIloscDokumentow','StatusOpisuDokumentu','Symbol','Zdarzenia','ZrodloDanych']:
      afield=aclass.FieldsByName(afname)
      afield[boid]=afield[OID]
   aobj=aclass[OID]

   sref=''
   pobj=aobj.Pola
   while pobj:
      poid=pobj.AddObject()
      pobj.Dokument=aobj.AsString()
      for afname in ['Nazwa','Opis','RodzajPola','SGIsAliased','SGIsSearch','SGTabIndex','WartosciSlownika','WarunkiPoprawnosci','ZrodloDanych']:
         afield=pobj.Class.FieldsByName(afname)
         afield[poid]=afield[pobj.OID]
      sref=sref+pobj.AsRefString()
      pobj.Next()
   aobj.Class.Pola[boid]=sref

   sref=''
   pobj=aobj.Procedury
   while pobj:
      poid=pobj.AddObject()
      for afname in ['JednostkaOrganizacyjna','Symbol']:
         afield=pobj.Class.FieldsByName(afname)
         afield[poid]=afield[pobj.OID]
      cref=''
      cobj=pobj.Czynnosci
      while cobj:
         coid=cobj.AddObject()
         for afname in ['Nazwa','SGIsFlashing']:
            afield=cobj.Class.FieldsByName(afname)
            afield[coid]=afield[cobj.OID]
         cref=cref+cobj.AsRefString()
         cobj.Next()
      pobj.Czynnosci=cref
      sref=sref+pobj.AsRefString()
      pobj.Next()
   aobj.Class.Procedury[boid]=sref
   return



