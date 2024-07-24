#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, font, filedialog, Entry
from tkinter.messagebox import askokcancel, showinfo, WARNING
from datetime import datetime
import getpass
from PIL import ImageTk, Image
import csv
import pyautogui
import tkcap
import img2pdf
import numpy as np
import time
import os
# -----------------------------
#   OWN SCRIPTS
import read_img
import integrator


class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Herramienta para el apoyo al diagnóstico en imágenes radiográficas de tórax")

        #   BOLD FONT
        fonti = font.Font(weight='bold')

        self.root.geometry("1660x1120")        
        self.root.resizable(0,0)

        #   LABELS
        self.lab1 = ttk.Label(self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con mapa de calor", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Diagnóstico probable:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="DNI Paciente:", font=fonti)
        self.lab5 = ttk.Label(self.root, text="Herramienta para el apoyo al diagnóstico en imágenes radiográficas de tórax", font=fonti)
        self.lab6 = ttk.Label(self.root, text="Probabilidad:", font=fonti)

        #   TWO STRING VARIABLES TO CONTAIN ID AND RESULT
        self.ID = StringVar()
        self.result = StringVar()

        #   TWO INPUT BOXES
        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)

        #   GET ID
        self.ID_content = self.text1.get()

        #   TWO IMAGE INPUT BOXES
        self.text_img1 = Text(self.root, width=25, height=14)
        self.text_img2 = Text(self.root, width=25, height=14)
        self.text2 = Text(self.root)
        self.text3 = Text(self.root)

        #   BUTTONS
        self.button1 = ttk.Button(self.root, text="Predecir", state='disabled', command=self.run_model) 
        self.button2 = ttk.Button(self.root, text="Cargar Imagen", command=self.load_img_file)
        self.button3 = ttk.Button(self.root, text="Borrar", command=self.delete)
        self.button4 = ttk.Button(self.root, text="PDF", state='disabled', command=self.create_pdf)
        self.button6 = ttk.Button(self.root, text="Guardar", command=self.save_results_csv)

        #   WIDGETS POSITIONS   
        self.lab1.place(x=290, y=130)
        self.lab2.place(x=1160, y=130)        
        self.lab3.place(x=1030, y=700)
        self.lab4.place(x=130, y=700)
        self.lab5.place(x=470, y=50)
        self.lab6.place(x=1030, y=750)
        self.button1.place(x=440, y=920)
        self.button2.place(x=140, y=920)
        self.button3.place(x=1340, y=920)
        self.button4.place(x=1040, y=920)
        self.button6.place(x=740, y=920)
        self.text1.place(x=345, y=700, width=290, height=40)
        self.text2.place(x=1240, y=700, width=290, height=40)
        self.text3.place(x=1240, y=750, width=290, height=40)
        self.text_img1.place(x=130, y=160)
        self.text_img2.place(x=1030, y=160)

        #   FOCUS ON PATIENT ID
        self.text1.focus_set()

        #  se reconoce como un elemento de la clase
        self.array = None 

        #   NUMERO DE IDENTIFICACIÓN PARA GENERAR PDF
        self.reportID = 0

        #   RUN LOOP
        self.root.mainloop()  
        
    #   METHODS
    def load_img_file(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo de imagen
        filepath = filedialog.askopenfilename(
            initialdir="/", 
            title="Seleccione imagen", 
            filetypes=(
                ('DICOM', '*.dcm'), 
                ('JPEG', '*.jpeg'), 
                ('JPEG', '*.jpg')
            )
        )
        
        
        if filepath:
            try:
                # Obtener la extensión del archivo
                ext = os.path.splitext(filepath)[-1].lower()
            
                # Leer el archivo de imagen adecuado según la extensión
                if ext == '.dcm':
                    self.array, img2show = read_img.read_dicom_file(filepath)
                elif ext in ['.jpg', '.jpeg', '.png']:
                    self.array, img2show = read_img.read_jpg_file(filepath)
                else:
                    raise ValueError("Formato de archivo no soportado: {}".format(ext))
            
                # Redimensionar y mostrar la imagen
                self.img1 = img2show.resize((500, 500), Image.LANCZOS)
                self.img1 = ImageTk.PhotoImage(self.img1)
                self.text_img1.image_create(END, image=self.img1)
                self.button1['state'] = 'enabled'
                
        
            except ValueError as ve:
                print(ve)
            except Exception as e:
                print("Error al leer el archivo:", e)


    def run_model(self):
        self.label, self.proba, self.heatmap = integrator.predict(self.array) 
        self.img2 = Image.fromarray(self.heatmap)
        self.img2 = self.img2.resize((500,500), Image.LANCZOS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        print('OK')
        self.text_img2.image_create(END, image=self.img2)
        self.text2.tag_configure('custom_font', font=('Helvetica', 9))
        self.text3.tag_configure('custom_font', font=('Helvetica', 9))
        self.text2.insert(END, self.label, 'custom_font')
        self.text3.insert(END, '{:.2f}'.format(self.proba)+'%', 'custom_font')
        
        #self.text2.insert(END, self.label)
        #self.text3.insert(END, '{:.2f}'.format(self.proba)+'%')
        
        #  HABILITAR BOTÓN PARA GENERAR PDF
        self.button4['state'] = 'enabled'        
    
    def save_results_csv(self):
        with open('historial.csv', 'a') as csvfile:
            w=csv.writer(csvfile, delimiter='-')
            w.writerow([self.text1.get(), self.label, '{:.2f}'.format(self.proba)+'%'])
            showinfo(title='Guardar', message='Los datos se guardaron con éxito.')

    def create_pdf(self):
        try:
            # Capturar la pantalla de la ventana raíz
            cap = tkcap.CAP(self.root)
            
            # Obtener la fecha y hora actuales
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d-%H-%M")
            
            # Crear el nombre del archivo JPG con la fecha y hora
            jpg_filename = f'Rep-{timestamp}.jpg'
            cap.capture(jpg_filename)
            
            # Abrir la imagen capturada
            img = Image.open(jpg_filename)
            
            # Convertir la imagen a RGB
            img = img.convert('RGB')
            
            # Crear el nombre del archivo PDF con la fecha y hora
            pdf_filename = f'Rep-{timestamp}.pdf'
            
            # Guardar la imagen como PDF
            img.save(pdf_filename)
            
            # Mostrar mensaje de éxito
            showinfo(title='PDF', message='El PDF fue generado con éxito.')
        
        except Exception as e:
            print("Error al generar el PDF:", e)
            showinfo(title='Error', message='Ocurrió un error al generar el PDF.')

    def delete(self):
        answer = askokcancel(title='Confirmación', message='Se borrarán todos los datos.', icon=WARNING)
        if answer:
            self.text1.delete(0, 'end')
            self.text2.delete(1.0, 'end')
            self.text3.delete(1.0, 'end')
            self.text_img1.delete(self.img1, 'end')
            self.text_img2.delete(self.img2, 'end')
            showinfo(title='Borrar', message='Los datos se borraron con éxito')           

def main():
    my_app = App()
    return 0

if __name__ == '__main__':
    main()
