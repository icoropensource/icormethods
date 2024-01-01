# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

import time
#from CLASSES_Library_ICORBase_Interface_ICORInterface import *
import CLASSES_Library_ICORBase_Interface_ICORUtil as ICORUtil
import string
import os
import time
import mapscript

MAP_DIR='c:/icor/util/mapserver/'
IMAGE_DIR='c:/icor/wwwroot/output/'
DEBUG=0

def GetUniqueValue():
   import os,time,random,md5
   astr=str(time.time())+'_'+str(time.clock())+'_'+str(os.getpid())+'_'+str(random.randint(0,10000000))
   ahash=md5.new(astr)
   return ahash.hexdigest()      
                                     
class MapPlatnik:
   def __init__(self,amapfile):
      self.mapobj=mapscript.mapObj(amapfile)
      self.mapobj.resolution=96
      self.randid=GetUniqueValue()
      if DEBUG:
         self.randid='111'
      self.mapobj.mappath=MAP_DIR
   def SelectOtputFormat(self,formatname=''):
      self.oOutputFormat=self.mapobj.outputformat
      if formatname=='png':
         self.oOutputFormat.driver='GD/PNG'
         self.oOutputFormat.mimetype='image/png'
         self.oOutputFormat.imagemode=mapscript.MS_IMAGEMODE_PC256
         self.oOutputFormat.extension='png'
         self.oOutputFormat.transparent=mapscript.MS_ON
      elif formatname=='jpeg':
         self.oOutputFormat.driver='GD/JPEG'
         self.oOutputFormat.mimetype='image/jpeg'
         self.oOutputFormat.imagemode=mapscript.MS_IMAGEMODE_RGB
         self.oOutputFormat.extension='jpg'
      self.oOutputFormat.name=formatname      
      self.mapobj.imagetype=formatname
   def PixelToGeo(self,px,py,omapkind):
      minx,miny,maxx,maxy=omapkind.extent.minx,omapkind.extent.miny,omapkind.extent.maxx,omapkind.extent.maxy
      dx= maxx-minx
      dy= maxy-miny
      w=omapkind.width
      h=omapkind.height
      dxpp=dx/w
      dypp=dy/h
      geox=minx+dxpp*px
      geoy=maxy-dypp*py
      oPoint=mapscript.pointObj()
      oPoint.x,oPoint.y=geox,geoy
      return oPoint
   def ShowAllEntireMap(self):
      self.mapobj.extent=self.mapobj.reference.extent
#      self.oExtent.minx,self.oExtent.miny,self.oExtent.maxx,self.oExtent.maxy=self.mapobj.reference.minx,self.mapobj.reference.miny,self.mapobj.reference.maxx,self.mapobj.reference.maxy
   def QueryLayersByPoint(self,px,py,mpkind,layers=None):
      if mpkind==1:
         mapKind=self.mapobj
      elif mpkind==2:
         mapKind=self.mapobj.reference
      blayers=[]
      if layers is None:
         for i in range(0,self.mapobj.numlayers):
            blayers.append(self.mapobj.getLayer(i))
      else:
         for alayer in layers:
            alayer=self.mapobj.getLayerByName(alayer)
            if not alayer is None:
               blayers.append(alayer)
      oPoint=self.PixelToGeo(px,py,mapKind)
      print oPoint.x,oPoint.y
      alayersAttributes=[]
      print 'blayers:',blayers
      for oLayer in blayers:
         adbfnames=[]            
         adbfvalues=[]
         print 'oLayer.name:',oLayer.name
         if oLayer.name!='Selekcja' and oLayer.connectiontype==mapscript.MS_OGR and oLayer.type in [mapscript.MS_LAYER_POINT,mapscript.MS_LAYER_LINE,mapscript.MS_LAYER_POLYGON] and (self.mapobj.scale>=oLayer.minscale or oLayer.minscale==-1) and (self.mapobj.scale<=oLayer.maxscale or oLayer.maxscale==-1):
            afile,aext=os.path.splitext(MAP_DIR+oLayer.connection)
            adec=0
            if aext=='.tab':
                adec=-1
            adbfile=afile+'.dbf'
            print oLayer.name,adbfile
            try:
               aret=oLayer.queryByPoint(self.mapobj,oPoint,mapscript.MS_SINGLE,0)
               oResCMemberObj=oLayer.getResult(aret) 
               ashpIndex=oResCMemberObj.shapeindex
               print ashpIndex
               aTable=mapscript.msDBFOpen(adbfile,'rb')
               if aTable:
                  afieldcount=aTable.nFields
                  for i in range(0,afieldcount):
                     afieldname=aTable.getFieldName(i)
                     afieldvalue=mapscript.msDBFReadStringAttribute(aTable,ashpIndex+adec,i)
