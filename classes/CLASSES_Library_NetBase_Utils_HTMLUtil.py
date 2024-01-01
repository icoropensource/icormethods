# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_Utils_XMLUtil import GetXMLStringAsString
import time
import re
import string

def mkexpires(h = 1, m = 0, s = 0):
   t0, t1, t2, t3, t4, t5, t6, t7, t8 = time.gmtime(time.time())
   t3 = t3 + h
   t4 = t4 + m
   t5 = t5 + s
   return "Expires: %s" % time.strftime("%a, %d %b %Y %T GMT", (t0, t1, t2, t3, t))

def ParseTable(atext):
   p1=re.compile('(\<[tT][rR].*?\<\/[tT][rR]\>)',re.M | re.S)
   p2=re.compile('\<[tT][dD].*?\<\/[tT][dD]\>',re.M | re.S)
   p3=re.compile('\<[tT][dD].*?\>(.*?)\<\/[tT][dD]\>',re.M | re.S)
   ret=[]
   slr=p1.findall(atext)
   for arow in slr:
      sld=p2.findall(arow)
      slc=[]
      for acell in sld:
         m=p3.match(acell)
         if m:
            s=string.replace(m.group(1),chr(13),'')
            s=string.replace(s,'\n',' ')
            slc.append(GetXMLStringAsString(s))
      ret.append(slc)
   return ret



