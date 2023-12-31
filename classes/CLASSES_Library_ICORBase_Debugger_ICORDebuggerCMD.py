# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import string

PROMPT = '(Cmd) '
IDENTCHARS = string.letters + string.digits + '_'

class Cmd:
    prompt = PROMPT
    identchars = IDENTCHARS
    ruler = '='
    lastcmd = ''
    cmdqueue = []
    intro = None
    doc_leader = ""
    doc_header = "Documented commands (type help <topic>):"
    misc_header = "Miscellaneous help topics:"
    undoc_header = "Undocumented commands:"
    nohelp = "*** No help on %s"

    def __init__(self): pass

    def cmdloop(self, intro=None):
        self.preloop()
        if intro != None:
            self.intro = intro
        if self.intro:
            print self.intro
        stop = None
        while not stop:
            if self.cmdqueue:
                line = self.cmdqueue[0]
                del self.cmdqueue[0]
            else:
                try:
                    line = raw_input(self.prompt)
                except EOFError:
                    line = 'EOF'
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()

    def precmd(self, line):
        return line

    def postcmd(self, stop, line):
        return stop

    def preloop(self):
        pass

    def postloop(self):
        pass

    def onecmd(self, line):
        line = string.strip(line)
        if not line:
            return self.emptyline()
        elif line[0] == '?':
            line = 'help '+line[1:]
        elif line[0] == '!':
            if hasattr(self, 'do_shell'):
                line = 'shell'
            else:
                return self.default(line)
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

    def emptyline(self):
        if self.lastcmd:
            return self.onecmd(self.lastcmd)

    def default(self, line):
        print '*** Unknown syntax:', line

    def do_help(self, arg):
        if arg:
            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except:
                try:
                    doc=getattr(self, 'do_' + arg).__doc__
                    if doc:
                        print doc
                        return
                except:
                    pass
                print self.nohelp % (arg,)
                return
            func()
        else:
            # Inheritance says we have to look in class and
            # base classes; order is not important.
            names = []
            classes = [self.__class__]
            while classes:
                aclass = classes[0]
                if aclass.__bases__:
                    classes = classes + list(aclass.__bases__)
                names = names + dir(aclass)
                del classes[0]
            cmds_doc = []
            cmds_undoc = []
            help = {}
            for name in names:
                if name[:5] == 'help_':
                    help[name[5:]]=1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd=name[3:]
                    if help.has_key(cmd):
                        cmds_doc.append(cmd)
                        del help[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)
            print self.doc_leader
            self.print_topics(self.doc_header,   cmds_doc,   15,80)
            self.print_topics(self.misc_header,  help.keys(),15,80)
            self.print_topics(self.undoc_header, cmds_undoc, 15,80)

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if cmds:
            print header;
            if self.ruler:
                print self.ruler * len(header)
            (cmds_per_line,junk)=divmod(maxcol,cmdlen)
            col=cmds_per_line
            for cmd in cmds:
                if col==0: print
                print (("%-"+str(cmdlen)+"s") % cmd),
                col = (col+1) % cmds_per_line
            print "\n"


