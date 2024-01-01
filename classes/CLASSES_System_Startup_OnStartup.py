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
   import os
   import string
   fname=icorapi.GetVariable(0,'_ICOR_BASE_DIR')+'/log/startup_terminate_log.txt'
   file=open(fname,'a+')
   try:
      file.write('%s startup: %s\n'%(str(time.localtime(time.time())),Value,))
      if Value=='ApplicationX':
         try:
            DEFAULT_PROCESS_DAEMON='"'+icorapi.GetVariable(0,'_DEFAULT_PYTHON_TOP_DIR')+'/External/default/redaemon.py'+'"' #
#            DEFAULT_PROCESS_DAEMON=icorapi.GetVariable(0,'_DEFAULT_PYTHON_TOP_DIR')+'/External/default/redaemon.py' #
            DEFAULT_PROCESS_EXECUTOR=icorapi.GetVariable(0,'_DEFAULT_PROCESS_EXECUTOR')
            DEFAULT_PROCESS_DAEMON=string.replace(DEFAULT_PROCESS_DAEMON,'/','\\')
            DEFAULT_PROCESS_EXECUTOR=string.replace(DEFAULT_PROCESS_EXECUTOR,'/','\\')
            os.spawnv(os.P_NOWAIT,DEFAULT_PROCESS_EXECUTOR,['"'+DEFAULT_PROCESS_EXECUTOR+'"',DEFAULT_PROCESS_DAEMON]) #
         except:
            import traceback
            traceback.print_exc(None,file)
   finally:
      file.close()
   return

