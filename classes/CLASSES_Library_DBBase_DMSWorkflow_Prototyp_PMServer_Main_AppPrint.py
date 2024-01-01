# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import CLASSES_Library_NetBase_Utils_XMLUtil as XMLUtil
import CLASSES_Library_ICORBase_External_MLog as MLog
import CLASSES_Library_NetBase_WWW_HTML_Util_ConversionsPL as ConversionsPL
import CLASSES_Library_DBBase_DMSWorkflow_Prototyp_PMServer_Main_XMLParserDrukowania as icorxmlpmparser
import os
import re
import sys
import string
import cStringIO
import sha
import win32print
import win32ui
import optparse

import types, pprint
import win32api, win32con

from spmprint import pmwydruki
from spmprint import pmwydrukradix
from spmprint import pmwydrukiconst
import appplatform.startutil as startutil
#import icorpclconst

#from dane import d1,d2


__VERSION__='1.0.1'


"""
Printer:  HP LaserJet 2200 Series PCL 6x
   HORZRES: 4760
   HORZSIZE:   201
   LOGPIXELSX: 600
   LOGPIXELSY: 600
   PHYSICALHEIGHT:   7014
   PHYSICALOFFSETX:  100
   PHYSICALOFFSETY:  100
   PHYSICALWIDTH: 4960
   VERTRES: 6814
   VERTSIZE:   288
   pageSize:   {0: [4960, 7014], 1: [8.2666666666666675, 11.69], 2: [209.97333333333333, 296.92599999999999]}
   printableArea: {0: [4760, 6814], 1: [7.9333333333333336, 11.356666666666667], 2: [201.50666666666666, 288.45933333333335]}
   printerMargins:   {0: [100, 100, 100, 100], 1: [0.16666666666666666, 0.16666666666666666, 0.16666666666666666, 0.16666666666666666], 2: [4.2333333333333334, 4.2333333333333334, 4.2333333333333334, 4.2333333333333334]}
   res:  {0: [1, 1], 1: [600, 600], 2: [23.622047244094489, 23.622047244094489]}
"""

dformcodes={
   'um-czysty-1':'<Esc>&l1H', #gorny dla HP2200 i HP2430
#   'um-przelew-1':'<Esc>&l5H', #dolny dla HP2200 i HP2430
   'um-przelew-1':'<Esc>&l4H', #trzeci w ricoh aficio 1045
   'um-przelew-4':'<Esc>&l4H', #trzeci w ricoh aficio 1045
   'um-przelew-2':'<Esc>&l4H', #trzeci w ricoh aficio 1045
#   'um-przelew-3':'<Esc>&l5H', #dolny dla HP2200 i HP2430
   'um-lista-1':'<Esc>&l1H', #gorny dla HP2200 i HP2430
}

def ExitWithError(avalue):
   print avalue
   sys.exit(2)

def PrintDefaultPrinter():
   printer_name=win32print.GetDefaultPrinter()
   print 'Default printer:',printer_name
   return printer_name

def ChangeDefaultPrinter(aprinter):
   try:
      win32print.SetDefaultPrinter(aprinter)
      return 1
   except:
      print '  Specified printer %s not available'%aprinter
   return 0


# lists and dictionaries of constants
ptypelist=[
   (win32print.PRINTER_ENUM_SHARED,'shared'),
   (win32print.PRINTER_ENUM_LOCAL,'local'),
   (win32print.PRINTER_ENUM_CONNECTIONS,'network')
]
cmds={'Pause':win32print.JOB_CONTROL_PAUSE,'cancel':win32print.JOB_CONTROL_CANCEL,'resume':win32print.JOB_CONTROL_RESUME,'prior_low':win32print.MIN_PRIORITY,'prior_high':win32print.MAX_PRIORITY,'prior_normal':win32print.DEF_PRIORITY}
status_codes={'deleting':win32print.JOB_STATUS_DELETING,'error':win32print.JOB_STATUS_ERROR,'offline':win32print.JOB_STATUS_OFFLINE,'paper out':win32print.JOB_STATUS_PAPEROUT,'paused':win32print.JOB_STATUS_PAUSED,'printed':win32print.JOB_STATUS_PRINTED,'printing':win32print.JOB_STATUS_PRINTING,'spooling':win32print.JOB_STATUS_SPOOLING}

