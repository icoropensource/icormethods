# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:54

import string

t_iso=chr(177)+chr(230)+chr(234)+chr(179)+chr(241)+chr(243)+chr(182)+chr(188)+chr(191) + chr(161)+chr(198)+chr(202)+chr(163)+chr(209)+chr(211)+chr(166)+chr(172)+chr(175)
t_win=chr(185)+chr(230)+chr(234)+chr(179)+chr(241)+chr(243)+chr(156)+chr(159)+chr(191) + chr(165)+chr(198)+chr(202)+chr(163)+chr(209)+chr(211)+chr(140)+chr(143)+chr(175)
t_asc="acelnoszzACELNOSZZ"
trans_tab_ISO2Win=string.maketrans(t_iso,t_win)
trans_tab_Win2ISO=string.maketrans(t_win,t_iso)
trans_tab_ISO2Asc=string.maketrans(t_iso,t_asc)
trans_tab_Win2Asc=string.maketrans(t_win,t_asc)

def ISO2Win(atext):
   return atext[:].translate(trans_tab_ISO2Win)

def Win2ISO(atext):
   return atext[:].translate(trans_tab_Win2ISO)

def ISO2Asc(atext):
   return atext[:].translate(trans_tab_ISO2Asc)

def Win2Asc(atext):
   return atext[:].translate(trans_tab_Win2Asc)

