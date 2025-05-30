import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        
        self.original_image = None
        self.cropped_image = None
        self.crop_start = None
        self.crop_rect = None
        
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.draw_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)
        
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_button = tk.Button(self.right_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)
        
        self.save_button = tk.Button(self.right_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)
        
        self.resize_label = tk.Label(self.right_frame, text="Resize:")
        self.resize_label.pack(pady=(20, 0))
        self.resize_slider = ttk.Scale(self.right_frame, from_=10, to=200, orient='horizontal', command=self.resize_image)
        self.resize_slider.set(100)
        self.resize_slider.pack(pady=10)
        
        self.tk_image = None
        self.tk_crop = None
        self.image_on_canvas = None
        self.cropped_on_canvas = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            self.original_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
            self.display_image(self.original_image)
            self.cropped_image = None
            self.resize_slider.set(100)
    
    def display_image(self, image, cropped=False):
        image_pil = Image.fromarray(image)
        self.tk_image = ImageTk.PhotoImage(image_pil)

        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL), width=self.tk_image.width(), height=self.tk_image.height())

        if cropped and self.cropped_image is not None:
            cropped_pil = Image.fromarray(self.cropped_image)
            self.tk_crop = ImageTk.PhotoImage(cropped_pil)
            self.cropped_on_canvas = self.canvas.create_image(self.tk_image.width() + 10, 0, anchor=tk.NW, image=self.tk_crop)

    def start_crop(self, event):
        if self.original_image is not None:
            self.crop_start = (event.x, event.y)
            if self.crop_rect:
                self.canvas.delete(self.crop_rect)
            self.crop_rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red')

    def draw_crop(self, event):
        if self.crop_start:
            self.canvas.coords(self.crop_rect, self.crop_start[0], self.crop_start[1], event.x, event.y)

    def end_crop(self, event):
        if self.crop_start and self.original_image is not None:
            x0, y0 = self.crop_start
            x1, y1 = event.x, event.y
            x0, x1 = sorted((x0, x1))
            y0, y1 = sorted((y0, y1))
            
            x0 = max(0, x0)
            y0 = max(0, y0)
            x1 = min(self.original_image.shape[1], x1)
            y1 = min(self.original_image.shape[0], y1)
            
            self.cropped_image = self.original_image[y0:y1, x0:x1]
            self.display_image(self.original_image, cropped=True)
            self.resize_slider.set(100)

    def resize_image(self, value):
        if self.cropped_image is not None:
            scale = float(value) / 100.0
            resized = cv2.resize(self.cropped_image, (0, 0), fx=scale, fy=scale)
            self.tk_crop = ImageTk.PhotoImage(Image.fromarray(resized))
            self.canvas.delete(self.cropped_on_canvas)
            self.cropped_on_canvas = self.canvas.create_image(self.tk_image.width() + 10, 0, anchor=tk.NW, image=self.tk_crop)

    def save_image(self):
        if self.cropped_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")])
            if save_path:
                scale = self.resize_slider.get() / 100.0
                resized = cv2.resize(self.cropped_image, (0, 0), fx=scale, fy=scale)
                cv2.imwrite(save_path, cv2.cvtColor(resized, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
