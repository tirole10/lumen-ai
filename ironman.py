from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
import cohere 
load_dotenv()

# Initialize chat history
chat_history = ""

# Initialize the TTS engine
def initialize_tts_engine():
    """Initialize the text-to-speech engine."""
    engine = pyttsx3.init()
    return engine

def say(text, engine):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def close_window(process_name):
    """Close a specific window by process name."""
    os.system(f"taskkill /f /im {process_name}.exe")

def take_command():
    """Listen to the user's voice command and recognize it."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {command}")
            return command
        except sr.WaitTimeoutError:
            return "I did not hear anything. Please repeat."
        except sr.UnknownValueError:
            return "Sorry, I could not understand that."
        except Exception as e:
            print(f"Error: {e}")
            return "Some error occurred. Sorry from Jarvis."

def ai(prompt,engine):
    """Generate a response using the AI model."""
    global chat_history
    try:
        cohere_api_key = os.getenv("cohere_api")
        co = cohere.Client(cohere_api_key)
        response = co.generate(
        model='command',
        prompt=prompt,
        max_tokens=300,
        temperature=0.9,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE')
        ai_response = response.generations[0].text.strip() 
        print(f"AI Response: {ai_response}")  
        say(ai_response, engine) 

    except Exception as e:
        print(f"Error in AI function: {e}")
        say("There was an issue processing your request.")

def main():
    print("Welcome to Jarvis A.I")
    engine = initialize_tts_engine()
    say("Welcome to Jarvis A I", engine)

    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.org",
        "google": "https://www.google.com"
    }

    apps = {
        "camera" : "start microsoft.windows.camera:",
        "chrome" : "C:/Users/hustl/OneDrive/Desktop/Google/Chrome/Application/chrome.exe",
    }

    windows = {
        "camera": "WindowsCamera",
        "chrome": "chrome",
        "media player": "Microsoft.Media.Player",
        "explorer": "msedge"
    }

    music_path = r"C:/Users/hustl/OneDrive/Desktop/ag/babli_tero.mp3"

    while True:
        query = take_command().lower()

        # Goodbye condition to exit the program
        if "goodbye" in query or "good bye" in query:
            say("See you soon sir!", engine)
            print("Terminating program...")
            break

        # Open specific sites
        for site_name, site_url in sites.items():
            if f"open {site_name}" in query:
                say(f"Opening {site_name}...", engine)
                webbrowser.open(site_url)
                break
        # Open Specific Apps
        for app,app_url in apps.items():
            if f"open {app}" in query:
                say(f"Opening {app}...",engine)
                os.system(app_url)

        # Close specific windows
        for window_name, process in windows.items():
            if f"close {window_name}" in query:
                say(f"Closing {window_name}...", engine)
                close_window(process)
                break

        # Play a specific song
        if "play music" in query:
            if os.path.exists(music_path):
                os.startfile(music_path)
            else:
                say("Sorry, I couldn't find the music file.", engine)

        # Tell the time
        elif "the time" in query:
            now = datetime.datetime.now()
            say(f"The time is {now.hour} hours and {now.minute} minutes.", engine)

        
        # Reset chat
        elif "reset chat" in query:
            global chat_history
            chat_history = ""
            say("Chat history has been reset.", engine)

        # Use AI
        elif "using ai" in query:
            say("What do you want to know?", engine)
            prompt = take_command()
            ai(prompt, engine)


if __name__ == '__main__':
    main()
