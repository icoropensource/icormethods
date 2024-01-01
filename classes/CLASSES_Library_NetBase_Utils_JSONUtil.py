# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import types

class WriteException(Exception):
    pass

class JsonWriter:
        
    def _append(self, s):
        self._results.append(s)

    def write(self, obj, escaped_forward_slash=0):
        self._escaped_forward_slash = escaped_forward_slash
        self._results = []
        self._write(obj)
        return "".join(self._results)

    def _write(self, obj):
        ty = type(obj)
        if ty is types.DictType:
            n = len(obj)
            self._append("{")
            for k, v in obj.items():
                self._write(k)
                self._append(":")
                self._write(v)
                n = n - 1
                if n > 0:
                    self._append(",")
            self._append("}")
        elif ty is types.ListType or ty is types.TupleType:
            n = len(obj)
            self._append("[")
            for item in obj:
                self._write(item)
                n = n - 1
                if n > 0:
                    self._append(",")
            self._append("]")
        elif ty is types.StringType or ty is types.UnicodeType:
            self._append('"')
            obj = obj.replace('\\', r'\\')
            if self._escaped_forward_slash:
                obj = obj.replace('/', r'\/')
            obj = obj.replace('"', r'\"')
            obj = obj.replace('\b', r'\b')
            obj = obj.replace('\f', r'\f')
            obj = obj.replace('\n', r'\n')
            obj = obj.replace('\r', r'\r')
            obj = obj.replace('\t', r'\t')
            self._append(obj)
            self._append('"')
        elif ty is types.IntType or ty is types.LongType:
            self._append(str(obj))
        elif ty is types.FloatType:
            self._append("%f" % obj)
        elif obj is True:
            self._append("true")
        elif obj is False:
            self._append("false")
        elif obj is None:
            self._append("null")
        else:
            raise WriteException, "Cannot write in JSON: %s" % repr(obj)

def write(obj, escaped_forward_slash=0):
    return JsonWriter().write(obj, escaped_forward_slash)

