import os, sys
import time
import curses #pip install windows-curses

input_path = sys.argv[1]

inputFile = open(input_path, "r")
frameHeight = int(inputFile.readline()) #height of the video (in characters)
framerate = float(inputFile.readline()) #framerate of the video
numFrames = int(inputFile.readline()) #total number of frames

stdscr = curses.initscr()
print("Hello")

#print("\033[1;1HHello!")

sleepTime = 1.0 / framerate
"""
for i in range(numFrames):
    start_time = time.time()
    output = ""
    for line in range(frameHeight):
        output += inputFile.readline()
    stdscr.clear()
    stdscr.addstr(output)
    stdscr.refresh()
    #print(output, end=None)
    elapsed_time = time.time() - start_time
    if elapsed_time <= sleepTime:
        time.sleep(sleepTime - elapsed_time)

curses.endwin()
inputFile.close()
"""