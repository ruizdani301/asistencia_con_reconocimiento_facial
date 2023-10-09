import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime
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

# Tomar registro
def registro():
    file = open('registro.csv', 'r+')
    datos = file.readlines()
    registro_nombre = []
    for linea in datos:
        ingreso = linea.split(',')
        registro_nombre.append(ingreso[0])
    if nombre not in registro_nombre:
        hora_actual = datetime.now()
        hora_actual = hora_actual.strftime('%H:%M:%S')
        file.writelines(f'\n{nombre}, {hora_actual}')




lista_asistentes_codificadas = codificar(nueva_lista_asistentes)

#Tomar una imagen desde la camaraWeb
captura = cv2.VideoCapture(1, cv2.CAP_DSHOW)

#Leer la imagen de la camara
""" 
    captura.read() devolvera 2 elementos si se ha podido
    o no hacer la captura y la imagen
"""
exitoso, imagen = captura.read()
if not exitoso:
    print("no se pudo tomar la foto")
else:
    # reconocer cara en captura
    captura_cara = fr.face_locations(imagen)

    # codificar la cara capturada
    # fr.face_encodings() toma dos parametros, la imagen q entrega captura.read()
    # y y la captura_cara q entrega face_locations()
    cara_capturada_codificada = fr.face_encodings(imagen, captura_cara)

     # Buscar coincidencias
    for c_codifi, c_ubicada in zip(cara_capturada_codificada, captura_cara):
        # se entrega la lista de fotos y la foto q se tomo desde la camara
        coincidencia = fr.compare_faces(lista_asistentes_codificadas, c_codifi)
        distancia = fr.face_distance(lista_asistentes_codificadas, c_codifi)
        print(distancia)

        indice_coincidencia = numpy.argmin(distancia)
        #mostrar coincidencias
        if distancia[indice_coincidencia] > 0.6:
            print("No coincide")
        else :
            #Como coincide BUscar el nombre
            nombre = nombres_asistentes[indice_coincidencia]

            # mostrar rectangulo donde aparece el rostro
            y1, x2, y2, x1 = c_ubicada
            cv2.rectangle(imagen,(x1, y1), (x2, y2), (0, 255, 0), 2)
            # mostrar rectangulo con el nombre
            cv2.rectangle(imagen, (x1, y2 - 35),(x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, 250,255,255)

            # para crear registro en un csv
            registro(nombre)
            #mostrar la imagen obtenida
            cv2.imshow('imagen mostrada', imagen)

            #Mantener ventana abierta
            cv2.waitKey(0)

