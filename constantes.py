"""
Constantes para el cálculo del área del lago.
"""


"""
La escala del grafico realizado en geogebra, donde 1 unidad en el grafico 
equivale a 0.766666666666667 km en la realidad.
"""
from mapa.escala import escala_lago

ESCALA = escala_lago.factor

"""
La escala al cuadrado, para convertir áreas del grafico a km2.
"""
ESCALA_KM2 = escala_lago.aplicar(ESCALA)

"""
Intervalo de integración para el cálculo del área entre las curvas f y g.
"""
INTERVALO = (0, 30)

"""
Area de referencia para el lago Villarrica, según la Ilustre Municipalidad de Villarrica.
"""
AREA_REFERENCIA_KM2 = 176


"""
Fuente de la información del área de referencia del lago Villarrica.
"""
FUENTE_REFERENCIA = "Ilustre Municipalidad de Villarrica: extension aproximada 176 km2."


COLOR_MAPA_FONDO = "#061827"
COLOR_MAPA_NORTE = "#ffb45a"
COLOR_MAPA_SUR = "#eaf7ff"
COLOR_MAPA_AREA = "#00c8ff"
COLOR_MAPA_LEYENDA = "#0a2236"
