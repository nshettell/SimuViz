from lattice import *

def general_info(Bkg):
    return """
//POV-Ray animation pov file
//Visual Representation of a Lattice
//Version 3.0
//Author: Nathan Shettell

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings {assumed_gamma 1}
background {%s}

""" %(Bkg)
################################################################################
def camera_info(cam,Lx,Ly,Lz,bx,by,bz):
    m=-max(Vector(bx).magnitude()*Lx,Vector(by).magnitude()*Ly)
    if cam=='centered':
        loc=Vector([0,0,0]).translate({tuple(bx):0.5*Lx,tuple(by):0.5*Ly,tuple(bz):1.2*m})
    elif cam=='slight offset':
        loc=Vector([0,0,0]).translate({tuple(bx):0.8*Lx,tuple(by):0.8*Ly,tuple(bz):1.2*m})
    elif cam=='large offset':
        loc=Vector([0,0,0]).translate({tuple(bx):1.2*Lx,tuple(by):1.2*Ly,tuple(bz):1.5*m})
    else:
        loc=cam
    look=Vector([0,0,0]).translate({tuple(bx):0.5*Lx,tuple(by):0.5*Ly,tuple(bz):0.5*Lz})
    
    loc="<%f,%f,%f>"%(loc[0],loc[1],loc[2])
    look="<%f,%f,%f>"%(look[0],look[1],look[2])
    return """

camera {
    location %s
    look_at %s}
""" %(loc,look)
################################################################################
def light_info(light):
    msg=""
    for l in light:
        msg+="light_source{%s,White}\n" %(l)
    return msg