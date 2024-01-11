#This program takes in a video and converts it to a text version of that video
#pip install pillow
#also need to install ffmpeg: https://github.com/BtbN/FFmpeg-Builds/releases

import os, sys
import subprocess
import time
import glob
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

global img
img = Image.new("L", (0, 0), 0)
numCharacters = 100 #the number of characters to be used horizontally
multiplier = 4 #the pixels represented per character
#e.g. the image is shrinked to (numCharacters * multiplier) pixels long
global outputSize
global newSize
fontSize = 12

#create the character map from character_map.txt
character_map = []
with open("character_map.txt", "r") as cMapFile:
    for line in cMapFile:
        #character_map.append((float(line.split(" ")[1]), line.split(" ")[0]))
        #if using dark mode, use the 2 lines below instead
        character_map.append((255 - float(line.split(" ")[1]), line.split(" ")[0]))
character_map.reverse()

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

def toText():
    global img
    #enhance image
    contrast_enhancer = ImageEnhance.Contrast(img)
    img = contrast_enhancer.enhance(1.5)
    
    #convert image to grayscale
    img = img.convert("L")
    
    #resize the image
    img = img.resize(newSize)
    
    #convert to text
    output = ""
    for y in range(outputSize[1]):
        currentLine = ""
        for x in range(outputSize[0]):
            currentLine += toChar(x, y)
        output += currentLine + "\n"
    
    return output

#--------------------clear output image folders--------------------
folder_path = "output_frames"
outputFiles = os.listdir(folder_path)
for file in outputFiles:
    file_path = os.path.join(folder_path, file)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

#--------------------measure time it takes for program to run--------------------
start_time = time.time()

#--------------------convert video to images--------------------
print("converting video to images...")
video_path = sys.argv[1]
videoName, videoExt = os.path.splitext(video_path)
videoName = videoName.split("\\")[-1] #only gets the file name from the whole filepath

output_frames = "output_frames\\frame_%04d.jpg"
cmd = ["ffmpeg", "-i", video_path, output_frames]
subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#get the framerate
cmd = [
    "ffmpeg",
    "-i", video_path,
    "2>&1 | grep 'Stream #0:0' | grep -oP '[0-9]+[.]?[0-9]+(?= fps)'"
]
result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
framerate = float(result.stdout.strip())
print("framerate:", framerate)

#--------------------convert images to text--------------------

print("converting images to text...")

fnt = ImageFont.truetype("Consolas.ttf", fontSize)

img_paths = glob.glob("output_frames\\*.jpg")
print(len(img_paths), "frames to be processed")

#get the size of a text frame
img = Image.open(img_paths[0])
#image needs to be shrinked vertically because text characters are rectangular, not square
outputSize = (numCharacters, int((img.size[1] / img.size[0]) * (8/16) * numCharacters)) #dimensions of text output
newSize = (outputSize[0] * multiplier, outputSize[1] * multiplier) #dimensions of actual processed picture
tempOutput = toText()
tempImg = Image.new("RGB", (1920, 1080), (0, 0, 0))
d = ImageDraw.Draw(tempImg)
bounds = d.multiline_textbbox((0, 0), tempOutput, font=fnt)
if bounds[3] % 2 == 1:
    bounds = (bounds[0], bounds[1], bounds[2], bounds[3] + 1)

outputFile = open("output_text\\" + videoName + "_output.txt", "w")
outputFile.write(str(outputSize[1]) + "\n" + str(framerate) + "\n" + str(len(img_paths)) + "\n")

for img_path in img_paths:
    #open the image file
    img = Image.open(img_path)
    imgName, imgExt = os.path.splitext(img_path)
    imgName = imgName.split("\\")[-1] #only gets the file name from the whole filepath
    
    outputFile.write(toText())
outputFile.close()

#--------------------measure time it takes for program to run--------------------
end_time = time.time()
print(f"Elapsed time: {end_time - start_time} seconds")

#--------------------_____--------------------
#print(img.format, img.size, img.mode)
#format: file type (jpg)
#size: dimensions (width, height)
#mode: color/grayscale (RGB) / (L))
#print(list(img.getdata()))