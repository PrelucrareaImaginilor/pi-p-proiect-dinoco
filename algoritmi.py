import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
def filtru_medie(img, n=3):
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

def filtrusobel(img):
    img_gray = img.convert("L")
    img_array = np.array(img_gray)

    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])

    height, width = img_array.shape

    filtered_img_array = np.zeros_like(img_array)

    for i in range(1, width - 1):
        for j in range(1, height - 1):

            region = img_array[j - 1:j + 2, i - 1:i + 2]

            grad_x = np.sum(region * sobel_x)
            grad_y = np.sum(region * sobel_y)

            # Calculăm magnitudinea gradientului
            magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)

            # Valoarea pixelului în imaginea finală
            filtered_img_array[j, i] = magnitude

    # Normalizăm imaginea la intervalul [0, 255]
    filtered_img_array = np.clip(filtered_img_array, 0, 255)

    # Convertim înapoi la imagine
    img_filtered = Image.fromarray(filtered_img_array.astype(np.uint8))

    return img_filtered