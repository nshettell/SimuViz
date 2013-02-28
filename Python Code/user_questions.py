def poss_resolutions():
    R=[[128,128],[160,120],[320,200],[320,240],[512,384],[640,480],[800,600],[1024,768],[1280,1024],[1600,1200]]
    print "The possible resolutions are:"
    for r in R:
        print "%dx%d" %(r[0],r[1])
################################################################################
def resolutions():
    return [[128,128],[160,120],[320,200],[320,240],[512,384],[640,480],[800,600],[1024,768],[1280,1024],[1600,1200]]
################################################################################
def offset_q():
    offset=raw_input("""Option 1: Would you like the camera to appear to have an offset angle from the image? If so how large? The options are: none, small and large. Please enter your choice: """)
    if offset not in ['none','small','large']:
        print "You did not input an available option, please enter: none, small or large."
        return offset_q()   
    else:
        return offset
################################################################################
def cam_q():
    cam=raw_input("""Option 2: Which axis would you like the camera to be on? The options are: x, y and z. Please enter your choice: """)
    if cam not in ['x','y','z']:
        print "You did not input an available option, please enter: x, y or z."
        return cam_q()   
    else:
        return cam
################################################################################
def image_q():
    image=raw_input("""Option 3: Which kind of image would you like to be produced? The options are: jpg and png. Please enter your choice: """)
    if image not in ['jpg','png']:
        print "You did not input an available option, please enter: jpg or png."
        return image_q()   
    else:
        return image
################################################################################
def spinrep_q_sites():
    rep=raw_input("""Option 4: How would you like to represent the spin objects on the lattice? The options are: colours, arrows and arrows+colours. Please enter your choice: """)
    if rep not in ['colours','arrows','arrows+colours']:
        print "You did not input an available option, please enter: arrows, colours or arrows+colours."
        return spinrep_q_sites()   
    else:
        return rep
################################################################################
def spinrep_q_bonds():
    rep=raw_input("""Option 4: How would you like to represent the spin objects on the lattice-bonds? The options are: dimers and cylinders. Please enter your choice: """)
    if rep not in ['dimers','cylinders']:
        print "You did not input an available option, please enter: dimers or cylinders."
        return spinrep_q_bonds()
    else:
        return rep
################################################################################
def transparency_q():
    trans=raw_input("""Option 5: Would you like the objects at the front of the lattice to appear more transparent than those at the back? The options are: yes and no. Please enter your choice: """)
    if trans not in ['yes','no']:
        print "You did not input an available option, please enter: yes or no."
        return transparency_q()  
    else:
        return trans
################################################################################
def processors_q(maximum):
    while True:
        try:
            p=input("""Option 6: How many processors would you like to utilize? The number entered must be a postive integer less than or equal to %d (total number of processors). It is recommended that the number of processors does not exceed the number of free processors. Please enter your choice: """ %(maximum))
            p=int(p)
            if p<=0:
                print "That was not a valid entry, please try again.\n"
            elif p>maximum:
                print "There is not enough processors, please try again.\n"
            else:
                return p
        except TypeError:
                print "That was not a valid entry, please try again.\n"
        except ValueError:
            print "That was not a valid entry, please try again.\n"
        except NameError:
            print "That was not a valid entry, please try again.\n"
################################################################################
def fps_q():
    while True:
        try:
            d=input("""Option 7: How many frames per second would you like to be displayed? Please enter a positive integer: """)
            d=int(d)
            if d<=0:
                print "That was not a valid entry, please try again.\n"
            else:
                return d
        except TypeError:
                print "That was not a valid entry, please try again.\n"
        except ValueError:
            print "That was not a valid entry, please try again.\n"
        except NameError:
            print "That was not a valid entry, please try again.\n"