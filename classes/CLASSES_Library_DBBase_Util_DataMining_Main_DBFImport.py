# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import struct
import string

class DBFImport: 
   def __init__(self,adefinition=None):
      self.Definition=adefinition
   def Open(self,fname):
      self.fname = fname
      self.f = open(self.fname,'rb') 
      head = self.f.read(32)
      if (head[0] != '\003') and (head[0] != '\203') and (head[0] != '\365'):
         raise TypeError, 'Not a Dbase III+ file!'
      (self.nrecs, self.hlen, self.rlen) = struct.unpack('4xihh20x', head)
      fdalen = (self.hlen - 33)/32 
      fda = [] 
      for k in range(fdalen): 
         fda.append(self.f.read(32)) 
      self.fields = [] 
      for fd in fda:
         bytes = struct.unpack('12c4xBb14x', fd)
         field = '' 
         for i in range(11): 
            if bytes[i] == '\000': 
               break 
            field = field+bytes[i] 
         atype = bytes[11] 
         length = bytes[12] 
         dec = bytes[13] 
         self.fields.append((field,atype,length,dec)) 
      self.cnt=0
      self.Record={}
   def Close(self):
      self.f.close()
   def Next(self,acnt=-1):
      self.Record={}
      if acnt>=0:
         self.cnt=acnt
      if self.cnt<0 or self.cnt>=self.nrecs:
         return
      self.f.seek(self.hlen + self.cnt*self.rlen,0)
      raw=self.f.read(self.rlen) 
      res=[]
      self.IsDeleted=raw[:1]!=' '
      pos = 0
      for field in self.fields:
         end = pos+field[2]
         item = string.strip(raw[pos+1:end+1])
         field_type = field[1]
         if field_type == 'N':
            if item == '':
               value = 0.0
            else:
               value=float(item)
         elif field_type == 'D':
            if item == '':
               value=(0,0,0)
            else:
               value=map(int,[item[:4],item[4:6],item[6:]])
         elif field_type == 'C':
            value=item
         elif (field_type == 'L'):
            if item == '' or item=='f':
               value=0
            else:
               value=1
         else:
            print 'Unknown type for value:',item
            value='<BAD!>'
         pos=end 
         self.Record[field[0]]=value
      self.cnt=self.cnt+1
      return
   def DumpRecord(self):
      for field in self.fields:
         print self.Record.get(field[0],''),
      print
   def Dump(self):
      print ''
      print 'Header length    :', self.hlen
      print 'Record length    :', self.rlen
      print 'Number of records :',  self.nrecs
      print ''
      print '%-12s %-12s %-12s %-12s' % ('Field','Type','Length','Decimal')
      print '%-12s %-12s %-12s %-12s' % ('-----','----','------','-------')
      for afield in self.fields:
         print '%-12s %-12s %-12s %-12s' % afield
      print ''



