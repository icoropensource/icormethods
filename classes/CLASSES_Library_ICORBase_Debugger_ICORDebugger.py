# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
import sys
import m32api
import bdb
import tokenize
import CLASSES_Library_ICORBase_Debugger_ICORDebuggerPDB as ipdbpdb
import CLASSES_Library_NetBase_Utils_XMLUtil

def GetCommand(avalue=''):
#   import icorapi
   return icorapi.getcommand(0,avalue,'','')

def GetSourceLine(filename,lineno):
#   import ICORDelphi
   return icorapi.getline(filename,lineno)

class ICORDebugger(ipdbpdb.Pdb):
   def __init__(self):
      ipdbpdb.Pdb.__init__(self)
      self.IsDebuggerStackVisible=1
      self.IsVariablesVisible=1
      self.MaxVariableLength=256
      self.MaxDepth=100

# z ipdbcmd
   def lookupmodule(self, filename):
      x='CLASSES'
#      print 'lookupmodule',filename,filename[:len(x)]
      if filename[:len(x)]==x:
         return filename
      return ipdbpdb.Pdb.lookupmodule(filename)
   def checkline(self,filename,lineno):
      x='CLASSES'
#      print 'checkline',filename,filename[:len(x)]
      if filename[:len(x)]==x:
         return lineno
      return ipdbpdb.Pdb.checkline(self,filename,lineno)
   def set_break(self, filename, lineno, temporary=0, cond = None):
      filename = self.canonic(filename)
      if not self.breaks.has_key(filename):
         self.breaks[filename] = []
      list = self.breaks[filename]
      if not lineno in list:
         list.append(lineno)
      bp = bdb.Breakpoint(filename, lineno, temporary, cond)
   def updatedisplay(self):
      self.showstack()
      self.do_showvariables(len(self.stack)-self.curindex-1)
   def preloop(self):
      self.drilldownvariableinfo=None
      ipdbpdb.Pdb.preloop(self)
#   def precmd(self,line):
#      return ipdbpdb.Pdb.precmd(self,line)
#      return line
   def postcmd(self, stop, line):
      self.updatedisplay()
      return ipdbpdb.Pdb.postcmd(self,stop,line)
#      return stop
   def cmdloop(self, intro=None):
      self.do_list()
      self.updatedisplay()
      self.preloop()
#      if intro != None:
#         self.intro = intro
#      if self.intro:
#         print self.intro
      stop = None
      line = 'n'
      while not stop:
         if self.cmdqueue:
            line = self.cmdqueue[0]
            del self.cmdqueue[0]
         else:
            try:
               line = GetCommand(line)
            except EOFError:
               line = 'EOF'
         line = self.precmd(line)
         stop = self.onecmd(line)
         stop = self.postcmd(stop, line)
      self.postloop()
   # z ipdbpdb
   def do_list(self, arg=None):
      self.lastcmd = 'list'
      filename = self.curframe.f_code.co_filename
