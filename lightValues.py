import os, sys
from PIL import Image

input_string = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
input_list = list(input_string)
numCharacters = len(input_string)

#open the image
image_path = sys.argv[1]
img = Image.open(image_path)
img = img.convert("L")
imgName, imgExt = os.path.splitext(image_path)
imgName = imgName.split("\\")

#dimensions of a single character
xWidth = int(img.size[0] / numCharacters)
yWidth = img.size[1]

#find the light values of each character
lightValues = []
for i in range(numCharacters):
    lightVal = 0
    curImg = img.crop((i * xWidth, 0, i * xWidth + xWidth, yWidth))
    curImg.save("character_map_images\\" + str(i) + ".png")
    for x in range(i * xWidth, i * xWidth + xWidth):
        for y in range(yWidth):
            lightVal += img.getpixel((x, y))
    lightValues.append(lightVal)
# lightValues.append(xWidth * yWidth * 255)

input_dict = dict(zip(input_list, lightValues))
sorted_input = sorted(input_dict.items(), key=lambda item: item[1]) #list of tuples
sorted_input.pop(0)

#shift every value to within the range [0, 255]
output = [] #list of tuples (char, light value in range [0, 255])
minValue = sorted_input[0][1]
maxValue = sorted_input[len(sorted_input) - 1][1]
diffValue = maxValue - minValue

for i in range(len(sorted_input)):
    newValue = sorted_input[i][1]
    newValue -= minValue
    newValue *= 255 / diffValue
    output.append((sorted_input[i][0], newValue))
    #print(sorted_input[i][0], sorted_input[i][1], newValue)

#output
for i in output:
    print(i[0], i[1])




#!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
#lightValues = ['@', '&', '%', 'Q', 'g', 'W', 'N', 'B', '0', 'M', '$', '#', 'D', 'R', '8', 'X', 'H', 'm', 'G', 'b', 'K', 'A', 'U', 'O', '4', 'p', 'V', 'd', '9', '6', 'P', 'q', 'h', 'k', 'w', 'E', 'S', '2', 'a', ']', '5', 'Z', 'x', 'e', 'j', 'y', 'Y', 'o', 't', 'l', 'n', '[', 'u', '1', '3', 'I', 'f', 'C', 'F', 'i', '}', '{', '7', 'J', '(', '|', ')', 's', 'v', 'L', 'T', 'z', '?', '\\', '/', 'c', '*', 'r', '!', '+', '<', '>', ';', '=', '"', '~', '^', ',', '_', ':', "'", '-', '.', '`']
