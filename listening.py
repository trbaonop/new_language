import os
import random
import ffmpeg
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog

def extract_audio(video_path, audio_path):
    ffmpeg.input(video_path).output(audio_path, format='wav').run(overwrite_output=True)

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Error: Could not request results"

def generate_gap_fill(text):
    words = text.split()
    if len(words) > 5:
        num_gaps = min(3, len(words) // 4)  # Tạo khoảng trống cho 1/4 số từ
        gaps = random.sample(range(len(words)), num_gaps)
        for i in gaps:
            words[i] = "____"
    return " ".join(words)

def process_video(video_path):
    audio_path = "temp_audio.wav"
    extract_audio(video_path, audio_path)
    text = transcribe_audio(audio_path)
    os.remove(audio_path)
    return generate_gap_fill(text)

def select_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if file_path:
        exercise_text.set(process_video(file_path))

app = tk.Tk()
app.title("IELTS Listening Practice")

tk.Button(app, text="Chọn video", command=select_video).pack()
exercise_text = tk.StringVar()
tk.Label(app, textvariable=exercise_text, wraplength=400, font=("Arial", 12)).pack()

tk.Entry(app).pack()
tk.Button(app, text="Kiểm tra", command=lambda: print("Check answer logic here")).pack()

app.mainloop()
