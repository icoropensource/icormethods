# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_DBBase_Query_MultiDimension_Main_ICORMultiDimensionQuery import GenerateMDQuery,mdqt_Excel
from CLASSES_Library_ICORBase_Interface_ICORUtil import tdatetime,tdatetime2fmtstr
import traceback
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   basename=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath)+'RS_428_36_mdqueryExcel_'
   flog=open('d:/icor/log_query.txt','a+')
   flog.write('\n*** Początek generowania wszystkich zestawień %s\n'%(tdatetime2fmtstr(tdatetime()),))
   start=time.time()
   try:
      if OID<0:
         aoid=574
      else:
         aoid=OID
      fname=basename+str(aoid)+'.html'
      try:
         file=open(fname,'w')
         try:
            GenerateMDQuery(file,aoid,atype=mdqt_Excel,logfile=flog)
         finally:
            file.close()
      except:
         s='### błąd podczas generowania zestawienia: '+fname
         print s
         flog.write(s+'\n')
         traceback.print_exc(file=flog)
   finally:
      finish=time.time()
      flog.write('*** koniec generowania wszystkich zestawień, czas: %s\n'%(str(finish-start),))
      flog.close()
   return



