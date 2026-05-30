from voice import speak, listen
from tkinter import filedialog
from PIL import Image

import customtkinter as ctk
import threading
import ollama
import os
import webbrowser
import pyautogui
import psutil
import requests

from datetime import datetime

ctk.set_appearance_mode("dark")

app = ctk.CTk()

app.geometry("800x620")

app.title("AI Assistant ")

app.configure(fg_color="#0f172a")

# ================= TITLE =================

title = ctk.CTkLabel(

    app,

    text="🤖 AI Assistant",

    font=("Arial", 34, "bold"),

    text_color="#00FFCC"

)

title.pack(
    pady=10
)
jarvis = ctk.CTkLabel(

    app,

    text="🟢",

    font=("Arial", 20, "bold",),

    text_color="#00FFFF"

)

jarvis.pack(
    pady=5
)

# ================= STATUS =================

status = ctk.CTkLabel(

    app,

    text="🟢 Idle",

    font=("Arial", 15),

    text_color="#00FF99"

)

status.pack()

wave = ctk.CTkLabel(
    app,
    text="▁▁▁▁▁",
    font=("Consolas", 28, "bold"),
    text_color="#00FFFF"
)
wave.pack(pady=2)
# ================= out box =================

chat_frame = ctk.CTkScrollableFrame(

    app,

    width= 900,

    height=350,

    corner_radius=20,

    fg_color="#1e1b4b",
    border_color="#a855f7"

)

chat_frame.pack(
    pady=20
)



# ================= INPUT BOX =================

input_box = ctk.CTkEntry(
    app,
    width=500,
    height=50,
    corner_radius=25,
    border_width=2,
    border_color="#38bdf8",
    fg_color="#1e293b",
    text_color="white",
    font=("Arial", 16),
    placeholder_text="💬 message"
)

input_box.pack(
    pady=10
)

# ================= VARIABLES =================

waiting_weather = False
waiting_song = False
listening=False

def jarvis_idle():

    jarvis.configure(
        text="◉"
    )


def jarvis_listening():

    jarvis.configure(
        text="◎"
    )


def jarvis_thinking():

    jarvis.configure(
        text="⬤"
    )

def pulse():

    current = jarvis.cget("text_color")

    if current == "#00ffff":
        jarvis.configure(text_color="#66ffff")
    else:
        jarvis.configure(text_color="#00ffff")

    app.after(500, pulse)
    

def voice_wave():

    frames = [

        "▁▂▃▄▅▄▃▂▁",
        "▂▄▆█▆▄▂",
        "▃▅▇█▇▅▃",
        "▄▆█▇█▆▄",
        "▅█▇▆▇█▅"

    ]

    def animate(i=0):

        if listening:

            wave.configure(
                text=frames[i % len(frames)]
            )

            app.after(
                120,
                lambda: animate(i + 1)
            )

        else:

            wave.configure(
                text="▁▁▁▁▁"
            )

    animate()


# ================= SHOW TEXT =================

def show_user(text):

    bubble = ctk.CTkFrame(
        chat_frame,
        fg_color="#005C4B",
        corner_radius=15
    )

    bubble.pack(
        anchor="e",
        pady=5,
        padx=10
    )

    msg = ctk.CTkLabel(
        bubble,
        text="🧑 " + text,
        text_color="white"
    )

    msg.pack(
        padx=10,
        pady=5
    )


def show_ai(text):

    bubble = ctk.CTkFrame(
        chat_frame,
        fg_color="#202C33",
        corner_radius=15
    )

    bubble.pack(
        anchor="w",
        pady=5,
        padx=10
    )

    msg = ctk.CTkLabel(
        bubble,
        text= text,
        text_color="white"
    )

    msg.pack(
        padx=10,
        pady=5
    )

def upload_photo():

    file = filedialog.askopenfilename(

        filetypes=[

            ("Images", "*.png *.jpg *.jpeg *.webp")

        ]

    )

    if not file:

        return

    show_user("📷 Photo Uploaded")

    show_ai("🤖 Analyzing Image...")

    answer = ai_image(file)

    show_ai(answer)  

