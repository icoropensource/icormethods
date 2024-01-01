# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import sys
#sys.ICOR_SERVER="makpc"
import icorpipe
import urllib

import CLASSES_Library_ICORBase_External_Broker_Communicator
brokercommunicator=CLASSES_Library_ICORBase_External_Broker_Communicator

from CLASSES_Library_ICORBase_Interface_ICORInterface import FilePathAsSystemPath
from CLASSES_Library_ICORBase_Interface_ICORSecurity import GetUIDByUserPassword
from CLASSES_Library_ICORBase_External_MLog import Log
from CLASSES_Library_ICORBase_Interface_ICORUtil import tdatetime,tdatetime2fmtstr

LOG_FILE=FilePathAsSystemPath(r'%ICOR%\\log\\isapiauth.log')
def demo(c):
   env = c.Input()
   user = c.Input()
   password = c.Input()
   env=env.split('\0')
   dct = {}
   for i in env:
      i=i.strip()
      if i:
         k,v=i.split('=',1)
         v=v.strip()
         if v:
            dct[k]=v
   where= dct.get('PATH_INFO','/')
   what = dct.get('QUERY_STRING','/')
   rc=1
   uid=-1
   if where=='/dav.icor':
      uid = GetUIDByUserPassword(user,password,awwwuser=1)
      rc=2
      if uid>=0:
         rc=0
   s=tdatetime2fmtstr(tdatetime(),longfmt=1)
   Log('%s\t%d\t%d\t%s\t%s\t%s\t%s\n' %(s,rc,uid,user,dct['REQUEST_METHOD'],where,what),fname=LOG_FILE)
   #0==OK
   #1==Next Notification
   #2==Deny
   c.Output(rc,1)

def main(pname):
   s=brokercommunicator.CommunicatorServer(pname)
   while 1:
      try:
         demo(s)
         brokercommunicator.SendCmd('DONE %s' %pname,withrecv=0)
      except:
#         import traceback; traceback.print_exc(); raw_input('!')
         s.Close()
         brokercommunicator.SendCmd('DONE %s' %pname,withrecv=0)
         sys.exit(1)

#main(sys.argv[1])




