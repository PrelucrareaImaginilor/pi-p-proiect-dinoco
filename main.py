import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk

import algoritmi

start_x = 0
start_y = 0
img2 = None
img_tk2 = None
label_img2 = None
img_resized2 = None
width2 = 0
height2 = 0
label_width_max = 400
label_height_max = 400

options = ["Bilateral", "Medie", "Median","Gaussian","CLAHE","Egalizare Histograma","Gaussian Fourier","Top Hat","Black Hat","Ajustare Contrast"]

img_offset_x = 0
img_offset_y = 0

applied_filters = []

def clear_filters(): #functie pentru resetare lista de filtre
    global applied_filters, applied_filters_label
    applied_filters.clear()
    applied_filters_label.config(text="Filtre aplicate:")

def add_filter():#functie pentru adaugare filtru la lista de filtre pe care dorim sa o aplicam la poza
    selected_filter = clicked.get()
    if selected_filter not in applied_filters:
        applied_filters.append(selected_filter)
        applied_filters_label.config(text="Filtre aplicate: " + ", ".join(applied_filters))

def apply_action(panel): #aplicam filtrele la o copie a pozei si afisam noua poza
    global image, image_tk, zoom_fact, label_image, img_resized, img2, img_tk2, label_img2, width2, height2, applied_filters
    if image:
        #Resetam imaginea la fiecare Apply
        if img2 is not None:
            img2 = None
            img_tk2 = None

        #Aici ne asiguram imaginea sa fie albnegru
        if len(np.array(image).shape) ==2:
            image_gray = np.array(image)
        else:
            image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        processed_image = image_gray

        # Aplicam filtrele selectate
        for filter_name in applied_filters:
            if filter_name == "Medie":
                processed_image = algoritmi.filtruMedie(processed_image)
            elif filter_name == "Median":
                processed_image = algoritmi.filtruMedian(processed_image)
            elif filter_name == "Gaussian":
                processed_image = algoritmi.filtruGaussian(processed_image)
            elif filter_name == "Bilateral":
                processed_image = algoritmi.filtruBilateral(processed_image)
            elif filter_name == "CLAHE":
                processed_image = algoritmi.filtruCLAHE(processed_image)
            elif filter_name == "Egalizare Histograma":
                processed_image = algoritmi.filtruEqualizareHistogram(processed_image)
            elif filter_name == "Gaussian Fourier":
                processed_image = algoritmi.filtruGaussianFourier(processed_image)
            elif filter_name == "Top Hat":
                processed_image = algoritmi.filtruTopHat(processed_image)
            elif filter_name == "Black Hat":
                processed_image = algoritmi.filtruBlackHat(processed_image)
            elif filter_name == "Ajustare Contrast":
                processed_image = algoritmi.filtruAjustareContrast(processed_image)


        processed_image = Image.fromarray(processed_image)
        img2 = processed_image

        if label_img2 is not None:
            label_img2.destroy()

        #Obiect ImageTk.PhotoImage pentru afisare
        img_tk2 = ImageTk.PhotoImage(img2)
        label_img2 = tk.Label(panel, width=label_width_max, height=label_height_max,
                              highlightbackground="black", highlightthickness=0)
        label_img2.config(image=img_tk2)
        label_img2.image = img_tk2

        #Adaugam imaginea
        label_img2.pack(side=tk.RIGHT, anchor=tk.N, padx=10, pady=10)



def load_action(panel): #incarcam poza
    global image, image_tk, label_image, zoom_fact, image_resized, image_width, height, width

    file_path = filedialog.askopenfilename(title="Selecteaza o imagine",
                                           filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"),
        ("All Files", "*.*")])

    if file_path:
        image = Image.open(file_path)
        zoom_fact = 1.0  # Reseteaza factorul de zoom la 1 (normal)

        image_resized = image

        # Redimensioneaza imaginea pentru a se potrivi initial in label
        image_resized = image.resize((label_width_max, int(image.height * (label_width_max / image.width))))
        if image_resized.height > label_height_max:
            image_resized = image_resized.resize(
                (int(image_resized.width * (label_height_max / image_resized.height)), label_height_max))
        width = image_resized.width
        height = image_resized.height
        image_resized = image.resize((image_resized.width, image_resized.height))

        # Convertește imaginea in format compatibil Tkinter
        image_tk = ImageTk.PhotoImage(image_resized)
        if label_image is not None:
            label_image.destroy()

        label_image = tk.Label(panel, width=label_width_max, height=label_height_max,
                               highlightbackground="black", highlightthickness=0)

        # Seteaza imaginea pe label
        label_image.config(image=image_tk)
        label_image.image = image_tk  # Pastreaza referinta

        label_image.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=10)

        # Conecteaza evenimentele de miscare la label
        label_image.bind("<Button-1>", start_move)
        label_image.bind("<B1-Motion>", move_image_call)

