# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from win32com.client import gencache

def mkpy(appID,iid,lcid,vmaj,vmin):
   return gencache.EnsureModule(iid,lcid,vmaj,vmin)

mtxas=mkpy("Microsoft Transaction Server Type Library",'{74C08640-CEDB-11CF-8B49-00AA00B8A790}',0,1,0)
aspLib=mkpy("Microsoft Active Server Pages Object Library","{D97A6DA0-A85C-11CF-83AE-00A0C90C2BD8}",0,2,0)

def gv(rsv,i,v):
   try:
      return rsv.ServerVariables.GetItem(i)
   except:
      return v

def safeAction(ctx):
   Request=ctx.Item("Request")
   Response=ctx.Item("Response")
   try:
      Response.Write('wow dziala<br>')
      print "Request.QueryString",Request.QueryString
      i=gv(Request,"ALL_RAW",'?')
      print "ALL_RAW=",i
      i = int(gv(Request,"CONTENT_LENGTH",'0'))
      print 'length=',i
      CT=gv(Request,"HTTP_Content_Type",'?')
      print 'C type=',CT
      print 'C length=',gv(Request,"HTTP_Content_Length",'?')
   finally:
      del Response,Request
#   data = Request.BinaryRead(i)
#   fp=open(r"C:\icor\python\aspoutput","wb")
#   fp.write("Content-Type: ")
#   fp.write(str(CT))
#   fp.write('\r\n\r\n')
#   fp.write(data[0])
#   fp.close()

def Action():
   s=mtxas.AppServer()
   ctx=s.GetObjectContext()
#   try:

   safeAction(ctx)

   ctx.SetComplete()
#   except:
#      print 'error!'
#      ctx.Abort()
   del ctx
   del s
   return 'bylem'

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   print 'Jestem w IISME'
   return Action()



