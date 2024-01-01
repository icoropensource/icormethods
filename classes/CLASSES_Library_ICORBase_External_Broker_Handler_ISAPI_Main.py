# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

result='''\
HTTP/1.1 200 OK
Content-Type: text/html
Pragma: nocache
Expires: Thu, 01 Dec 1994 16:00:00 GMT

<HTML>
<HEAD>
<TITLE>Jakis tytul</TITLE>
</HEAD>
<BODY BGCOLOR="#FFFFFF">
Wiec sie wykonalo inaczej!
</BODY>
</HTML>
'''

import CLASSES_Library_ICORBase_External_Broker_Communicator
brokercommunicator=CLASSES_Library_ICORBase_External_Broker_Communicator
import sys

def demo(c):
   s_env = c.Input()
   print 'len(s_env): %s' %len(s_env),
#  s_env=s_env.split('\0')
#  print 's_env: %s' %s_env
   s_req = c.Input()
   print '\tlen(s_req): %d' %len(s_req)
   c.Output(result,1)

def main(pname):
   print 'broker-isapi: %s' %pname
   s=brokercommunicator.CommunicatorServer(pname)
   while 1:
      try:
         demo(s)
         brokercommunicator.SendCmd('DONE %s' %pname,withrecv=0)
      except:
         import traceback
         traceback.print_exc()
         raw_input('enter!')
         s.Close()
         brokercommunicator.SendCmd('DONE %s' %pname,withrecv=0)
         sys.exit(1)

#main(sys.argv[1])