#                        print aTable.getFieldType(i)
                     adbfnames.append(afieldname)
                     adbfvalues.append(afieldvalue)
                  alayersAttributes.append((oLayer.name,adbfnames,adbfvalues))
                  mapscript.msDBFClose(aTable)
            except:
               import traceback
               traceback.print_exc()
      return alayersAttributes
   def QueryByField(self,layername,fieldname,fieldvalue):
      if layername and fieldname and fieldvalue:
         try:
            print layername,fieldname,fieldvalue
            oLayer=self.mapobj.getLayerByName(layername)
            asout=''
            for achar in fieldvalue:
               asout=asout+'[%s%s]'%(ICORUtil.strUpperPL(achar),ICORUtil.strLowerPL(achar))
            fieldvalue='/%s$/'%asout
            aret=oLayer.queryByAttributes(self.mapobj,fieldname,fieldvalue,mapscript.MS_MULTIPLE)
            resultCacheObj=oLayer.resultcache
            nResults=resultCacheObj.numresults
            osExtent=resultCacheObj.bounds
            print nResults
            if nResults>0:
               oLayerSel=self.mapobj.getLayerByName('Selekcja')
               oLayerSel.type=oLayer.type
               oLayerSel.connectiontype=oLayer.connectiontype
               oLayerSel.connection=oLayer.connection
               oLayerSel.filteritem=fieldname
               aret=oLayerSel.setFilter(fieldvalue)
               oClass=oLayerSel.getClass(0)
               oStyle = mapscript.styleObj()
               oStyle.maxsize=100
               oStyle.minsize=1    
               if oLayerSel.type==mapscript.MS_LAYER_LINE:
                  oStyle.size=3
                  oStyle.symbol=13
                  oStyle.symbolname='circle'
                  oStyle.backgroundcolor.red,oStyle.backgroundcolor.green,oStyle.backgroundcolor.blue=255,0,0
                  oStyle.color.red,oStyle.color.green,oStyle.color.blue=255,0,0
               elif oLayerSel.type==mapscript.MS_LAYER_POLYGON:
                  oLayerSel.transparency=50
                  oStyle.size=5
                  oStyle.symbol=17
                  oStyle.symbolname='line4'
                  oStyle.backgroundcolor.red,oStyle.backgroundcolor.green,oStyle.backgroundcolor.blue=255,255,255
                  oStyle.color.red,oStyle.color.green,oStyle.color.blue=255,0,0
                  oStyle.outlinecolor.red,oStyle.outlinecolor.green,oStyle.outlinecolor.blue=255,0,0
               else:
                  oStyle.size=10
                  oStyle.symbol=13
                  oStyle.symbolname='circle'
                  oStyle.color.red,oStyle.color.green,oStyle.color.blue=0,0,255
                  oStyle.outlinecolor.red,oStyle.outlinecolor.green,oStyle.outlinecolor.blue=255,0,0
               oClass.styles=oStyle   
               oLayerSel.status=mapscript.MS_ON   
               if (osExtent.minx==osExtent.maxx) and (osExtent.miny==osExtent.maxy):
                  #znaleziono punkt
                  self.mapwidth=self.zoom
                  self.mapheigt=1.0*self.mapwidth*self.mapobj.height/self.mapobj.width
                  self.oExtent.minx=osExtent.minx-self.mapwidth/2
                  self.oExtent.maxx=osExtent.maxx+self.mapwidth/2
                  self.oExtent.miny=osExtent.miny-self.mapheigt/2
                  self.oExtent.maxy=osExtent.maxy+self.mapheigt/2
               else:
                  #znaleziono wiecej niz 1 obiekt
                  nXBuffer=(osExtent.maxx-osExtent.minx)*0.05
                  nYBuffer=(osExtent.maxy-osExtent.miny)*0.05
                  self.oExtent.minx=osExtent.minx-nXBuffer
                  self.oExtent.maxx=osExtent.maxx+nXBuffer
                  self.oExtent.miny=osExtent.miny-nYBuffer
                  self.oExtent.maxy=osExtent.maxy+nYBuffer
            oLayer.close()
            return 0
         except:
            import traceback
            traceback.print_exc()               
            return 1
      else:
         return 1 
   def SaveMapImages(self,aaction,araster):
      if araster==1:
         self.SelectOtputFormat('jpeg')
      else:
         self.SelectOtputFormat('png')
      if aaction==0:
         self.imgobj=self.mapobj.draw()
      else:
         self.imgobj=self.mapobj.drawQuery()
      atmpfile='%s.%s'%(self.randid,self.oOutputFormat.extension)
      self.pictMapExtension=self.oOutputFormat.extension
      mapscript.msSaveImage(self.mapobj,self.imgobj,'%smap_%s'%(IMAGE_DIR,atmpfile))
      mapscript.msFreeImage(self.imgobj)   
      self.SelectOtputFormat('png')
      atmpfile='%s.%s'%(self.randid,self.oOutputFormat.extension)
      self.imgobj=self.mapobj.drawScalebar()
      mapscript.msSaveImage(self.mapobj,self.imgobj,'%sscb_%s'%(IMAGE_DIR,atmpfile))
      mapscript.msFreeImage(self.imgobj)
      self.imgobj=self.mapobj.drawLegend()
      mapscript.msSaveImage(self.mapobj,self.imgobj,'%sleg_%s'%(IMAGE_DIR,atmpfile))
      mapscript.msFreeImage(self.imgobj)
      self.imgobj=self.mapobj.drawReferenceMap()
      mapscript.msSaveImage(self.mapobj,self.imgobj,'%sref_%s'%(IMAGE_DIR,atmpfile))
      mapscript.msFreeImage(self.imgobj)
   def GenerateMap(self,aaction,araster):
      self.SaveMapImages(aaction,araster)
      self.mapwidth=self.oExtent.maxx-self.oExtent.minx
      self.mapheight=self.oExtent.maxy-self.oExtent.miny
