import math

class Sphere:
    def __init__(self,location,radius,colour,transparency):
        self.loc='<%f,%f,%f>' %(location[0],location[1],location[2])
        self.r=radius
        self.c=colour
        self.trans=transparency
    def msg(self):
        return """sphere {%s, %f
texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(self.loc,self.r,self.c,self.trans)
################################################################################
class Cylinder:
    def __init__(self,front,back,radius,colour,transparency):
        self.e1='<%f,%f,%f>' %(front[0],front[1],front[2])
        self.e2='<%f,%f,%f>' %(back[0],back[1],back[2])
        self.r=radius
        self.c=colour
        self.trans=transparency
    def msg(self):
        return """cylinder {%s, %s, %f
texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(self.e1,self.e2,self.r,self.c,self.trans)
################################################################################
class Dimer:
    def __init__(self,front,back,radius,colour,transparency):
        self.center='<%f,%f,%f>' %((front[0]+back[0])/2.0,(front[1]+back[1])/2.0,(front[2]+back[2])/2)
        self.z_rotate=0 if front[0]==back[0] and front[1]==back[1] else 90 if front[0]==back[0]\
            else math.atan((back[1]-front[1])/(back[0]-front[0]))*180/math.pi
        self.y_rotate=0 if front[0]==back[0] and front[2]==back[2] else 90 if front[0]==back[0]\
            else math.atan((back[2]-front[2])/(back[0]-front[0]))*180/math.pi
        self.rotate='<0,%f,%f>' %(self.y_rotate,self.z_rotate)
        self.size=math.sqrt((back[0]-front[0])**2+(back[1]-front[1])**2+(back[2]-front[2])**2)
        self.r=radius
        self.scale='<%f,%f,%f>' %(self.size/2.0,self.r,self.r)
        self.c=colour
        self.trans=transparency
    def msg(self):
        return """sphere {
0,1 scale %s
rotate %s
translate %s
texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(self.scale,self.rotate,self.center,self.c,self.trans)
################################################################################
class Triangle:
    def __init__(self,corner1,corner2,corner3,colour,transparency):
        self.c1='<%f,%f,%f>' %(corner1[0],corner1[1],corner1[2])
        self.c2='<%f,%f,%f>' %(corner2[0],corner2[1],corner2[2])
        self.c3='<%f,%f,%f>' %(corner3[0],corner3[1],corner3[2])
        self.c=colour
        self.trans=transparency
    def msg(self):
        return """
triangle{%s, %s, %s texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(self.c1,self.c2,self.c3,self.c,self.trans)
    
    

#HERE IS AN OLD CLASS THAT I HAVEN'T UPDATED YET, IT IS AN ARROW AND WAS USED AS A SITE REPRESENTATION:
class Arrow:
    def __init__(self,spin,pos,trans_factor):
        self.rotate='<45,-45,0>' if spin==1 else '<-45,135,0>'
        self.colour='Red' if spin==1 else 'Blue'
        self.trans=trans_factor
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def msg(self):
        return """union {
cylinder{
    <0,0,0.25>,<0,0,-0.25>,0.17}
cone{
    <0,0,-0.25>, 0.28
    <0,0,-0.5>, 0}
texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}
rotate %s
translate <%f,%f,%f>}
""" %(self.colour,self.trans,self.rotate,self.i,self.j,self.k)