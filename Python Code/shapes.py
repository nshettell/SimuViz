import math

class Cylinder_plain:
    def __init__(self,begin,end):
        self.i1=begin[0]
        self.i2=end[0]
        self.j1=begin[1]
        self.j2=end[1]
        self.k1=begin[2]
        self.k2=end[2]
    def msg(self):
        return """cylinder {<%f,%f,%f>, <%f,%f,%f>, 0.055
texture{pigment{color Gray85 transmit 0.2} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(self.i1,self.j1,self.k1,self.i2,self.j2,self.k2)
################################################################################       
class Sphere_C:
    def __init__(self,spin,pos,trans_factor):
        self.colour='Red' if spin==1 else 'Blue'
        self.trans=trans_factor
        self.i=pos[0]
        self.j=pos[1]
        self.k=pos[2]
    def msg(self):
        return """sphere {<%f,%f,%f>, 0.25
texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(self.i,self.j,self.k,self.colour,self.trans)
################################################################################
class Arrow:
    def __init__(self,spin,pos,trans_factor):
        self.rotate='<45,-45,0>' if spin==1 else '<-45,135,0>'
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
texture{pigment{color Green transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}
rotate %s
translate <%f,%f,%f>}
""" %(self.trans,self.rotate,self.i,self.j,self.k)
################################################################################
class Arrow_C:
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
################################################################################
class Dimer_C:
    def __init__(self,spin,pos,trans_factor):
        self.i1=pos[0][0]
        self.i2=pos[1][0]
        self.j1=pos[0][1]
        self.j2=pos[1][1]
        self.k1=pos[0][2]
        self.k2=pos[1][2]
        self.colour='NavyBlue' if spin==1 else 'Cyan'
        self.trans=trans_factor
        self.d=math.sqrt((self.i2-self.i1)**2+(self.j2-self.j1)**2+(self.k2-self.k1)**2)
    def msg(self):
        if self.i1==self.i2 and self.j1==self.j2:
            zr=0
        elif self.i1==self.i2:
            zr=90
        else:
            zr=math.atan((self.j2-self.j1)/(self.i2-self.i1))*180/math.pi
            
        if self.i1==self.i2 and self.k1==self.k2:
            yr=0
        elif self.i1==self.i2:
            yr=90
        else:
            yr=math.atan((self.k2-self.k1)/(self.i2-self.i1))*180/math.pi
            
        scale="<%f,%f,%f>" %(self.d/2,self.d/8,self.d/8)
        rot="<0,%f,%f>" %(yr,zr)
        center="<%f,%f,%f>" %((self.i1+self.i2)/2.0,(self.j1+self.j2)/2.0,(self.k1+self.k2)/2.0)
        
        return """sphere {
0,1 scale %s
rotate %s
translate %s
texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(scale,rot,center,self.colour,self.trans)
################################################################################
class Cylinder_C:
    def __init__(self,spin,pos,trans_factor):
        self.i1=pos[0][0]
        self.i2=pos[0][1]
        self.j1=pos[1][0]
        self.j2=pos[1][1]
        self.k1=pos[2][0]
        self.k2=pos[2][1]
        self.colour='NavyBlue' if spin==1 else 'Cyan'
        self.trans=trans_factor
    def msg(self):        
        return """cylinder {
<%f,%f,%f>, <%f,%f,%f>, 0.25
texture{pigment{color %s transmit %f} finish{ambient 0.1 diffuse 0.3 phong 0.6 phong_size 20}}}
""" %(self.i1,self.j1,self.k1,self.i2,self.j2,self.k2,self.colour,self.trans)