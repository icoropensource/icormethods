# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil

import sys,string,linecache,repr
import bdb

line_prefix = '\n-> '   # Probably a better default

PROMPT = '(Cmd) '
IDENTCHARS = string.letters + string.digits + '_'

def GetCommand(avalue=''):
#   return CLASSES_Library_ICORBase_Interface_ICORUtil.InputString('Debugger','Komenda',avalue)
#   import ICORDelphi
   return icorapi.getcommand(0,avalue,'','')

def GetSourceLine(filename,lineno):
#   import ICORDelphi
   return icorapi.getline(filename,lineno)
                          
class Cmd:
        def __init__(self):
                self.identchars = IDENTCHARS
                self.lastcmd = ''
        def default(self, line):
                print '*** No default handler for "%s"' %line
        def handleevent(self):
                line='n'
                stop = None
                while not stop:
                        try:
                                line = GetCommand(line)
                        except EOFError:
                                line = 'EOF'
                        stop = self.onecmd(line)
        def onecmd(self, line):
                line = string.strip(line)
                if not line:
                        line = self.lastcmd
                else:
                        self.lastcmd = line
                i, n = 0, len(line)
                while i < n and line[i] in self.identchars: i = i+1
                cmd, arg = line[:i], string.strip(line[i:])
                if cmd == '':
                        return self.default(line)
                else:
                        try:
                                func = getattr(self, 'do_' + cmd)
                        except AttributeError:
                                return self.default(line)
                        return func(arg)


class Debugger(bdb.Bdb, Cmd):
        def __init__(self):
                bdb.Bdb.__init__(self)
                Cmd.__init__(self)
                self.prompt = '(Debugger) '
        
        def reset(self):
                bdb.Bdb.reset(self)
                self.forget()
        
        def forget(self):
                self.lineno = None
                self.stack = []
                self.curindex = 0
                self.curframe = None
        
        def setup(self, f, t):
                self.forget()
                self.stack, self.curindex = self.get_stack(f, t)
                self.curframe = self.stack[self.curindex][0]
        
        # Override Bdb methods (except user_call, for now)
        
        def user_line(self, frame):
                # This function is called when we stop or break at this line
                self.interaction(frame, None)
        
        def user_return(self, frame, return_value):
                # This function is called when a return trap is set here
                frame.f_locals['__return__'] = return_value
                print '--Return--'
                self.interaction(frame, None)
        
        def user_exception(self, frame, (exc_type, exc_value, exc_traceback)):
                # This function is called if an exception occurs,
                # but only if we are to stop at or just below this level
                frame.f_locals['__exception__'] = exc_type, exc_value
                if type(exc_type) == type(''):
                        exc_type_name = exc_type
                else: exc_type_name = exc_type.__name__
                print exc_type_name + ':', repr.repr(exc_value)
                self.interaction(frame, exc_traceback)
        
        # General interaction function
        
        def interaction(self, frame, traceback):
                self.setup(frame, traceback)
