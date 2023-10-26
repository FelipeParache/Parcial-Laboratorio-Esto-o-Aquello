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
import re
from Funciones.funciones_calcular import calcular_promedio_votantes, calcular_respuesta_ganadora

def determinar_respuesta_maquina(valor_rojo:str, valor_azul:str, votos_rojo:int, votos_azul:int) -> str:
    '''
    Brief: Recibe el diccionario que contiene la pregunta actual,
    determina los votos de los participantes y calcula el promedio de cada uno
    Parameters:
        pregunta_actual -> Diccionario que contiene una pregunta y dos respuestas
    Return:
        str -> Respuesta de los participantes formateada
    '''
    try:
        if type(valor_rojo) is str and type(valor_azul) is str:
            respuesta_ganadora = calcular_respuesta_ganadora(votos_rojo, votos_azul, valor_rojo, valor_azul)
            promedio = calcular_promedio_votantes(votos_rojo, votos_azul)
            obtener_promedio_mayor = lambda promedio: promedio[0] if promedio[0] > promedio[1] else promedio[1]
            return f"La opcion más votada por los participantes es {respuesta_ganadora} con un {obtener_promedio_mayor(promedio)}%"
        return ''
    except TypeError as e:
        print(f"Hubo un error al determinar el promedio mayor: {e}")

def obtener_respuesta_mas_votada(texto: str) -> str:
    '''
    Brief: Recibe la respuesta de los votantes y con una regex obtiene la respuesta mas votada
    Parameters:
        texto -> Texto donde esta la respuesta mas votada
    Return:
        str -> Respuesta mas votada
    '''
    try:
        match = re.search(r'La opcion más votada por los participantes es (\w+)', texto)
        if match:
            return match.group(1)
        return ''
    except TypeError as e:
        print(f"Hubo un error al obtener la respuesta correcta: {e}")

def validar_respuesta_corecta(respuesta_correcta:str, respuesta_usuario:str) -> bool:
    '''
    Brief: Recibe la respuesta correcta y la respuesta del usuario y determina si son iguales
    Parameters:
        respuesta_correcta -> Respuesta mas votada
        respuesta_usuario -> Respuesta del usuario
    Return:
        bool -> True si la respuesta del usuario es correcta, False en caso contrario
    '''
    if type(respuesta_correcta) == str and type(respuesta_usuario) == str:
        if respuesta_usuario == respuesta_correcta:
            return True
        return False
    return False