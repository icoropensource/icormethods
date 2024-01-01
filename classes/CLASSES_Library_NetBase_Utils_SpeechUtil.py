# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from wxPython.wx import *
import sunau
import wave
import os
import random

def Powiedz(atext):
   ICOR_DIR=aICORDBEngine.Variables['_ICOR_BASE_DIR']
   arnd=random.randrange(0,100000000)
   afnameout=ICOR_DIR+'/tmp/output_%d.au'%arnd
   afnamein=ICOR_DIR+'/tmp/output_%d.wav'%arnd
   os.spawnv(os.P_WAIT,ICOR_DIR+'/bin/powiedz.exe',[ICOR_DIR+'/bin/powiedz.exe','-x','1000','-S','1','-f','7','-R','-o',afnameout,atext])
   fin=sunau.open(afnameout,'r')
   f=wave.open(afnamein,'w')
   f.setnchannels(fin.getnchannels())
   f.setsampwidth(fin.getsampwidth())
   f.setframerate(fin.getframerate())
   f.setnframes(fin.getnframes())
   f.writeframes(fin.readframes(sunau.AUDIO_UNKNOWN_SIZE))
   fin.close()
   f.close()
   awave=wxWave(afnamein)
   awave.Play(0)
   os.unlink(afnameout)
   os.unlink(afnamein)

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   ICOR_DIR=aICORDBEngine.Variables['_ICOR_BASE_DIR']
   Powiedz('ala ma kota a kot ma ale')
   return