#      breaklist = self.get_file_breaks(filename)
      try:
         line = GetSourceLine(filename,self.curframe.f_lineno)
      except KeyboardInterrupt:
         pass
   do_l = do_list
   def do_step(self, arg):
      self.do_list(arg)
      self.set_step()
      return 1
   do_s = do_step
   def do_next(self, arg):
      self.do_list(arg)
      self.set_next(self.curframe)
      return 1
   do_n = do_next

   def set_trace(self):
      try:
         1 + ''
      except:
         frame = sys.exc_info()[2].tb_frame.f_back.f_back
      self.reset()
      while frame:
         frame.f_trace = self.trace_dispatch
         self.botframe = frame
         frame = frame.f_back
      self.set_step()
      sys.settrace(self.trace_dispatch)
   def showstack(self):
      if not self.IsDebuggerStackVisible:
         return
      ls=[]
      counter=0
      for frame, lineno in self.stack:
         name = frame.f_code.co_name
         if not name:
            name = "<lambda>"
         ls.append(string.join([
            name,frame.f_code.co_filename,str(lineno)
            ],chr(253))
         )
         counter=counter+1
         if counter>=self.MaxDepth:
            break
      ls.reverse()
      aICORDBEngine.RepositoryChange('DebuggerCallStack',-1,-1,string.join(ls,chr(254)))

   def do_showvariables(self,astacklevel="0"):
      if not self.IsVariablesVisible:
         return
      astacklevel = int(astacklevel)
      if astacklevel<0:
         astacklevel=0
      if astacklevel>len(self.stack):
         astacklevel=len(self.stack)
      astacklevel=len(self.stack)-astacklevel-1
      if astacklevel!=self.curindex:
         self.curframe = self.stack[astacklevel][0]
         self.curindex = astacklevel
      ls=self.getdictasstring('l','.%s',0,self.curframe.f_locals)
      aICORDBEngine.RepositoryChange('DebuggerVariablesLocal',-1,-1,ls)
      ls=self.getdictasstring('g','.%s',0,self.curframe.f_globals)
      aICORDBEngine.RepositoryChange('DebuggerVariablesGlobal',-1,-1,ls)
   def GetVariableValueAsString(self,avariable,adefault):
      if hasattr(avariable,'__doc__'):
         adoc=avariable.__doc__
         if not adoc:
            adoc='.'
      else:
         adoc='.'
      try:
         s=repr(avariable)[:self.MaxVariableLength]
      except:
         try:
            s=avariable.__class__.__name__
         except:
            s='??? %s ???' % adefault
      return s,adoc
   def getdictasstring(self,name,vfmt,stringize,vdict,dump=0):
      if not vdict:
         return ''
      keys=vdict.keys()
      keys.sort()
      ls=[]
      vfmt='%d,%s'+vfmt
      for avariablename in keys:
         avariablevalue=vdict[avariablename]
         s,adoc=self.GetVariableValueAsString(avariablevalue,avariablename)
         if stringize and type(avariablename)==types.StringType:
            avariablename=repr(avariablename)
#         print avariablename,s,adoc
         ls.append(string.join([
            avariablename,
            s,
            str(type(avariablevalue)),
            vfmt %(id(vdict),name,avariablename),
            adoc,
            ],chr(253))
         )
      ls.sort()
      return string.join(ls,chr(254))
   def getvariableidpath(self,avariableinfo):
      data=string.split(avariableinfo,',')
      return data[0],string.join(data[1:],',')
   def getvariablenametokens(self,avariablepath):
      s=[1,avariablepath,'']
      toks=[]
      def readline(s=s):
         i=s[0]
         s[0]=i+1
         return s[i]
      def printtoken(type, token, (srow, scol), (erow, ecol), line,toks=toks):
         toks.append(token)
      tokenize.tokenize(readline, printtoken)
      return toks[:-1]
   def getvariablename(self,avariablepath):
      toks=self.getvariablenametokens(avariablepath)
      i=len(toks)-1
      if toks[i]==']':
         while toks[i]!='[':
            i=i-1
         i=i-1
      return string.join(toks[i:],'')
   def getvariablenamedict(self,avariablepath,aencode=None):
      toks=self.getvariablenametokens(avariablepath)
      i=len(toks)-1
      if toks[i]==']':
         while toks[i]!='[':
            i=i-1
         toks=toks[:i]
      else:
         i=i-1
         if toks[i]=='.':
            i=i-1
         toks=toks[:i+1]
      if aencode:
         for i in range(len(toks)):
            toks[i]=CLASSES_Library_NetBase_Utils_XMLUtil.GetAsXMLString(toks[i])
         toks=string.join(toks,chr(254))
      else:
         toks=string.join(toks,'')
      return toks
   def do_drilldownvariable(self,avariableinfo):
      try:
         self._do_drilldownvariable(avariableinfo)
      except:
         import traceback
         traceback.print_exc()
   def _do_drilldownvariable(self,avariableinfo):
      self.drilldownvariableinfo=avariableinfo
      avariabledict,avariablepath=self.getvariableidpath(avariableinfo)
      print 'aktualny kontekst:',avariablepath
      avariabledict=m32api.classfromid(int(avariabledict))
      avariablename=self.getvariablename(avariablepath)
