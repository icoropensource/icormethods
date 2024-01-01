# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

print 'import 1'
import sys
print 'import 2'
import time
print 'import 3'

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   print 'import 4'
   while 1:
      s=time.ctime(time.time())
      sys.stdout.write('%s\n' %s)
      print s
      time.sleep(1)
   return



