# CPSC353_project1
Steganography Project

Khanh Truong
California State University Fullerton
Oct 29, 2017

-----------
Description
-----------
This progam embeds and extracts text in image files thru the process of steganography. Embeded images are saved as new images (the original file is not altered), and extracted images are displayed in the command window.

--------------
Included Files
--------------
sten.py			-main code
README.txt		-this file
source_code.png		-image containing source code (see notes section)

------------
Requirements
------------
Python 3.5 or above
Python Imaging Library (PIL) 4.3.0 or above

----------
How to Run
----------
To start the program, run sten.py in the command window.

Format: sten.py -[function] [image file]
Example: sten.py -x image.png

[function] (required)
-m | -x 
	-m - Embeds a text string into the image and saves the results into a new image. Note: when embed is selected, the user is then prompted to input a string to embed and the name of the file to output.
	-x - Extracts text from the image and displays it in the command window.

[image file] (required)
Name of the file to embed or extact. Must include file extension.

-----
Notes
-----
-Does not work on images with a width of less than 12 pixels.
-When embedding, the user must specify a noncompressed file extension such as .png
-Text inside source_code.png has been formatted in order to convert properly to a string.
	-instances of " has been replaced with [double quote]
	-newlines and tabs has been removed