#      aprevvariabledict=self.getvariablenamedict(avariablepath,avariabledict)
      try:
         avariableitem=avariabledict[avariablename]
      except:
         try:
            avariableitem=eval(avariablepath[2:],self.curframe.f_globals,self.curframe.f_locals)
         except:
            avariableitem=eval(repr(avariablepath[2:]),self.curframe.f_globals,self.curframe.f_locals)
      vtype=type(avariableitem)
      if vtype in [types.TupleType,types.ListType]:
         ls=[]
         vindex=0
         while vindex<len(avariableitem) and vindex<self.MaxDepth:
            v=avariableitem[vindex]
            s,adoc=self.GetVariableValueAsString(v,vindex)
            ls.append(string.join([
               str(vindex),
               s,
               str(type(v)),                                      
               '%d,%s[%s]' %(id(avariabledict),avariablepath,vindex),
               adoc,
               ],chr(253))
            )
            vindex=vindex+1
         aICORDBEngine.RepositoryChange('DebuggerVariableDrillDown',-1,-1,string.join(ls,chr(254)))
      elif vtype in [types.InstanceType,types.ModuleType,types.ClassType]:
         ls=self.getdictasstring(avariablepath,'.%s',0,avariableitem.__dict__)
         aICORDBEngine.RepositoryChange('DebuggerVariableDrillDown',-1,-1,ls)
      elif vtype==types.DictType:
         ls=self.getdictasstring(avariablepath,'[%s]',1,avariableitem)
         aICORDBEngine.RepositoryChange('DebuggerVariableDrillDown',-1,-1,ls)
      elif vtype==types.FileType:
         ddict={
            'name':avariableitem.name,
            'closed':avariableitem.closed,
            'mode':avariableitem.mode,
            'softspace':avariableitem.softspace,
             }
         ls=self.getdictasstring(avariablepath,'.%s',0,ddict)
         aICORDBEngine.RepositoryChange('DebuggerVariableDrillDown',-1,-1,ls)
      else:
         pass
   def do_setobjectvalue(self,avariableinfo):
      try:
         self._do_setobjectvalue(avariableinfo)
      except:
         print 'blad przypisania'
   def _do_setobjectvalue(self,avariableinfo):
      avariabledict,avariablepath=self.getvariableidpath(avariableinfo[2:])
      avariablename=s=avariablepath[2:]
      ret=ICORUtil.InputString('Podaj wartosc zmiennej',avariablename,'')
      if avariablepath[0]=='g':
         i=0
         s=s+'.'
         while s[i] not in '.[':
            i=i+1
         s='global '+s[:i]+';'+s
      self.default(s+'='+ret)
      if avariableinfo[0]=='1':
         self.do_drilldownvariable(self.drilldownvariableinfo)
      else:
         self.drilldownvariableinfo=None
   def do_drilldownvariableup(self,args):
      if self.drilldownvariableinfo:
         avariabledict,avariablepath=self.getvariableidpath(self.drilldownvariableinfo)
         ppath=self.getvariablenamedict(avariablepath)
         if len(ppath)>1:
            ppath=avariabledict+','+ppath
            self.do_drilldownvariable(ppath)
         else:
            self.do_drilldownvariable(self.drilldownvariableinfo)

#   def do_setdebuggershowoptions(self,ashowstack,ashowglobalvariables,amaxvariablelength):
#      self.IsDebuggerStackVisible=ashowstack
#      self.IsVariablesVisible=ashowglobalvariables
#      self.MaxVariableLength=amaxvariablelength #256



_GlobalDebugger = None
def _GetDebugger():
   global _GlobalDebugger
   if _GlobalDebugger is None:
      _GlobalDebugger=ICORDebugger()
   return _GlobalDebugger

def run(statement, globals=None, locals=None):
   _GetDebugger().run(statement, globals, locals)

def runeval(expression, globals=None, locals=None):
   return _GetDebugger().runeval(expression, globals, locals)

def runctx(statement, globals, locals):
   # B/W compatibility
   run(statement, globals, locals)

def runcall(*args):
   return apply(_GetDebugger().runcall, args)

def set_trace():
   _GetDebugger().set_trace()

# Post-Mortem interface

def post_mortem(t):
   p = _GetDebugger()
   p.reset()
   while t.tb_next <> None: t = t.tb_next
   p.interaction(t.tb_frame, t)

def pm():
   import sys
   post_mortem(sys.last_traceback)

def debugger(signo,frame):
#   print '\nsignal=',signo,frame
   _GetDebugger().set_trace()
import signal
signal.signal(signal.SIGINT,debugger)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return

#[
#[l,253pz],254
#[l,253pz,253t],254
#[l,253pz,253t,x],254
#[l,pz,t,x[(256,"aaa")]],
#]



