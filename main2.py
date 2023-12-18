#This program takes in an image and converts it to a text version of that image

import os, sys
from PIL import Image, ImageEnhance

global img
numCharacters = 200 #the number of characters to be used horizontally
multiplier = 4 #the pixels represented per character
#e.g. the image is shrinked to (numCharacters * multiplier) pixels long

#create the character map from character_map.txt
character_map = []
with open("character_map.txt", "r") as cMapFile:
    for line in cMapFile:
        character_map.append((float(line.split(" ")[1]), line.split(" ")[0]))
        #if using dark mode, use the 2 lines below instead
        #character_map.append((255 - float(line.split(" ")[1]), line.split(" ")[0]))
#character_map.reverse()

#function to convert a pixel region in the picture to a character
def toChar(x, y):
    #calculate the average light value of the region
    lightVal = 0
    for i in range(multiplier):
        for j in range(multiplier):
            lightVal += img.getpixel((x * multiplier + i, y * multiplier + j))
    lightVal /= multiplier * multiplier
    #find the character that corresponds to the light value
    for i in range(1, len(character_map)):
        if character_map[i][0] > lightVal:
            return character_map[i - 1][1]
    return character_map[len(character_map) - 1][1]

# Open the image file
image_path = sys.argv[1]
img = Image.open(image_path)
imgName, imgExt = os.path.splitext(image_path)
imgName = imgName.split("\\")[-1] #only gets the file name from the whole filepath

#enhance image
#brightness_enhancer = ImageEnhance.Brightness(img)
#img = brightness_enhancer.enhance(1.2)
contrast_enhancer = ImageEnhance.Contrast(img)
img = contrast_enhancer.enhance(1.5)

#convert image to grayscale
img = img.convert("L")

#resize the image
#image needs to be shrinked vertically because text characters are rectangular, not square
outputSize = (numCharacters, int((img.size[1] / img.size[0]) * (7/16) * numCharacters)) #dimensions of output
newSize = (outputSize[0] * multiplier, outputSize[1] * multiplier) #dimensions of actual processed picture
img = img.resize(newSize)

#convert the text
output = []
for y in range(outputSize[1]):
    currentLine = ""
    for x in range(outputSize[0]):
        currentLine += toChar(x, y)
    output.append(currentLine)

#save the text into output_text\[image]_output.txt
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
