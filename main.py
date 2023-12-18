import os, sys
from PIL import Image
#import numpy as np

"""
This program takes in an image and converts it to a text version of that images
"@" and "." are used for black and white
"""

global img
numCharacters = 150 #the number of characters to be used horizontally
#                   number of characters to be used vertically also depends on the same varaible

def toText(x, y):
    if img.getpixel((x, y)) < 90:
        #return '⬛'
        return '@'
    else:
        #return '⬜'
        return '.'


# Open the image file
image_path = sys.argv[1]
img = Image.open(image_path)
imgName, imgExt = os.path.splitext(image_path)
imgName = imgName.split("\\")[-1] #only gets the file name from the whole filepath

#convert to grayscale
img = img.convert("L")

#resize the image
#image needs to be shrinked vertically because text characters are rectangular, not square
newSize = (numCharacters, int((img.size[1] / img.size[0]) * (9/16) * numCharacters))
img = img.resize(newSize)

#convert the text
output = []
for y in range(newSize[1]):
    currentLine = ""
    for x in range(newSize[0]):
        currentLine += toText(x, y)
    output.append(currentLine)

#save the text into output.txt
outputFile = open("output_text\\" + imgName + "_output.txt", 'w')
for line in output:
    outputFile.write(line + "\n")
    #print(line)

#save the output image
img.save("output_images\\" + imgName + "_output" + imgExt)

#print(img.format, img.size, img.mode)
#format: file type (jpg)
#size: dimensions (width, height)
#mode: color/grayscale (RGB) / (L))
#print(list(img.getdata()))