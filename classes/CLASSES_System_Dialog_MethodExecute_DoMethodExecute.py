# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
import string
import sys
import time

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   if OID<0:
      adialog=InputElementDialog('Wybierz klasę',0,0)
      if not adialog.Show():
         return
      bclass=aICORDBEngine.Classes[adialog.ClassPath]
      if bclass is None:
         return
   else:
      bclass=aICORDBEngine.Classes[OID]
   aoid=aclass.FirstObject()
   if aoid<0:
      aoid=aclass.AddObject()
   aclass.ExecuteForAllObjects[aoid]='0'
   aclass.PFieldName[aoid]=''
   aclass.POID[aoid]='-1'
   aclass.PUID[aoid]=''
   aclass.PValue[aoid]=''
   aclass.RedirectStdOut[aoid]='0'
   aclass.QueuedExecution[aoid]='0'
   aclass.DoEventsBetweenCalls[aoid]='1'
   if not aclass.EditObject(aoid):
      return
   pfieldname=aclass.PFieldName[aoid]
   poid=aclass.POID.ValuesAsInt(aoid)
   pvalue=aclass.PValue[aoid]
   puid=UID
   bdoevents=aclass.DoEventsBetweenCalls.ValuesAsInt(aoid)>0
   bqueued=aclass.QueuedExecution.ValuesAsInt(aoid)>0
   urefs=aclass.PUID.GetRefList(aoid)
   if urefs:
      puid=urefs.OID

   if aclass.DoClearStdOutBeforeExecute.ValuesAsInt(aoid)>0:
      ClearStdOut()

   redirectstdout=aclass.RedirectStdOut.ValuesAsInt(aoid)>0
   if redirectstdout:
      stdoutlocation=FilePathAsSystemPath(aclass.StdOutLocation[aoid])
      if aclass.StdOutAppendToFile.ValuesAsInt(aoid)>0:
         amode='a+'
      else:
         amode='w'
      fout=open(stdoutlocation,amode)
      oldstdout=sys.stdout
      sys.stdout=fout
   try:
      bmethod=bclass.MethodsByName(FieldName)
      lastUID=UID
      UID=puid
      try:
         start=time.time()
         if aclass.ExecuteForAllObjects.ValuesAsInt(aoid)>0:
            coid=bclass.FirstObject()
            while coid>=0:
               if bdoevents:
                  DoEvents()
               try:
                  bmethod.Execute(pfieldname,coid,pvalue,aqueued=bqueued)
               except:
                  print 'BANG!'
                  import traceback
                  traceback.print_exc()
                  break
               coid=bclass.NextObject(coid)
         else:
            bmethod.Execute(pfieldname,poid,pvalue,aqueued=bqueued)
         finish=time.time()
         if aclass.CheckExecutionTime.ValuesAsInt(aoid)>0:
            print 'czas wykonania metody:',finish-start
      finally:
         UID=lastUID
   finally:
      if redirectstdout:
         sys.stdout=oldstdout
   if aclass.ShowMessageAfterFinish.ValuesAsInt(aoid)>0:
      MessageDialog('Koniec wykonywania metody '+bmethod.Name,abuttons=mbOK)
   return

