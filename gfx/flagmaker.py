#HOI4 Flagconverter (made for HGO and Shinsekai)
#To use for yourself: Install Python 3 on your computer, then open command line and 
#You can then drag and drop an image onto the .py file and it will automatically convert the flags
#if you have bugs DM Exocamp#8255 kthx

#TODO later: Specify saving the flag of a certain ideology

import os
import sys
import time
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

#You may laugh at me for this list but you'll see why I like it
pdx_list = [{"size":(82,52),"path":""},{"size":(41,26),"path":"\\medium"},{"size":(10,7),"path":"\\small"}]

#Rapscallions need to actually run this by dragging and dropping the image onto the script
try:
	input_flag = sys.argv[1]
	print(input_flag)
	input_img = Image.open(input_flag)
	print(input_img)
except IndexError:
	#sys.exit("No file was dragged onto the .py script")
	print("No file was dragged onto the .py script")
	e = input('Press ENTER to exit')
except OSError:
	#sys.exit("File is not a valid image file")
	print("File is not a valid image file")
	e = input('Press ENTER to exit: ')

tag_name = input("Enter name of tag: ") #just in case someone forgets PDX has their tags in ALL CAPS
tga_img = input_img.convert('RGBA')

#Right so I trust the person to have actually made the 'flag' 'medium' and 'small' directories before running this
#But let's be in clutch for them just in case (like in the .bat file)
flag_dir = os.getcwd() + "\\flags"
os.makedirs(flag_dir + "\\medium", exist_ok=True)
os.makedirs(flag_dir + "\\small", exist_ok=True)

#Now the actual process. This is why list came in handy
for p in pdx_list:
	print(f"Current dict: {p}")
	with tga_img as im:
		p_dir = flag_dir + p['path']
		p_img = im.resize(p['size'], Image.ANTIALIAS)
		p_img.save(p_dir + "\\" + tag_name + '.tga')

e = input('Press ENTER to exit: ')