def save_action(): #salvam poza procesata
    global img2
    if img2 is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            try:
                img2.save(file_path)
                messagebox.showinfo("Succes", "Imaginea a fost salvata")
            except Exception as e:
                messagebox.showerror("Eroare", "Nu s-a putut salva imaginea")
    else:
        messagebox.showwarning("Eroare", "Nu există o imagine procesata")

def zoom(event):#Functia de zoom
    global image, image_tk, zoom_fact, label_image, img_resized, width, height, img2, img_tk2, img_resized2
    if image:
        if event.delta > 0 and zoom_fact < 6:
            zoom_fact *= 1.075
        elif event.delta < 0 and zoom_fact > 1:
            zoom_fact /= 1.075

        img_resized = image.resize((int(width * zoom_fact), int(height * zoom_fact)), Image.NEAREST)

        image_tk = ImageTk.PhotoImage(img_resized)
        label_image.config(image=image_tk)
        label_image.image = image_tk

    if img2:
        if event.delta > 0 and zoom_fact < 6:
            zoom_fact *= 1.075
        elif event.delta < 0 and zoom_fact > 1:
            zoom_fact /= 1.075

        img_resized2 = img2.resize((int(width * zoom_fact), int(height * zoom_fact)), Image.NEAREST)

        img_tk2 = ImageTk.PhotoImage(img_resized2)
        label_img2.config(image=img_tk2)
        label_img2.image = img_tk2

# Functia de start pentru drag
def start_move(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def move_image_call(event):
    if image:
        move_image(event, image, image_tk, label_image, img_resized)
    if img2:
        move_image(event, img2, img_tk2, label_img2, img_resized2)

# Functia de miscare a imaginii, cu suport pentru zoom si aplicare pe ambele imagini
def move_image(event, img, img_tk, label_img, img_resized):
    global img_offset_x, img_offset_y, start_x, start_y
    if img_resized is None:
        img_resized = img.resize((int(width * zoom_fact), int(height * zoom_fact)), Image.NEAREST)
    if img:
        # Calculam diferenta fata de pozitia initiala
        dx = event.x - start_x
        dy = event.y - start_y

        # Actualizam coordonatele de offset ale imaginii
        img_offset_x -= dx
        img_offset_y -= dy

        # Transformam imaginea pentru a reflecta noua pozitie
        img_moved = img_resized.copy()
        img_moved = img_moved.transform(
            (img_resized.width, img_resized.height),
            Image.AFFINE,
            (1, 0, img_offset_x, 0, 1, img_offset_y),
            fillcolor="white"  # pentru a umple marginile cu alb sau alta culoare
        )

        # Actualizam imaginea afisata
        img_tk = ImageTk.PhotoImage(img_moved)
        label_img.config(image=img_tk)
        label_img.image = img_tk

        # Actualizam coordonatele de inceput pentru miscarea continua
        start_x = event.x
        start_y = event.y


# Interfata
root = tk.Tk()

root.title("Ultrasonic Image Enhancement")

root.geometry("900x600")

frame = tk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.X)

button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

image: Image.Image = None
image_tk = None
zoom_fact = 1.0
label_image = None
img_resized = None
width = 0
height = 0

clicked = tk.StringVar()

load = tk.Button(button_frame, text="Load Image",
                 command=lambda: load_action(root),
                 width=20, height=3)
load.pack(side=tk.LEFT, padx=5, pady=5)

apply = tk.Button(button_frame, text="Apply", command=lambda: apply_action(root), width=20, height=3)
apply.pack(side=tk.RIGHT, padx=5, pady=5)
add_button = tk.Button(button_frame, text="Adaugă Filtru", command=add_filter, width=20, height=3)
add_button.pack(side=tk.RIGHT, padx=5, pady=5)
add_button = tk.Button(button_frame, text="Sterge toate filtrele", command=clear_filters, width=20, height=3)
add_button.pack(side=tk.RIGHT, padx=5, pady=5)
save_button = tk.Button(button_frame, text="Save", command=save_action, width=20, height=3)
save_button.pack(side=tk.LEFT, padx=5, pady=5)
root.bind("<MouseWheel>", zoom)

clicked.set(options[0])
drop = tk.OptionMenu(root, clicked, *options)
drop.pack()

applied_filters_label = tk.Label(root, text="Filtre aplicate: ")
applied_filters_label.pack(pady=10)
root.mainloop()
