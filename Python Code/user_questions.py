def resolution_options():
    R=[[128,128],[160,120],[320,200],[320,240],[512,384],[640,480],[800,600],[1024,768],[1280,1024],[1600,1200]]
    print "The possible resolutions are:"
    for r in R:
        print "%dx%d" %(r[0],r[1])
################################################################################
def colour_options():
    C=['None','Red','Green','Blue','Yellow','Cyan','Magenta','Clear','White','Black','Gray05','Gray10','Gray15','Gray20','Gray25','Gray30','Gray35','Gray40','Gray45','Gray50','Gray55','Gray60','Gray65','Gray70','Gray75','Gray80','Gray85','Gray90','Gray95','DimGray''Aquamarine','BlueViolet','Brown','DimGrey','Gray','Grey','LightGray','LightGrey','VLightGray','VLightGrey','CadetBlue','Coral','CornflowerBlue','DarkGreen','DarkOrchid','DarkSlateBlue','DarkSlateGray','DarkSlateGrey','DarkTurquoise','Firebrick','ForestGreen','Gold','Goldenrod','GreenYellow','IndianRed','Khaki','LightBlue','LightSteelBlue','LimeGreen','MediumAquamarine','Maroon','MediumBlue','MediumForestGreen','MediumGoldenrod','MediumOrchid','MediumSeaGreen','MediumSlateBlue','MediumSpringGreen','MediumTurquoise','MediumVioletRed','MidnightBlue','Navy','NavyBlue','Orange','OrangeRed','Orchid','PaleGreen','Pink','Plum','Salmon','SeaGreen','Sienna','SkyBlue','SlateBlue','SpringGreen','SteelBlue','Tan','Thistle','Turquoise','Violet','VioletRed','Wheat','YellowGreen','SummerSky','RichBlue','Brass','Copper','Bronze','Bronze2','Silver','BrightGold','OldGold','Feldspar','Quartz','NeonPink','DarkPurple','NeonBlue','CoolCopper','MandarinOrange','LightWood','MediumWood','DarkWood','SpicyPink','SemiSweetChoc','BakersChoc','Flesh','NewTan','NewMidnightBlue','VeryDarkBrown','DarkBrown','DarkTan','GreenCopper','DkGreenCopper','DustyRose','HuntersGreen','SCarlet','Med_Purple','Light_Purple','Very_Light_Purple']
    print "These are the options for colours:"
    for c in C:
        print c
################################################################################
def resolutions():
    return [[128,128],[160,120],[320,200],[320,240],[512,384],[640,480],[800,600],[1024,768],[1280,1024],[1600,1200]]
################################################################################
def colours():
    return ['None','Red','Green','Blue','Yellow','Cyan','Magenta','Clear','White','Black','Gray05','Gray10','Gray15','Gray20','Gray25','Gray30','Gray35','Gray40','Gray45','Gray50','Gray55','Gray60','Gray65','Gray70','Gray75','Gray80','Gray85','Gray90','Gray95','DimGray''Aquamarine','BlueViolet','Brown','DimGrey','Gray','Grey','LightGray','LightGrey','VLightGray','VLightGrey','CadetBlue','Coral','CornflowerBlue','DarkGreen','DarkOrchid','DarkSlateBlue','DarkSlateGray','DarkSlateGrey','DarkTurquoise','Firebrick','ForestGreen','Gold','Goldenrod','GreenYellow','IndianRed','Khaki','LightBlue','LightSteelBlue','LimeGreen','MediumAquamarine','Maroon','MediumBlue','MediumForestGreen','MediumGoldenrod','MediumOrchid','MediumSeaGreen','MediumSlateBlue','MediumSpringGreen','MediumTurquoise','MediumVioletRed','MidnightBlue','Navy','NavyBlue','Orange','OrangeRed','Orchid','PaleGreen','Pink','Plum','Salmon','SeaGreen','Sienna','SkyBlue','SlateBlue','SpringGreen','SteelBlue','Tan','Thistle','Turquoise','Violet','VioletRed','Wheat','YellowGreen','SummerSky','RichBlue','Brass','Copper','Bronze','Bronze2','Silver','BrightGold','OldGold','Feldspar','Quartz','NeonPink','DarkPurple','NeonBlue','CoolCopper','MandarinOrange','LightWood','MediumWood','DarkWood','SpicyPink','SemiSweetChoc','BakersChoc','Flesh','NewTan','NewMidnightBlue','VeryDarkBrown','DarkBrown','DarkTan','GreenCopper','DkGreenCopper','DustyRose','HuntersGreen','SCarlet','Med_Purple','Light_Purple','Very_Light_Purple']
################################################################################
def colour_question(word,activity):
    if word=='background':
        c=raw_input("""Please enter the desired colour for the background
[note for a list of desired colours please call colour_options()]: """)
    elif word!='bond_noact':
        c=raw_input("""Please enter the desired colour to represent %d activity on a %s
[note for a list of choices please call colour_options()]: """ %(activity,word))
    else:
        c=raw_input("""Please enter the desired colour to represent the bonds
[note for a list of desired colours please call colour_options()]: """)
    if c not in colours():
        print "That option is not available, try again."
        return colour_question(word,activity)
    return c
