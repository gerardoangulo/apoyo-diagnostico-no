import pydicom as dicom
import numpy as np
from PIL import Image
import cv2
import os

def read_dicom_file(path):
    """
    Lee un archivo DICOM y lo procesa.
    
    Args:
        path (str): Ruta al archivo DICOM.
    
    Returns:
        img_RGB (np.array): Imagen en formato RGB.
        img2show (PIL.Image): Imagen en formato PIL para mostrar.
    """
    img = dicom.read_file(path)
    img_array = img.pixel_array
    img2show = Image.fromarray(img_array)
    img2 = img_array.astype(float)
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    img2 = np.uint8(img2)
    img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
    return img_RGB, img2show

def read_jpg_file(path):
    """
    Lee un archivo JPG y lo procesa.
    
    Args:
        path (str): Ruta al archivo JPG.
    
    Returns:
        img2 (np.array): Imagen en formato RGB.
        img2show (PIL.Image): Imagen en formato PIL para mostrar.
    """
    img = cv2.imread(path)
    img_array = np.asarray(img)
    img2show = Image.fromarray(img_array)
    img2 = img_array.astype(float)
    img2 = (np.maximum(img2, 0) / img2.max()) * 255.0
    img2 = np.uint8(img2)
    return img2, img2show

def read_image_file(path):
    """
    Lee un archivo de imagen (DICOM o JPG) y llama a la función adecuada.
    
    Args:
        path (str): Ruta al archivo de imagen.
    
    Returns:
        img2 (np.array): Imagen en formato RGB.
        img2show (PIL.Image): Imagen en formato PIL para mostrar.
    """
    ext = os.path.splitext(path)[-1].lower()
    if ext in ['.dcm']:
        return read_dicom_file(path)
    elif ext in ['.jpg', '.jpeg']:
        return read_jpg_file(path)
    else:
        raise ValueError("Formato de archivo no soportado: {}".format(ext))
