# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_WWW_Server_ICORWWWInterface import *
import re

def OnBeforeWWWAction(aobj,amenu,file):
   w=1
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelView',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelEdit',amenu.uid)
   if 0:
      w=w and ICORSecurity.CheckRecursiveAccessLevelForUser(aobj,'AccessLevelDelete',amenu.uid)
   return w

def OnWWWAction(aobj,amenu,file):
   if amenu.Action=='ObjectApplyMethods':
      dpe={}
      de={}
      uobj=aobj.Plugins
      while uobj:
         eobj=uobj.PluginEvents
         while eobj:
            kobj=eobj.EventKind
            if kobj:
               atk=(kobj.EventName,eobj.EventKey)
               de[atk]=1
               dd=dpe.get(atk,{})
               dd[uobj.Nazwa]=1
               dpe[atk]=dd
            eobj.Next()
         tobj=uobj.Template
         while tobj:
            eobj=tobj.TemplateEvents
            while eobj:
               kobj=eobj.EventKind
               if kobj:
                  atk=(kobj.EventName,eobj.EventKey)
                  de[atk]=1
                  dd=dpe.get(atk,{})
                  dd[uobj.Nazwa]=1
                  dpe[atk]=dd
               eobj.Next()
            tobj.Next()
         uobj.Next()
      l=de.keys()
      l.sort()
      atext=''
      tobj=aobj.PageTemplate
      while tobj:
         if tobj:
            atext=atext+tobj.PageTop1+tobj.PageLeft+tobj.PageContent+tobj.PageRight+tobj.PageBottom
         file.write('<hr><hr><h1>Wzorzec strony: %s [%d]</h1>\n'%(tobj.Template,tobj.OID))
         file.write('<h3>Zdarzenia OnCMS...:</h3>\n')
         file.write('<code>')
         for s,sk in l:
            if string.find(s,'OnCMS')==0 and not s in ['OnCMSSQLCreate','OnCMSWrite','OnCMSPageNamedSection','OnCMSChapterMenuBefore','OnCMSChapterMenuAfter','OnCMSInit','OnCMSWriteCSS','OnCMSWriteCSSSingle','OnCMSWriteChapterAfter','OnCMSWriteChapterCSS','OnCMSWriteChapterJS','OnCMSWriteChapterText',]:
               sfre=re.compile('''this\.ProcessEvents\([\'\"]%s[\'\"]'''%s,re.M)
               acolor='red'
               if sfre.search(atext):
                  acolor='green'
               file.write("<br><font color=%s>this.ProcessEvents('%s')</font><br>\n"%(acolor,s))
               dd=dpe[s,sk]
               lk=dd.keys()
               lk.sort()
               for sp in lk:
                  file.write("<font color=brown>&nbsp;&nbsp;&nbsp;&nbsp;%s</font><br>\n"%(sp,))
         file.write('</code>')
         file.write('<hr>\n')
         file.write('<h3>Zdarzenia w/g klucza:</h3>\n')
         file.write('<code>')
         for s,sk in l:
            if s=='OnCMSPageNamedSection' and sk:
               sfre=re.compile('''this\.ProcessEvents\([\'\"]%s[\'\"](,|,akey\=)[\'\"]%s[\'\"]'''%(s,sk),re.M)
               acolor='red'
               if sfre.search(atext):
                  acolor='green'
               file.write("<br><font color=%s>this.ProcessEvents('%s','%s')</font><br>\n"%(acolor,s,sk))
               dd=dpe[s,sk]
               lk=dd.keys()
               lk.sort()
               for sp in lk:
                  file.write("<font color=brown>&nbsp;&nbsp;&nbsp;&nbsp;%s</font><br>\n"%(sp,))
         file.write('</code>')
         tobj.Next()
   return 2 # show back reference to main object (1-link, 2-button)

