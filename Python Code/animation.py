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

def start(file_info,lattice_info,directory):
    """
    Version 3.0
    This function must intake 3 parameter:
    
    file_info: The name of the file the spin information is found on.
    All of the following lines should contain information about the spin objects at certain
    positions in the Lattice. After the script has encountered enough spin objects to fill the
    lattice it will assume the rest of the objects belong on following frames.
    
    lattice_info: The name of the file the information about the lattice if found.
    There is a very specific template the file shouls follow. Please see an example
    for instructions on how to create the file.

    directory: The desired name for the directory of all the files to be outputted in.
    All the files in the directory will have a similar name with different extensions.
    name but with varying extensions.
    """
    
    #Check to see if the directory already exists, if so stop the program:
    if os.path.isdir(directory):
        return 'The new directory name requested already exists, please try again'
    
    #The files which will be accessed during the script
    f_i=open(file_info,'r') #Data file
    f_l=open(lattice_info,'r') #Lattice file
    
    D=os.getcwd()+'/'+directory #Name of the new directory
    os.mkdir(D) #Create the new directory
    exe=open(D+'/'+'execute','w') #Name of the execution file
    pov=open(D+'/'+directory+'.pov','w') #Name of the .pov file
    
    #Gather information about the lattice size
    l_info=f_l.readlines()
    #Determine what kind of activity is present
    s_act='#Sites\n' in l_info or '#Sites\r\n' in l_info
    b_act='#Bonds_a\n' in l_info or '#Bonds_a\r\n' in l_info
    b_noact='#Bonds_na\n' in l_info or '#Bonds_na\r\n' in l_info
    p_act='#Plaquettes\n' in l_info or '#Plaquettes\r\n' in l_info
    
    Frames=int(l_info[0])
    Lx,Ly,Lz=size(l_info[1]) #Size of lattice
    bx,by,bz=vectors(l_info[3:]) #Lattice vectors
    if s_act: #If there is activity on sites, determine the co-ordinates
        i=index_locator(l_info,'#Sites\n','#Sites\r\n')
        Site=basis(l_info[i+1:])
        s_len=len(Site) #keep track of the number of sites with activity
    else:
        s_len=0
    if b_act: #Similary, the co-ordinates for the bonds need to be determined
        i=index_locator(l_info,'#Bonds_a\n','#Bonds_a\r\n')
        Bonds=basis(l_info[i+1:])
        b_len=len(Bonds) #keep track of the number of bonds with activity
    else: #Even the bonds don't have any ativity on them they still need to be located
        i=index_locator(l_info,'#Bonds_na\n','#Bonds_na\r\n')
        Bonds=basis(l_info[i+1:])
        b_len=0
    if p_act: #Finally, determine the co-ordinates of the plaquettes, if there are any
        i=index_locator(l_info,'#Plaquettes\n','#Plaquettes\r\n')
        Plaquettes=basis(l_info[i+1:])
        p_len=len(Plaquettes) #keep track of the number of plaquettes with activity
    else:
        p_len=0
    Total_len=s_len+b_len+p_len #keep track of the total amount of sites+bonds+plaquettes with activity
    
    f_l.close() #All of the data from the lattice file has been extracted
    
    #Extract info from the data file
    info=filter(lambda i: i!='\n' and i!='\r\n' and '#' not in i, f_i.readlines()) #Recall: All lines with a '#' are ignored
    info=[i.split() for i in info]
    I=[]
    for i in info:
        I+=[int(activity) for activity in i] #List of all the activity
    
    f_i.close() #All of the data has been analyzed and the data file can be closed
    
    #This is a check to ensure the amount of data expected is equal to the amount of data given
    if Total_len*Frames*Lx*Ly*Lz!=len(I):
        return """There is an error in the information provided, either in the lattice file or the data file.
The amount of data provided (number of entries in the data file) does not match the amount of data expected:
Lx*Ly*Lz*Frames*T where T is the total number of objects with activity defined on the lattice."""
    
    #Create activity lists specific to sites, bonds and plaquettes:
    if s_act:
        SI=[]
        for m in range(Frames*Lx*Ly*Lz):
            for n in range(s_len):
                SI+=[I[n+m*Total_len]]
    if b_act:
        BI=[]
        for m in range(Frames*Lx*Ly*Lz):
            for n in range(b_len):
                BI+=[I[s_len+n+m*Total_len]]
    if p_act:
        PI=[]
        for m in range(Frames*Lx*Ly*Lz):
            for n in range(p_len):
                PI+=[I[s_len+b_len+n+m*Total_len]]
    
    #Later we use the shortest bond length in calculations, it is calculated here:
    sbl=shortest(Bonds)
    #Now the user will be asked a series of questions regarding the desired output:
    
    #If there is activity on the sites these questions are asked
    if s_act:
        s_colour_0=colour_question('site',0)
        if s_colour_0!='None':
            s_size_0=size_question('site',0,0.1,0.4)
            s_trans_0=trans_question1('sites',0,0,0.25)
        s_colour_1=colour_question('site',1)
        if s_colour_1!='None':
            s_size_1=size_question('site',1,0.1,0.4)
            s_trans_1=trans_question1('sites',1,0,0.25)
    #If there is activity on the bonds these questions are asked
    if b_act:
        b_colour_0=colour_question('bond',0)
        if b_colour_0!='None':
            b_rep_0=rep_question(0)
            b_size_0=size_question('bond+act',0,0.05,0.35)
            b_trans_0=trans_question1('bonds',0,0,0.25)
        b_colour_1=colour_question('bond',1)
        if b_colour_1!='None':
            b_rep_1=rep_question(1)
            b_size_1=size_question('bond+act',1,0.05,0.35)
            b_trans_1=trans_question1('bonds',1,0,0.25)
    #If there is no activity on the bonds these question are asked
    else:
        b_colour=colour_question('bond_noact',0)
        if b_colour!='None':
            b_rep=rep_question('none')
            b_size=size_question('bond+noact',0,0.05,0.35)
            b_trans=trans_question1('bonds+noact',0,0,0.25)
    #If there is activity on the plaquettes these questions are asked
    if p_act:
        p_colour_0=colour_question('plaquette',0)
        if p_colour_0!='None':
            p_trans_0=trans_question1('plaquettes',0,0,0.25)
        p_colour_1=colour_question('plaquette',1)
        if p_colour_1!='None':
            p_trans_1=trans_question1('plaquettes',1,0,0.25)
    
    #General questions regarding everything else
    gen_trans=trans_question2()
    im_type=image_question()
    processors=processors_question(min(Frames/2,multiprocessing.cpu_count()))
    fps=fps_question()
    cam_location=camera_question()
    Bkg=colour_question('background',0)
    res=resolution_question()
    
    #Create all of the .ini files:
    for i in range(1,processors+1):
        first_frame=1+Frames*(i-1)/processors #determine the first and last frame each processor will be handling
        final_frame=Frames*i/processors
        
        tmp=open(D+'/'+directory+" - "+str(i)+'.ini','w') #Open the .ini file
        tmp.write(ini_creator(first_frame,final_frame,res,im_type,directory+'.pov')) #Writes to the .ini file
        tmp.close() #Close the .ini file
        
        exe.write("povray '%s' +I'%s' &\n" %(directory+' - '+str(i)+'.ini',directory+'.pov')) #Write to the execution file
    
    #After all of the .ini files have been created, the execution file will also be finished and can be closed
    exe.close()
    
    #Now its time to create the .pov file, first we will create a set of light locations to improve image quality:
    Lights=lights(Lx,Ly,Lz,bx,by,bz)
    
    #Add the general info, camera info and light info to the .pov file now:
    pov.write(general_info(Bkg))
    pov.write(camera_info(cam_location,Lx,Ly,Lz,bx,by,bz))
    pov.write(light_info(Lights))
    
    #Now to add the sites, bonds and plaquettes
    for frame in range(Frames):
        pov.write("\n#if (frame_number = %d)\n" %(frame+1))
        
        for i in range(Lx):
            for j in range(Ly):
                for k in range(Lz):
                    
                    #First look at the sites:
                    if s_act:
                        for s in range(s_len):
                            #Determine the activity
                            activity=SI[s+s_len*(i+Lx*(j+Ly*(k+Lz*frame)))]
                            
                            #Determine if theres any transparency
                            t_factor=0.5-k*0.5/(Lz-1) if gen_trans=='yes' else 0
                            
                            #Do stuff relating to an activity of zero:
                            if activity==0 and s_colour_0!='None':
                                t_factor+=s_trans_0
                                center=Vector(Site[s][0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                temp=Sphere(center,s_size_0*sbl,s_colour_0,t_factor)
                                pov.write(temp.msg())
                            #Do other stuff if the activity is one:
                            elif activity==1 and s_colour_1!='None':
                                t_factor+=s_trans_1
                                center=Vector(Site[s][0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                temp=Sphere(center,s_size_1*sbl,s_colour_1,t_factor)
                                pov.write(temp.msg())
                                
                    #Now look at the bonds (with activity):
                    if b_act:
                        for b in range(b_len):
                            #Determine the activity
                            activity=BI[b+b_len*(i+Lx*(j+Ly*(k+Lz*frame)))]
                            
                            #Determine if theres any transparency
                            t_factor=0.5-k*0.5/(Lz-1) if gen_trans=='yes' else 0
                            
                            #Do stuff relating to an activity of zero:
                            if activity==0 and b_colour_0!='None':
                                t_factor+=b_trans_0
                                end1=Vector(Bonds[b][0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                end2=Vector(Bonds[b][1]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                if b_rep_0=='cylinders':
                                    temp=Cylinder(end1,end2,b_size_0*sbl/2.0,b_colour_0,t_factor)
                                    pov.write(temp.msg())
                                else:
                                    temp=Dimer(end1,end2,b_size_0*sbl/2.0,b_colour_0,t_factor)
                                    pov.write(temp.msg())
                            #Do other stuff if the activity is one:
                            elif activity==1 and b_colour_1!='None':
                                t_factor+=b_trans_1
                                end1=Vector(Bonds[b][0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                end2=Vector(Bonds[b][1]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                if b_rep_1=='cylinders':
                                    temp=Cylinder(end1,end2,b_size_1*sbl/2.0,b_colour_1,t_factor)
                                    pov.write(temp.msg())
                                else:
                                    temp=Dimer(end1,end2,b_size_1*sbl/2.0,b_colour_1,t_factor)
                                    pov.write(temp.msg())
                                    
                    #Finally, look at the plaquettes:
                    if p_act:
                        for p in range(p_len):

                            #Determine the activity
                            activity=PI[p+p_len*(i+Lx*(j+Ly*(k+Lz*frame)))]
                            
                            #Determine if theres any transparency
                            t_factor=0.5-k*0.5/(Lz-1) if gen_trans=='yes' else 0
                            
                            #Do stuff relating to an activity of zero:
                            if activity==0 and p_colour_0!='None':
                                t_factor+=p_trans_0
                                Plaq=Plaquettes[p]
                                temp_clist=""
                                for c in Plaq:
                                    c=Vector(c).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                    temp_clist+=",<%f,%f,%f>" %(c[0],c[1],c[2])
                                temp=Polygon(len(Plaq),temp_clist,p_colour_0,t_factor)
                                pov.write(temp.msg())
                            #Do other stuff if the activity is one:
                            elif activity==1 and p_colour_1!='None':
                                t_factor+=p_trans_1
                                Plaq=Plaquettes[p]
                                temp_clist=""
                                for c in Plaq:
                                    c=Vector(c).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                                    temp_clist+=",<%f,%f,%f>" %(c[0],c[1],c[2])
                                temp=Polygon(len(Plaq),temp_clist,p_colour_1,t_factor)
                                pov.write(temp.msg())
            
        #Now everything is added to the image in the frame and end statement is required in the .pov file
        pov.write("#end\n")
        
    #If the cylinders don't have activity on them add them to the image now:
    if b_noact and b_colour!='None':
        for bpair in Bonds:
            for i in range(Lx):
                for j in range(Ly):
                    for k in range(Lz): 
                        t_factor=0.5-k*0.5/(Lz-1)+b_trans if gen_trans=='yes' else b_trans
                        end1=Vector(bpair[0]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                        end2=Vector(bpair[1]).translate({tuple(bx):i,tuple(by):j,tuple(bz):k})
                        if b_rep=='cylinders':
                            temp=Cylinder(end1,end2,b_size*sbl/2.0,b_colour,t_factor)
                            pov.write(temp.msg())
                        else:
                            temp=Dimer(end1,end2,b_size*sbl/2.0,b_colour,t_factor)
                            pov.write(temp.msg())
    
    #Everything has been written on the .pov file, now we can close it
    pov.close()
    #And start rendering the images
    os.system("cd '%s' && . ./execute" %(D))
    
    #Before the animation is made, all of the images must be rendered so the program waits until povray is no
    #longer one of your computers tasks
    time.sleep(20)
    while 'povray' in commands.getoutput('ps -A'):
        time.sleep(15)
    
    #Change the variable im_type for simplicity:
    im_type='png' if im_type=='N' else 'jpg'
    
    #For the animation to be in the right order, the images must be renamed to be in lexicogrpahic order
    os.chdir('%s' %(directory))
    for f_name in glob.glob("*.%s" %(im_type)):
        num=f_name[len(directory):-len(im_type)-1]
        num=1 if num=='' else int(num)
        new="%s%.06d.%s" %(directory,num,im_type)
        os.system("mv '%s' '%s'" %(f_name,new))
    
    #Lastly, create the animation using imagemagick
    os.system('convert -delay %f *.%s animation.gif' %(100.0/fps,im_type))
    
    return """The program has finished, now just wait til imagemagick finishes converting
the images to an animation. This can take a while."""