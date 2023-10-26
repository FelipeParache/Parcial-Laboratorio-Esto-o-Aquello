# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=non-ascii-name
# pylint: disable=trailing-newlines
# pylint: disable=invalid-name
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=consider-using-enumerate
# pylint: disable=unidiomatic-typecheck
# pylint: disable=missing-final-newline
# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long
# pylint: disable=consider-using-dict-items
# pylint: disable=singleton-comparison
# pylint: disable=broad-exception-caught
# pylint: disable=unnecessary-lambda-assignment
# ========================================================================================
from datetime import datetime
import re
import json
import random
import pygame

def obtener_preguntas(path:str) -> list | bool:
    '''
    Brief: Recibe una ruta de un archivo en formato CSV y la procesa
    para devolver una lista de diccionarios con la información de cada pregunta.
    Parameters:
        path -> Ruta del archivo CSV que contiene las preguntas.
    Return:
        list -> Una lista de diccionarios,
        donde cada diccionario representa cada pregunta.
        bool -> Si el archivo está vacío.
    '''
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            if len(archivo.readline()) != 0:
                lista_preguntas = []
                for linea in archivo:
                    linea_pregunta = re.split(",|\n", linea)
                    pregunta = {}
                    opciones = {}
                    votos = {}
                    pregunta['pregunta'] = linea_pregunta[0].strip()
                    opciones['rojo'] = linea_pregunta[1].strip().upper()
                    opciones['azul'] = linea_pregunta[2].strip().upper()
                    votos['rojo'] = random.randint(0,5)
                    votos['azul'] = 5 - votos['rojo']
                    pregunta['opciones'] = opciones
                    pregunta['votos'] = votos
                    pregunta['premio'] = 1000
                    pregunta['bandera'] = False
                    lista_preguntas.append(pregunta)
                return lista_preguntas
            print("El archivo esta vacío")
            return False
    except FileNotFoundError:
        print(f"El archivo '{path}' no exite, verificá la ruta.")
    except Exception as e:
        print(f"Comunicar a sistemas el siguiente error: {e}")

def filtrar_preguntas_disponibles(lista:list) -> list:
    '''
    Brief: Filtra las preguntas disponibles segun la bandera
    Parameters:
        lista -> Lista de diccionarios que contienen las preguntas y respuestas.
    Return:
        list -> Lista de los diccionarios disponibles
    '''
    if len(lista) != 0:
        preguntas_disponibles = []
        for pregunta in lista:
            if pregunta['bandera'] == False:
                preguntas_disponibles.append(pregunta)
        return preguntas_disponibles
    return []

def elegir_pregunta_random(lista:list) -> dict:
    '''
    Brief: Elige un diccionario al azar de las preguntas disponibles
    y modifica la bandera para que no se vuelva a elegir la pregunta.
    Parameters:
        lista -> Lista de diccionarios que contienen las preguntas y respuestas.
    Return:
        dict -> Diccionario que contiene una pregunta y dos respuestas.
        bool -> Si la lista está vacía.
    '''
    if len(lista) != 0:
        pregunta_elegida = random.choice(lista)
        pregunta_elegida['bandera'] = True
        return pregunta_elegida
    return {}

def guardar_progreso(dinero_acumulado:int, respuestas_correctas:int) -> None:
    '''
    Brief: Recibe los datos de dinero acumulado y las respuestas correctas para guardarlos
    en un archivo json con la fecha y hora
    Parameters:
        dinero_acumulado -> Entero que representa el dinero acumulado por el usuario
        respuestas_correctas -> Entero que representa las respuestas correctas del usuario
    '''
    if type(dinero_acumulado) == int and type(respuestas_correctas) == int:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Crear un diccionario con la información de la partida
        jugador_info = {
            'fecha': fecha,
            'dinero_acumulado': f"${dinero_acumulado}",
            'respuestas_correctas': respuestas_correctas
        }
        # Guardar la información en un archivo JSON
        with open('Esto_o_Aquello_Pygame/progreso.json', 'w', encoding="utf-8") as archivo:
            json.dump(jugador_info, archivo, indent=4)
    else:
        raise ValueError("Los argumentos dinero_acumulado y respuestas_correctas deben ser enteros no negativos")


def finalizar_juego(acumulador_premio:int, respuestas_correctas:int, bandera:bool) -> bool:
    '''
    Brief: Recibe el premio acumulado y las respuestas correctas del usuario para guardarlos en un archivo json
    y cambia la bandera del bucle para cerrar y finalizar el juego.
    Parameters:
        acumulador_premio -> Entero que representa el dinero acumulado por el usuario
        respuestas_correctas -> Entero que representa las respuestas correctas del usuario
        bandera -> Bandera de control del bucle del juego
    Return:
        bandera -> Bandera en False para cerrar la ventana
    '''
    pygame.display.update()
    pygame.time.delay(4000)
    guardar_progreso(acumulador_premio, respuestas_correctas)
    bandera = False
    return bandera
