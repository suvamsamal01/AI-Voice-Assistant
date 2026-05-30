import pyttsx3
import speech_recognition as sr
import threading

engine = pyttsx3.init()

# Voice Settings
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

# Female voice (agar available ho)
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)

lock = threading.Lock()

def speak(text):

    with lock:

        try:

            print("AI:", text)

            engine.say(str(text))

            engine.runAndWait()

        except Exception as e:

            print(e)

def listen():

    r = sr.Recognizer()

    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8

    with sr.Microphone() as source:

        print("🎤 Listening...")

        try:

            audio = r.listen(
                source,
                timeout=5,
                phrase_time_limit=50
            )

            text = r.recognize_google(
                audio,
                language="en-IN"
            )

            print("You:", text)

            return text.lower()

        except:
            return ""