"""
Constantes para el cálculo del área del lago.
"""


"""
La escala del grafico realizado en geogebra, donde 1 unidad en el grafico 
equivale a 0.766666666666667 km en la realidad.
"""
ESCALA = 0.766

"""
La escala al cuadrado, para convertir áreas del grafico a km2.
"""
ESCALA_KM2 = ESCALA ** 2

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