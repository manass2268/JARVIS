import eel



def start():
    eel.init("Frontend")
    # Import playAssistantSound lazily to avoid import-time circulars
    from Backend.feature import playAssistantSound
    # play startup sound (non-blocking)
    playAssistantSound()
    # Start eel — let eel open the browser after server is ready
    eel.start("index.html", mode="edge", host="localhost", block=True)