import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


def filtrumedie(img, n=3):
    if img:
        img_gray = img.convert("L")
        img_array = np.array(img_gray)
        width, height = img_array.shape
        filtered_img_array = np.zeros_like(img_array)
        for i in range(int(n / 2), int(width - n / 2) + 1):
            for j in range(int(n / 2), int(height - n / 2) + 1):
                window = 0
                for k in range(-int(n / 2), int(n / 2) + 1):
                    for l in range(-int(n / 2), int(n / 2) + 1):
                        window += int(img_array[i + k, j + l])
                filtered_img_array[i, j] = window / (n * n)

        img2 = Image.fromarray(filtered_img_array.astype(np.uint8))
        return img2



def filtrusobel(img)
