"""Resultados numericos del modelo del Lago Villarrica.

Usa las funciones por tramos de functions/ y las clases de Area/ para calcular
las magnitudes pedidas por el proyecto.
"""

from __future__ import annotations

from dataclasses import dataclass

from Area.Integral import Integral
from Area.area_entre_curvas_riemann import AreaEntreCurvasRiemann
from Area.metodos_riemann import PuntoMedio
from functions.funciones import f, g
from Area.area_entre_curvas_integral import AreaEntreCurvasIntegral
from constantes import AREA_REFERENCIA_KM2, INTERVALO

punto_medio = PuntoMedio()


@dataclass(frozen=True)
class ResultadoLago:
    n: int
    curvas: int
    curvas_por_lado: int
    area_riemann_km2: float
    area_integral_km2: float
    error_riemann_pct: float
    error_integral_pct: float

def calcular_resultados(n: int) -> ResultadoLago:
    n = int(n)
    area_riemann_km2 = AreaEntreCurvasRiemann(f, g, n, punto_medio).area_escalada(INTERVALO)
    area_integral_km2 = AreaEntreCurvasIntegral(f, g).area_escalada(INTERVALO)

    curvas = len(f.tramos) + len(g.tramos)
    return ResultadoLago(
        n=n,
        curvas=curvas,
        curvas_por_lado=curvas // 2,
        area_riemann_km2=area_riemann_km2,
        area_integral_km2=area_integral_km2,
        error_riemann_pct=100 * (area_riemann_km2 - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2,
        error_integral_pct=100 * (area_integral_km2 - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2,
    )


def tabla_riemann(valores_n: tuple[int, ...] = (15, 30, 60, 100)) -> str:
    lineas = ["n     area km2     error"]
    for n in valores_n:
        area = AreaEntreCurvasRiemann(f, g, n, punto_medio).area_escalada(INTERVALO)
        error = 100 * (area - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2
        lineas.append(f"{n:<5} {area:>8.3f}   {error:>+6.2f}%")
    return "\n".join(lineas)
