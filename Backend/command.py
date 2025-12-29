import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm Listening...")
        eel.DisplayMessage("I'm Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, 10, 6)
        except Exception as e:
            return "" # Timeout or no audio
            
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return "" # Return empty string on error so loop continues quietly
    
    return query.lower()

@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()
        if not query:
            return
        print(query)
        eel.senderText(query)
    else:
        query = message
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            if "open" in query:
                from Backend.feature import openCommand
                openCommand(query)
            elif "send message" in query or "call" in query or "video call" in query:
                from Backend.feature import whatsApp, findContact
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            elif "on youtube" in query:
                # Error Fixed: PlayYoutube -> PlayYouTube (Capital T match)
                from Backend.feature import PlayYouTube 
                PlayYouTube(query)
            else:
                from Backend.feature import chatBot
                chatBot(query)
        else:
            print("No command detected")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    eel.ShowHood()