#                self.print_stack_entry(self.stack[self.curindex])
                self.handleevent()
                self.forget()

        def default(self, line):
                if line[:1] == '!': line = line[1:]
                locals = self.curframe.f_locals
                globals = self.curframe.f_globals
                globals['__privileged__'] = 1
                try:
                        code = compile(line + '\n', '<stdin>', 'single')
                        exec code in globals, locals
                except:
                        t, v = sys.exc_info()[:2]
                        if type(t) == type(''):
                                exc_type_name = t
                        else: exc_type_name = t.__name__
                        print '***', exc_type_name + ':', v

        # Command definitions, called by cmdloop()
        # The argument is the remaining string on the command line
        # Return true to exit from the command loop 
        
        def do_break(self, arg):
                if not arg:
                        print self.get_all_breaks() # XXX
                        return
                # Try line number as argument
                try:
                        arg = eval(arg, self.curframe.f_globals,
                                   self.curframe.f_locals)
                except:                        
                        print '*** Could not eval argument:', arg
                        return

                # Check for condition
                try: arg, cond = arg
                except: arg, cond = arg, None

                try:    
                        lineno = int(arg)
                        filename = self.curframe.f_code.co_filename
                except:
                        # Try function name as the argument
                        try:
                                func = arg
                                if hasattr(func, 'im_func'):
                                        func = func.im_func
                                code = func.func_code
                        except:
                                print '*** The specified object',
                                print 'is not a function', arg
                                return
                        lineno = code.co_firstlineno
                        filename = code.co_filename

                # now set the break point
                err = self.set_break(filename, lineno, cond)
                if err: print '***', err

        do_b = do_break
        
        def do_clear(self, arg):
                if not arg:
                        self.clear_all_breaks()
                        return
                try:
                        lineno = int(eval(arg))
                except:
                        print '*** Error in argument:', str(arg)
                        return
                filename = self.curframe.f_code.co_filename
                err = self.clear_break(filename, lineno)
                if err: print '***', err
        do_cl = do_clear # 'c' is already an abbreviation for 'continue'
        
        def do_where(self, arg):
                self.print_stack_trace()
        do_w = do_where
        
        def do_up(self, arg):
                if self.curindex == 0:
                        print '*** Oldest frame'
                else:
                        self.curindex = self.curindex - 1
                        self.curframe = self.stack[self.curindex][0]
                        self.print_stack_entry(self.stack[self.curindex])
                        self.lineno = None
        do_u = do_up
        
        def do_down(self, arg):
                if self.curindex + 1 == len(self.stack):
                        print '*** Newest frame'
                else:
                        self.curindex = self.curindex + 1
                        self.curframe = self.stack[self.curindex][0]
                        self.print_stack_entry(self.stack[self.curindex])
                        self.lineno = None
        do_d = do_down
        
        def do_step(self, arg):
                self.set_step()
                self.do_list()
                return 1
        do_s = do_step
        
        def do_next(self, arg):
                self.set_next(self.curframe)
                self.do_list()
                return 1
        do_n = do_next
        
        def do_return(self, arg):
                self.set_return(self.curframe)
                return 1
        do_r = do_return
        
        def do_continue(self, arg):
                self.set_continue()
                return 1
        do_c = do_cont = do_continue
        
        def do_quit(self, arg):
                self.set_quit()
                return 1
        do_q = do_quit
        
        def do_args(self, arg):
                if self.curframe.f_locals.has_key('__args__'):
                        print str(self.curframe.f_locals['__args__'])
                else:
                        print '*** No arguments?!'
        do_a = do_args

        def do_argsx(self, arg):
            dbgFunc  = self.curframe.f_code
            funcVars = self.curframe.f_locals
            print funcVars
            try: print "dbgFunc = ", dbgFunc.__members__
            except: pass
            try: print "dbgFunc.co_filename =", dbgFunc.co_filename
            except: pass
            try: print "dbgFunc.co_name     =", dbgFunc.co_name
            except: pass
            try: print "dbgFunc.co_argcount =", dbgFunc.co_argcount
            except: pass
            try: print "dbgFunc.co_varnames =", dbgFunc.co_varnames
            except: pass
            try: print "dbgFunc.co_names    =", dbgFunc.co_names
            except: pass
            try: print "dbgFunc.co_flags    =", dbgFunc.co_flags
            except: pass
            try: print "dbgFunc.co_nlocals  =", dbgFunc.co_nlocals
            except: pass
            try: print "dbgFunc.co_consts   =", dbgFunc.co_consts
            except: pass
            vvpairs = []
            try: 
                for ix in range(dbgFunc.co_argcount):
                        var = dbgFunc.co_varnames[ix]
                        val = funcVars[var]
                        vvpairs.append('%s=%s' % (var, val))
                arglist = string.join(vvpairs, ', ')
                print "  %s(%s)" %(dbgFunc.co_name, arglist)
            except: pass
        do_ax = do_argsx

        def do_retval(self, arg):
                if self.curframe.f_locals.has_key('__return__'):
                        print self.curframe.f_locals['__return__']
                else:
                        print '*** Not yet returned!'
        do_rv = do_retval
        
        def do_p(self, arg):
                self.curframe.f_globals['__privileged__'] = 1
                try:
                        value = eval(arg, self.curframe.f_globals, \
                                        self.curframe.f_locals)
                except:
                        t, v = sys.exc_info()[:2]
                        if type(t) == type(''):
                                exc_type_name = t
                        else: exc_type_name = t.__name__
                        print '***', exc_type_name + ':', str(v)
                        return

                print str(value)

        def do_list(self, arg=None):
                self.lastcmd = 'list'
                last = None
                if arg:
                        try:
                                x = eval(arg, {}, {})
                                if type(x) == type(()):
                                        first, last = x
                                        first = int(first)
                                        last = int(last)
                                        if last < first:
                                                # Assume it's a count
                                                last = first + last
                                else:
                                        first = max(1, int(x) - 5)
                        except:
                                print '*** Error in argument:', str(arg)
                                return
                elif self.lineno is None:
                        first = max(1, self.curframe.f_lineno - 5)
                else:
                        first = self.lineno + 1
                if last == None:
                        last = first + 10
                filename = self.curframe.f_code.co_filename
                breaklist = self.get_file_breaks(filename)
                try:
                        if 0==1:
                                 for lineno in range(first, last+1):
                                         line = GetSourceLine(filename,lineno)
                                         if not line:
                                                 line = linecache.getline(filename, lineno)
                                         if not line:
                                                 print '[EOF]'
                                                 break
                                         else:
                                                 s = string.rjust(str(lineno), 3)
                                                 if len(s) < 4: s = s + ' '
                                                 if lineno in breaklist: s = s + 'B'
                                                 else: s = s + ' '
                                                 if lineno == self.curframe.f_lineno:
                                                         s = s + '->'
                                                 print s + '\t' + line
                                                 self.lineno = lineno
                        else:
                                line = GetSourceLine(filename,self.curframe.f_lineno)
                except KeyboardInterrupt:
                        pass
        do_l = do_list

        def do_whatis(self, arg):
                try:
                        value = eval(arg, self.curframe.f_globals, \
                                        self.curframe.f_locals)
                except:
                        t, v = sys.exc_info()[:2]
                        if type(t) == type(''):
                                exc_type_name = t
                        else: exc_type_name = t.__name__
                        print '***', exc_type_name + ':', str(v)
                        return
                code = None
                # Is it a function?
                try: code = value.func_code
                except: pass
                if code:
                        print 'Function', code.co_name
                        return
                # Is it an instance method?
                try: code = value.im_func.func_code
                except: pass
                if code:
                        print 'Method', code.co_name
                        return
                # None of the above...
                print type(value)
        
        def print_stack_trace(self):
                try:
                        for frame_lineno in self.stack:
                                self.print_stack_entry(frame_lineno)
                except KeyboardInterrupt:
                        pass
        
        def print_stack_entry(self, frame_lineno, prompt_prefix=line_prefix):
                frame, lineno = frame_lineno
                if frame is self.curframe:
                        print '>',
                else:
                        print ' ',
                print self.format_stack_entry(frame_lineno, prompt_prefix)

################################################################################
# Simplified interface

class ICORDebugger(Debugger):
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


def run(statement, globals=None, locals=None):
        ICORDebugger().run(statement, globals, locals)

def runeval(expression, globals=None, locals=None):
        return ICORDebugger().runeval(expression, globals, locals)

def runctx(statement, globals, locals):
        # B/W compatibility
        run(statement, globals, locals)

def runcall(*args):
        return apply(ICORDebugger().runcall, args)

def set_trace():
        ICORDebugger().set_trace()

# Post-Mortem interface

def post_mortem(t):
        p = ICORDebugger()
        p.reset()
        while t.tb_next <> None: t = t.tb_next
        p.interaction(t.tb_frame, t)

def pm():
        import sys
        post_mortem(sys.last_traceback)


def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   return



