# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import sys
import os
#import Image

class SpriteItem(object):
   def __init__(self,afilename,afilenameimage,acssclass,left,top,right,bottom):
      self.filename=afilename
      self.filenameimage=afilenameimage
      self.cssclass=acssclass
      self.l=left
      self.t=top
      self.r=right
      self.b=bottom
      self.w=self.r-self.l
      self.h=self.b-self.t
   def DrawTo(self, img):
      return #$$
      aimage=Image.open(self.filename)
      img.paste(aimage,(self.l,self.t,self.r,self.b))
      del aimage
   def CssRule(self,imgfile):
      return ".%(rule)s {border:medium none;background: transparent url(%(file)s) -%(x)dpx -%(y)dpx no-repeat; width: %(w)dpx; height: %(h)dpx; }"%{'rule':self.cssclass,'file':imgfile,'x':self.l,'y':self.t,'w':self.w,'h':self.h}
   def CssRule2(self,imgfile):
      return ".%(rule)s {border:medium none;left:-%(x)dpx;position:absolute;top:-%(y)dpx;}"%{'rule':self.cssclass,'file':imgfile,'x':self.l,'y':self.t,'w':self.w,'h':self.h}

class SpriteBuilder(object):
   def __init__(self):
      self.sprites={}
      self.xsize=0
      self.ysize=0
   def Parse(self,l,acssclassbasename):
      return #$$
      li=[]
      maxw,maxh=600,0
      for afnameimage,afname in l:
         if afname[-3:] in ['png','gif']:
            img=Image.open(afname)
            iw,ih=img.size[0],img.size[1]
            if iw>maxw:
               maxw=iw
            maxh=maxh+ih
            del img
            li.append([iw*ih,ih,iw,afname,afnameimage])
      cp=CygonRectanglePacker(maxw,maxh)
      li.sort()
      for ia,ih,iw,afname,afnameimage in li:
         p=cp.Pack(iw,ih)
         itm=SpriteItem(afname,afnameimage,'ics_'+acssclassbasename+'_'+os.path.basename(afname).replace(".","_").replace(" ","_"),p.x,p.y,p.x+iw,p.y+ih)
         self.sprites[afname]=itm
         self.xsize=max(self.xsize,itm.r)
         self.ysize=max(self.ysize,itm.b)
      self.xsize=1+self.xsize
      self.ysize=1+self.ysize
   def HtmlDemo(self,imgfile):
      r="<html><head></head><body>\n"
      for s in self.sprites.values():
        r+="<h1>%s</h1>\n"%s.filenameimage
        r+="<style>%s</style>\n"%s.CssRule(imgfile)
        r+="<p><pre>%s</pre></p>\n"%s.CssRule(s.filenameimage)
        r+="<div class='%s'></div>\n\n"%s.cssclass
      r+="</body></html>\n"
      return r
   def Save(self,afnameimage1,afnameimage2,afnamehtml=''):
      return #$$
      img=Image.new("RGBA",(self.xsize,self.ysize))
      for s in self.sprites.values():
         s.DrawTo(img)
      img.save(afnameimage1+afnameimage2)
      del img
      if afnamehtml:
         fout=open(afnamehtml,'w')
         fout.write(self.HtmlDemo(afnameimage2))
         fout.close()

def main():
   builder=SpriteBuilder()
   l=[os.path.join(sys.argv[1],x) for x in os.listdir(sys.argv[1])]
   builder.Parse(l)
   builder.Save(sys.argv[2],sys.argv[3])

##############################################################################################
"""This library is free software; you can redistribute it and/or
modify it under the terms of the IBM Common Public License as
published by the IBM Corporation; either version 1.0 of the
License, or (at your option) any later version.
 
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
IBM Common Public License for more details.
 
You should have received a copy of the IBM Common Public
License along with this library
"""
from bisect import bisect_left
 
class OutOfSpaceError(Exception): pass
 
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
    def __cmp__(self, other):
        """Compares the starting position of height slices"""
        return self.x - other.x
 
