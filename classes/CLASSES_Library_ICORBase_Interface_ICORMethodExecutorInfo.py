# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import time

class ICORMethodExecutorInfo:
   def __init__(self, CID=-1, FieldName='', OID=-1, Value='', UID=-1, xcb=None, xev=None):
      self.CID=CID
      self.FieldName=FieldName
      self.OID=OID
      self.Value=Value
      self.UID=UID
      #
      self.StartTime=0.0
      self.FinishTime=0.0
      self.Result=None
      self.AllowExecute=0
      self.Error=0
      self.Callback = xcb
      self.Event = xev
   def ICORMainPre(self,rmodule):
      self.AllowExecute=1         
      try:
         amethod=getattr(rmodule,'ICORMainPre')
         amethod(self)
      except:
         pass
      if self.Event:
         self.Event.post()
   def ICORMainPost(self,rmodule):
      try:
         amethod=getattr(rmodule,'ICORMainPost')
         amethod(self)
      except:
         pass
   def CallbackCall(self):
      if self.Callback:
         try:
            self.Callback.Terminate()
         except:
            pass
   def ICORMainError(self,rmodule):
      self.Error=1
      self.Result=None
   def ICORMain(self,rmodule):
      self.StartTime=time.time()
      self.ICORMainPre(rmodule)
      if self.AllowExecute:
#         print dir(rmodule)
         try:
            self.Result=rmodule.ICORMain(self.CID, self.FieldName, self.OID, self.Value, self.UID)
         except:
            self.ICORMainError(rmodule)
            self.CallbackCall()
            raise
         self.FinishTime=time.time()
         self.ICORMainPost(rmodule)
      self.CallbackCall()
      return self.Result