#      self.mapres=self.mapobj.resolution/2.54
#      self.mapscale=self.mapwidth/self.mapobj.width*self.mapres*100
      self.centerX=self.oExtent.minx+self.mapwidth/2
      self.centerY=self.oExtent.miny+self.mapheight/2
      newExt='%s,%s,%s,%s'%(str(self.oExtent.minx),str(self.oExtent.miny),str(self.oExtent.maxx),str(self.oExtent.maxy))
      return 'OK'+chr(255)+str(self.centerX)+chr(255)+str(self.centerY)+chr(255)+str(self.mapobj.scale)+chr(255)+str(self.mapwidth)+chr(255)+str(self.mapheight)+chr(255)+str(self.mapobj.width)+chr(255)+str(self.mapobj.height)+chr(255)+newExt+chr(255)+self.randid+chr(255)+str(self.mapobj.units)+chr(255)+self.pictMapExtension

def ICORMain(CID=-1, FieldName='', OID=-1, Value='', UID=-1):
#   aclass=aICORDBEngine.Classes[CID]
   try:
      t1=time.clock()
      mparams,qparams=string.split(Value,chr(254))
      print mparams
      print qparams
      
      athema,aaction,extents,amaptool,zoomfactor,mappictkind,mapdynamiczoom,mapshowall,mappan,alayers,alayersstat,asize=string.split(mparams,chr(255))
      if not athema:
         athema='default'
      aaction=int(aaction)
      amaptool=int(amaptool)
      zoomfactor=float(zoomfactor)
      mappictkind=int(mappictkind)
      mapdynamiczoom=int(mapdynamiczoom)
      mapshowall=int(mapshowall)
      print 'alayers',alayers
      if alayers and alayersstat:
         maplayers=string.split(alayers,'|')
         maplayersstat=string.split(alayersstat,'|')
      else:
         maplayers=[]
         maplayersstat=[]

      maplayersdict={}
      for ml,mls in zip(maplayers,maplayersstat):
         maplayersdict[ml]=int(mls)


