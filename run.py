import multiprocessing
def startJarvis():
    print("Process 1" \
    " Starting Jarvis...")
    from main import start
    start()

def listenHotword():
    print("Process 2" \
    " Listening for hotword...")
    from Backend.feature import hotword
    hotword()       
if __name__ == "__main__":
    process1= multiprocessing.Process(target=startJarvis)
    process2= multiprocessing.Process(target=listenHotword)
    process1.start()
    process2.start()
    process1.join()

    if process2.is_alive():
        process2.terminate()
        print("Process 2 terminated.")
        process2.join()
    print("System shutdown complete.")
    process1.terminate()