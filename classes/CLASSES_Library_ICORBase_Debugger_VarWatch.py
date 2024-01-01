# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import types, string
from traceback import *

def varwatch ( variable , auserinfo=''):
   stack = extract_stack ( )[-2:][0]
   actualCall = stack[3]
   left = string.find ( actualCall, '(' )
   right = string.find ( actualCall, ',' )
   varType = type ( variable )
   if auserinfo:
      auserinfo=auserinfo+' - '
   print "%svariable '%s' == '%s' of type '%s' at line %d of file '%s'" % (
      auserinfo,string.strip ( actualCall[left+1:right] ),
      variable,
      str(varType)[7:-2],
      stack[1],
      stack[0] )