class RectanglePacker(object):
    """Base class for rectangle packing algorithms
 
    By uniting all rectangle packers under this common base class, you can
    easily switch between different algorithms to find the most efficient or
    performant one for a given job.
 
    An almost exhaustive list of packing algorithms can be found here:
    http://www.csc.liv.ac.uk/~epa/surveyhtml.html"""
 
    def __init__(self, packingAreaWidth, packingAreaHeight):
        """Initializes a new rectangle packer
 
        packingAreaWidth: Maximum width of the packing area
        packingAreaHeight: Maximum height of the packing area"""
        self.packingAreaWidth = packingAreaWidth
        self.packingAreaHeight = packingAreaHeight
 
    def Pack(self, rectangleWidth, rectangleHeight):
        """Allocates space for a rectangle in the packing area
 
        rectangleWidth: Width of the rectangle to allocate
        rectangleHeight: Height of the rectangle to allocate
 
        Returns the location at which the rectangle has been placed"""
        point = self.TryPack(rectangleWidth, rectangleHeight)
 
        if not point:
            raise OutOfSpaceError("Rectangle does not fit in packing area")
 
        return point
 
    def TryPack(self, rectangleWidth, rectangleHeight):
        """Tries to allocate space for a rectangle in the packing area
 
        rectangleWidth: Width of the rectangle to allocate
        rectangleHeight: Height of the rectangle to allocate
 
        Returns a Point instance if space for the rectangle could be allocated
        be found, otherwise returns None"""
        raise NotImplementedError
 