# ================= AI CHAT =================

def ai_chat(question):

    try:

        response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": str(question)
        }
    ],
)
        return response["message"]["content"]

    except Exception as e:

        return "AI Error : " + str(e)

def ai_image(image_path):

    try:

        response = ollama.chat(

            model="llava",

            messages=[

                {

                    "role": "user",

                    "content": "Describe this image",

                    "images": [image_path]

                }

            ]

        )

        return response["message"]["content"]

    except Exception as e:

        return str(e)
# ================= PROCESS =================

def process(command):

    global waiting_weather
    global waiting_song

    command = command.lower()
    show_user(command)


    # ========= WEATHER =========

    if waiting_weather:

        waiting_weather = False

        try:

            weather = requests.get(

                f"https://wttr.in/{command}?format=3"

            ).text

            show_ai(
                "🤖 AI : " + weather
            )

        except:

            show_ai(
                "🤖 AI : Weather failed"
            )

        return

    # ========= SONG =========

    if waiting_song:

        waiting_song = False

        song = command

        show_ai(
            "🎵 Playing : " + song
        )

        webbrowser.open(

            f"https://www.youtube.com/results?search_query={song}"

        )

        return

    # ========= OPEN APPS =========

    if "open chrome" in command:

        os.system(
            "start chrome"
        )

    elif "open whatsapp" in command:

        os.system(
            "start whatsapp:"
        )

    elif "open youtube" in command:

        webbrowser.open(
            "https://youtube.com"
        )
    elif"play" in command:
        song=command.replace(
            "play",
            ""
        ).strip()

        if song == "":

            show_ai("🤖which song?")
        else:
            show_ai("playing:"+ song)
            webbrowser.open("https://www.youtube.com/results?search_query="
        + song

    )
        
    
    elif "open calculator" in command:

        os.system(
            "calc"
        )

    elif "open paint" in command:

        os.system(
            "mspaint"
        )

    elif "open notepad" in command:

        os.system(
            "notepad"
        )

    elif "open vscode" in command:

        os.system(
            "code"
        )

    elif "open camera" in command:

        os.system(
            "start microsoft.windows.camera:"
        )

    # ========= PLAY SONG =========

    elif "play song" in command:

        waiting_song = True

        show_ai(
            "🤖 AI : Which song?"
        )

    # ========= WEATHER =========

    elif "weather" in command:

        waiting_weather = True

        show_ai(
            "🤖 AI : Type city"
        )

    # ========= BATTERY =========

    elif "battery" in command:

        battery = psutil.sensors_battery()

        msg = f"Battery {battery.percent}%"

        show_ai(
            "🤖 AI : " + msg
        )

    # ========= CPU =========

    elif "cpu" in command:

        cpu = psutil.cpu_percent()

        msg = f"CPU {cpu}%"

        show_ai(
            "🤖 AI : " + msg
        )

    # ========= TIME =========

    elif "time" in command:

        now = datetime.now().strftime(
            "%I:%M %p"
        )

        show_ai(
            "🤖 AI : " + now
        )

    # ========= MATH =========

    elif any(

        x in command

        for x in

        [

            "+",

            "-",

            "*",

            "/",

            "plus",

            "minus",

            "multiply",

            "divide"

        ]

    ):

        try:

            math_text = (

                command

                .replace(
                    "plus",
                    "+"
                )

                .replace(
                    "minus",
                    "-"
                )

                .replace(
                    "multiply",
                    "*"
                )

                .replace(
                    "divide",
                    "/"
                )

            )

            ans = eval(
                math_text
            )

            show_ai(
                f"🤖 AI : {ans}"
            )

        except:

            show_ai(
                "🤖 AI : Math Error"
            )

    # ========= SCREENSHOT =========

    elif "screenshot" in command:

        img = pyautogui.screenshot()

        img.save(
            "screen.png"
        )

        show_ai(
            "🤖 AI : Screenshot Saved"
        )

    # ========= VOLUME =========

    elif "volume up" in command:

        pyautogui.press(
            "volumeup"
        )

    elif "volume down" in command:

        pyautogui.press(
            "volumedown"
        )

    elif "mute" in command:

        pyautogui.press(
            "volumemute"
        )

    # ========= BUILDER =========

    elif "who built you" in command:

        show_ai(
            "🤖 AI : Built by SUVAM"
        )

    # ========= STOP =========

    elif "stop" in command:
        global listening
        listening = False
        app.quit()
        return

        

    # ========= AI CHAT =========

    else:

        show_ai(
            "Thinking..."
        
        )
        


        jarvis_thinking()

        answer = ai_chat(
            command
        )

        if len(answer) > 500:

            answer = answer[:500]

        show_ai(
            "AI : " + answer
        )
        speak(answer)

        jarvis_idle()
        wave.configure(
            text="_____"
        )