def GetPrinterList():
   pList=[]
   defPName=win32print.GetDefaultPrinter()
   for pt in ptypelist:
      try:
         for (Flags,pDescription,pName,pComment) in list(win32print.EnumPrinters(pt[0])):
            tmpdic ={}
            tmpdic['PrinterType']=pt[1]
            tmpdic['Flags']=Flags
            tmpdic['Description']=pDescription
            if pName==defPName:
               tmpdic['DefaultPrinter']=1
            else:
               tmpdic['DefaultPrinter']=0
            tmpdic['Name']=pName
            tmpdic['Comment']=pComment
            pList.append(tmpdic)
      except:
         pass
   return pList

def GetJobList(printer):
   phandle=win32print.OpenPrinter(printer)
   try:
   #now get all the print jobs (start at job 0 and -1 for all jobs)
      jlist=win32print.EnumJobs(phandle,0,-1,1)
   finally:
      win32print.ClosePrinter(phandle)
   return jlist # this lists all jobs on all printers

def GetJobInfo(printer,jobID):
   phandle=win32print.OpenPrinter(printer)
   try:
      ilist=win32print.GetJob(phandle,jobID,1)
   finally:
      win32print.ClosePrinter(phandle)
   return ilist #this lists all info available at level 1 for selected job.

def SetJobCmd(printer,jobID,JobInfo,RCmd):
   phandle = win32print.OpenPrinter(printer)
   try:
      win32print.SetJob(phandle,jobID,1,JobInfo,Cmds[RCmd])
   finally:
      win32print.ClosePrinter(phandle)

# test functions
#e = PMFuncs()
#while 1:
#   time.sleep(1)
#   e = PMFuncs()
#   for i in e.PrinterList():
#      try:
#         p = e.GetJobList(i['Name'])
#         for w in p:
#            print e.GetJobInfo(i['Name'],w['JobID'])
#      except:
#         pass

def GetTextAsPCL(avalue):
   if type(avalue)==type([]):
      avalue=string.join(avalue,'')
   avalue=string.replace(avalue,'\e',chr(27))
   avalue=string.replace(avalue,'<Esc>',chr(27))
   avalue=string.replace(avalue,chr(166),chr(173))
   avalue=ConversionsPL.Win2ISO(avalue)
   return avalue

def SendCommand(avalue):
   avalue=GetTextAsPCL(avalue)
   astartuppcl=GetTextAsPCL(pmwydrukiconst.STARTUP_PCL)
   printer_name=win32print.GetDefaultPrinter()
   print 'Default printer:',printer_name
   hPrinter=win32print.OpenPrinter(printer_name)
   try:
      hJob=win32print.StartDocPrinter(hPrinter,1,("ICOR Print 0",None,"RAW"))
      try:
         win32print.WritePrinter(hPrinter,astartuppcl)
         win32print.WritePrinter(hPrinter,avalue)
      finally:
         win32print.EndDocPrinter(hPrinter)
   finally:
      win32print.ClosePrinter(hPrinter)

def ProcessDump(options):
   PrintDefaultPrinter()   

def ProcessTest(options):
   wydruk=pmwydruki.Wydruk()
   for aformname,acode in dformcodes.items():
      print aformname
      dfields={
         'TrescPieczatki':'',
         'TrescDecyzji':aformname,
      }
      bformularz=pmwydrukradix.F_RADIX_Decyzja(dfields,acode=acode)
      wydruk.DodajFormularz(bformularz)
   wydruk.Rysuj()
   wydruk.Save('wydruk02.prn')
   wydruk.Print(aprinter=options.PRINTER)

def ProcessEnumPrinters(options):
   pList=GetPrinterList()
   for d in pList:
      print '=================================================================='
      print 'Name: "%s"'%d['Name']
      print 'Printer type: %s'%d['PrinterType']
#      print 'Flags:',d['Flags']
      if d['Description']:
         print 'Description:"%s"'%d['Description']
      if d['DefaultPrinter']:
         print 'Default printer: YES'
      if d['Comment']:
         print 'Comment:"%s"'%d['Comment']

