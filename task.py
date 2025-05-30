import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor App")
        
        
        self.original_image = None      
        self.display_image = None       
        self.cropped_image = None       
        self.tk_original_image = None   
        self.tk_cropped_image = None    
        
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        
        self.setup_ui()

    def setup_ui(self):
        
        load_btn = ttk.Button(self.root, text="Load Image", command=self.load_image)
        load_btn.pack(pady=5)

        
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        
        self.canvas_original = tk.Canvas(self.frame, width=400, height=400, bg='gray')
        self.canvas_original.grid(row=0, column=0, padx=5, pady=5)

        
        self.canvas_cropped = tk.Canvas(self.frame, width=400, height=400, bg='gray')
        self.canvas_cropped.grid(row=0, column=1, padx=5, pady=5)

        
        self.resize_slider = ttk.Scale(self.root, from_=10, to=300, orient=tk.HORIZONTAL, command=self.resize_cropped)
        self.resize_slider.pack(fill='x', padx=10, pady=10)
        self.resize_slider.set(100)

        
        save_btn = ttk.Button(self.root, text="Save Modified Image", command=self.save_image)
        save_btn.pack(pady=5)

        
        self.canvas_original.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas_original.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas_original.bind("<ButtonRelease-1>", self.on_button_release)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if not file_path:
            return

        self.original_image = cv2.imread(file_path)
        if self.original_image is None:
            messagebox.showerror("Error", "Failed to load image.")
            return

        
        image_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        self.display_image = Image.fromarray(image_rgb)

        
        self.display_image.thumbnail((400, 400))
        
        self.tk_original_image = ImageTk.PhotoImage(self.display_image)
        
        self.canvas_original.config(width=self.tk_original_image.width(), height=self.tk_original_image.height())
        self.canvas_original.delete("all")
        self.canvas_original.create_image(0, 0, anchor=tk.NW, image=self.tk_original_image)
        
        self.canvas_cropped.delete("all")
        self.resize_slider.set(100)
        self.cropped_image = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas_original.delete(self.rect)
        self.rect = None

    def on_mouse_drag(self, event):
        if self.rect:
            self.canvas_original.delete(self.rect)
        self.rect = self.canvas_original.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline='red', width=2
        )

    def on_button_release(self, event):
        if self.original_image is None:
            return

        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)

        
        img_w, img_h = self.display_image.width, self.display_image.height
        scale_x = self.original_image.shape[1] / img_w
        scale_y = self.original_image.shape[0] / img_h

        ix1, iy1 = int(x1 * scale_x), int(y1 * scale_y)
        ix2, iy2 = int(x2 * scale_x), int(y2 * scale_y)

        
        if ix2 <= ix1 or iy2 <= iy1:
            messagebox.showwarning("Warning", "Invalid crop area!")
            return

        self.cropped_image = self.original_image[iy1:iy2, ix1:ix2]
        if self.cropped_image.size == 0:
            messagebox.showwarning("Warning", "Crop area too small!")
            return

        crop_rgb = cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB)
        pil_cropped = Image.fromarray(crop_rgb)
        pil_cropped.thumbnail((400, 400))
        self.tk_cropped_image = ImageTk.PhotoImage(pil_cropped)

        self.canvas_cropped.config(width=self.tk_cropped_image.width(), height=self.tk_cropped_image.height())
        self.canvas_cropped.delete("all")
        self.canvas_cropped.create_image(0, 0, anchor=tk.NW, image=self.tk_cropped_image)

        self.resize_slider.set(100)

    def resize_cropped(self, value):
        if self.cropped_image is None:
            return
        
        scale_percent = float(value) / 100
        height, width = self.cropped_image.shape[:2]
        new_width = max(1, int(width * scale_percent))
        new_height = max(1, int(height * scale_percent))

        resized = cv2.resize(self.cropped_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        resized_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        pil_resized = Image.fromarray(resized_rgb)

        self.tk_cropped_image = ImageTk.PhotoImage(pil_resized)
        self.canvas_cropped.config(width=self.tk_cropped_image.width(), height=self.tk_cropped_image.height())
        self.canvas_cropped.delete("all")
        self.canvas_cropped.create_image(0, 0, anchor=tk.NW, image=self.tk_cropped_image)

    def save_image(self):
        if self.cropped_image is None:
            messagebox.showwarning("Warning", "No cropped image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("BMP files", "*.bmp")]
        )
        if not file_path:
            return

        scale_percent = self.resize_slider.get() / 100
        height, width = self.cropped_image.shape[:2]
        new_width = max(1, int(width * scale_percent))
        new_height = max(1, int(height * scale_percent))

        resized = cv2.resize(self.cropped_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(file_path, resized)
        messagebox.showinfo("Saved", f"Image saved successfully at:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
