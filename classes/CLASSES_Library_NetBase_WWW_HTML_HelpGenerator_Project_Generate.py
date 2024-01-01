# -*- coding: windows-1250 -*-
# saved: 2021/06/08 16:36:32

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_ICORBase_Interface_ICORUtil import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import aICORWWWServerInterface
from CLASSES_Library_NetBase_WWW_Server_DoSummaryParameters import GenerateSummaryParameters
from CLASSES_Library_NetBase_WWW_Server_DoSummaryExecute import GenerateSummaryExecute

class HTMLHelpGenerator:
   def __init__(self,amenu,poid=-1):
      self.menu=amenu
      self.projectid=poid
      self.ClassItem=aICORDBEngine.Classes['CLASSES_Library_NetBase_WWW_HTML_HelpGenerator_Project']
   def DoGenerate(self):
      if self.projectid<0:
         arefs=self.ClassItem.SelectObjects('Wybierz projekt',adisabletoolbar=0,adisableediting=0)
         if not arefs:
            return
         self.projectid=arefs.OID
      self.OutputDirectory=FilePathAsSystemPath(self.ClassItem.OutputDirectory[self.projectid])+'/'
      self.Name=self.ClassItem.Name[self.projectid]
      self.Title=self.ClassItem.Title[self.projectid]
      self.OutputFileName=self.ClassItem.OutputFileName[self.projectid]
      self.DefaultHeader=self.ClassItem.DefaultHeader[self.projectid]
      self.DefaultFooter=self.ClassItem.DefaultFooter[self.projectid]
      self.firstmenuid=None
      self.GenerateHHC()
      self.GenerateHHK()
      self.GenerateHHP()
      self.GenerateCMD()
      print 'hhc '+self.ProjectFileName
   def GenerateCMD(self):
      fname=self.OutputDirectory+self.OutputFileName+'.cmd'
      fout=open(fname,'w')
      fout.write('hhc %s\n'%self.ProjectFileName)
      fout.close()
   def GenerateHHP(self):
      d={'FileName':self.OutputFileName, 'DefaultTopic':self.firstmenuid, 'Title':self.Title,}
      s="""
[OPTIONS]
Auto Index=Yes
Compatibility=1.1 or later
Compiled file=%(FileName)s.chm
Contents file=%(FileName)s.hhc
Default Font=Arial CE,8,0
Default topic=menu_%(DefaultTopic)d.htm
Display compile notes=No
Display compile progress=No
Index file=%(FileName)s.hhk
Language=0x415 Polish
Title=%(Title)s

[INFOTYPES]
"""%d
      self.ProjectFileName=self.OutputDirectory+self.OutputFileName+'.hhp'
      print 'plik:',self.ProjectFileName
      fout=open(self.ProjectFileName,'w')
      fout.write(s)
      fout.close()
   def GenerateHHC(self):
      fname=self.OutputDirectory+self.OutputFileName+'.hhc'
      print 'plik:',fname
      fout=open(fname,'w')
      try:
         s="""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML>
<HEAD>
<meta name="GENERATOR" content="ICOR Help Generator Module">
<!-- Sitemap 1.0 -->
</HEAD><BODY>
<OBJECT type="text/site properties">
   <param name="Window Styles" value="0x800025">
</OBJECT>
<UL>
"""
         fout.write(s)

         for bmenu in self.menu.SubMenus:
            self.GenerateMenuItem(fout,bmenu)
         s="""
</UL>
</BODY></HTML>
"""
         fout.write(s)
      finally:
         fout.close()
   def GenerateMenuItem(self,fout,bmenu):
      if self.firstmenuid is None:
         self.firstmenuid=bmenu.oid
      fout.write('<LI> <OBJECT type="text/sitemap"><param name="Name" value="%s"><param name="Local" value="menu_%d.htm"></OBJECT>\n'%(bmenu.Caption,bmenu.oid))
      fname=self.OutputDirectory+'menu_'+str(bmenu.oid)+'.htm'
      fdata=open(fname,'w')
      try:
         fdata.write(self.DefaultHeader)
         fdata.write(bmenu.PageHTML)

         sref=bmenu.Summaries
         while sref:
            fdata.write('<hr>')
            soid=sref.Summary[sref.OID]
            try:
               soid=int(soid)
            except:
               soid=-1
            fname=FilePathAsSystemPath(aICORWWWServerInterface.OutputPath+'SE_'+str(soid)+'.html')
            bfile=open(fname,'w')
            try:
               if soid>=0:
                  if sref.ShowParameters.ValuesAsInt(sref.OID):
                     GenerateSummaryParameters(bfile,soid)
                  else:
                     GenerateSummaryExecute(bfile,soid)
            finally:
               bfile.close()
            bfile=open(fname,'r')
            try:
               fdata.write(bfile.read())
            finally:
               bfile.close()
      
            wref=sref.WorksheetQueries.GetRefList(sref.OID)
            while wref:
               fdata.write(wref.Class.TextAsHTML[wref.OID])
               wref.Next()
      
            mname=sref.CustomPageByMethod[sref.OID]
            if mname!='':
               mname=string.replace(mname,'\\','_')
               mname=string.replace(mname,'/','_')
               pagemethod=__import__(mname)
               pageevent=getattr(pagemethod,'DoCustomPageByMethod')
               aparam=sref.Parameter[sref.OID]
               if not pageevent is None:
                  apply(pageevent,(fdata,bmenu,self.menu.uid,aparam))
            sref.Next()

         fdata.write(self.DefaultFooter)
      finally:
         fdata.close()
      if bmenu.SubMenus:
         fout.write('<UL>\n')
         for cmenu in bmenu.SubMenus:
            self.GenerateMenuItem(fout,cmenu)
         fout.write('</UL>\n')
   def GenerateHHK(self):
      s="""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML>
<HEAD>
<meta name="GENERATOR" content="ICOR Help Generator Module">
<!-- Sitemap 1.0 -->
</HEAD><BODY>
<UL>
</UL>
</BODY></HTML>
"""
      fname=self.OutputDirectory+self.OutputFileName+'.hhk'
      print 'plik:',fname
      fout=open(fname,'w')
      fout.write(s)
      fout.close()

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   from icorlib.wwwmenu.menuutil import ICORWWWMenuItem
   aclass=aICORDBEngine.Classes[CID]
   amenu=ICORWWWMenuItem(0,721)
   agenerator=HTMLHelpGenerator(amenu,1)
   agenerator.DoGenerate()
   return