def ProcessStat(options):
   if options.FILE is None:
      ExitWithError('opcja -f <plik_we> jest wymagana')
   if not os.path.exists(options.FILE):
      ExitWithError('plik wejsciowy nie istnieje')
   d={
      'LISTA ':0,
      'PAKIET ':0,
      'PRZESYLKA ':0,
   }
   fin=open(options.FILE,'r')
   l=fin.readline()
   while l:
      for akey in d.keys():
         if string.find(l,'<'+akey)>=0:
            d[akey]=1+d[akey]
      l=fin.readline()
   print 'plik:',options.FILE
   for akey in d.keys():
      print akey,'-',d[akey]
   return d['LISTA '],d['PAKIET '],d['PRZESYLKA ']

def ProcessXMLSplit(options):
   if options.COUNTER<1 or options.COUNTER>1000:
      ExitWithError('opcja -c <n> jest wymagana 1<n<1000')
   amaxlista,amaxpakiet,amaxprzesylka=ProcessStat(options)
   if amaxlista:
      amaxsplit=1+amaxpakiet/options.COUNTER
   else:
      amaxsplit=(1+amaxpakiet)/options.COUNTER
   print 'Podzial na',options.COUNTER,'plikow, kazdy po ok.',amaxsplit,'przesylek'
   ret=[]
   bfpath,bfname=os.path.split(options.FILE)
   bfname,bfext=os.path.splitext(bfname)
   if bfpath:
      bfpath=bfpath+'/'
   state=0
   acnt=0
   afilecnt=1
   aheader=''
   fout=None
   fin=open(options.FILE,'r')
   l=fin.readline()
   wsplit=0
   if amaxlista:
      asplittag='LISTA'
   else:
      asplittag='PAKIET'
   while l:
      if string.find(l,'<%s '%(asplittag,))>=0:
         state=1
      elif string.find(l,'</PAKIETY>')>=0:
         break
      if state==0:
         aheader=aheader+l
      elif state==1:
         if string.find(l,'<PAKIET ')>=0:
            acnt=acnt+1
            if acnt>amaxsplit:
               wsplit=1
         if string.find(l,'</%s'%(asplittag,))>=0 and wsplit and not fout is None:
            print 'Podzial - plik nr:',afilecnt,'ilosc pakietow:',acnt
            fout.write(l)
            fout.write('   </PAKIETY>\n</PMWYDRUKI>\n')
            fout.close()
            afilecnt=afilecnt+1
            fout=None
            wsplit=0
            acnt=0
         else:
            if fout is None:
               cfname=bfpath+'out/'+bfname+'_%08d'%afilecnt+bfext
               ret.append(cfname)
               fout=open(cfname,'w')
               fout.write(aheader)
            fout.write(l)
      l=fin.readline()
   if not fout is None:
      print 'Podzial - plik nr:',afilecnt,'ilosc pakietow:',acnt
      fout.write('   </PAKIETY>\n</PMWYDRUKI>\n')
      fout.close()
   return ret

def ProcessXMLPMPrint(options):
   if options.FILE is None:
      ExitWithError('opcja -f <plik_we> jest wymagana')
   if not os.path.exists(options.FILE):
      ExitWithError('plik wejsciowy nie istnieje')
   
   aodbiorca=startutil.appconfig.IParams['pm_adres2']
#   dformcodes={}
#'<Esc>&l5H', #gorny dla HP2200 i HP2430
#'<Esc>&l1H', #dolny dla HP2200 i HP2430
   aparser=icorxmlpmparser.ICORPMPrintPrzesylkiParser()
   aparser.ParseFile(options.FILE,aodbiorca=aodbiorca,dformcodes=dformcodes,alastidtransakcji=options.IDTRANSAKCJI,akorektax=options.KOREKTAX,akorektay=options.KOREKTAY)
   awydrukfname=options.PRNFILE
   if awydrukfname=='':
      awydrukfname='WYDRUK_'+ICORUtil.tdate2fmtstr(ICORUtil.tdatetime(),delimiter='',longfmt=1)+ICORUtil.ttime2fmtstr(ICORUtil.tdatetime(),longfmt=1,delimiter='')+'.prn'
   if awydrukfname:
      aparser.Save(awydrukfname)
   if not options.WRITEONLY:
      aejectpages=0
      if not len(dformcodes.keys()):
         aejectpages=1
      aparser.Print(aprinter=options.PRINTER,aejectpages=aejectpages)

