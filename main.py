import tkinter as tk
from hangman import HangmanFrame
from lesson import LessonFrame
from recognize import RecognizeFrame
from catchwords import CatchwordsFrame
from crosswords import CrosswordFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learning Modes")
        self.geometry("600x500")

        self.main_menu = MainMenu(self)
        self.main_menu.pack()

    def show_main_menu(self):
        """ Hiển thị lại menu chính """
        for widget in self.winfo_children():
            widget.pack_forget()
        self.main_menu.pack()

    def show_hangman(self):
        """ Chuyển sang chế độ Hangman """
        self.main_menu.pack_forget()
        self.current_frame = HangmanFrame(self)
        self.current_frame.pack()
        self.add_back_button()
    
    def show_catchwords(self):
        """ Chuyển sang chế độ Hangman """
        self.main_menu.pack_forget()
        self.current_frame = CatchwordsFrame(self)
        self.current_frame.pack()
        self.add_back_button()
        
    def show_crossword(self):
        """ Chuyển sang chế độ Hangman """
        self.main_menu.pack_forget()
        self.current_frame = CrosswordFrame(self)
        self.current_frame.pack()
        self.add_back_button()

    def show_lesson(self):
        """ Chuyển sang chế độ Học từ vựng """
        self.main_menu.pack_forget()
        self.current_frame = LessonFrame(self)
        self.current_frame.pack()
        self.add_back_button()

    def show_recognize(self):
        """ Chuyển sang chế độ Nhận diện chữ viết """
        self.main_menu.pack_forget()
        self.current_frame = RecognizeFrame(self)
        self.current_frame.pack()
        self.add_back_button()

    def add_back_button(self):
        """ Thêm nút quay lại """
        back_button = tk.Button(self, text="Quay lại", command=self.show_main_menu)
        back_button.pack(pady=10)

class MainMenu(tk.Frame):
    """ Màn hình chính để chọn chế độ """
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Chọn chế độ học", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Chơi Hangman", font=("Arial", 14), command=parent.show_hangman).pack(pady=10)
        tk.Button(self, text="Đuổi hình bắt chữ", font=("Arial", 14), command=parent.show_catchwords).pack(pady=10)
        tk.Button(self, text="trò chơi ô chữ", font=("Arial", 14), command=parent.show_crossword).pack(pady=10)
        tk.Button(self, text="Học từ vựng", font=("Arial", 14), command=parent.show_lesson).pack(pady=10)
        tk.Button(self, text="Nhận diện chữ viết", font=("Arial", 14), command=parent.show_recognize).pack(pady=10)
        tk.Button(self, text="Thoát", font=("Arial", 14), command=parent.quit).pack(pady=20)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
