import customtkinter as ctk
from PIL import Image, ImageTk
import speech_recognition as sr
import subprocess
import sounddevice as sd
import numpy as np
import io
import wave
import queue
import threading
import time
import base64
import pyttsx3

# ==========================================
# ⚙️ SYSTEM CONFIGURATION
# ==========================================
DEVICE_IP = "10.229.214.177:5555"
audio_queue = queue.Queue()
ENCRYPTED_PIN_BASE64 = "MDEwOQ=="  
is_speaking = False  

# ==========================================
# 🗣️ TEXT-TO-SPEECH (JARVIS VOICE ENGINE)
# ==========================================
def speak_in_background(text):
    global is_speaking
    is_speaking = True  
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id) 
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        pass
    finally:
        with audio_queue.mutex:
            audio_queue.queue.clear()
        time.sleep(0.3) 
        is_speaking = False 

def speak(text):
    t = threading.Thread(target=speak_in_background, args=(text,))
    t.start()

# ==========================================
# 📱 PHONE CONTROLLER (ADB)
# ==========================================
def send_to_phone(adb_command):
    full_cmd = f"adb -s {DEVICE_IP} shell {adb_command}"
    subprocess.run(full_cmd, shell=True)

# ==========================================
# 🎙️ AUDIO CAPTURE & STREAMING
# ==========================================
def audio_callback(indata, frames, time_info, status):
    global is_speaking
    if not is_speaking:
        audio_queue.put(bytes(indata))

