# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

#from win32com.client import gencache

#def mkpy(appID,iid,lcid,vmaj,vmin):
#   return gencache.EnsureModule(iid,lcid,vmaj,vmin)

#mtxas=mkpy("Microsoft Transaction Server Type Library",'{74C08640-CEDB-11CF-8B49-00AA00B8A790}',0,1,0)
#aspLib=mkpy("Microsoft Active Server Pages Object Library","{D97A6DA0-A85C-11CF-83AE-00A0C90C2BD8}",0,2,0)

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
   def ICORMainError(self,rmodule):
      self.Error=1
      self.Result=None
   def CallbackCall(self):
      if self.Callback:
         try:
            self.Callback.Terminate()
         except:
            pass
   def Execute(self,rmodule):
#      s=mtxas.AppServer()
#      ctx=s.GetObjectContext()
##      try:
#      rmodule.Session=ctx.Item("Session")
#      rmodule.Response=ctx.Item("Response")
#      rmodule.Request=ctx.Item("Request")
#      rmodule.Server=ctx.Item("Server")
      try:
         res=rmodule.ICORMain(self.CID, self.FieldName, self.OID, self.Value, self.UID)
      finally:
         pass
#         del rmodule.Server
#         del rmodule.Request
#         del rmodule.Response
#         del rmodule.Session
#      ctx.SetComplete()
##      except:
##         print 'Execute error: transaction aborted'
##         ctx.Abort()
##         res=''
#      del ctx
#      del s
      return res
   def ICORMain(self,rmodule):
      self.StartTime=time.time()
      self.ICORMainPre(rmodule)
      if self.AllowExecute:
#         print dir(rmodule)
         try:
            self.Result=self.Execute(rmodule)
         except:
            self.ICORMainError(rmodule)
            self.CallbackCall()
            raise
         self.FinishTime=time.time()
         self.ICORMainPost(rmodule)
      self.CallbackCall()
      return self.Result



