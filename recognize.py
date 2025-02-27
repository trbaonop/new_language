import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from keras import models
from PIL import Image, ImageDraw

word_dict = {i: chr(65 + i) for i in range(26)}
model = models.load_model('src/modelHandWritten.h5')

class RecognizeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=200, height=200, bg='white')
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)

        self.image = Image.new("RGB", (200, 200), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.clear_canvas()

        tk.Button(self, text="Dự đoán từ vẽ", command=self.predict_from_canvas).pack()
        tk.Button(self, text="Xóa", command=self.clear_canvas).pack()
        tk.Button(self, text="Chọn ảnh", command=self.predict_character).pack()

        self.result_text = tk.StringVar()
        self.result_label = tk.Label(self, textvariable=self.result_text, font=("Arial", 12), justify="left")
        self.result_label.pack()

    def paint(self, event):
        x1, y1 = event.x - 5, event.y - 5
        x2, y2 = event.x + 5, event.y + 5
        self.canvas.create_oval(x1, y1, x2, y2, fill='black', width=10)
        self.draw.ellipse([x1, y1, x2, y2], fill="black")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, 200, 200], fill="white")

    def predict_character(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28)) / 255.0
        img = np.reshape(img, (1, 28, 28, 1))

        prediction = model.predict(img).flatten()
        top3_indices = np.argsort(prediction)[-3:][::-1]
        self.result_text.set("\n".join(f"{word_dict[i]}: {prediction[i]:.2%}" for i in top3_indices))

    def predict_from_canvas(self):
        self.image.save("temp_canvas.png")
        self.predict_character()
