from math import *

def x(u,v):
    return (8+2*cos(u))*cos(v)

def y(u,v):
    return (8+2*cos(u))*sin(v)

def z(u,v):
    return 2*sin(u)

USET=[2*pi*n/24 for n in range(25)]
VSET=[2*pi*n/96 for n in range(98)]

msg=""
for i in range(24):
    for j in range(96):
        if i%2==0:
            u1=USET[i]
            u2=USET[i+1]
            v1=VSET[j]
            v2=0.5*(VSET[j]+VSET[j+1])
            v3=VSET[j+1]
            v4=0.5*(v3+VSET[j+2])
        else:
            u1=USET[i]
            u2=USET[i+1]
            v1=0.5*(VSET[j]+VSET[j+1])
            v2=VSET[j+1]
            v3=0.5*(v2+VSET[j+2])
            v4=VSET[j+2]
        c1='<%f,%f,%f>'%(x(u1,v1),y(u1,v1),z(u1,v1))
        c2='<%f,%f,%f>'%(x(u2,v2),y(u2,v2),z(u2,v2))
        c3='<%f,%f,%f>'%(x(u1,v3),y(u1,v3),z(u1,v3))
        c4='<%f,%f,%f>'%(x(u2,v4),y(u2,v4),z(u2,v4))
        msg+="""
triangle{%s, %s, %s texture{pigment{color Blue transmit 0.3} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
triangle{%s, %s, %s texture{pigment{color Blue transmit 0.3} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(c1,c2,c3,c2,c3,c4)
        if i%4==0 and j%2==0 or i%4==2 and j%2==1:
            msg+="""
cylinder {%s, %s, 0.05 texture{pigment{color Black} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
cylinder {%s, %s, 0.05 texture{pigment{color Black} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
cylinder {%s, %s, 0.05 texture{pigment{color Black} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
"""%(c1,c2,c1,c3,c2,c3)
        elif i%4==1 and j%2==1 or i%4==3 and j%2==0:
            msg+="""
cylinder {%s, %s, 0.05 texture{pigment{color Black} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
cylinder {%s, %s, 0.05 texture{pigment{color Black} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
cylinder {%s, %s, 0.05 texture{pigment{color Black} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
"""%(c2,c3,c2,c4,c3,c4)

imsg="""
Antialias=Off
Antialias_Threshold=0.1
Antialias_Depth=2
Display=Off
+W1600
+H1200
Input_File_Name='torus3.pov'
Output_File_Type=N
Initial_Frame=1
Final_Frame=1
Initial_Clock=0
Final_Clock=1
Cyclic_Animation=on
Pause_when_Done=off    
"""

general="""
#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings { assumed_gamma 1}
background {White}

camera {
    location <0,-30,10>
    look_at <0,0,0>
    rotate <0,0,115>}
    
light_source{<0,0,0>,White}
light_source{<10,8,0>,White}
light_source{<-10,8,0>,White}
light_source{<0,0,3>,White}
light_source{<0,0,-3>,White}
light_source{<5,18,-3>,White}
light_source{<5,-18,-3>,White}

"""
def torus(msg,imsg,cam):
    p=open('torus3.pov','w')
    i=open('torus3.ini','w')
    
    i.write(imsg)
    i.close()
    
    p.write(cam)
    p.write(msg)
    p.close()
torus(msg,imsg,general)