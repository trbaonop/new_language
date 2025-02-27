import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os, random

class CatchwordsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.revealed_count = 0
        self.max_pieces = 6  # Số mảnh che
        
        # Khởi tạo game
        self.init_game()

    def init_game(self):
        # Load hình ảnh
        folder = "src/catch"  # Thay bằng thư mục chứa ảnh
        files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
        if not files:
            messagebox.showerror("Lỗi", "Không tìm thấy ảnh trong thư mục!")
            return
        
        selected_file = random.choice(files)
        self.image_path = os.path.join(folder, selected_file)
        self.correct_answer = os.path.splitext(selected_file)[0].lower().strip()
        
        self.image = Image.open(self.image_path)
        self.img_width, self.img_height = self.image.size
        self.tk_image = ImageTk.PhotoImage(self.image)
        
        # Tạo giao diện
        self.canvas = tk.Canvas(self, width=self.img_width, height=self.img_height)
        self.canvas.pack(pady=10)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        
        # Tạo lớp che ảnh
        self.overlay_ids = []
        self.rows, self.cols = 2, 3
        piece_width, piece_height = self.img_width / self.cols, self.img_height / self.rows
        
        for i in range(self.rows):
            for j in range(self.cols):
                x1, y1 = j * piece_width, i * piece_height
                x2, y2 = x1 + piece_width, y1 + piece_height
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="gray")
                self.overlay_ids.append(rect_id)
        
        # Ô nhập đáp án
        self.entry = tk.Entry(self, font=("Arial", 16))
        self.entry.pack(pady=5)
        
        # Nút đoán
        self.submit_btn = tk.Button(self, text="Đoán", command=self.check_answer)
        self.submit_btn.pack(pady=5)
        
        # Nút chơi lại
        self.reset_btn = tk.Button(self, text="Chơi lại", command=self.reset_game)
        self.reset_btn.pack(pady=5)
    
    def check_answer(self):
        guess = self.entry.get().lower().strip()
        if guess == self.correct_answer:
            score = int(((self.max_pieces - self.revealed_count) / self.max_pieces) * 100)
            messagebox.showinfo("Chúc mừng", f"Bạn trả lời đúng!\nĐiểm: {score}")
            self.reset_game()
        else:
            messagebox.showerror("Sai", "Bạn trả lời sai!")
            self.reveal_piece()
            if self.revealed_count >= self.max_pieces:
                messagebox.showinfo("Kết thúc", f"Bạn đã hết lượt đoán!\nĐáp án: {self.correct_answer}")
                self.reset_game()
    
    def reveal_piece(self):
        if self.revealed_count < self.max_pieces:
            rect_id = self.overlay_ids[self.revealed_count]
            self.canvas.delete(rect_id)
            self.revealed_count += 1
    
    def reset_game(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.revealed_count = 0
        self.init_game()
