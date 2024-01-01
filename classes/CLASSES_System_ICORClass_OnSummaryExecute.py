# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORSummary import ICORSummary,SummarySpace2HTML,GenerateAsHTML,GenerateAsHTML_TDC
from CLASSES_Library_ICORBase_Interface_ICORMDSpace import ICORMDSpace

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   if OID<0:
      return
   ret=MessageDialog('Naciśnięcie "Tak", spowoduje pokazanie zestawienia w postaci HTML,\nnaciśnięcie "Nie" spowoduje przeniesienie zestawienia do MS Excel. Pamiętaj o uprzednim uruchomieniu MS Excel.',mtConfirmation,mbYesNoCancel)
   if ret==mrCancel:
      return
   excel=0
   html=0
   if ret==mrYes:
      html=1
   if ret==mrNo:
      excel=1
   fname=FilePathAsSystemPath('%ICOR%\\html\\output\\summary.html')
   aclass=aICORDBEngine.Classes[CID]
   aspace=ICORMDSpace()
   asummary=ICORSummary(OID,aspace,aIsInteractive=0)
   InfoStatus('Przygotowanie zestawienia')
   cnt=asummary.ProcessAll()
   if cnt==0:
      MessageDialog('Brak danych spełniających zadane reguły!',mtWarning,mbOK)
      InfoStatus('')
      return
   if html:
      InfoStatus('Przenoszenie do HTML')
#      GenerateAsHTML_TDC(asummary,aspace,fname,1,'c:/icor/html/output/')
      GenerateAsHTML(asummary,aspace,fname,1,FilePathAsSystemPath('%ICOR%/html/output/'))
      ExecuteShellCommand(fname)
   if excel:
      InfoStatus('Przenoszenie do Excel\'a')
#      siterator=SummarySpace2Excel(aspace)
#      siterator.ShowProgress=1
#      siterator.ForEachNotEmptyRow()
#      siterator.excel.Show()
#      del siterator
   InfoStatus('')
   return

