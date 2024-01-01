# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

class SessionParameters:
   def Load(self):
      self.UID=Session("IIISuid")
      self.UserName=Session("IIISUserName")
      self.CSSFile=Session("IIISCSSFile")
      self.CSSTitle=Session("IIISCSSTitle")
      self.ServerOutputPath=Session("IIISServerOutputPath")
      self.ServerAppOutputPath=Session("IIISServerAppOutputPath")
#   def Save(self):
#      Session("IIISuid")=self.UID
#      Session("IIISUserName")=self.UserName
#      Session("IIISCSSFile")=self.CSSFile
#      Session("IIISCSSTitle")=self.CSSTitle
#      Session("IIISServerOutputPath")=self.ServerOutputPath
#      Session("IIISServerAppOutputPath")=self.ServerAppOutputPath
   def Dump(self):
      print 'UID',self.UID,type(self.UID)
      print 'UserName',self.UserName,type(self.UserName)
      print 'CSSFile',self.CSSFile,type(self.CSSFile)
      print 'CSSTitle',self.CSSTitle,type(self.CSSTitle)
      print 'ServerOutputPath',self.ServerOutputPath,type(self.ServerOutputPath)
      print 'ServerAppOutputPath',self.ServerAppOutputPath,type(self.ServerAppOutputPath)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   print 'Jestem'
#   asessionparameters=SessionParameters()
#   asessionparameters.Load()
#   try:
#      asessionparameters.Dump()
#   finally:
#      asessionparameters.Save()
   return 'Byłem1'



