from __future__ import division # allows floating point division from integers
import FreeCAD, Part, math
from FreeCAD import Base

class WankelBlock:
    def __init__(self, obj):
        ''' Add the properties: Radius, Eccentricity, Height, Segments (see Property View) '''
        obj.addProperty("App::PropertyLength","Radius","Wankel","Base radius").Radius=60.0
        obj.addProperty("App::PropertyLength","Eccentricity","Wankel","Rotor eccentricity").Eccentricity=12.0
        obj.addProperty("App::PropertyLength","Height","Wankel","Height of the block").Height=30.0
        obj.addProperty("App::PropertyLength","Segments","Wankel","Number of the line segments").Segments=72
        obj.Proxy = self

    def onChanged(self, fp, prop): 
        if prop == "Radius" or prop == "Eccentricity" or prop == "Height" or prop == "Segments": #if one of these is changed
            self.execute(fp)

    def execute(self, fp): #main part of script
        steps=int(fp.Segments) #get value from property
        dang=math.radians(360/steps)
        e=fp.Eccentricity
        r=fp.Radius
        h=fp.Height
        ang=0
        z=0
        halfw=r+e+20
        halfh=r+e+20

        for i in range(steps):
            if i==0:
                x1=e*math.cos(3*ang)+r*math.cos(ang) #coords for line startpoint
                y1=e*math.sin(3*ang)+r*math.sin(ang)
                ang=dang 
                x2=e*math.cos(3*ang)+r*math.cos(ang) #coords for line endpoint
                y2=e*math.sin(3*ang)+r*math.sin(ang)
                seg=Part.makeLine((x1,y1,z),(x2,y2,z))
                wire2=Part.Wire([seg])
                x1=x2
                y1=y2
            else:
                x2=e*math.cos(3*ang)+r*math.cos(ang)
                y2=e*math.sin(3*ang)+r*math.sin(ang)
                seg=Part.makeLine((x1,y1,z),(x2,y2,z))
                wire2=Part.Wire([wire2,seg])
                x1=x2
                y1=y2
            ang=ang+dang #increment angle
        edge1 = Part.makeLine((-halfw,halfh,0), (halfw,halfh,0)) #lines needed to create rectangle
        edge2 = Part.makeLine((halfw,halfh,0), (halfw,-halfh,0))
        edge3 = Part.makeLine((halfw,-halfh,0), (-halfw,-halfh,0))
        edge4 = Part.makeLine((-halfw,-halfh,0), (-halfw,halfh,0))
        wire1 = Part.Wire([edge1,edge2,edge3,edge4]) #rectangle
        face1 = Part.Face(wire1) #face from rectangle
        face2=Part.Face(wire2) #face from epitrochoid http://en.wikipedia.org/wiki/Epitrochoid
        diff = face1.cut(face2) #boolean cut epitrochoid from rectangle
        ext=diff.extrude(Base.Vector(0,0,h)) #extrude the cut (face)
        fp.Shape = ext #result shape

def makeWankelBlock():
    doc = FreeCAD.activeDocument()
    if doc == None:
        doc = FreeCAD.newDocument()
    wankelblock=doc.addObject("Part::FeaturePython","Wankel_Block") #add object to document
    wankelblock.Label = "Wankel Block"
    WankelBlock(wankelblock)
    wankelblock.ViewObject.Proxy=0

if __name__ == "__main__": #feature will be generated after macro execution
    makeWankelBlock()
