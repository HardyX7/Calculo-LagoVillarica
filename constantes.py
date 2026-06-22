"""
Constantes para el cálculo del área del lago.
"""


"""
La escala del grafico realizado en geogebra, donde 1 unidad en el grafico 
equivale a 0.766666666666667 km en la realidad.
"""
from mapa.escala import escala_lago

ESCALA = int(escala_lago.factor)

"""
La escala al cuadrado, para convertir áreas del grafico a km2.
"""
ESCALA_KM2 = escala_lago.aplicar(ESCALA)
""""""""""
escala de metros a km
"""""""""""
KM2_A_M2 = 1_000_000
M2_A_KM2 = 1000000000
"""
Intervalo de integración para el cálculo del área entre las curvas f y g.
"""
INTERVALO = (0, 22.5)

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


from pathlib import Path

RUTA_IMAGENES = Path(__file__).parent / "images"
print(RUTA_IMAGENES)
RUTA_FONDO = RUTA_IMAGENES / "MoldeFondo.png"

COLOR_FONDO = "#030b15"
COLOR_PANEL = "#061827"
COLOR_PANEL_CLARO = "#0a2236"
COLOR_BORDE = "#00c8ff"
COLOR_TEXTO = "#eaf7ff"
COLOR_TEXTO_SUAVE = "#93b7c7"
COLOR_ACENTO = "#ffb45a"
COLOR_BOTON = "#0d344f"
COLOR_BOTON_ACTIVO = "#144a70"
COLOR_BARRA = "#05131f"
