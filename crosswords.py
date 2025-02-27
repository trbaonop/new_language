import tkinter as tk
import random
import csv

class CrosswordFrame(tk.Frame):
    def __init__(self, parent, csv_file="src/pus.csv"):
        super().__init__(parent)
        self.parent = parent
        self.grid_size = 10  # Kích thước lưới
        self.cells = {}  # Lưu ô nhập liệu
        self.csv_file = csv_file
        self.init_game()
    
    def init_game(self):
        self.word_list = self.load_words(self.csv_file)
        
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=10)
        
        self.hint_frame = tk.Frame(self)
        self.hint_frame.pack(pady=10)
        
        if self.word_list:
            self.create_puzzle()
        else:
            tk.Label(self, text="Không có dữ liệu trong file CSV").pack()
    
    def load_words(self, csv_file):
        words = []
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        words.append((row[0].strip(), row[1].strip().upper(), row[2].strip()))
        except Exception as e:
            print(f"Lỗi đọc file CSV: {e}")
        return words
    
    def create_puzzle(self):
        selected_word = random.choice(self.word_list)
        word_id, vertical_word, vertical_hint = selected_word
        self.word_list.remove(selected_word)
        
        start_row = (self.grid_size - len(vertical_word)) // 2
        start_col = random.randint(1, self.grid_size - 2)
        
        for i, letter in enumerate(vertical_word):
            entry = tk.Entry(self.grid_frame, width=2, font=('Arial', 14), justify='center')
            entry.grid(row=start_row + i, column=start_col)
            self.cells[(start_row + i, start_col)] = (entry, letter)
        
        tk.Label(self.hint_frame, text=f"Dọc ({word_id}): {vertical_hint}").pack(anchor='w')
        
        for word_id, word, hint in self.word_list:
            placed = False
            for i, letter in enumerate(word):
                if placed:
                    break
                for j, v_letter in enumerate(vertical_word):
                    if letter == v_letter:
                        row = start_row + j
                        col = start_col - i
                        if 0 <= col < self.grid_size - len(word):
                            placed = True
                            for k, w_letter in enumerate(word):
                                entry = tk.Entry(self.grid_frame, width=2, font=('Arial', 14), justify='center')
                                entry.grid(row=row, column=col + k)
                                self.cells[(row, col + k)] = (entry, w_letter)
                            tk.Label(self.hint_frame, text=f"Ngang ({word_id}): {hint}").pack(anchor='w')
                            break
    
    def reset_game(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.cells.clear()
        self.init_game()
