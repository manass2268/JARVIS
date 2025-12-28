import eel
import os
from Backend.feature import *
from Backend.command import *

def start():
    eel.init("Frontend")
    os.system('start msedge "http://localhost:8000"')
    playAssistantSound()
    eel.start("index.html", mode="edge", host="localhost", block=True)

start()