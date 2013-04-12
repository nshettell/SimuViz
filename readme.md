Simuviz
=======
Simuviz is an easy to use is an easy to use image/animation creator which takes advantage of a POV-Ray
(a ray tracer to visualize the data), Python (to process the data) and ImageMagick (to convert the images into an
animation).<br> <br> Simuviz aims to provide insight on lattice transformation as the environment is modified. 
Simuviz was developed with the user and freedom of choice in mind, the user is given a handful of options and
the code is easy enough to understand (given that the user has some knowledge of python) such that the user can edit
and make their own changes for any desirable effect POV-Ray has to offer. <br> <br> Developed by [Nathan Shettell] (https://github.com/nshettell),
with the assistance of [Roger Melko] (https://github.com/rgmelko) and Stephen Inglis.
<br>
Requirements
============
Currently, Simuviz only functions on OS X and UNIX. The system must be capable of running Enthought Python v7.3, 
POV-Ray v3.6 and ImageMagick v.6.8.3-9. All three programs are free to download. The UNIX source code for POV-Ray 
should be installed.<br><br>
An Enthought distribution can be found [here] (http://www.enthought.com/products/epd_free.php). <br>
Source code for POV-Ray can be found [here] (http://www.povray.org/download/). <br>
An ImageMagick distribution can be found [here] (http://www.imagemagick.org/script/download.php). <br>
Installation
============
*Stephen can you edit this portion when you get a chance; I am not familiar enough with the correct
prompts when installing POV-Ray and ImageMagick via Terminal. Thank you!*
Windows
=======
Currently, Simuviz does not function on Windows since ImageMagick is not built for Windows and command prompt is not
as flexible as terminal. However, Simuviz may still be used on Windows if the user removes the portion of the python
code which calls ImageMagick and sorts the produced files in lexicographic order. <br> <br>
If this is desired, it is advised that pvengine.exe is added as an environment variable (alternatively,
pvengine.exe will have to exist in the same folder your data is located). The code will also have to be edited
such that the commands function on command prompt.
Using Simuviz
=============
In the animation.py module, the main function which needs to be called is start. The function requires the following
input: file_info, lattice_info and directory. <br><br>
file_info: This is the name of the file with the information of the activity on the lattice. The data file is assumed to
contain exactly (S+B+P)*Lx*Ly*Lz*F data points in the file, where Lx, Ly and Lz correspond to the size of the lattice,
F is the number of frames and S, B and P correspond to activity points on sites, bonds and plaquettes.
Python reads the data in the following order: S, B, P, Lx, Ly, Lz, F. Currently, the data in the
file is assumed to be 0 or 1. Any line in the data file which contains a hashtag (#) will be ignored.<br><br>
lattice_info: This is the name of the file with the information about the desired lattice; this file must be in
the same file as the python scripts. The file has a very specific format to be properly analyzed by python,
for instructions please read *FormatInstructions.docx* located in *Sample Lattice Files*. <br><br>
directory: The user must input a string which is the desired name of the directory created by Simuviz in the
current folder. No special characters should be in the string, nor should it be a name of a directory which
already exists in the folder.
Modifying the Python Code
=========================
When the python code is executed the user is prompted about their desired appearence of the lattice. The code only
has a finite number of options though. The code was made simple enough to edit/add your own options for a more
desirable result. <br> Simuviz takes advantage of POV-Ray, help on syntax and options can be found [here] (http://wiki.povray.org/content/Main_Page)
and [here] (http://www.povray.org/documentation/).
Known Bugs
==========
Simuviz currently has issues dealing with the following: <br>
-Simuviz takes advantage of parallel processing and if a processor only has one frame to process a blank image is
produced (The issue comes from POV-Rays .ini syntax and cannot be fixed). To avoid this, when prompted for the amount
of processors you want to use make sure you use less than 0.5*n processors, where n is the number of frames.
For example if you have data for 7 frames, use no more than 3 processors. <br>
-Python takes advantage of a garbage collector which greatly limits memory capacity; python will crash if there are
too many calculations to be performed. For safety, the quantity (S+B+P)*Lx*Ly*Lz*F should be less than 10 million.
To Do
=====
-Extend the allowed data value to be any number in the range [0,1] instead of just 0 or 1.<br>
-Create an extension of the 2 dimensional plaquettes to 3 dimensional solids.
