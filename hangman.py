import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pygame
from PIL import Image, ImageTk

pygame.mixer.init()
sounds = {
    "win": pygame.mixer.Sound("src/sound/win.wav"),
    "lose": pygame.mixer.Sound("src/sound/lose.wav"),
    "click": pygame.mixer.Sound("src/sound/click.wav")
}

wordsVI = ["HA NOI", "HAI PHONG", "DA NANG", "HUE", "NHA TRANG", "SAI GON"]
wordsEN = ["NEW YORK", "LONDON", "TOKYO", "PARIS", "BERLIN", "SYDNEY"]

class HangmanFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.words = wordsEN  # Mặc định là tiếng Anh
        self.word = ""
        self.guessed = []
        self.errors = 0
        self.max_errors = 6
        
        self.images = [ImageTk.PhotoImage(Image.open(f"src/imgs/v{i}.png")) for i in range(7)]
        self.canvas = tk.Label(self, image=self.images[0])
        self.canvas.pack()
        
        self.word_display = tk.Label(self, text="", font=("Arial", 24))
        self.word_display.pack(pady=10)
        
        self.letter_buttons = {}
        button_frame = tk.Frame(self)
        button_frame.pack()
        
        for letter in string.ascii_uppercase:
            btn = tk.Button(button_frame, text=letter, width=4, command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=(ord(letter) - 65) // 9, column=(ord(letter) - 65) % 9)
            self.letter_buttons[letter] = btn
        
        self.message_label = tk.Label(self, text="", font=("Arial", 14), fg="red")
        self.message_label.pack(pady=5)
        
        self.language_var = tk.StringVar(value="EN")
        self.language_menu = ttk.Combobox(self, textvariable=self.language_var, values=["EN", "VI"], state="readonly")
        self.language_menu.pack()
        
        self.start_button = tk.Button(self, text="Bắt đầu", command=self.start_game)
        self.start_button.pack(pady=10)
        
        self.reset_button = tk.Button(self, text="Chơi lại", command=self.reset_game)
        self.reset_button.pack(pady=10)
    
    def start_game(self):
        self.words = wordsVI if self.language_var.get() == "VI" else wordsEN
        self.reset_game()
    
    def guess_letter(self, letter):
        if letter in self.guessed:
            return
        
        self.guessed.append(letter)
        self.letter_buttons[letter].config(state=tk.DISABLED)
        sounds["click"].play()
        
        if letter not in self.word:
            self.errors += 1
            self.canvas.config(image=self.images[self.errors])
            if self.errors >= self.max_errors:
                sounds["lose"].play()
                self.end_game(False)
        else:
            self.update_display()
            if all(ch in self.guessed for ch in self.word if ch.isalpha()):
                sounds["win"].play()
                self.end_game(True)
    
    def update_display(self):
        self.word_display.config(text=" ".join(ch if ch in self.guessed else "_" for ch in self.word))
    
    def end_game(self, won):
        messagebox.showinfo("Kết quả", "Bạn thắng!" if won else f"Bạn thua! Từ cần đoán là {self.word}")
        self.reset_game()
    
    def reset_game(self):
        self.word = random.choice(self.words)
        self.guessed.clear()
        self.errors = 0
        self.canvas.config(image=self.images[0])
        self.update_display()
        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL)

