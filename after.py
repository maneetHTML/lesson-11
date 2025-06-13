import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def apply_color_filter(image, filter_type):
    filtered_image = image.copy()

    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0  
        filtered_image[:, :, 0] = 0 

    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0  
        filtered_image[:, :, 2] = 0  

    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0 
        filtered_image[:, :, 2] = 0  

    elif filter_type == "increase_red":
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], 50)

    elif filter_type == "decrease_blue":
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], 50)

    return filtered_image

def update_image(filter_type):
    global original_image, display_panel, current_filtered_image

    filtered = apply_color_filter(original_image, filter_type)
    current_filtered_image = filtered.copy()  # Store for saving

    img_rgb = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    display_panel.config(image=img_tk)
    display_panel.image = img_tk

def load_image():
    global original_image, display_panel, current_filtered_image
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if not path:
        return
    original_image = cv2.imread(path)
    current_filtered_image = original_image.copy()  # Reset filtered image

    img_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    display_panel.config(image=img_tk)
    display_panel.image = img_tk

def save_image():
    global current_filtered_image
    if current_filtered_image is None:
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg *.jpeg")])
    if file_path:
        cv2.imwrite(file_path, current_filtered_image)
        print("Image saved to:", file_path)


root = tk.Tk()
root.title("Image Color Filter with Save Option")


btn_frame = tk.Frame(root)
btn_frame.pack(side="top", pady=10)

tk.Button(btn_frame, text="Load Image", command=load_image).pack(side="left", padx=5)
tk.Button(btn_frame, text="Red Tint", command=lambda: update_image("red_tint")).pack(side="left", padx=5)
tk.Button(btn_frame, text="Blue Tint", command=lambda: update_image("blue_tint")).pack(side="left", padx=5)
tk.Button(btn_frame, text="Green Tint", command=lambda: update_image("green_tint")).pack(side="left", padx=5)
tk.Button(btn_frame, text="Increase Red", command=lambda: update_image("increase_red")).pack(side="left", padx=5)
tk.Button(btn_frame, text="Decrease Blue", command=lambda: update_image("decrease_blue")).pack(side="left", padx=5)
tk.Button(btn_frame, text="Download", command=save_image).pack(side="left", padx=5)

display_panel = tk.Label(root)
display_panel.pack(padx=10, pady=10)

original_image = None
current_filtered_image = None

root.mainloop()