################################################################################
def size_question(word,activity,minimum,maximum):
    while True:
        try:
            if word=='site':
                s=input("""Relative to the shortest bond length, how large would you like to represent
the radius of the site spheres when the activity is %d? The minimum input is %f and the max is %f: """ %(activity,minimum,maximum))
            elif word=='bond+act':
                s=input("""Relative to the shortest bond length, how thick would you the bonds with %d activity to be?
The minimum input is %f and the max is %f: """ %(activity,minimum,maximum))
            else:
                s=input("""Relative to the shortest bond length, how thick would you the bonds to be?
The minimum input is %f and the max is %f: """ %(minimum,maximum))
            s=float(s)
            if s<minimum:
                print "That was less than the minimum, please try again.\n"
            elif s>maximum:
                print "That was greater than the maximum, please try again.\n"
            else:
                return s
        except TypeError:
                print "That was not a valid entry, please try again.\n"
        except ValueError:
            print "That was not a valid entry, please try again.\n"
        except NameError:
            print "That was not a valid entry, please try again.\n"
################################################################################
def trans_question1(word,activity,minimum,maximum):
    while True:
        try:
            if word!='bonds+noact':
                t=input("""Would you like the %s would %d activity on them to be more transparent than normal?
If so how much? Enter a number between %f and %f: """ %(word,activity,minimum,maximum))
            else:
                t=input("""Would you like the bonds to be more transparent than normal?
If so how much? Enter a number between %f and %f: """ %(minimum,maximum))
            t=float(t)
            if t<minimum:
                print "That was less than the minimum, please try again.\n"
            elif t>maximum:
                print "That was greater than the maximum, please try again.\n"
            else:
                return t
        except TypeError:
                print "That was not a valid entry, please try again.\n"
        except ValueError:
            print "That was not a valid entry, please try again.\n"
        except NameError:
            print "That was not a valid entry, please try again.\n"
################################################################################
def rep_question(activity):
    if activity=='none':
        r=raw_input("How would you like to represent the bonds? The options are cylinders and dimers: ")
    else:
        r=raw_input("""How would you like to represent the bonds with an activity of %d?
The options are cylinders and dimers: """ %(activity))
    if r not in ['cylinders','dimers']:
        print "You did not input an available option, please enter: cylinders or dimers."
        return rep_question(activity)   
    else:
        return r
################################################################################
def trans_question2():
    t=raw_input("""Would you like the objects at the front of the lattice to appear more transparent than
those at the back? The options are: yes and no: """)
    if t not in ['yes','no']:
        print "You did not input an available option, please enter: yes or no."
        return trans_question2()
    else:
        return t
################################################################################
def image_question():
    image=raw_input("""Which kind of image would you like to be produced? The options are: jpg and png.
Please enter J for jpg and N for png: """)
    if image not in ['J','N']:
        print "You did not input an available option, please enter: J or P."
        return image_question()   
    else:
        return image
################################################################################
def processors_question(maximum):
    while True:
        try:
            p=input("""How many processors would you like to utilize? Enter a positive integer less than
or equal to %d. It is recommended that the number of processors does not exceed the number of free processors. 
Please enter your choice: """ %(maximum))
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
def fps_question():
    while True:
        try:
            d=input("""How many frames per second would you like to be displayed? Please enter a positive integer: """)
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
################################################################################
def camera_question():
    while True:
        try:
            cam=raw_input("""Where would you like the camera to be located in cartesian co-ordinates?
Note the front-bottom-left cornor will contain what is defined in the lattice file (no translations).
If you are unsure there are threee built-in options: centered, slight offset and large offset. If you choose to input
your own location please enter it in the form: x y z. Please enter your choice: """)
            if cam in ['centered','slight offset','large offset']:
                return cam
            else:
                cam=[float(i) for i in cam.split()]
                return cam
        except TypeError:
                print "That was not a valid entry, please try again.\n"
        except ValueError:
            print "That was not a valid entry, please try again.\n"
        except NameError:
            print "That was not a valid entry, please try again.\n"
################################################################################
def resolution_question():
    r=raw_input("""Please enter the desired resolution of the images to be produced in the form
WxH, the best quality is 1600x1200. For list of choices please call resolution_options(): """)
    try:
        r=[int(r.split('x')[0]),int(r.split('x')[1])]
        if r not in resolutions():
            print "That option is not available, try again."
            return resolution_question()
        else:
            return r
    except TypeError:
        print "That was not a valid entry, please try again.\n"
        return resolutions_question()
    except ValueError:
        print "That was not a valid entry, please try again.\n"
        return resolutions_question()
    except NameError:
        print "That was not a valid entry, please try again.\n"
        return resolutions_question()