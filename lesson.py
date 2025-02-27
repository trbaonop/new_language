import tkinter as tk
import csv
import os
import pygame
import re
import tempfile
from gtts import gTTS

pygame.mixer.init()

def sanitize_word(word):
    sanitized = re.sub(r'[^\w\s]', '', word)
    sanitized = sanitized.strip().replace(" ", "_")
    return sanitized.lower()

def play_audio_for_word(word, lang="en"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
    try:
        tts = gTTS(text=word, lang=lang)
        tts.save(temp_path)
        sound = pygame.mixer.Sound(temp_path)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.delay(100)
    except Exception as e:
        print("Lỗi khi phát âm thanh:", e)
    finally:
        os.remove(temp_path)

class LessonFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.lessons = self.load_lessons("src/vor.csv")
        self.lesson_ids = list(self.lessons.keys())
        self.current_lesson = self.lesson_ids[0] if self.lesson_ids else None
        self.current_index = 0
        self.create_widgets()

    def load_lessons(self, filepath):
        lessons = {}
        try:
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lesson_id = row["lesson_id"]
                    if lesson_id not in lessons:
                        lessons[lesson_id] = []
                    lessons[lesson_id].append(row)
        except Exception as e:
            print("Error loading lessons:", e)
        return lessons

    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)
        tk.Label(top_frame, text="Chọn bài học:").pack(side=tk.LEFT)

        if self.lesson_ids:
            self.lesson_var = tk.StringVar(value=self.lesson_ids[0])
            self.lesson_menu = tk.OptionMenu(top_frame, self.lesson_var, *self.lesson_ids, command=self.on_lesson_change)
            self.lesson_menu.pack(side=tk.LEFT)
        else:
            tk.Label(top_frame, text="Không có bài học").pack(side=tk.LEFT)

        self.card_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=2)
        self.card_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.word_label = tk.Label(self.card_frame, text="", font=("Arial", 24))
        self.word_label.pack(pady=10)
        self.meaning_label = tk.Label(self.card_frame, text="", font=("Arial", 18))
        self.meaning_label.pack(pady=5)
        self.example_label = tk.Label(self.card_frame, text="", font=("Arial", 14), wraplength=500, justify="center")
        self.example_label.pack(pady=5)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)
        tk.Button(bottom_frame, text="Previous", command=self.show_prev).pack(side=tk.LEFT, padx=10)
        tk.Button(bottom_frame, text="Play Audio", command=self.play_audio).pack(side=tk.LEFT, padx=10)
        tk.Button(bottom_frame, text="Next", command=self.show_next).pack(side=tk.LEFT, padx=10)

        self.update_flashcard()

    def on_lesson_change(self, value):
        self.current_lesson = value
        self.current_index = 0
        self.update_flashcard()

    def update_flashcard(self):
        if self.current_lesson and self.lessons.get(self.current_lesson):
            card = self.lessons[self.current_lesson][self.current_index]
            self.word_label.config(text=card.get("word", ""))
            self.meaning_label.config(text=card.get("meaning", ""))
            self.example_label.config(text=card.get("example", ""))
        else:
            self.word_label.config(text="No data")
            self.meaning_label.config(text="")
            self.example_label.config(text="")

    def show_next(self):
        if self.current_lesson and self.lessons.get(self.current_lesson):
            self.current_index = (self.current_index + 1) % len(self.lessons[self.current_lesson])
            self.update_flashcard()

    def show_prev(self):
        if self.current_lesson and self.lessons.get(self.current_lesson):
            self.current_index = (self.current_index - 1) % len(self.lessons[self.current_lesson])
            self.update_flashcard()

    def play_audio(self):
        if self.current_lesson and self.lessons.get(self.current_lesson):
            word = self.lessons[self.current_lesson][self.current_index].get("meaning", "")
            play_audio_for_word(word)
