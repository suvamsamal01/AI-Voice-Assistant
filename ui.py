import customtkinter as ctk
import threading
import webbrowser
import os
import pyautogui

from datetime import datetime
from voice import speak,listen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app=ctk.CTk()

app.title("AI Assistant Boss")

app.geometry("800x600")

title=ctk.CTkLabel(
app,
text="🤖 AI Assistant",
font=("Arial",28,"bold")
)

title.pack(pady=15)

status=ctk.CTkLabel(
app,
text="Idle",
font=("Arial",16)
)

status.pack()

output=ctk.CTkTextbox(
app,
width=700,
height=350,
font=("Arial",14)
)

output.pack(pady=20)

def show(text):

    output.insert(
    "end",
    text+"\n"
    )

    output.see("end")

def process(command):

    command=command.lower()

    if "open youtube" in command:

        speak(
        "Opening Youtube"
        )

        webbrowser.open(
        "https://youtube.com"
        )

        show(
        "AI : Youtube Opened"
        )

    elif "open google" in command:

        speak(
        "Opening Google"
        )

        webbrowser.open(
        "https://google.com"
        )

        show(
        "AI : Google Opened"
        )

    elif "open github" in command:

        speak(
        "Opening Github"
        )

        webbrowser.open(
        "https://github.com"
        )

        show(
        "AI : Github Opened"
        )

    elif "open whatsapp" in command:

        speak(
        "Opening Whatsapp"
        )

        webbrowser.open(
        "https://web.whatsapp.com"
        )

        show(
        "AI : Whatsapp Opened"
        )

    elif "open vs code" in command:

        speak(
        "Opening VS Code"
        )

        os.system(
        "code"
        )

        show(
        "AI : VS Code Opened"
        )

    elif "time" in command:

        now=datetime.now()

        current=now.strftime(
        "%I:%M %p"
        )

        speak(current)

        show(
        "AI : "+current
        )

    elif "screenshot" in command:

        image=pyautogui.screenshot()

        image.save(
        "screen.png"
        )

        speak(
        "Screenshot saved"
        )

        show(
        "AI : Screenshot Saved"
        )

    elif "shutdown" in command:

        speak(
        "Goodbye Boss"
        )

        app.destroy()

    else:

        speak(
        "Command Not Found"
        )

        show(
        "AI : Command Not Found"
        )

def assistant():

    speak(
    "AI Assistant Started Boss"
    )

    while True:

        status.configure(
        text="🎤 Listening"
        )

        command=listen()

        if not command:

            continue

        show(
        "You : "+command
        )

        status.configure(
        text="⚡ Processing"
        )

        process(command)

        status.configure(
        text="Idle"
        )

def start():

    thread=threading.Thread(
    target=assistant
    )

    thread.daemon=True

    thread.start()

button=ctk.CTkButton(
app,
text="🎤 Start Assistant",
width=250,
height=50,
font=("Arial",18),
command=start
)

button.pack()

app.mainloop()