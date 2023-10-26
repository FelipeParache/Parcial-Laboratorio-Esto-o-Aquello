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
# pylint: disable=undefined-variable
# pylint: disable=no-member
# pylint: disable=no-name-in-module
# ========================================================================================
import pygame
from Funciones.funciones_respuesta import obtener_respuesta_mas_votada, validar_respuesta_corecta, determinar_respuesta_maquina
from Funciones.funciones_preguntas import obtener_preguntas, filtrar_preguntas_disponibles, finalizar_juego, elegir_pregunta_random
from Funciones.funciones_mostrar import mostrar_opciones, mostrar_mensaje, mostrar_comodines, cargar_imagen, dibujar_rectangulo

pygame.init()

# Configuraciones
WIDTH = 800
HEIGHT = 600
VENTANA = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("¿Esto o Aquello?")
ICONO = pygame.image.load("Imagenes/logo.jpeg")
pygame.display.set_icon(ICONO)

# Colores y fuentes
COLOR_ROJO = (255,0,0)
COLOR_AZUL = (0,0,255)
COLOR_BLANCO = (255,255,255)
COLOR_NEGRO = (0,0,0)
fuente_texto = pygame.font.SysFont("Arial", 20)
fuente_botones = pygame.font.SysFont("Georgia", 20)
fuente_respuesta = pygame.font.SysFont("Avenir", 22)

# Dimensiones y posición de los rectángulos
rectangulo_rojo = pygame.Rect(150, 350, 200, 100) # (Posición X, Posición Y, Ancho en PX, Alto en PX)
rectangulo_borde_negro = pygame.Rect(150, 350, 210, 110)
rectangulo_azul = pygame.Rect(450, 350, 200, 100)
rectangulo_next = pygame.Rect(150, 500, 100, 50)
rectangulo_half = pygame.Rect(350, 500, 100, 50)
rectangulo_reload = pygame.Rect(550, 500, 100, 50)

# Imagenes
fondo = cargar_imagen("Imagenes/fondo.jpeg", (WIDTH, HEIGHT))
fondo_respuesta_correcta = cargar_imagen("Imagenes/respuesta_correcta.jpeg", (WIDTH, HEIGHT))
fondo_respuesta_incorrecta = cargar_imagen("Imagenes/respuesta_incorrecta.jpeg", (WIDTH, HEIGHT))
fondo_comodin = cargar_imagen("Imagenes/fondo_comodin.jpeg", (100, 50))

# Banderas para mostrar preguntas o respuestas
bandera_mostrar_pregunta = True
bandera_mostrar_respuesta = False
# Bnaderas comodines
bandera_next = True
bandera_half = True
bandera_reload = True
# Banderas mensajes comodines
bandera_mensaje_comodin = False
bandera_mensaje_half = False
# Acumuladores de tiempo, premio y respuesta correcta
temporizador = 0
acumulador_premio = 0
respuestas_correctas = 0
# Tiempo desde que se muestra la primer pregunta
tiempo_inicio_pregunta = pygame.time.get_ticks()

# Obtengo las preguntas del CSV
lista_preguntas = obtener_preguntas('preguntas.csv')
# Determino cual va a ser la primer pregunta que se va a mostrar
preguntas_disponibles = filtrar_preguntas_disponibles(lista_preguntas)
pregunta_actual = elegir_pregunta_random(preguntas_disponibles)