#      print maplayers
#      print athema
      amapplatnik=MapPlatnik(MAP_DIR+athema+'.map')

      #new size
      if asize:
         w,h=string.split(asize,',')
         amapplatnik.mapobj.width,amapplatnik.mapobj.height=int(w),int(h)
         #trzeba zmienic skale???

      if amapplatnik.mapobj.width<=50 or amapplatnik.mapobj.height<=50:
         amapplatnik.mapobj.width=500
         amapplatnik.mapobj.height=300
      amapplatnik.aspect=1.0*amapplatnik.mapobj.height/amapplatnik.mapobj.width
      amapplatnik.zoom=amapplatnik.mapobj.extent.maxx-amapplatnik.mapobj.extent.minx #szerokosc (w ukladzie mapy)

      #store original extents
      amapplatnik.oExtent=mapscript.rectObj()      
      amapplatnik.oExtent=amapplatnik.mapobj.extent
      #amapplatnik.minx,amapplatnik.miny,amapplatnik.maxx,amapplatnik.maxy=(amapplatnik.oExtent.minx,amapplatnik.oExtent.miny,amapplatnik.oExtent.maxx,amapplatnik.oExtent.maxy)
      
      #set new user extents
      if extents:
         x1,y1,x2,y2 = string.split(extents,',')
         amapplatnik.oExtent.minx,amapplatnik.oExtent.miny,amapplatnik.oExtent.maxx,amapplatnik.oExtent.maxy=(float(x1),float(y1),float(x2),float(y2))
      print 'user extents:',str(amapplatnik.mapobj.extent.minx),str(amapplatnik.mapobj.extent.miny),str(amapplatnik.mapobj.extent.maxx),str(amapplatnik.mapobj.extent.maxy)
      #calculate scale
      amapplatnik.mapwidth=amapplatnik.oExtent.maxx-amapplatnik.oExtent.minx
      amapplatnik.mapheight=amapplatnik.oExtent.maxy-amapplatnik.oExtent.miny
      
      amapplatnik.centerX=amapplatnik.oExtent.minx+amapplatnik.mapwidth/2
      amapplatnik.centerY=amapplatnik.oExtent.miny+amapplatnik.mapheight/2
      amapplatnik.mapobj.prepareQuery()
      #processing layers
      araster=0
      oColor=mapscript.colorObj()
      oColor.red,oColor.green,oColor.blue=255,255,255
      layersnamesout=[]
      layerstypesout=[]
      layersstatusout=[]
      print 'maplayersdict:',maplayersdict
      for i in range(0,amapplatnik.mapobj.numlayers):
        oLayer=amapplatnik.mapobj.getLayer(i)
        for j in range(0,oLayer.numclasses):
           oClass=oLayer.getClass(j)
           if oClass.name:
              oClass.name=unicode(oClass.name, "cp1250").encode("UTF-8")
        if maplayersdict.has_key(oLayer.name):
           if maplayersdict[oLayer.name]==1:
              oLayer.status=mapscript.MS_ON
              if oLayer.type==mapscript.MS_LAYER_RASTER:
                 araster=1
                 oColor.red,oColor.green,oColor.blue=0,0,0
           else:
              oLayer.status=mapscript.MS_OFF
        if oLayer.name not in [layersnamesout,'Selekcja'] :
           layersnamesout.append(oLayer.name)
           layerstypesout.append(str(oLayer.type))
           layersstatusout.append(str(oLayer.status))

      amapplatnik.mapobj.imagecolor=oColor
      #case type of action on the map
      if mapdynamiczoom>=0: #dynamic zoom
         if amapplatnik.mapobj.width<amapplatnik.mapobj.height:                                                                                       
            newW=1.0*(((mapdynamiczoom*mapdynamiczoom*(amapplatnik.mapobj.reference.extent.maxx-amapplatnik.mapobj.reference.extent.minx-amapplatnik.zoom))/10000)+amapplatnik.zoom)/2
            newH=newW*amapplatnik.aspect
         else:   
            newH=1.0*(((mapdynamiczoom*mapdynamiczoom*(amapplatnik.mapobj.reference.extent.maxy-amapplatnik.mapobj.reference.extent.miny-(amapplatnik.zoom*amapplatnik.aspect)))/10000)+(amapplatnik.zoom*amapplatnik.aspect))/2
            newW=newH*amapplatnik.aspect
         amapplatnik.oExtent.minx=amapplatnik.centerX-newW
         amapplatnik.oExtent.maxx=amapplatnik.centerX+newW
         amapplatnik.oExtent.miny=amapplatnik.centerY-newH
         amapplatnik.oExtent.maxy=amapplatnik.centerY+newH
         ret=amapplatnik.GenerateMap(0,araster)
      elif mapshowall:
         amapplatnik.ShowAllEntireMap()
         ret=amapplatnik.GenerateMap(0,araster)
      elif mappan:
         dx,dy=string.split(mappan,',')
         dx,dy=float(dx),float(dy)
         #print dx,dy
         #amapplatnik.oExtent.minx=amapplatnik.oExtent.minx+dx
         #amapplatnik.oExtent.maxx=amapplatnik.oExtent.maxx+dx
         #amapplatnik.oExtent.miny=amapplatnik.oExtent.miny+dy
         #amapplatnik.oExtent.maxy=amapplatnik.oExtent.maxy+dy
         oPoint=mapscript.pointObj()
         dx,dy=amapplatnik.mapobj.width/2+dx,amapplatnik.mapobj.height/2-dy
         oPoint.x,oPoint.y=dx,dy
         aret=amapplatnik.mapobj.zoomPoint(1, oPoint, amapplatnik.mapobj.width, amapplatnik.mapobj.height, amapplatnik.mapobj.extent,None) 
         ret=amapplatnik.GenerateMap(0,araster)
      elif aaction==0: #0=browse
         px,py=string.split(qparams,chr(255))
         px,py=int(px),int(py)
         oPoint=mapscript.pointObj()
         oPoint.x,oPoint.y=px,py
         print 'px,py:',oPoint.x,oPoint.y
         if mappictkind==1:
            if amaptool==0: #recenter
               aret=amapplatnik.mapobj.zoomPoint(1, oPoint, amapplatnik.mapobj.width, amapplatnik.mapobj.height, amapplatnik.mapobj.extent,None) 
            elif amaptool in (-1,1): # zoom in
   #            print 'px,py:',oPoint.x,oPoint.y
               oPointM=amapplatnik.PixelToGeo(px,py,amapplatnik.mapobj)
   #            print 'mpx,mpy 0:',oPointM.x,oPointM.y
   #            print 'extents 0:',str(amapplatnik.mapobj.extent.minx),str(amapplatnik.mapobj.extent.miny),str(amapplatnik.mapobj.extent.maxx),str(amapplatnik.mapobj.extent.maxy)
   #            print 'extents 0e:',str(amapplatnik.oExtent.minx),str(amapplatnik.oExtent.miny),str(amapplatnik.oExtent.maxx),str(amapplatnik.oExtent.maxy)
               
   #            aret=amapplatnik.mapobj.zoomPoint(1, oPoint, amapplatnik.mapobj.width, amapplatnik.mapobj.height, amapplatnik.oExtent,None)
   #            oPointM=amapplatnik.PixelToGeo(px,py)
   #            print 'mpx,mpy 1:',oPointM.x,oPointM.y
   #            print 'extents 1:',str(amapplatnik.mapobj.extent.minx),str(amapplatnik.mapobj.extent.miny),str(amapplatnik.mapobj.extent.maxx),str(amapplatnik.mapobj.extent.maxy)
   #            print 'extents 1e:',str(amapplatnik.oExtent.minx),str(amapplatnik.oExtent.miny),str(amapplatnik.oExtent.maxx),str(amapplatnik.oExtent.maxy)
               newW=1.0*(amapplatnik.mapwidth)/2
               newH=1.0*(amapplatnik.mapheight)/2

