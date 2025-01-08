from tkinter import simpledialog, messagebox
import cv2
import numpy as np
from scipy.signal import wiener

def filtruMedie(img):
    if img is not None:
        n = simpledialog.askinteger(
            "Filtru Medie",
            "Dimensiunea matricei(n-numar impar):",
            minvalue=1,
            maxvalue=31,
            initialvalue=3
        )
        if n is None:
            return img
        if n % 2 == 0:
            messagebox.showerror("Eroare", "Dimensiunea matricei trebuie să fie un numar impar.")
            return img
        filtered_img = cv2.blur(img, (n, n))
        return filtered_img

def filtruMedian(img):
    if img is not None:
        n = simpledialog.askinteger(
            "Filtru Median",
            "Dimensiunea matricei(n-numar impar):",
            minvalue=1,
            maxvalue=31,
            initialvalue=3
        )
        if n is None:
            return img
        if n % 2 == 0:
            messagebox.showerror("Eroare", "Dimensiunea matricei trebuie să fie un numar impar.")
            return img
        filtered_img = cv2.medianBlur(img, n)
        return filtered_img

def filtruGaussian(img):
    if img is not None:
        ksize = simpledialog.askinteger(
            "Filtru Gaussian",
            "Dimensiunea matricei (n-număr impar):",
            minvalue=1,
            maxvalue=31,
            initialvalue=5
        )
        sigma = simpledialog.askfloat(
            "Filtru Gaussian",
            "Sigma:",
            minvalue=0,
            maxvalue=100,
            initialvalue=1.0
        )
        if ksize is None or sigma is None:
            return img
        if ksize % 2 == 0:
            messagebox.showerror("Eroare", "Dimensiunea matricei trebuie să fie un numar impar.")
            return img
        filtered_img = cv2.GaussianBlur(img, (ksize, ksize), sigma)
        return filtered_img

def filtruBilateral(img):
    if img is not None:
        d = simpledialog.askinteger(
            " Filtru Bilateral",
            "Diametrul (d):",
            minvalue=1,
            maxvalue=100,
            initialvalue=9
        )
        sigma_color = simpledialog.askfloat(
            "Filtru Bilateral",
            "Sigma de intensitate:",
            minvalue=1,
            maxvalue=200,
            initialvalue=75
        )
        sigma_space = simpledialog.askfloat(
            "Filtru Bilateral",
            "Sigma Space:",
            minvalue=1,
            maxvalue=200,
            initialvalue=75
        )
        if d is None or sigma_color is None or sigma_space is None:
            return img
        filtered_img = cv2.bilateralFilter(img, d, sigma_color, sigma_space)
        return filtered_img

def filtruCLAHE (img): #Contrast Limited Adaptive Histogram Equalization
    if img is not None:
        clip_limit = simpledialog.askfloat( #clip_limit este o limita a ajustarii contrastului
            "CLAHE ",
            "Introdu valoarea pentru Clip Limit:",
            minvalue=0.1,
            maxvalue=10.0,
            initialvalue=2.0
        )
        if clip_limit is None:
            return img

        grid_size = simpledialog.askinteger(
            "CLAHE",
            "Introdu dimensiunea gridului:",
            minvalue=1,
            maxvalue=32,
            initialvalue=8
        )
        if grid_size is None:
            return img

        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
        filtered_img = clahe.apply(img)
        return filtered_img

def filtruEqualizareHistogram(img):
    if img is not None:
        equalized_img = cv2.equalizeHist(img)
        return equalized_img

def filtruTopHat(img): #Eroziune+Diluare
    if img is not None:
        kernel_size = simpledialog.askinteger(
            "Filtru Top Hat",
            "Dimensiunea matricei (numar impar):",
            minvalue=1,
            maxvalue=31,
            initialvalue=5
        )
        if kernel_size is None:
            return img
        if kernel_size % 2 == 0:
            messagebox.showerror("Eroare", "Dimensiunea matricei trebuie să fie un numar impar.")
            return img
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        filtered_img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
        return filtered_img

def filtruBlackHat(img): #Diluare+Eroziune
    if img is not None:
        kernel_size = simpledialog.askinteger(
            "Filtru Black Hat",
            "Dimensiunea kernelului (numar impar):",
            minvalue=1,
            maxvalue=31,
            initialvalue=5
        )
        if kernel_size is None:
            return img
        if kernel_size % 2 == 0:
            messagebox.showerror("Eroare", "Dimensiunea kernelului trebuie să fie un numar impar.")
            return img
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        filtered_img = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
        return filtered_img

def filtruAjustareContrast(img):
    if img is not None:
        alpha = simpledialog.askfloat( #>1 crestere contrast
            "Ajustare Contrast",
            "Factorul de contrast (alpha):",
            minvalue=0.1,
            maxvalue=10.0,
            initialvalue=1.5
        )
        beta = simpledialog.askinteger( #>0 creste luminozitate
            "Ajustare Contrast",
            "Factorul de luminozitate (beta):",
            minvalue=-100,
            maxvalue=100,
            initialvalue=0
        )
        if alpha is None or beta is None:
            return img
        filtered_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        return filtered_img

def fft_image(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    return fshift

def ifft_image(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    image_reconstructed = np.fft.ifft2(f_ishift)
    image_reconstructed = np.abs(image_reconstructed)
    return image_reconstructed

def filtruGaussianFourier(image, sigma=10):
    sigma = simpledialog.askfloat(
        "Filtru Gaussian Fourier",
        "Sigma:",
        minvalue=0,
        maxvalue=100,
        initialvalue=1.0
    )

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)


    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2  # Centrul imaginii
    x = np.linspace(-ccol, ccol, cols)
    y = np.linspace(-crow, crow, rows)
    x, y = np.meshgrid(x, y)
    gaussian_mask = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))


    fshift_filtered = fshift * gaussian_mask


    f_ishift = np.fft.ifftshift(fshift_filtered)
    image_filtered = np.fft.ifft2(f_ishift)
    image_filtered = np.abs(image_filtered)
    if len(np.array(image_filtered).shape) == 2:
        image_gray = np.array(image_filtered)
    else:
        image_gray = cv2.cvtColor(np.array(image_filtered), cv2.COLOR_BGR2GRAY)

    return image_gray