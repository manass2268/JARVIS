import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
      # Set the speech rate
#speak("Hello, I am Jarvis. How can i Help you")


def takecommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm Listening...")
        eel.DisplayMessage("I'm Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,10,8)
    try:
        print("Recognizing...")
        eel.DisplayMessage("Reconiging...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        #time.sleep(3)
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return "I'm sorry, I didn't catch that. Please repeat. Your sentence"
    
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
                from Backend.feature import PlayYoutube
                PlayYoutube(query)
            else:
                from Backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
    eel.ShowHood()