# ================= TYPE COMMAND =================

def type_command():

    command = input_box.get()

    if command.strip() != "":
        process(command)

        input_box.delete(0, ctk.END)

# ================= ASSISTANT =================

def assistant():

    while True:

        command = listen()


        if not command:
            continue

        command = command.lower()

        if "jarvis" in command:

            status.configure(text="⚡ Activated")

            show_ai("🤖 Yes Boss")

            speak("Yes Boss")

            command = listen()

            if command:

                status.configure(
                    text="⚡ Processing..."
                )

                process(command)

                status.configure(
                    text="🟢 Idle"
                
    )

# ================= START =================

def start():

    global listening

    if listening:

        listening=False

        status.configure(
            text="🛑 Stopped"
        )

        return

    listening=True

    status.configure(
        text="🎤 Listening..."
    )

    thread=threading.Thread(
        target=assistant
    )

    thread.daemon=True

    thread.start()

# ================= BUTTON FRAME =================

button_frame = ctk.CTkFrame(

    app,

    width=260,

    height=80,

    corner_radius=40,

    fg_color="#1e393b",

    border_width=2,

    border_color="#00FFCC"

)

button_frame.pack(
    pady=20
)

# ================= VOICE BUTTON =================

voice_btn = ctk.CTkButton(
    app,
    text="🎙️",
    width=70,
    height=70,
    corner_radius=35,
    font=("Arial", 28, "bold"),
    command=start
)

voice_btn.place(
    relx=0.92,
    rely=0.88
)

voice_btn.place(
    x=15,
    y=12
)

# ================= SEND BUTTON =================

run_btn = ctk.CTkButton(

    button_frame,

    text="➤",

    width=90,

    height=55,

    corner_radius=28,

    fg_color="#7CFF7C",

    hover_color="#55DD55",

    text_color="black",

    font=("Arial",26,"bold"),

    command=type_command

)

run_btn.place(
    x=150,
    y=12
)
def show_user(text):

    bubble = ctk.CTkFrame(
        chat_frame,
        fg_color="#005C4B",
        corner_radius=15
    )

    bubble.pack(
        anchor="e",
        pady=5,
        padx=10
    )

    msg = ctk.CTkLabel(
        bubble,
        text="🧑 " + text,
        text_color="white"
    )

    msg.pack(
        padx=10,
        pady=5
    )


def show_ai(text):

    bubble = ctk.CTkFrame(
        chat_frame,
        fg_color="#202C33",
        corner_radius=15
    )

    bubble.pack(
        anchor="w",
        pady=5,
        padx=10
    )

    msg = ctk.CTkLabel(
        bubble,
        text="🤖 " + text,
        text_color="white",
        justify="left",
        wraplength=500
    )

    msg.pack(
        padx=10,
        pady=5
    )
photo_btn = ctk.CTkButton(

    button_frame,

    text="🖼",

    width=55,

    height=55,

    corner_radius=260,

    command=upload_photo

)

photo_btn.place(
    x=80,
    y=12
)
# ================= ENTER KEY =================

app.bind(

    "<Return>",

    lambda event: type_command()

)

# ================= MAIN LOOP =================
pulse()
threading.Thread(
    target=assistant,
    daemon=True
).start()

app.mainloop()