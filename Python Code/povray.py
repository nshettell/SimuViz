from lattice import *

def general_info():
    return """
//Visual Representation of an Ising model Square Lattice
//Version 2.2
//Author: Nathan Shettell

#include "shapes.inc"
#include "textures.inc"
#include "colors.inc"

global_settings { assumed_gamma 1}
background {Black}
"""
################################################################################
def camera_info(axis,offset,Lx,Ly,Lz,bx,by,bz):
    if axis=='x':
        m=-max(Vector(by).magnitude()*Ly,Vector(bz).magnitude()*Lz)
        if offset=='none':
            loc=Vector([0,0,0]).translate({tuple(bx):1.2*m,tuple(by):0.5*Ly,tuple(bz):0.5*Lz})
        elif offset=='small':
            loc=Vector([0,0,0]).translate({tuple(bx):1.2*m,tuple(by):0.8*Ly,tuple(bz):0.8*Lz})
        else:
            loc=Vector([0,0,0]).translate({tuple(bx):1.5*m,tuple(by):1.2*Ly,tuple(bz):1.2*Lz})
    elif axis=='y':
        m=-max(Vector(bx).magnitude()*Lx,Vector(bz).magnitude()*Lz)
        if offset=='none':
            loc=Vector([0,0,0]).translate({tuple(bx):0.5*Lx,tuple(by):1.2*m,tuple(bz):0.5*Lz})
        elif offset=='small':
            loc=Vector([0,0,0]).translate({tuple(bx):0.8*Lx,tuple(by):1.2*m,tuple(bz):0.8*Lz})
        else:
            loc=Vector([0,0,0]).translate({tuple(bx):1.2*Lx,tuple(by):1.5*m,tuple(bz):1.2*Lz})
    elif axis=='z':
        m=-max(Vector(bx).magnitude()*Lx,Vector(by).magnitude()*Ly)
        if offset=='none':
            loc=Vector([0,0,0]).translate({tuple(bx):0.5*Lx,tuple(by):0.5*Ly,tuple(bz):1.2*m})
        elif offset=='small':
            loc=Vector([0,0,0]).translate({tuple(bx):0.8*Lx,tuple(by):0.8*Ly,tuple(bz):1.2*m})
        else:
            loc=Vector([0,0,0]).translate({tuple(bx):1.2*Lx,tuple(by):1.2*Ly,tuple(bz):1.5*m})
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
        msg+="light_source{<%f,%f,%f>,White}\n"%(l[0],l[1],l[2])
    return msg