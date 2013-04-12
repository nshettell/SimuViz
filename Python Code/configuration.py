def ini_creator(first_frame,final_frame,res,image_type,pov_name):
    return """
;POV-Ray animation ini file
;Visual Representation of a Lattice
;Version 3.0
;Author: Nathan Shettell

Antialias=Off
Antialias_Threshold=0.1
Antialias_Depth=2
Display=Off
+W%d
+H%d

Input_File_Name='%s'
Output_File_Type=%s

Initial_Frame=%d
Final_Frame=%d
Initial_Clock=0
Final_Clock=1

Cyclic_Animation=on
Pause_when_Done=off    
""" %(res[0],res[1],pov_name,image_type,first_frame,final_frame)