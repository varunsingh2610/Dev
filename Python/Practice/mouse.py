import pyautogui
from random import randint
import os

#os.environ['DISPLAY'] = ':0'
#_display = Display(os.environ[':0'])

# xDisplay = "192.168.2.130:0.0"
# pyautogui.platformModule._display = Xlib.display.Display(xDisplay)

# export DISPLAY=:0
# Use above command first.
while(1):
    pyautogui.moveTo(randint(1, 1000), randint(1, 1000), duration = .5)
