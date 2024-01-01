# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_Utils_WWWColors import scolor2color

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   ClearStdOut()
   aclass=aICORDBEngine.Classes[CID]
   k=scolor2color.keys()
   k.sort()
   print """
type
   TWWWColor = RECORD
      name : STRING;
      value : Integer;
      END;
const
   tab_scolor2color : ARRAY [1..%d] of TWWWColor = (""" % (len(k))
   i=0
   for ac in k:
      if ac!='transparent':
         print "(name:'%s';value:%d),"%(ac,scolor2color[ac]),
         i=i+1
         if i%5==0:
            print 
   print ');'
   return