def Main():
   parser=optparse.OptionParser(version="%prog "+__VERSION__,description="drukuje i zarzadza wydrukami z ICOR SPM")

   parser.set_defaults(VERBOSE=0)
   parser.set_defaults(PRINTER='')
   parser.set_defaults(PRNFILE='')
   parser.set_defaults(COUNTER=1)
   parser.set_defaults(WRITEONLY=0)
   parser.set_defaults(IDTRANSAKCJI='')
   parser.set_defaults(KOREKTAX=0)
   parser.set_defaults(KOREKTAY=0)
#   parser.set_defaults(BYTES_PER_SECTOR=512)
#   parser.set_defaults(SECTORS_PER_TRACK=63)
   parser.add_option("-m","--mode",action="store",type="choice",choices=['PRINT','SPLIT','DUMP','TEST','ENUMPRINTERS','STAT',],dest="MODE",help="przyjmuje wartosci: PRINT, SPLIT, DUMP, TEST, ENUMPRINTERS, STAT")
   parser.add_option("-f","--file",action="store",type="string",dest="FILE",help="plik wejsciowy")
   parser.add_option("-p","--printer",action="store",type="string",dest="PRINTER",help="wyjsciowa drukarka")
   parser.add_option("-j","--job",action="store",type="string",dest="JOB",help="nazwa zadania w kolejce drukarki")
   parser.add_option("-c","--counter",action="store",type="int",dest="COUNTER",help="licznik w przypadku trybu SPLIT oznacza ilosc wyjsciowych plikow")
   parser.add_option("-w","--writeonly",action="store_const",const=1,dest="WRITEONLY",help="tylko zapis wydruku, bez fizycznego drukowania")
   parser.add_option("-i","--id",action="store",type="string",dest="IDTRANSAKCJI",help="IDTransakcji ostatniego poprawnego pakietu")
   parser.add_option("-r","--prnfile",action="store",type="string",dest="PRNFILE",help="nazwa pliku PRN z danymi wynikowymi")
   parser.add_option("-x","--offsetx",action="store",type="int",dest="KOREKTAX",help="korekta X w mm")
   parser.add_option("-y","--offsety",action="store",type="int",dest="KOREKTAY",help="korekta Y w mm")

#   parser.add_option("-p","--partition",action="store",type="choice",choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],dest="PARTITION",help="source partition (A-Z)")
#   parser.add_option("-d","--diskid",action="store",type="int",dest="DISK_ID",help="source disk id (0,1,2...)")
#   parser.add_option("-s","--startingaddress",action="store",type="int",dest="STARTING_ADDRESS",help="starting address (relative to start of disk) of image dump")
#   parser.add_option("-e","--endingaddress",action="store",type="int",dest="ENDING_ADDRESS",help="ending address (relative to start of disk) of image dump")
#   parser.add_option("--startingoffset",action="store",type="int",dest="STARTING_OFFSET",help="starting offset (relative to start of partition) of image dump")
#   parser.add_option("--endingoffset",action="store",type="int",dest="ENDING_OFFSET",help="ending offset (relative to start of partition) of image dump")
   parser.add_option("-v","--verbose",action="store_const",const=1,dest="VERBOSE",help="wyswietlaj wszystkie komunikaty")
   parser.add_option("-q","--quiet",action="store_const",const=0,dest="VERBOSE",help="nie wyswietlaj zadnych komunikatow")
#   parser.add_option("-t","--notrackbefore",action="store_const",const=1,dest="EXCLUDE_TRACK_BEFORE",help="don't add to image one track (with partition info) before starting address (offset)")
#   parser.add_option("-b","--bytespersector",action="store",type="int",dest="BYTES_PER_SECTOR",help="bytes per sector (for CHECKIMAGE mode) - defaults %default")
#   parser.add_option("-r","--sectorspertrack",action="store",type="int",dest="SECTORS_PER_TRACK",help="sectors per track (for CHECKIMAGE mode) - defaults %default")

   options,args=parser.parse_args()

   if options.MODE is None:
      parser.error("opcja -m jest wymagana!")

   if options.MODE=='PRINT':
      ProcessXMLPMPrint(options)
   if options.MODE=='SPLIT':
      ProcessXMLSplit(options)
   if options.MODE=='DUMP':
      ProcessDump(options)
   if options.MODE=='TEST':
      ProcessTest(options)
   if options.MODE=='ENUMPRINTERS':
      ProcessEnumPrinters(options)
   if options.MODE=='STAT':
      ProcessStat(options)




