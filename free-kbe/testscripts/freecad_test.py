from __future__ import division # allows floating point division from integers
import FreeCAD, FreeCADGui, Part 
from FreeCAD import Base
import math
steps=360 #number of polyline segments
dang=math.radians(360/steps) #step angle
e=10 #eccentricity
r=60 #radius
ang=0 #start anle
z=0 #line z coordinate
halfw=r+e+20
halfh=r+e+20

for i in range(steps): #make many lines and connect they in wire (polyline, epitrochoid)
    if i==0: #for first line
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
ext=diff.extrude(Base.Vector(0,0,30)) #extrude the cut (face)
Part.show(ext) #show extrude in FreeCAD window