#               newW=1.0*(amapplatnik.oExtent.maxx-amapplatnik.oExtent.minx)/2
#               newH=1.0*(amapplatnik.oExtent.maxy-amapplatnik.oExtent.miny)/2
   #            print newW,newH
               if amaptool<0:
                  newW=newW*zoomfactor
                  newH=newH*zoomfactor
               else:
                  newW=newW/zoomfactor
                  newH=newH/zoomfactor            
   #            print 'extents 2:',str(amapplatnik.mapobj.extent.minx),str(amapplatnik.mapobj.extent.miny),str(amapplatnik.mapobj.extent.maxx),str(amapplatnik.mapobj.extent.maxy)            
               amapplatnik.oExtent.minx=oPointM.x-newW
               amapplatnik.oExtent.maxx=oPointM.x+newW
               amapplatnik.oExtent.miny=oPointM.y-newH
               amapplatnik.oExtent.maxy=oPointM.y+newH
   #            print 'extents 3:',str(amapplatnik.mapobj.extent.minx),str(amapplatnik.mapobj.extent.miny),str(amapplatnik.mapobj.extent.maxx),str(amapplatnik.mapobj.extent.maxy)
         elif mappictkind==2:
            oPointM=amapplatnik.PixelToGeo(px,py,amapplatnik.mapobj.reference)
