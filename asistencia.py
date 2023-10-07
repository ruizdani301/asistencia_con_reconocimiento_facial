import cv2
import face_recognition as fr
import os
from pathlib import Path

# crear lista con imagenes simulando la base de datos
ruta = 'imagenes'
lista_asistentes = os.listdir(ruta)
nueva_lista_asistentes = []
nombres_asistentes = []

for asistente in lista_asistentes:
    # imread() Se utiliza para leer una imagen desde el sistema
    # de archivos y cargarla en forma de una matriz NumPy en Python
    imagen_actual = cv2.imread(f'{ruta}/{asistente}')
    #imagen_actual = fr.load_image_file(f'{ruta}/{asistente}')
    nueva_lista_asistentes.append(imagen_actual)
    nombres_asistentes.append(os.path.splitext(asistente)[0])

# Codificar imagenes
def codificar(imagenes):
    # lista codificada
    lista_codificada = []
    # pasar las imagenes a rgb
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        #codificar
        codificadas = fr.face_encodings(imagen)[0]

        # agregamos a la lista
        lista_codificada.append(codificadas)

    # devolver lista codificada
    return lista_codificada

lista_asistentes_codificadas = codificar(nueva_lista_asistentes)

#Tomar una imagen desde la camaraWeb
captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Leer la imagen de la camara
""" captura.read() devolvera 2 elementos si se ha podido
    o no hacer la captura y la imagen
"""
exitoso, imagen = captura.read()


