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

def calcular_promedio_votantes(votos_rojo:int, votos_azul:int) -> list:
    '''
    Brief: Recibe los valores numericos de los votos y
    determina el promedio de cada uno
    Parameters:
        votos_rojo -> Entero que representa los votos de la opcion roja
        votos_azul -> Entero que representa los votos de la opcion azul
    Return:
        list -> Lista que contiene el promedio de los votos de cada opcion
    '''
    try:
        total_votos = votos_rojo + votos_azul
        retorno_promedios = []
        promedio_rojo = (votos_rojo / total_votos) * 100
        promedio_azul = (votos_azul / total_votos) * 100
        retorno_promedios.append(promedio_rojo)
        retorno_promedios.append(promedio_azul)
        return retorno_promedios
    except ZeroDivisionError:
        print("No se puede dividir por cero, revisa los valores de 'votos_rojo' y 'votos_azul'")

def calcular_respuesta_ganadora(votos_rojo:int, votos_azul:int, valor_rojo:str, valor_azul:str) -> str:
    '''
    Brief: Recibe los valores numericos de los votos y las opciones
    de la pregunta para determinar la respuesta mas y menos votada
    Parameters:
        votos_rojo -> Entero que representa los votos de la opcion roja
        votos_azul -> Entero que representa los votos de la opcion azul
        valor_rojo -> String que representa el valor de la clave rojo
        valor_azul -> String que representa el valor de la clave azul
    Return:
        str -> Respuesta ganadora
    '''
    if votos_rojo >= 0 and votos_azul >= 0:
        if type(valor_rojo) == str and type(valor_azul) == str:
            respuesta_ganadora = ''
            if votos_rojo > votos_azul:
                respuesta_ganadora = valor_rojo
            else:
                respuesta_ganadora = valor_azul
            return respuesta_ganadora
        return ''
    return ''