class CygonRectanglePacker(RectanglePacker):
    """
    Packer using a custom algorithm by Markus 'Cygon' Ewald
 
    Algorithm conceived by Markus Ewald (cygon at nuclex dot org), though
    I'm quite sure I'm not the first one to come up with it :)
 
    The algorithm always places rectangles as low as possible in the packing
    area. So, for any new rectangle that is to be added, the packer has to
    determine the X coordinate at which the rectangle can have the lowest
    overall height without intersecting any other rectangles.
 
    To quickly discover these locations, the packer uses a sophisticated
    data structure that stores the upper silhouette of the packing area. When
    a new rectangle needs to be added, only the silouette edges need to be
    analyzed to find the position where the rectangle would achieve the lowest"""
 
    def __init__(self, packingAreaWidth, packingAreaHeight):
        """Initializes a new rectangle packer
 
        packingAreaWidth: Maximum width of the packing area
        packingAreaHeight: Maximum height of the packing area"""
        RectanglePacker.__init__(self, packingAreaWidth, packingAreaHeight)
 
        # Stores the height silhouette of the rectangles
        self.heightSlices = []
 
        # At the beginning, the packing area is a single slice of height 0
        self.heightSlices.append(Point(0,0))
 
    def TryPack(self, rectangleWidth, rectangleHeight):
        """Tries to allocate space for a rectangle in the packing area
 
        rectangleWidth: Width of the rectangle to allocate
        rectangleHeight: Height of the rectangle to allocate
 
        Returns a Point instance if space for the rectangle could be allocated
        be found, otherwise returns None"""
        placement = None
 
        # If the rectangle is larger than the packing area in any dimension,
        # it will never fit!
        if rectangleWidth > self.packingAreaWidth or rectangleHeight > \
        self.packingAreaHeight:
            return None
 
        # Determine the placement for the new rectangle
        placement = self.tryFindBestPlacement(rectangleWidth, rectangleHeight)
 
        # If a place for the rectangle could be found, update the height slice
        # table to mark the region of the rectangle as being taken.
        if placement:
            self.integrateRectangle(placement.x, rectangleWidth, placement.y \
            + rectangleHeight)
 
        return placement
 
    def tryFindBestPlacement(self, rectangleWidth, rectangleHeight):
        """Finds the best position for a rectangle of the given dimensions
 
        rectangleWidth: Width of the rectangle to find a position for
        rectangleHeight: Height of the rectangle to find a position for
 
        Returns a Point instance if a valid placement for the rectangle could
        be found, otherwise returns None"""
        # Slice index, vertical position and score of the best placement we
        # could find
        bestSliceIndex = -1 # Slice index where the best placement was found
        bestSliceY = 0 # Y position of the best placement found
        # lower == better!
        bestScore = self.packingAreaWidth * self.packingAreaHeight 
 
        # This is the counter for the currently checked position. The search
        # works by skipping from slice to slice, determining the suitability
        # of the location for the placement of the rectangle.
        leftSliceIndex = 0
 
        # Determine the slice in which the right end of the rectangle is located
        rightSliceIndex = bisect_left(self.heightSlices, Point(rectangleWidth, 0))
        if rightSliceIndex < 0:
            rightSliceIndex = ~rightSliceIndex
 
        while rightSliceIndex <= len(self.heightSlices):
            # Determine the highest slice within the slices covered by the
            # rectangle at its current placement. We cannot put the rectangle
            # any lower than this without overlapping the other rectangles.
            highest = self.heightSlices[leftSliceIndex].y
            for index in xrange(leftSliceIndex + 1, rightSliceIndex):
                if self.heightSlices[index].y > highest:
                    highest = self.heightSlices[index].y
 
            # Only process this position if it doesn't leave the packing area
            if highest + rectangleHeight < self.packingAreaHeight:
                score = highest
 
                if score < bestScore:
                    bestSliceIndex = leftSliceIndex
                    bestSliceY = highest
                    bestScore = score
 
            # Advance the starting slice to the next slice start
            leftSliceIndex += 1
            if leftSliceIndex >= len(self.heightSlices):
                break
 
            # Advance the ending slice until we're on the proper slice again,
            # given the new starting position of the rectangle.
            rightRectangleEnd = self.heightSlices[leftSliceIndex].x + rectangleWidth
            while rightSliceIndex <= len(self.heightSlices):
                if rightSliceIndex == len(self.heightSlices):
                    rightSliceStart = self.packingAreaWidth
                else:
                    rightSliceStart = self.heightSlices[rightSliceIndex].x
 
                # Is this the slice we're looking for?
                if rightSliceStart > rightRectangleEnd:
                    break
 
                rightSliceIndex += 1
 
            # If we crossed the end of the slice array, the rectangle's right
            # end has left the packing area, and thus, our search ends.
            if rightSliceIndex > len(self.heightSlices):
                break
 
        # Return the best placement we found for this rectangle. If the
        # rectangle didn't fit anywhere, the slice index will still have its
        # initialization value of -1 and we can report that no placement
        # could be found.
        if bestSliceIndex == -1:
            return None
        else:
            return Point(self.heightSlices[bestSliceIndex].x, bestSliceY)
 
    def integrateRectangle(self, left, width, bottom):
        """Integrates a new rectangle into the height slice table
 
        left: Position of the rectangle's left side
        width: Width of the rectangle
        bottom: Position of the rectangle's lower side"""
        # Find the first slice that is touched by the rectangle
        startSlice = bisect_left(self.heightSlices, Point(left, 0))
 
        # Did we score a direct hit on an existing slice start?
        if startSlice >= 0:
            # We scored a direct hit, so we can replace the slice we have hit
            firstSliceOriginalHeight = self.heightSlices[startSlice].y
            self.heightSlices[startSlice] = Point(left, bottom)
        else: # No direct hit, slice starts inside another slice
            # Add a new slice after the slice in which we start
            startSlice = ~startSlice
            firstSliceOriginalHeight = self.heightSlices[startSlice - 1].y
            self.heightSlices.insert(startSlice, Point(left, bottom))
 
        right = left + width
        startSlice += 1
 
        # Special case, the rectangle started on the last slice, so we cannot
        # use the start slice + 1 for the binary search and the possibly
        # already modified start slice height now only remains in our temporary
        # firstSliceOriginalHeight variable
        if startSlice >= len(self.heightSlices):
            # If the slice ends within the last slice (usual case, unless it
            # has the exact same width the packing area has), add another slice
            # to return to the original height at the end of the rectangle.
            if right < self.packingAreaWidth:
                self.heightSlices.append(Point(right, firstSliceOriginalHeight))
        else: # The rectangle doesn't start on the last slice
            endSlice = bisect_left(self.heightSlices, Point(right,0), \
            startSlice, len(self.heightSlices))
 
            # Another direct hit on the final slice's end?
            if endSlice > 0:
                del self.heightSlices[startSlice:endSlice]
            else: # No direct hit, rectangle ends inside another slice
                # Make index from negative bisect_left() result
                endSlice = ~endSlice
 
                # Find out to which height we need to return at the right end of
                # the rectangle
                if endSlice == startSlice:
                    returnHeight = firstSliceOriginalHeight
                else:
                    returnHeight = self.heightSlices[endSlice - 1].y
 
                # Remove all slices covered by the rectangle and begin a new
                # slice at its end to return back to the height of the slice on
                # which the rectangle ends.
                del self.heightSlices[startSlice:endSlice]
                if right < self.packingAreaWidth:
                    self.heightSlices.insert(startSlice, Point(right, returnHeight))

#if __name__=='__main__':
#   main()

