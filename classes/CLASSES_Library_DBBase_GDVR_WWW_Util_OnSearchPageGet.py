# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import *
from CLASSES_Library_ICORBase_Interface_ICORObjectsViewer import *
from CLASSES_Library_NetBase_WWW_Server_DoSiteMap import DoSearchMenu
from CLASSES_Library_NetBase_Utils_MDSpaceUtil import *
import string
import re

def WriteFormBegin(file,amenu):
   file.write('<form METHOD="post" ACTION="icormain.asp?jobtype=reportsubmit&OID=%d&ReportOID=%d">\n'%(amenu.oid,amenu.Reports.OID))
   
def WriteFormEnd(file):
   file.write('<input TYPE="submit" VALUE="  Pokaż wyniki  " tabIndex=2>')

dm_l1 = [(10,'słowników w/g nazwy'),
   (20,'pozycji w/g kodu'),
   (30,'pozycji w/g nazwy'),
   (40,'pozycji w/g opisu i źródła danych'),
   (50,'pozycji w/g zakresu kont'),
   ]

def WriteReportModesSelect(file,ilist):
   file.write('znajdź ciąg znaków&nbsp;<INPUT type="text" id=searchvalue1 name=searchvalue1 value=""> wśród:&nbsp;<br><br>')
   scv=' CHECKED'
   for v,t in ilist:
      file.write('<INPUT TYPE=RADIO name=reportmodeselect1 id=reportmodeselect1 value=%d%s>%s<br>'%(v,scv,t))
      scv=''
#   file.write('<SELECT id=reportmodeselect1 name=reportmodeselect1>')
#   for v,t in ilist:
#      file.write('<OPTION value=%d>%s'%(v,t))
#   file.write('</SELECT>\n')

################################################################

# Ogolna Liczba Pozyskanych Czlonkow
def DoSearchPage(amenu,file):
   WriteFormBegin(file,amenu)
   WriteReportModesSelect(file,dm_l1)
   file.write('<BR><BR>\n')
   WriteFormEnd(file)

def SlownikCheck(aviewer,aclass,aoid,arow):
   if aviewer.ValueCheck.search(aclass.DictName[aoid]):
      return 1
   return 0
def Pozycje1Check(aviewer,aclass,aoid,arow):
   if aviewer.ValueCheck.search(aclass.ItemCode[aoid]):
      return 1
   return 0
def Pozycje2Check(aviewer,aclass,aoid,arow):
   if aviewer.ValueCheck.search(aclass.ItemName[aoid]):
      return 1
   return 0
def Pozycje3Check(aviewer,aclass,aoid,arow):
   if aviewer.ValueCheck.search(aclass.ItemSource[aoid]+' '+aclass.Description[aoid]):
      return 1
   return 0
def Pozycje4Check(aviewer,aclass,aoid,arow):
   arefs=aclass.AccountRange.GetRefList(aoid)
   s=''
   while arefs:
      s=s+arefs.AccountFrom[arefs.OID]+' '+arefs.AccountTo[arefs.OID]+' '+arefs.AccountMask[arefs.OID]+' '
      arefs.Next()
   if aviewer.ValueCheck.search(s):
      return 1
   return 0

def DoSearchPageSubmit(amenu,areport,file):
   if areport['reportmodeselect1']=='10':
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Main']
      ffunc=SlownikCheck
   elif areport['reportmodeselect1']=='20':
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Dictionary_Item']
      ffunc=Pozycje1Check
   elif areport['reportmodeselect1']=='30':
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Dictionary_Item']
      ffunc=Pozycje2Check
   elif areport['reportmodeselect1']=='40':
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Dictionary_Item']
      ffunc=Pozycje3Check
   elif areport['reportmodeselect1']=='50':
      aclass=aICORDBEngine.Classes['CLASSES_Library_DBBase_GDVR_Dictionary_Item']
      ffunc=Pozycje4Check
   else:
      return
   aspace=ICORMDSpace()
   aspace.Caption=aclass.WWWDescription
   cov=ICORClassObjectsViewer(aclass,aspace)
   try:
      s=areport['searchvalue1']
      cov.ValueCheck=re.compile(s,re.I)
   except re.error, msg:
      file.write('<h2>Błedny ciąg znaków do wyszukiwania</h2><br>')
      return
   cov.OnIsObjectValid=ffunc
   cov.Process()
   if cov.ObjectsCount==0:
      file.write('<h2>Nie znaleziono danych</h2><br>')
   else:
#     titerator=ICORClassObjects2HTML(cov.space,file,0,'')
      titerator=ICORClassObjects2XMLDSO(cov.space,file,0,'')
      titerator.ForEachNotEmptyRow()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return



