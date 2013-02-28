from configuration import ini_creator
from shapes import *
from user_questions import *
from povray import *
from lattice import *
import multiprocessing
import os
import sys
import glob
import commands
import time

def start_sites(file_info,lattice_info,directory,res=[1600,1200]):
    """
    Version 2.1
    This function must intake 3 parameter:
    
    file_info: The name of the file the spin information is found on.
    All of the following lines should contain information about the spin objects at certain
    positions in the Lattice. After the script has encountered enough spin objects to fill the
    lattice it will assume the rest of the objects belong on following frames.
    
    lattice_info: The name of the file the information about the lattice if found.
    There is a very specific template the file shouls follow. Please see an example
    for instructions on how to create a file.

    directory: The desired name for the directory of all the files to be outputted in.
    All the files in the directory will have a similar name with different extensions.
    name but with varying extensions.
    
    The optional parameter determines the resolution of the images created. The default is 640x480.
    To view the other options please call the function: poss_resolutions().
    It must be entered in the form: [W,H]. Where W and H are integers (image witdth and height)
    when the different resolutions are printed they are in the form WxH.
    If a valid resolution is not entered, the default will be used.
    """
    
    #The file which will be accessed during the script
    f_i=open(file_info,'r')
    f_l=open(lattice_info,'r')
    
    OS='OS X' if os.name=='posix' else 'Linux' if sys.platform=='linux2' else 'Windows' #Determine the operating system
    #Create a directory to store all the files as well as a .pov file:
    if OS=='Windows': #Different os systems use different path names
        sc='\\'
        D=os.getcwd()+sc+directory
        os.mkdir(D)
        exe=open(D+sc+'execute.bat','w')
    else:
        sc='/'
        D=os.getcwd()+sc+directory
        os.mkdir(D)
        exe=open(D+sc+'execute','w')
    pov=open(D+sc+directory+'.pov','w')
    
    #Gather information about the lattice size
    l_info=f_l.readlines()
    Lx,Ly,Lz=size(l_info[0]) #Size of lattice
    Site,l_info=site(l_info[2:]) #Lattice site co-ordinates
    bx,by,bz=vectors(l_info) #Lattice vectors
    Bonds=bonds(l_info[4:]) #Bond locations

    Lattice=l_dict(Lx,Ly,Lz,bx,by,bz,Site)
    #Note:
    #Lattice is a dictionary where the keys are position of spin sites and the value
    #is a list of all spins at that location.
    mx,my,mz=extrema(Lattice)
    #maximum x y and z co-ordinate (needed to ensure no bonds are placed that are attached to only one site)
    Bonds=bond_list(Lx,Ly,Lz,mx,my,mz,bx,by,bz,Bonds)

    info=filter(lambda i: i!='\n' and '#' not in i, f_i.readlines())
    info=[i.split() for i in info]
    I=[]
    for i in info:
        I+=[int(spin) for spin in i]
    Lattice,counter=l_spin(Lx,Ly,Lz,bx,by,bz,Site,Lattice,I)
            
    Lights=light_list(Lx,Ly,Lz,bx,by,bz,Site)

    #All of the data has been analyzed and the files can be closed:
    f_i.close()
    f_l.close()

    #Gather more information from the user:
    offset=offset_q()
    cam=cam_q()
    image=image_q()
    spinrep=spinrep_q_sites()
    trans=transparency_q()
    processors=processors_q(multiprocessing.cpu_count())
    fps=fps_q()
    res=[1600,1200] if res not in resolutions() else res
    
    #Create all of the .ini files:
    for i in range(1,processors+1):
        first_frame=1+counter*(i-1)/processors
        final_frame=counter*i/processors
        
        tmp=open(D+sc+directory+" - "+str(i)+'.ini','w')
        tmp.write(ini_creator(first_frame,final_frame,res,image,directory+'.pov'))
        tmp.close()
        
        if OS=='Windows':
            exe.write("pvengine /render '%s' &\n" %(directory+' - '+str(i)+'.ini'))
        else:
            exe.write("povray '%s' +I'%s' &\n" %(directory+' - '+str(i)+'.ini',directory+'.pov'))    
    exe.close()
    
    #Create the .pov file
    #First add greneral and camera info about the camera
    pov.write(general_info())
    pov.write(camera_info(cam,offset,Lx,Ly,Lz,bx,by,bz))
    pov.write(light_info(Lights))
    
    #Add the sphapes to the image
    frame=1
    while frame<=counter:
        if counter!=1:
            pov.write("#if (frame_number = %d)\n" %(frame))
        for pos in Lattice:
            if trans=="yes" and cam=='x' and Lx>1:
                t_factor=0.5-pos[0]*0.5/(Lx-1)
            elif trans=="yes" and cam=='y' and Ly>1:
                t_factor=0.5-pos[1]*0.5/(Ly-1)
            elif trans=="yes" and cam=='z' and Lz>0:
                t_factor=0.5-pos[2]*0.5/(Lz-1)
            else:
                t_factor=0
                    
            if spinrep=='colours':
                temp=Sphere_C(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
            elif spinrep=='arrows':
                temp=Arrow(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
            else:
                temp=Arrow_C(Lattice[pos][frame-1],(pos[0],pos[1],pos[2]),t_factor)
                pov.write(temp.msg())
        if counter!=1:
            pov.write("#end\n")
        frame+=1
        
    #Adds the cylinders ('bonds') to the image
    for pair in Bonds:
        temp=Cylinder_plain(pair[0],pair[1])
        pov.write(temp.msg())
    pov.close()
    
    #Start rendering the images
    if OS=='Windows':
        os.system("cd\ && cd %s && execute.bat" %(D))
    else:
        os.system("cd '%s' && . ./execute" %(D))
    
    time.sleep(15)
    while 'povray' in commands.getoutput('ps -A'):
        time.sleep(10)
    
    os.chdir('%s' %(directory))
    for f_name in glob.glob("*.%s" %(image)):
        num=f_name[len(directory):-len(image)-1]
        num=1 if num=='' else int(num)
        new="%s%.06d.%s" %(directory,num,image)
        os.system("mv '%s' '%s'" %(f_name,new))
    
    #Create the animation    
    os.system('convert -delay %f *.%s animation.gif' %(100.0/fps,image))
################################################################################
def start_bonds(file_info,lattice_info,directory,res=[1600,1200]):
    """
    Version 2.2
    This function must intake 3 parameter:
    
    file_info: The name of the file the spin information is found on.
    All of the following lines should contain information about the spin objects at certain
    positions in the Lattice. After the script has encountered enough spin objects to fill the
    lattice it will assume the rest of the objects belong on following frames.
    
    lattice_info: The name of the file the information about the lattice if found.
    There is a very specific template the file shouls follow. Please see an example
    for instructions on how to create a file.

    directory: The desired name for the directory of all the files to be outputted in.
    All the files in the directory will have a similar name with different extensions.
    name but with varying extensions.
    
    The optional parameter determines the resolution of the images created. The default is 640x480.
    To view the other options please call the function: poss_resolutions().
    It must be entered in the form: [W,H]. Where W and H are integers (image witdth and height)
    when the different resolutions are printed they are in the form WxH.
    If a valid resolution is not entered, the default will be used.
    """
    
    #The file which will be accessed during the script
    f_i=open(file_info,'r')
    f_l=open(lattice_info,'r')
    
    OS='OS X' if os.name=='posix' else 'Linux' if sys.platform=='linux2' else 'Windows' #Determine the operating system
    #Create a directory to store all the files as well as a .pov file:
    if OS=='Windows': #Different os systems use different path names
        sc='\\'
        D=os.getcwd()+sc+directory
        os.mkdir(D)
        exe=open(D+sc+'execute.bat','w')
    else:
        sc='/'
        D=os.getcwd()+sc+directory
        os.mkdir(D)
        exe=open(D+sc+'execute','w')
    pov=open(D+sc+directory+'.pov','w')
    
    #Gather information about the lattice size
    l_info=f_l.readlines()
    Lx,Ly,Lz=size(l_info[0]) #Size of lattice
    bx,by,bz=vectors(l_info[2:]) #Lattice vectors
    Bonds=bonds(l_info[6:]) #Bond locations
                
    BLattice=b_dict(Lx,Ly,Lz,bx,by,bz,Bonds)

    info=filter(lambda i: i!='\n' and '#' not in i, f_i.readlines())
    info=[i.split() for i in info]
    I=[]
    for i in info:
        I+=[int(spin) for spin in i]
    BLattice,counter=b_spin(Lx,Ly,Lz,bx,by,bz,Bonds,BLattice,I)
            
    Lights=b_light_list(Lx,Ly,Lz,bx,by,bz,Bonds)

    #All of the data has been analyzed and the files can be closed:
    f_i.close()
    f_l.close()

    #Gather more information from the user:
    offset=offset_q()
    cam=cam_q()
    image=image_q()
    spinrep=spinrep_q_bonds()
    trans=transparency_q()
    processors=processors_q(multiprocessing.cpu_count())
    fps=fps_q()
    res=[1600,1200] if res not in resolutions() else res
    
    #Create all of the .ini files:
    for i in range(1,processors+1):
        first_frame=1+counter*(i-1)/processors
        final_frame=counter*i/processors
        
        tmp=open(D+sc+directory+" - "+str(i)+'.ini','w')
        tmp.write(ini_creator(first_frame,final_frame,res,image,directory+'.pov'))
        tmp.close()
        
        if OS=='Windows':
            exe.write("pvengine /render '%s' &\n" %(directory+' - '+str(i)+'.ini'))
        else:
            exe.write("povray '%s' +I'%s' &\n" %(directory+' - '+str(i)+'.ini',directory+'.pov'))    
    exe.close()
    
    #Create the .pov file
    #First add greneral and camera info about the camera
    pov.write(general_info())
    pov.write(camera_info(cam,offset,Lx,Ly,Lz,bx,by,bz))
    pov.write(light_info(Lights))
    
    #Add the sphapes to the image
    frame=1
    while frame<=counter:
        if counter!=1:
            pov.write("#if (frame_number = %d)\n" %(frame))
        for pos in BLattice:
            if trans=="yes" and cam=='x' and Lx>1:
                t_factor=0.5-pos[0][0]*0.5/(Lx-1)
            elif trans=="yes" and cam=='y' and Ly>1:
                t_factor=0.5-pos[1][0]*0.5/(Ly-1)
            elif trans=="yes" and cam=='z' and Lz>0:
                t_factor=0.5-pos[2][0]*0.5/(Lz-1)
            else:
                t_factor=0
                    
            if spinrep=='dimers':
                temp=Dimer_C(BLattice[pos][frame-1],pos,t_factor)
                pov.write(temp.msg())
            else:
                temp=Cylinder_C(BLattice[pos][frame-1],pos,t_factor)
                pov.write(temp.msg())
        if counter!=1:
            pov.write("#end\n")
        frame+=1
    
    pov.close()
    
    #Start rendering the images
    if OS=='Windows':
        os.system("cd\ && cd %s && execute.bat" %(D))
    else:
        os.system("cd '%s' && . ./execute" %(D))
    
    time.sleep(15)
    while 'povray' in commands.getoutput('ps -A'):
        time.sleep(10)
    
    os.chdir('%s' %(directory))
    for f_name in glob.glob("*.%s" %(image)):
        num=f_name[len(directory):-len(image)-1]
        num=1 if num=='' else int(num)
        new="%s%.06d.%s" %(directory,num,image)
        os.system("mv '%s' '%s'" %(f_name,new))
    
    #Create the animation    
    os.system('convert -delay %f *.%s animation.gif' %(100.0/fps,image))