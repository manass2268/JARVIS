#import playsound
#import os
#import eel
#@eel.expose
#def playAssistantSound():
 #   base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  #  music_dir = os.path.join(base_dir, "C:\\Users\\manas\\OneDrive\\Desktop\\JARVIS1\\Frontend\\assets\\Audio\\start_sound.mp3")
   # playsound.playsound(music_dir)
import os
import eel
import webbrowser
import pygame
import sqlite3
import pywhatkit as kit
from Backend.config import ASSISTANT_NAME
from Backend.helper import extract_yt_term, remove_words
from urllib.parse import quote
import pvporcupine
import pyaudio
import struct
import time
import subprocess
import pyautogui
import hugchat


pygame.mixer.init()




con=sqlite3.connect('Jarvis.db')
cur=con.cursor()


@eel.expose
def playAssistantSound():
    sound_file = "Frontend\\assets\\Audio\\start_sound.mp3"
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():

def openCommand(query):
    from Backend.command import speak
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip()
    # normalize spaces and lowercase for comparisons
    app_name = ' '.join(query.split()).lower()

    if app_name != "":
        try:
            # System Command (case-insensitive)
            cur.execute('SELECT File_Path FROM System_Command WHERE LOWER(Name) = ?', (app_name,))
            results = cur.fetchall()

            if results:
                speak("Opening " + app_name)
                try:
                    os.startfile(results[0][0])
                except Exception:
                    speak("File path not found or cannot be opened.")
                return

            # Web Command (case-insensitive)
            cur.execute('SELECT Url FROM Web_Command WHERE LOWER(Name) = ?', (app_name,))
            results = cur.fetchall()

            if results:
                speak("Opening " + app_name)
                webbrowser.open(results[0][0])
                return

            # If nothing matched, try generic open (Windows `start`)
            speak("Trying to open " + app_name)
            try:
                os.system('start "" ' + app_name)
            except Exception:
                speak("Not found")
        except Exception as e:
            speak("Something went wrong")
            print(e)

def PlayYouTube(query):
    from Backend.command import speak
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        porcupine=pvporcupine.create(keywords=["jarvis"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):
    from Backend.command import speak
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cur.execute("SELECT Phone_No, Sec_Phone_No, Name FROM Contact_Command WHERE LOWER(Name) LIKE ?", ('%' + query + '%',))
        results = cur.fetchall()
        if not results:
            speak('Contact not found.')
            return 0, 0

        # Prefer primary phone, else secondary
        mobile_number_str = str(results[0][0]) if results[0][0] else str(results[0][1])
        name_found = results[0][2]

        if not mobile_number_str.startswith('+91') and mobile_number_str.isdigit():
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, name_found
    except Exception as e:
        print("Error in findContact:", e)
        speak('Contact not found.')
        return 0, 0
def whatsApp(Phone, message, flag, name):
    from Backend.command import speak
    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

def makeCall(name, phone_no):
    try:
        from Backend.command import speak
        import webbrowser
        # Agar phone_no me +91 nahi hai to add karo
        if not phone_no.startswith('+91') and phone_no.isdigit():
            phone_no = '+91' + phone_no
        # Windows ke liye tel: protocol try karo (agar aapke system me dialer linked hai)
        url = f"tel:{phone_no}"
        webbrowser.open(url)
        speak(f"Calling {name} on {phone_no}")
    except Exception as e:
        print("Error in makeCall:", e)
        speak("Sorry, I couldn't make the call.")
def chatBot(query):
    from Backend.command import speak
    print(f"Chatbot received: {query}")
    speak("I am not connected to the internet for chatting yet, but I heard: " + query)
    # आप यहाँ अपना hugchat वाला logic लगा सकते हैं।
    hugchat_client = hugchat.ChatBot()
    response = hugchat_client.chat(query)
    print(f"Chatbot response: {response}")
    speak(response)
    return response