bandera = True
while bandera:

    VENTANA.blit(fondo, (0, 0))

    # Vuelvo a filtrar las preguntas disponibles segun su bandera
    preguntas_disponibles = filtrar_preguntas_disponibles(lista_preguntas)
    # Variables de la pregunta actual
    texto_pregunta = pregunta_actual['pregunta']
    opcion_rojo = pregunta_actual['opciones']['rojo']
    opcion_azul = pregunta_actual['opciones']['azul']
    votos_rojo = pregunta_actual['votos']['rojo']
    votos_azul = pregunta_actual['votos']['azul']

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            bandera = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Posiciones del click en la ventana
            clic_x = evento.pos[0]
            clic_y = evento.pos[1]

            # Determino cual es la respuesta que eligieron los participantes
            texto_respuesta_maquina = determinar_respuesta_maquina(opcion_rojo, opcion_azul, votos_rojo, votos_azul)
            # Obtengo el string que es la respuesta mas votada
            respuesta_correcta = obtener_respuesta_mas_votada(texto_respuesta_maquina)

            # Cambio la respuesta del usuario segun donde hace click
            if rectangulo_rojo.collidepoint(clic_x, clic_y):
                respuesta_usuario = opcion_rojo
            elif rectangulo_azul.collidepoint(clic_x, clic_y):
                respuesta_usuario = opcion_azul
            elif rectangulo_next.collidepoint(clic_x, clic_y):
                respuesta_usuario = 'next'
            elif rectangulo_half.collidepoint(clic_x, clic_y):
                respuesta_usuario = 'half'
            elif rectangulo_reload.collidepoint(clic_x, clic_y):
                respuesta_usuario = 'reload'
            else:
                respuesta_usuario = None

            # Manejo las diferentes respuestas del usuario si clickeó algún comodín
            if respuesta_usuario == 'next':
                if bandera_next:
                    respuesta_usuario = respuesta_correcta
                    bandera_next = False
                else:
                    bandera_mensaje_comodin = True
                    tiempo_respuesta = pygame.time.get_ticks()
            elif respuesta_usuario == 'half':
                if bandera_half:
                    bandera_mensaje_half = True
                    tiempo_mensaje_half = pygame.time.get_ticks()
                    bandera_half = False
                else:
                    bandera_mensaje_comodin = True
                    tiempo_respuesta = pygame.time.get_ticks()
            elif respuesta_usuario == 'reload':
                if bandera_reload:
                    pregunta_actual = elegir_pregunta_random(preguntas_disponibles)
                    temporizador = 0
                    bandera_reload = False
                else:
                    bandera_mensaje_comodin = True
                    tiempo_respuesta = pygame.time.get_ticks()

            # Manejo las respuestas del usuario si clickeó alguna opción
            if respuesta_usuario in [opcion_rojo, opcion_azul]:
                bandera_mostrar_respuesta = True
                bandera_mostrar_pregunta = False
                tiempo_respuesta = pygame.time.get_ticks()
                # Elijo la próxima pregunta actual
                pregunta_actual = elegir_pregunta_random(preguntas_disponibles)
                # Valido que la respuesta del usuario sea correcta
                validacion = validar_respuesta_corecta(respuesta_correcta, respuesta_usuario)
                if validacion:
                    acumulador_premio += 1000
                    respuestas_correctas += 1

    # Muestro la respuesta de la pregunta sea correcta o incorrecta
    if bandera_mostrar_respuesta:
        # Reinicio el tiempo cuando cambia la pregunta
        temporizador = 0
        if validacion:
            VENTANA.blit(fondo_respuesta_correcta, (0, 0))
            mostrar_mensaje(fuente_respuesta, COLOR_BLANCO, VENTANA, texto_respuesta_maquina, (60, 40))
            mostrar_mensaje(fuente_respuesta, COLOR_BLANCO, VENTANA, f"Respuesta correcta! Dinero acumulado ${acumulador_premio}", (60, 100))
        else:
            VENTANA.blit(fondo_respuesta_incorrecta, (0, 0))
            mostrar_mensaje(fuente_respuesta, COLOR_BLANCO, VENTANA, texto_respuesta_maquina, (60, 40))
            mostrar_mensaje(fuente_respuesta, COLOR_BLANCO, VENTANA, "Respuesta incorrecta, perdiste.", (60, 100))
            bandera = finalizar_juego(acumulador_premio, respuestas_correctas, bandera)

    # Muestro mensaje de comodin ya utilizado
    if bandera_mensaje_comodin:
        if pygame.time.get_ticks() - tiempo_respuesta < 1500:
            mostrar_mensaje(fuente_texto, COLOR_BLANCO, VENTANA, "Ya utilizaste este comodín", (275, 465), COLOR_NEGRO)
        else:
            bandera_mensaje_comodin = False

    # Muestro ayuda del comodin half
    if bandera_mensaje_half:
        if pygame.time.get_ticks() - tiempo_mensaje_half < 3000:
            mostrar_mensaje(fuente_texto, COLOR_BLANCO, VENTANA, f"La opcion roja tiene {votos_rojo} votos", (275, 465), COLOR_ROJO)
        else:
            bandera_mensaje_half = False

    # Muestro la pregunta, las opciones y comodines
    # únicamente si no se está mostrando la respuesta
    if bandera_mostrar_pregunta or pygame.time.get_ticks() - tiempo_respuesta > 6000:
        # Dibujo las opciones y comodines
        dibujar_rectangulo(VENTANA, COLOR_ROJO, rectangulo_rojo)
        dibujar_rectangulo(VENTANA, COLOR_AZUL, rectangulo_azul)
        dibujar_rectangulo(VENTANA, COLOR_BLANCO, rectangulo_next)
        dibujar_rectangulo(VENTANA, COLOR_BLANCO, rectangulo_half)
        dibujar_rectangulo(VENTANA, COLOR_BLANCO, rectangulo_reload)
        # Tiempo desde que se muestra la pregunta
        mostrar_mensaje(fuente_respuesta, COLOR_NEGRO, VENTANA, f"Tiempo: {temporizador}", (60,100))
        # Muestro los textos de las preguntas, opciones y comodines
        mostrar_mensaje(fuente_texto, COLOR_NEGRO, VENTANA, texto_pregunta, (150, 300))
        mostrar_opciones(fuente_botones, COLOR_BLANCO, VENTANA, opcion_rojo, opcion_azul, rectangulo_rojo, rectangulo_azul)
        mostrar_comodines(fuente_botones, COLOR_BLANCO, VENTANA, rectangulo_next, rectangulo_half, rectangulo_reload, fondo_comodin)
        # Cambio el estado de las banderas para que se muestre la pregunta y
        # no se muestre la respuesta en la siguiente iteracion
        bandera_mostrar_respuesta = False
        bandera_mostrar_pregunta = True

    # Aumento el temporizador
    if pygame.time.get_ticks() - tiempo_inicio_pregunta > 1000:
        temporizador += 1
        tiempo_inicio_pregunta = pygame.time.get_ticks()

    # Si se termina el tiempo, finaliza el juego luego de mostrar un mensaje
    if temporizador > 15:
        mostrar_mensaje(fuente_texto, COLOR_NEGRO, VENTANA, "Se acabó el tiempo, juego finalizado.", (60,130), COLOR_ROJO)
        bandera = finalizar_juego(acumulador_premio, respuestas_correctas, bandera)

    # Si el usuario contesta todas las preguntas, finaliza el juego
    if not pregunta_actual:
        mostrar_mensaje(fuente_texto, COLOR_BLANCO, VENTANA, "GANASTE EL JUEGO, FELICIDADES!!!", (60,130))
        bandera = finalizar_juego(acumulador_premio, respuestas_correctas, bandera)

    pygame.display.update()