def process_audio_stream():
    sample_rate = 16000
    chunk_duration_seconds = 3.0 
    chunk_size_bytes = int(sample_rate * 2 * chunk_duration_seconds)
    
    buffer = bytearray()
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 150        
    recognizer.dynamic_energy_threshold = False
    assistant_active = True

    status_label.configure(text="Nova system is online.", text_color="#00ff00")
    speak("Hello naaveesh, Nova system is online and ready for your commands.")

    while True:
        try:
            data = audio_queue.get()
            buffer.extend(data)

            if len(buffer) >= chunk_size_bytes:
                audio_chunk = bytes(buffer[:chunk_size_bytes])
                buffer = buffer[chunk_size_bytes:]

                wav_buffer = io.BytesIO()
                with wave.open(wav_buffer, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio_chunk)
                
                wav_buffer.seek(0)
                with sr.AudioFile(wav_buffer) as source:
                    audio = recognizer.record(source)

                text = recognizer.recognize_google(audio).lower().strip()
                
                if not text or len(text) < 3:
                    continue

                if text:
                    print(f"\n🗣️ You said: '{text}'")
                    # UI Text Update: Dikhayega tune kya bola
                    status_label.configure(text=f'"{text}"', text_color="#00aaff")
                    
                    # ==========================================
                    # 💤 SLEEP / WAKE SYSTEM CONTROLS
                    # ==========================================
                    if "stop listening" in text or "chup ho ja" in text or "deactivate" in text or "sleep" in text:
                        if assistant_active:
                            assistant_active = False
                            status_label.configure(text="System deactivated. Sleeping...", text_color="#ff5555")
                            speak("System deactivated. Standing by.")
                        continue

                    elif "wake up" in text or "jaag ja" in text or "activate" in text:
                        if not assistant_active:
                            assistant_active = True
                            status_label.configure(text="Nova is Activated!", text_color="#00ff00")
                            speak("Hi naaveesh, I am Nova and I am activated.")
                        continue

                    if not assistant_active:
                        continue 

                    # ==========================================
                    # 🚀 DIRECT COMMAND EXECUTION
                    # ==========================================
                    
                    if "lock" in text and "unlock" not in text:
                        status_label.configure(text="Locking phone...", text_color="#ffffff")
                        speak("Naaveesh I am Locking your device.")
                        send_to_phone("input keyevent 26")

                    elif "home" in text:
                        status_label.configure(text="Going to home screen...", text_color="#ffffff")
                        speak("Going to home screen.")
                        send_to_phone("input keyevent 3")

                    elif "piche" in text or "back" in text or "peeche" in text or "one step" in text:
                        status_label.configure(text="Going back...", text_color="#ffffff")
                        speak("Going back.")
                        send_to_phone("input keyevent 4")  

                    elif "recent" in text or "recent apps" in text or "haal ki apps" in text:
                        status_label.configure(text="Opening recent apps...", text_color="#ffffff")
                        speak("Opening recent applications.")
                        send_to_phone("input keyevent 187")  

                    elif "open google" in text:
                        status_label.configure(text="Opening Google...", text_color="#ffffff")
                        speak("Opening Google.")
                        send_to_phone('am start -a android.intent.action.VIEW -d "https://www.google.com"')

                    elif "google" in text:
                        search_query = text.replace("search", "").replace("google", "").strip()
                        if search_query:
                            status_label.configure(text=f"Searching: {search_query}", text_color="#00ff00")
                            speak(f"Searching for {search_query} on Google.")
                            safe_query = search_query.replace(" ", "+")
                            send_to_phone(f'am start -a android.intent.action.VIEW -d "https://www.google.com/search?q={safe_query}"')
                        else:
                            speak("What do you want to search on Google?")

                    elif "camera" in text or "open camera" in text:
                        status_label.configure(text="Opening Camera...", text_color="#ffffff")
                        speak("Opening camera.")
                        send_to_phone("am start -a android.media.action.STILL_IMAGE_CAMERA")

                    elif "photo" in text or "tasveer" in text or "khelo photo" in text:
                        status_label.configure(text="Clicking Photo...", text_color="#00ff00")
                        speak("Clicking a photo. Smile please.")
                        send_to_phone("am start -a android.media.action.STILL_IMAGE_CAMERA")
                        time.sleep(2.0)
                        send_to_phone("input keyevent 27")

                    elif ("unlock" in text or "phone kholo" in text) and "google" not in text and "open" not in text:
                        status_label.configure(text="Unlocking phone...", text_color="#00ff00")
                        speak("Unlocking your device.")
                        send_to_phone("input keyevent KEYCODE_WAKEUP")
                        time.sleep(0.8) 
                        send_to_phone("input swipe 500 1500 500 500")
                        time.sleep(1.5) 
                        try:
                            decoded_bytes = base64.b64decode(ENCRYPTED_PIN_BASE64)
                            actual_pin = decoded_bytes.decode('utf-8')
                            send_to_phone(f"input text {actual_pin}")
                            time.sleep(0.4)
                            send_to_phone("input keyevent 66")
                        except Exception as decoding_error:
                            pass

                    elif "call hitesh" in text or "hitesh ko call" in text:
                        status_label.configure(text="Calling Hitesh...", text_color="#00ff00")
                        speak("Calling Hitesh.")
                        send_to_phone("am start -a android.intent.action.CALL -d tel:9996972487")

                    elif "call nitesh" in text or "nitesh ko call" in text or "call to nitesh" in text:
                        status_label.configure(text="Calling Nitesh...", text_color="#00ff00")
                        speak("Connecting to Nitesh.")
                        send_to_phone("am start -a android.intent.action.CALL -d tel:7015710042")

                    elif "call ronak" in text or "ronak ko call" in text:
                        status_label.configure(text="Calling Ronak...", text_color="#00ff00")
                        speak("Calling Ronak.")
                        send_to_phone("am start -a android.intent.action.CALL -d tel:9053853191")

                    elif "call devi" in text or "devi ko call" in text or "call devil" in text:
                        status_label.configure(text="Calling Devi...", text_color="#00ff00")
                        speak("Calling Devi.")
                        send_to_phone("am start -a android.intent.action.CALL -d tel:7015874875")

                    elif "call prince" in text or "prince ko call" in text or "call prince" in text:
                        status_label.configure(text="Calling Prince...", text_color="#00ff00")
                        speak("Calling ishwar Uncle.")
                        send_to_phone("am start -a android.intent.action.CALL -d tel:8307340862")

                    elif "call mummy" in text or "mummy ko call" in text or "call mummy " in text:
                        status_label.configure(text="Calling Mummy...", text_color="#00ff00")
                        speak("Calling mummy .")
                        send_to_phone("am start -a android.intent.action.CALL -d tel:9518815322")

                    elif "receive call" in text or "call uthao" in text or "take call" in text:
                        status_label.configure(text="Accepting Call...", text_color="#00ff00")
                        speak("Accepting the call.")
                        send_to_phone("input keyevent 5")

                    elif "cut call" in text or "disconnect" in text or "reject" in text:
                        status_label.configure(text="Ending Call...", text_color="#ff5555")
                        speak("Disconnecting the call.")
                        send_to_phone("input keyevent 6")

                    elif "youtube" in text or "open youtube" in text or "youtube kholo" in text:
                        status_label.configure(text="Opening YouTube...", text_color="#ff0000")
                        speak("Opening YouTube for you, naaveesh.")
                        send_to_phone("am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n com.google.android.youtube/com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity")

                    # Skip Ad Command
                    elif "skip ad" in text or "skip" in text or "add hatao" in text:
                        status_label.configure(text="Skipping Ad...", text_color="#00ff00")
                        speak("Skipping the ad.")
                        # Yahan apna exact 'Skip Ad' coordinate daal dena
                        send_to_phone("input tap 648 342")

                    elif "scroll up" in text or "upar karo" in text or "go up" in text or "scroll it up" in text or "page up" in text or "roll up" in text:
                        status_label.configure(text="Scrolling Up...", text_color="#ffffff")
                        speak("Scrolling up.")
                        send_to_phone("input swipe 500 1500 500 500 300")

                    elif "scroll down" in text or "niche karo" in text or "go down" in text or "scroll it down" in text or "page down" in text or "roll down" in text:
                        status_label.configure(text="Scrolling Down...", text_color="#ffffff")
                        speak("Scrolling down.")
                        send_to_phone("input swipe 500 400 500 1600 250")

                    elif "video chalao" in text or "select video" in text:
                        status_label.configure(text="Selecting Video...", text_color="#ffffff")
                        speak("Selecting the Page.")
                        send_to_phone("input tap 500 800")

                    elif "volume up" in text or "aawaz badhao" in text or "increase volume" in text or "louder" in text or "sound up" in text:
                        status_label.configure(text="Increasing Volume...", text_color="#ffffff")
                        speak("Increasing volume.")
                        send_to_phone("input keyevent 24\ninput keyevent 24\ninput keyevent 24")

                    elif "volume down" in text or "aawaz kam" in text or "decrease volume" in text or "lower volume" in text or "sound down" in text:
                        status_label.configure(text="Decreasing Volume...", text_color="#ffffff")
                        speak("Decreasing volume.")
                        send_to_phone("input keyevent 25\ninput keyevent 25\ninput keyevent 25")

                    elif "stop video" in text or "pause" in text or "video roko" in text or "push" in text:
                        status_label.configure(text="Pausing Video...", text_color="#ff5555")
                        send_to_phone("input keyevent 127")
                        send_to_phone("input keyevent 127")
                        speak("Video paused.")

                    elif "play video" in text or "resume" in text or "start video" in text:
                        status_label.configure(text="Resuming Video...", text_color="#00ff00")
                        speak("Playing the video.")
                        send_to_phone("input tap 364 290") 

                    elif "search " in text:
                        search_query = text.split("search ", 1)[1].strip()
                        if search_query:  
                            status_label.configure(text=f"YT Search: {search_query}", text_color="#ff0000")
                            speak(f"Searching for {search_query}.")
                            safe_query = search_query.replace(" ", "+")
                            adb_cmd = f'am start -a android.intent.action.VIEW -d "https://www.youtube.com/results?search_query={safe_query}" -p com.google.android.youtube'
                            send_to_phone(adb_cmd)
                        else:
                            speak("What exactly do you want me to search?")

                    # Open 1st Result (Top)
                    elif "open website" in text or "click on page" in text or "click on video" in text:
                        status_label.configure(text="Opening page...", text_color="#00aaff")
                        speak("Opening page.")
                        # Google search mein pehla link usually upar hota hai
                        send_to_phone("input tap 500 450")

                    # Open Center Result (Tera purana wala)
                    elif "select page" in text or "click " in text:
                        status_label.configure(text="Opening page...", text_color="#00aaff")
                        speak("Selecting page.")
                        send_to_phone("input tap 500 800")

                    # Open Bottom Result
                    elif "select link" in text or "open link" in text or "zoom in" in text:
                        status_label.configure(text="Opening page...", text_color="#00aaff")
                        speak("Opening page.")
                        send_to_phone("input tap 500 1300")

        except sr.UnknownValueError:
            pass
        except Exception as e:
            time.sleep(0.1)

