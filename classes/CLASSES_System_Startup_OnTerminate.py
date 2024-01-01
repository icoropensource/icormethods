# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   import sys
   try:
      import ICORDelphi
      icorapi=ICORDelphi
      ICOR_EXECUTE_EXTERNAL=0
   except:
      import icorapi
      ICOR_EXECUTE_EXTERNAL=1
   import time
   fname=icorapi.GetVariable(0,'_ICOR_BASE_DIR')+'/log/startup_terminate_log.txt'
   file=open(fname,'a+')
   try:
      file.write('%s terminate: %s\n'%(str(time.localtime(time.time())),Value,))
   finally:
      file.close()
   return

