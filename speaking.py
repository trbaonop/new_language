import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import numpy as np
import librosa
import nltk
import torch
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from transformers import pipeline

# Tải các bộ dữ liệu cần thiết cho NLTK
nltk.download('punkt')
nltk.download('cmudict')
from nltk.tokenize import word_tokenize
from nltk.corpus import cmudict

# Khởi tạo từ điển phát âm (sẽ dùng cho phiên bản đơn giản nếu cần)
phoneme_dict = cmudict.dict()

# Khởi tạo mô hình sửa lỗi ngữ pháp nâng cao (sequence-to-sequence)
# Sử dụng pipeline với mô hình đã được fine-tune cho grammar correction
grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")

# Hàm sửa lỗi ngữ pháp: sử dụng mô hình sequence-to-sequence
def correct_grammar_advanced(text):
    # Mô hình này thường yêu cầu tiền xử lý dưới dạng "gec: " ở đầu chuỗi
    input_text = "gec: " + text
    corrected = grammar_corrector(input_text, max_length=128, clean_up_tokenization_spaces=True)
    # Giả sử kết quả trả về là danh sách dict, lấy kết quả đầu tiên
    return corrected[0]['generated_text']

# Hàm ghi âm từ microphone và lưu vào file WAV
def record_audio(filename, prompt="Please speak now..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        messagebox.showinfo("Recording", prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    return filename

# Hàm tạo audio tham chiếu bằng gTTS từ câu cho trước và lưu vào file MP3
def synthesize_reference(sentence, filename="ref_audio.mp3"):
    tts = gTTS(text=sentence, lang='en')
    tts.save(filename)
    # Nếu cần, chuyển MP3 sang WAV để xử lý bằng librosa
    sound = AudioSegment.from_mp3(filename)
    wav_filename = "ref_audio.wav"
    sound.export(wav_filename, format="wav")
    return wav_filename

# Hàm tính MFCC và sử dụng DTW để so sánh hai audio file
def evaluate_pronunciation_mfcc(ref_audio, user_audio):
    # Load audio file
    y_ref, sr_ref = librosa.load(ref_audio, sr=None)
    y_user, sr_user = librosa.load(user_audio, sr=None)
    # Tính MFCC với 13 hệ số
    mfcc_ref = librosa.feature.mfcc(y=y_ref, sr=sr_ref, n_mfcc=13)
    mfcc_user = librosa.feature.mfcc(y=y_user, sr=sr_user, n_mfcc=13)
    # Sử dụng DTW với metric cosine để tính khoảng cách
    D, wp = librosa.sequence.dtw(X=mfcc_ref, Y=mfcc_user, metric='cosine')
    distance = D[-1, -1]
    return distance

# Hàm chuyển văn bản thành giọng nói và phát qua hệ thống (sử dụng gTTS)
def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    # Phát file mp3 (trên nhiều hệ thống có thể dùng các thư viện khác)
    os.system("start response.mp3" if os.name == "nt" else "mpg123 response.mp3")

# ---------------------- Giao diện GUI ---------------------- #

class AITutorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI English Tutor")
        self.root.geometry("700x500")
        
        # Tạo Notebook với 2 tab
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        # Tab Grammar Correction
        self.grammar_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.grammar_frame, text="Grammar Correction")
        self.setup_grammar_tab()
        
        # Tab Pronunciation Evaluation
        self.pronunciation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pronunciation_frame, text="Pronunciation Evaluation")
        self.setup_pronunciation_tab()
    
    def setup_grammar_tab(self):
        ttk.Label(self.grammar_frame, text="Enter a sentence to correct:").pack(pady=5)
        self.grammar_input = tk.Text(self.grammar_frame, height=5, width=80)
        self.grammar_input.pack(pady=5)
        self.correct_btn = ttk.Button(self.grammar_frame, text="Correct Grammar", command=self.correct_grammar)
        self.correct_btn.pack(pady=5)
        ttk.Label(self.grammar_frame, text="Corrected Sentence:").pack(pady=5)
        self.grammar_output = scrolledtext.ScrolledText(self.grammar_frame, height=5, width=80, state='disabled')
        self.grammar_output.pack(pady=5)
    
    def setup_pronunciation_tab(self):
        ttk.Label(self.pronunciation_frame, text="Enter the sentence you want to practice:").pack(pady=5)
        self.pron_input = tk.Text(self.pronunciation_frame, height=3, width=80)
        self.pron_input.pack(pady=5)
        self.record_btn = ttk.Button(self.pronunciation_frame, text="Record and Evaluate Pronunciation", command=self.evaluate_pronunciation)
        self.record_btn.pack(pady=5)
        self.pron_output = ttk.Label(self.pronunciation_frame, text="Pronunciation Feedback will appear here.")
        self.pron_output.pack(pady=5)
    
    def correct_grammar(self):
        sentence = self.grammar_input.get("1.0", tk.END).strip()
        if not sentence:
            messagebox.showwarning("Input needed", "Please enter a sentence.")
            return
        self.grammar_output.config(state='normal')
        self.grammar_output.delete("1.0", tk.END)
        self.grammar_output.insert(tk.END, "Processing...")
        self.root.update()
        
        # Sử dụng threading để không làm treo giao diện
        def process():
            corrected = correct_grammar_advanced(sentence)
            self.grammar_output.delete("1.0", tk.END)
            self.grammar_output.insert(tk.END, corrected)
            speak_text(corrected)
        
        threading.Thread(target=process).start()
    
    def evaluate_pronunciation(self):
        sentence = self.pron_input.get("1.0", tk.END).strip()
        if not sentence:
            messagebox.showwarning("Input needed", "Please enter a sentence to practice.")
            return
        
        # Sử dụng threading để ghi âm và xử lý không làm treo GUI
        def process():
            self.pron_output.config(text="Synthesizing reference audio...")
            ref_audio = synthesize_reference(sentence)
            self.pron_output.config(text="Please record your speech now...")
            user_audio_file = "user_audio.wav"
            record_audio(user_audio_file, prompt="Speak the sentence clearly now...")
            self.pron_output.config(text="Evaluating pronunciation...")
            distance = evaluate_pronunciation_mfcc(ref_audio, user_audio_file)
            # Giả định: Nếu khoảng cách dưới 1000, thì phát âm tốt, càng cao thì càng kém
            if distance < 1000:
                feedback = f"Great job! (DTW Distance: {distance:.2f})"
            elif distance < 2000:
                feedback = f"Good, but there is room for improvement. (DTW Distance: {distance:.2f})"
            else:
                feedback = f"Pronunciation needs improvement. (DTW Distance: {distance:.2f})"
            self.pron_output.config(text=feedback)
            speak_text(feedback)
        
        threading.Thread(target=process).start()

# ---------------------- Chạy ứng dụng ---------------------- #

def main():
    root = tk.Tk()
    app = AITutorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