# ==========================================
# 🎨 GUI SETUP & ANIMATION (CUSTOMTKINTER)
# ==========================================
app = ctk.CTk()
app.geometry("500x650")
app.title("Nova - AI Core")
app.configure(fg_color="#000000") # Pure black background

# GIF Loading
gif_path = "ai_interface.gif"
img = Image.open(gif_path)
frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(img.copy().convert("RGBA")))
        img.seek(len(frames))
except EOFError:
    pass 

gif_label = ctk.CTkLabel(app, text="") 
gif_label.pack(expand=True, pady=20)

status_label = ctk.CTkLabel(app, text="Initializing...", font=("Helvetica", 20, "bold"), text_color="#555555")
status_label.pack(side="bottom", pady=50) 

frame_index = 0
def animate_gif():
    global frame_index
    gif_label.configure(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    app.after(40, animate_gif) 

# ==========================================
# 🚀 AUTOMATIC THREADING LAUNCHER (NO BUTTON)
# ==========================================
def start_mic_stream():
    sample_rate = 16000
    block_size = 8000
    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16', blocksize=block_size, callback=audio_callback):
        process_audio_stream()

def auto_activate():
    status_label.configure(text="Booting Audio Systems...", text_color="#00aaff")
    threading.Thread(target=start_mic_stream, daemon=True).start()

# Start GIF animation
animate_gif()

# UI poori tarah load hone ke 500ms baad Nova automatically start hogi
app.after(500, auto_activate)

# Keep window open
app.mainloop()