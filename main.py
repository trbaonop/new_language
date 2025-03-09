import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from hangman import HangmanFrame
from lesson import LessonFrame
from listening import ListeningFrame
from catchwords import CatchwordsFrame
from crosswords import CrosswordFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learning Modes")
        self.geometry("474x843")

        self.main_menu = MainMenu(self)
        self.main_menu.pack()
        self.current_frame = None
        self.back_button = None  # Biến lưu trữ nút quay lại

    def show_main_menu(self):
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.destroy()
            self.current_frame = None

        if self.back_button:
            self.back_button.pack_forget()  # Ẩn nút quay lại

        self.main_menu.pack()

    def switch_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.destroy()
        self.main_menu.pack_forget()

        self.current_frame = frame_class(self)
        self.current_frame.pack()
        self.show_back_button()
        
    
    def show_games(self):
        self.switch_frame(GameFrame)
    
    def show_lesson(self):
        self.switch_frame(LessonFrame)
    
    def show_listening(self):
        self.switch_frame(ListeningFrame)

    def show_back_button(self):
        if not self.back_button:
            self.back_button = tk.Button(self, text="Quay lại", command=self.show_main_menu)
        self.back_button.pack(pady=10)

class GameFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  
        self.create_widgets()
        self.game_frame = None  

    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Chọn trò chơi", font=("Arial", 18, "bold")).pack(pady=10)
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Hangman", font=("Arial", 14), command=lambda: self.load_game(HangmanFrame)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Catchwords", font=("Arial", 14), command=lambda: self.load_game(CatchwordsFrame)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Crossword", font=("Arial", 14), command=lambda: self.load_game(CrosswordFrame)).grid(row=0, column=2, padx=5)
        
        self.back_button = tk.Button(self, text="Quay lại", command=self.show_game_menu)
        self.back_button.pack(pady=10)
        self.back_button.pack_forget()  

    def load_game(self, game_class):
        if self.game_frame:
            self.game_frame.pack_forget()
            self.game_frame.destroy()

        for widget in self.winfo_children():
            widget.pack_forget()

        self.game_frame = game_class(self)
        self.game_frame.pack()
        self.back_button.pack(pady=10)  

    def show_game_menu(self):
        if self.game_frame:
            self.game_frame.pack_forget()
            self.game_frame.destroy()
            self.game_frame = None
        self.create_widgets()
        self.pack()

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.original_image = Image.open("src/imgs/bg2.jpg")
        self.resized_image = self.original_image.resize((473, 843), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.resized_image)
        
        self.canvas = tk.Canvas(self, width=473, height=843)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.button_frame = tk.Frame(self, bg="#f8f6de")
        self.button_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.button_frame, text="Chọn chế độ học", font=("Arial", 18, "bold"), bg="#f8f6de").pack(pady=10)
        tk.Button(self.button_frame, text="Chơi Game", font=("Arial", 14), command=parent.show_games).pack(pady=10)
        tk.Button(self.button_frame, text="Học từ vựng", font=("Arial", 14), command=parent.show_lesson).pack(pady=10)
        tk.Button(self.button_frame, text="Luyện nghe", font=("Arial", 14), command=parent.show_listening).pack(pady=10)
        tk.Button(self.button_frame, text="Thoát", font=("Arial", 14), command=parent.destroy).pack(pady=20)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
