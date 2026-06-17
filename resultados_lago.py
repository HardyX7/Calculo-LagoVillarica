"""Resultados numericos del modelo del Lago Villarrica.

Usa las funciones por tramos de functions/ y las clases de Area/ para calcular
las magnitudes pedidas por el proyecto.
"""

from __future__ import annotations

from dataclasses import dataclass

from Area.Integral import Integral
from Area.suma_riemann import SumaRiemann
from Area.metodos_riemann import PuntoMedio
from functions.funciones import f, g
from Area.area_entre_curvas import AreaEntreCurvas
from constantes import AREA_REFERENCIA_KM2, FUENTE_REFERENCIA

punto_medio = PuntoMedio()

h = AreaEntreCurvas(f, g)


@dataclass(frozen=True)
class ResultadoLago:
    n: int
    curvas: int
    curvas_por_lado: int
    area_riemann_km2: float
    area_integral_km2: float
    error_riemann_pct: float
    error_integral_pct: float


def area_por_riemann(n: int) -> float:
    return SumaRiemann(h, n, punto_medio)()


def area_por_integral() -> float:
    return Integral(h)()


def calcular_resultados(n: int) -> ResultadoLago:
    n = int(n)
    area_riemann = area_por_riemann(n)
    area_integral = area_por_integral()

    curvas = len(f.tramos) + len(g.tramos)
    return ResultadoLago(
        n=n,
        curvas=curvas,
        curvas_por_lado=curvas // 2,
        area_riemann_km2=area_riemann,
        area_integral_km2=area_integral,
        error_riemann_pct=100 * (area_riemann - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2,
        error_integral_pct=100 * (area_integral - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2,
    )


def tabla_riemann(valores_n: tuple[int, ...] = (15, 30, 60, 100)) -> str:
    lineas = ["n     area km2     error"]
    for n in valores_n:
        area = area_por_riemann(n)
        error = 100 * (area - AREA_REFERENCIA_KM2) / AREA_REFERENCIA_KM2
        lineas.append(f"{n:<5} {area:>8.3f}   {error:>+6.2f}%")
    return "\n".join(lineas)
