# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_NetBase_Utils_WWWColors
import gd
wwwcolors=CLASSES_Library_NetBase_Utils_WWWColors

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
   apath='c:/icor/wwwroot/images/dots/'
   aimage=gd.image((1,1))
   aimage.colorAllocate(wwwcolors.id2rgb[0])
   aimage.setPixel((0,0),0)
   aimage.colorTransparent(0)
   aimage.writeGif(apath+'_.gif')
   del aimage
   for aid in range(wwwcolors.COLOR_COUNT):
      aimage=gd.image((1,1))
      acol=wwwcolors.id2rgb[aid]
      aimage.colorAllocate(acol)
      aimage.setPixel((0,0),0)
      aimage.writeGif(apath+str(aid)+'.gif')
      scol='%02x%02x%02x'%acol
      aimage.writeGif(apath+scol+'.gif')
      del aimage