#            print 'mpx,mpy:',oPointM.x,oPointM.y
            newW=1.0*(amapplatnik.mapwidth)/2
            newH=1.0*(amapplatnik.mapheight)/2
            amapplatnik.oExtent.minx=oPointM.x-newW
            amapplatnik.oExtent.maxx=oPointM.x+newW
            amapplatnik.oExtent.miny=oPointM.y-newH
            amapplatnik.oExtent.maxy=oPointM.y+newH
            
#            aret=amapplatnik.mapobj.zoomPoint(1, oPoint, amapplatnik.mapobj.reference.width, amapplatnik.mapobj.reference.height, amapplatnik.mapobj.extent,None) 
         ret=amapplatnik.GenerateMap(aaction,araster)
      elif aaction==1: #1=query
         aLayer,aField,aValue=string.split(qparams,chr(255))
         amapplatnik.ShowAllEntireMap()
         aret=amapplatnik.QueryByField(aLayer,aField,aValue)
         if aret:
            ret='NORESULTS'
         else:
            ret=amapplatnik.GenerateMap(aaction,araster)
      elif aaction==2: #2=info (standard)            
         amapplatnik.mapobj.status=mapscript.MS_OFF
         px,py=string.split(qparams,chr(255))
         px,py=int(px),int(py)
         llvalues=amapplatnik.QueryLayersByPoint(px,py,1)
         print amapplatnik.mapobj.scale         
         if llvalues:
            fname='%sinf_%s.xml'%(IMAGE_DIR,amapplatnik.randid)
            astr='<?xml version="1.0" encoding="Windows-1250"?>\n<?xml-stylesheet type="text/xsl" href="/icormanager/inc/mapscript_layer_info.xsl"?>\n'
            astr=astr+'<LAYERS>\n'
            for aLayerTable in llvalues:
               aTable=aLayerTable[0]
               aFields=aLayerTable[1]
               aValues=aLayerTable[2]
               n=len(aFields)
               astr=astr+' '*3+'<LAYER name="%s">\n'%(aTable)
               for i in range(0,n):
                  aField=aFields[i]
                  aValue=aValues[i]
                  astr=astr+' '*6+'<FIELD name="%s" value="%s" />\n'%(aField,aValue)
               astr=astr+' '*3+'</LAYER>\n'   
            astr=astr+'</LAYERS>\n'
            fout=open(fname,'w')
            try:
               fout.write(astr)
            finally:
               fout.close()
            ret='OK,'+amapplatnik.randid
         else:   
            ret='NORESULTS'
      elif aaction==3: #3=info (geodezja)
         amapplatnik.mapobj.status=mapscript.MS_OFF
         px,py=string.split(qparams,chr(255))
         px,py=int(px),int(py)
         layers=['Dzia\xb3ki']
         llvalues=amapplatnik.QueryLayersByPoint(px,py,1,layers)
         if llvalues:
            ret='OK,%s%s,%s'%(llvalues[0][2][1],llvalues[0][2][2],llvalues[0][2][3])
         else:
            ret='NORESULTS'
   except:
      print 'Exception in code' 
      import traceback
      traceback.print_exc()      
      ret='BAD'
      if DEBUG:
         raise
   
   if ret[:2]=='OK': #dodanie informacji o warstwach
      sl1=string.join(layersnamesout,'|')
      sl2=string.join(layerstypesout,'|')
      sl3=string.join(layersstatusout,'|')
      t2=time.clock()
      exectime=t2-t1
      ret=ret+chr(254)+sl1+chr(255)+sl2+chr(255)+sl3+chr(254)+str(exectime)
   amapplatnik.mapobj.save('map.map')                    
   print ret
   return ret

if 0:
   DEBUG=1
   IMAGE_DIR=''
#   athema,aaction,extents,amaptool,zoomfactor,mappictkind,mapdynamiczoom,mapshowall,mappan,alayers,asize
   mparams=string.join(['default','1','','1','2','1','-1','0','','','',''],chr(255))
   qparams=string.join(['Ulice','Ulica','Felczaka'],chr(255))
   s=mparams+chr(254)+qparams
   ICORMain(-1,'',-1,s,0)


