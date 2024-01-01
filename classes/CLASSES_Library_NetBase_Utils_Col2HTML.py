# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
from CLASSES_Library_NetBase_Utils_WWWColors import scolor2id,scolor2color,id2rgb
import colorsys

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   aclass=aICORDBEngine.Classes[CID]
   f=open('c:/icor/tmp/out.htm','w')
   try:
      f.write('<html><body bgcolor="white">')
      d={}
      dg={}
      for scolor in scolor2id.keys():
         aid=scolor2id[scolor]
         acolor=scolor2color[scolor]
         argb=id2rgb[aid]
# YUV - grayscale conversion
#         d[(0.212671*argb[0] + 0.715160*argb[1] + 0.072169*argb[2])/3.0]=[aid,scolor,acolor]
         if argb[0]==argb[1] and argb[1]==argb[2]:
            dg[argb[0]]=[aid,scolor,acolor]
         else:
            h,l,s=colorsys.rgb_to_hls(argb[0]/256.0,argb[1]/256.0,argb[2]/256.0)
            d[s,l,h]=[aid,scolor,acolor]
      lc=d.keys()
      lc.sort()
      f.write('<font size=+1><br></font><TABLE WIDTH="800" BORDER=1 CELLSPACING=0 CELLPADDING=0 BORDERCOLOR=black>')
      for argb in lc:
         aid,acolor,hcolor=d[argb]
         f.write("""
<TR>
<TD WIDTH=250 BGCOLOR="%s"><B><FONT COLOR="black">&nbsp;%s</FONT></B></TD>
<TD WIDTH=200 BGCOLOR="%s"><B><FONT COLOR="white">&nbsp;%s</FONT></B></TD>
<TD WIDTH=150 BGCOLOR=black><B><FONT COLOR="%s">&nbsp;%s</FONT></B></TD>
<TD WIDTH=150 BGCOLOR=white><B><FONT COLOR="%s">&nbsp;%s</FONT></B></TD>
<TD WIDTH=50 BGCOLOR=white><B><FONT COLOR="black" face="courier new">%06x</FONT></B></TD>
</TR>
"""%(acolor,acolor,acolor,acolor,acolor,acolor,acolor,acolor,hcolor))
      f.write('</font></TABLE>')

      lc=dg.keys()
      lc.sort()
      f.write('<hr><font size=+1><br></font><TABLE WIDTH="800" BORDER=1 CELLSPACING=0 CELLPADDING=0 BORDERCOLOR=black>')
      for argb in lc:
         aid,acolor,hcolor=dg[argb]
         f.write("""
<TR>
<TD WIDTH=250 BGCOLOR="%s"><B><FONT COLOR="black">&nbsp;%s</FONT></B></TD>
<TD WIDTH=200 BGCOLOR="%s"><B><FONT COLOR="white">&nbsp;%s</FONT></B></TD>
<TD WIDTH=150 BGCOLOR=black><B><FONT COLOR="%s">&nbsp;%s</FONT></B></TD>
<TD WIDTH=150 BGCOLOR=white><B><FONT COLOR="%s">&nbsp;%s</FONT></B></TD>
<TD WIDTH=50 BGCOLOR=white><B><FONT COLOR="black" face="courier new">%06x</FONT></B></TD>
</TR>
"""%(acolor,acolor,acolor,acolor,acolor,acolor,acolor,acolor,hcolor))
      f.write('</font></TABLE>')

      f.write('</body></html>')
   finally:
      f.close()
   return


