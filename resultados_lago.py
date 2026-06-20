"""Resultados numericos del modelo del Lago Villarrica.

Usa las funciones por tramos de functions/ y las clases de Area/ para calcular
las magnitudes pedidas por el proyecto.
"""

from __future__ import annotations
from dataclasses import dataclass
from Area.area_entre_curvas_riemann import AreaEntreCurvasRiemann
from Area.metodos_riemann import PuntoMedio
from functions.funciones import f, g
from functions.funcion_por_tramos import FuncionPorTramos
from Area.area_entre_curvas_integral import AreaEntreCurvasIntegral
from constantes import AREA_REFERENCIA_KM2, INTERVALO

punto_medio = PuntoMedio()


@dataclass(frozen=True)
class ResultadoLago:
    
    """
    Clase que representa los resultados de un experimento de la función por tramos.
    """
    
    n: int
    curvas: int
    curvas_por_lado: int
    area_riemann_km2: float
    area_integral_km2: float
    error_riemann_pct: float
    error_integral_pct: float

class CalcularResultados:
    
    """
    Clase que calcula los resultados de un experimento de la función por tramos.
    Devuelve un objeto ResultadoLago, que contiene los resultados del calculo del lago.
    
    Uso:
    
    -from resultados_lago import CalcularResultados
    -resultados = CalcularResultados(f, g, intervalo, n).calcular()
    
    Donde:
    
    -f es la función por tramos de la parte superior de la curva
    -g es la función por tramos de la parte inferior de la curva
    -intervalo es el intervalo (a, b) en el que se calculan las curvas
    -n es el numero de rectangulos para la suma de Riemann
    
    Devuelve:
    
    resultados.n # número de rectangulos para la suma de Riemann
    resultados.curvas # número de curvas
    resultados.curvas_por_lado # número de curvas por lado
    resultados.area_riemann_km2 # área de Riemann escalada
    resultados.area_integral_km2 # área de integral escalada
    resultados.error_riemann_pct # error de Riemann
    resultados.error_integral_pct # error de integral
    """
    
    def __init__(
            self, 
            f: FuncionPorTramos,
            g: FuncionPorTramos,
            intervalo: tuple[float, float],
            n: int,
        ) -> None:
        
        self.f = f
        self.g = g
        self.intervalo = intervalo
        self.n = n

    def calcular(self) -> ResultadoLago:
        
        """
        Entrega el resultado de la medicion del lago.
        """
        
        area_riemann_km2 = AreaEntreCurvasRiemann(self.f, self.g, self.n, punto_medio).area_escalada(self.intervalo)
        area_integral_km2 = AreaEntreCurvasIntegral(self.f, self.g).area_escalada(self.intervalo)
        curvas = len(self.f.tramos) + len(self.g.tramos)
        return ResultadoLago(
            n=self.n,
            curvas=curvas,
            curvas_por_lado=curvas // 2,
            area_riemann_km2=area_riemann_km2,
            area_integral_km2=area_integral_km2,
            error_riemann_pct=100 * (area_riemann_km2 - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2,
            error_integral_pct=100 * (area_integral_km2 - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2,
        )

"""

Lo quito chavalines???

def tabla_riemann(valores_n: tuple[int, ...] = (15, 30, 60, 100)) -> str:
    lineas = ["n     area km2     error"]
    for n in valores_n:
        area = AreaEntreCurvasRiemann(f, g, n, punto_medio).area_escalada(INTERVALO)
        error = 100 * (area - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2
        lineas.append(f"{n:<5} {area:>8.3f}   {error:>+6.2f}%")
    return "\n".join(lineas)
"""
