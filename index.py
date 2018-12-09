import os
import sys
import random
import subprocess
import ctypes
import wx

# Start out with imports

CREATE_NO_WINDOW = 0x08000000
# This is important for later, as it prevents shells from opening

filesuffix = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
# A tuple of allowed suffixes

app = wx.App()
# Start up the WX frame

frame = wx.Frame(None, -1, "win.py")
frame.SetSize(0, 0, 200, 50)
# Set the standard frame size

ctypes.windll.user32.MessageBoxW(
    0,
    "First, select the directory with your images.\nThey must be either .jpg or .png formats",
    "Select Input",
    64,
)
# Tell the person the first step

openImportPath = wx.DirDialog(
    frame, "Choose input directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
)
openImportPath.ShowModal()
importDir = openImportPath.GetPath()
openImportPath.Destroy()
# Have them choose the directory we import photos from

ctypes.windll.user32.MessageBoxW(
    0, "Then, choose the zip file to hide in your images.", "Select hidden zip", 64
)
# Second step alert

cryptZipFile = wx.FileDialog(
    frame,
    "Choose Zip to hide",
    "",
    "",
    "Archive files (*.zip)|*.zip",
    wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
)
cryptZipFile.ShowModal()
cryptZip = cryptZipFile.GetPath()
cryptZipFile.Destroy()
# Get them to choose the ZIP file

ctypes.windll.user32.MessageBoxW(
    0, "Finally, choose where your files will be saved to.", "Select Output", 64
)
# Third Step alert

outputDirSet = wx.DirDialog(
    frame, "Choose output directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
)
outputDirSet.ShowModal()
outputDir = outputDirSet.GetPath()
outputDirSet.Destroy()
# Ask the user to choose where the photos are outputted

importdir = os.fsencode(importDir)
outputdir = os.fsencode(outputDir)
# This allows us to scan the directories and see if they exist

ctypes.windll.user32.MessageBoxW(0, "Beginning stenography now", "Starting up...", 64)
# Tell the user it's starting up

try:
    os.listdir(importdir)
except FileNotFoundError:
    ctypes.windll.user32.MessageBoxW(0, "Something went wrong...", "Error", 16)
    sys.exit()
# These two are important, they display an error when the file isn't found
try:
    os.listdir(outputDir)
except FileNotFoundError:
    ctypes.windll.user32.MessageBoxW(0, "Something went wrong...", "Error", 16)
    sys.exit()

# For each file in the directory
for file in os.listdir(importdir):
    filename = os.fsdecode(file)
    # Get the file name
    if filename.endswith(tuple(filesuffix)):
        # And if its suffix is in the tuple from earlier
        newfilename = random.randint(111_111, 999_999)
        # Generate a file name
        cmd = f'copy "{importDir}\\{filename}" /b + "{cryptZip}" /b "{outputDir}\\{newfilename}.png"'
        subprocess.call(cmd, shell=True, creationflags=CREATE_NO_WINDOW)
        # And copy the ZIP into the file
        # Then copy that to the output directory
    else:
        pass
        # If it isn't in the tuple, skip it

ctypes.windll.user32.MessageBoxW(0, "Your conversions are complete!", "Complete!", 48)
# When we're done, tell them

subprocess.Popen(f'explorer "{outputDir}"')
# And when they press ok, open the output folder
