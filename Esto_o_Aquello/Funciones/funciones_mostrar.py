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
# pylint: disable=import-error
# pylint: disable=no-name-in-module
# ========================================================================================
import re
import pygame

def mostrar_mensaje(fuente, color:tuple, ventana, mensaje:str, coordenadas:tuple, fondo:tuple=None) -> None:
    '''
    Brief: Muestra el mensaje que recibe por parametro
    Parameters:
        fuente -> La fuente y tamaño que tiene el mensaje
        color -> Una tupla que representa el color con valores rgb
        ventana -> La surface donde se muestra el mensaje
        mensaje -> El mensaje a mostrar
        coordenadas -> Una tupla que representa donde se muestra el mensaje
        fondo -> Parametro opcional para agregarle color al fondo del texto
    '''
    try:
        texto = fuente.render(mensaje, True, color, fondo)
        ventana.blit(texto, coordenadas)
    except TypeError:
        print(f"No se pudo renderizar el mensaje '{mensaje}'")
    except Exception as e:
        print(f"Comunicar a sistemas el siguiente error: {e}")

def mostrar_opciones(fuente, color:tuple, ventana, opcion_rojo:str, opcion_azul:str, rectangulo_rojo, rectangulo_azul) -> None:
    '''
    Brief: Muestra las opciones de la pregunta sobre el boton correspondiente
    Parameters:
        fuente -> La fuente y tamaño que tiene el mensaje
        color -> Una tupla que representa el color con valores rgb
        ventana -> La surface donde se muestra el mensaje
        opcion_rojo -> String que representa el valor de la clave rojo
        opcion_azul -> String que representa el valor de la clave azul
        rectangulo_rojo -> Superficie donde muestro la opcion rojo
        rectangulo_azul -> Superficie donde muestro la opcion azul
    '''
    if not type(opcion_rojo) == str:
        raise ValueError("El argumento opcion_rojo debe ser un string")
    if not type(opcion_azul) == str:
        raise ValueError("El argumento opcion_azul debe ser un string")
    if not type(rectangulo_rojo) == pygame.Rect:
        raise ValueError("El argumento rectangulo_rojo debe ser un pygame.Rect")
    if not type(rectangulo_azul) == pygame.Rect:
        raise ValueError("El argumento rectangulo_azul debe ser un pygame.Rect")

    mostrar_mensaje(fuente, color, ventana, opcion_rojo, (rectangulo_rojo.x + 40, rectangulo_rojo.y + 40))
    mostrar_mensaje(fuente, color, ventana, opcion_azul, (rectangulo_azul.x + 40, rectangulo_azul.y + 40))

def mostrar_comodines(fuente, color:tuple, ventana, rectangulo_next, rectangulo_half, rectangulo_reload, fondo_comodin) -> None:
    '''
    Brief: Muestra los textos de los comodines y blitea una imagen de fondo
    Parameters:
        fuente -> La fuente y tamaño que tiene el mensaje
        color -> Una tupla que representa el color con valores rgb
        ventana -> La surface donde se muestra el mensaje
        rectangulo_next -> Superficie donde muestro la imagen y el texto del comodín next
        rectangulo_half -> Superficie donde muestro la imagen y el texto del comodín half
        rectangulo_next -> Superficie donde muestro la imagen y el texto del comodín reload
        fondo_comodín -> Fondo de los comodines
    '''
    if not type(fondo_comodin) == pygame.Surface:
        raise ValueError("El argumento fondo_comodin debe ser una superficie")

    ventana.blit(fondo_comodin, (rectangulo_next.x, rectangulo_next.y))
    ventana.blit(fondo_comodin, (rectangulo_half.x, rectangulo_half.y))
    ventana.blit(fondo_comodin, (rectangulo_reload.x, rectangulo_reload.y))
    mostrar_mensaje(fuente, color, ventana, "NEXT", (rectangulo_next.x + 10, rectangulo_next.y + 10))
    mostrar_mensaje(fuente, color, ventana, "HALF", (rectangulo_half.x + 10, rectangulo_half.y + 10))
    mostrar_mensaje(fuente, color, ventana, "RELOAD", (rectangulo_reload.x + 10, rectangulo_reload.y + 10))

def dibujar_rectangulo(ventana, color, rectangulo) -> None:
    '''
    Brief: Dibuja el rectangulo recibido por argumento en la ventana
    Parameters:
        ventana -> La surface donde se muestra el mensaje
        color -> Una tupla que representa el color con valores rgb
        rectangulo -> Rectangulo que se dibuja
    '''
    if not type(ventana) == pygame.Surface:
        raise ValueError("El argumento ventana debe ser una superficie")
    if not type(rectangulo) == pygame.Rect:
        raise ValueError("El argumento rectangulo debe ser un pygame.Rect")

    pygame.draw.rect(ventana, color, rectangulo)

def cargar_imagen(path:str, tamaño:tuple):
    '''
    Brief: Carga una imagen segun el path recibido por parametro y ajusta su tamaño
    Parameters:
        path -> Ruta hacia la imagen
        tamaño -> Tamaño de la imagen
    '''
    # Matchea cualquier simbolo, seguido de un punto y la extension
    if not re.match(r'^.+\.(jpg|jpeg|png|bmp|gif)$', path):
        raise ValueError("Error en la extensión de la ruta")
    try:
        imagen = pygame.image.load(path)
        imagen = pygame.transform.scale(imagen, tamaño)
        return imagen
    except FileNotFoundError:
        print(f"El archivo '{path}' no exite, verificá la ruta.")
    except Exception as e:
        print(f"Comunicar a sistemas el siguiente error: {e}")