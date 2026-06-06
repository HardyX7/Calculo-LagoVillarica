"""Formulas del modelo del Lago Villarrica separadas por tipo de calculo."""

from __future__ import annotations

from functools import lru_cache
from math import cos, pi, radians
from types import SimpleNamespace

from estilizacion.constantes import (
    AREA_OFICIAL_KM2,
    CENTRO_LAGO_LAT,
    CENTRO_LAGO_LON,
    FUENTE_CONTORNO,
    FUENTE_IMAGEN,
    FUENTE_OFICIAL,
    KM_POR_GRADO_LAT,
    OSM_CONTORNO_KM,
    SEMIEJE_MAYOR_KM,
    SEMIEJE_MENOR_KM,
    ZOOM_INICIAL,
    ZOOM_MAXIMO,
    ZOOM_MINIMO,
)


class CalculosIndirectos:
    """Datos de apoyo, conversiones, geometria visual y formateos."""

    CURVAS_MINIMAS = 4
    CURVAS_MAXIMAS = 20
    AREA_OFICIAL_KM2 = AREA_OFICIAL_KM2
    FUENTE_OFICIAL = FUENTE_OFICIAL
    FUENTE_CONTORNO = FUENTE_CONTORNO
    FUENTE_IMAGEN = FUENTE_IMAGEN
    ZOOM_INICIAL = ZOOM_INICIAL
    ZOOM_MINIMO = ZOOM_MINIMO
    ZOOM_MAXIMO = ZOOM_MAXIMO
    CENTRO_LAGO = SimpleNamespace(lat=CENTRO_LAGO_LAT, lon=CENTRO_LAGO_LON)
    X_MIN = min(x for x, _y in OSM_CONTORNO_KM)
    X_MAX = max(x for x, _y in OSM_CONTORNO_KM)
    Y_MIN = min(y for _x, y in OSM_CONTORNO_KM)
    Y_MAX = max(y for _x, y in OSM_CONTORNO_KM)

    @staticmethod
    def validar_curvas(curvas: int) -> int:
        curvas = int(curvas)
        if curvas < CalculosIndirectos.CURVAS_MINIMAS or curvas > CalculosIndirectos.CURVAS_MAXIMAS or curvas % 2 != 0:
            raise ValueError("La cantidad de curvas debe ser par, entre 4 y 20.")
        return curvas

    @staticmethod
    def intersecciones_verticales_contorno(x: float) -> list[float]:
        x = min(max(x, CalculosIndirectos.X_MIN), CalculosIndirectos.X_MAX)
        intersecciones: list[float] = []
        for (x1, y1), (x2, y2) in zip(OSM_CONTORNO_KM, OSM_CONTORNO_KM[1:] + OSM_CONTORNO_KM[:1]):
            if abs(x2 - x1) < 1e-12:
                if abs(x - x1) < 1e-9:
                    intersecciones.extend([y1, y2])
                continue
            if (x1 <= x < x2) or (x2 <= x < x1):
                t = (x - x1) / (x2 - x1)
                intersecciones.append(y1 + t * (y2 - y1))
        return sorted(intersecciones)

    @staticmethod
    def intervalos_verticales_contorno(x: float) -> list[tuple[float, float]]:
        intersecciones = CalculosIndirectos.intersecciones_verticales_contorno(x)
        if len(intersecciones) < 2:
            return []
        return [(intersecciones[i], intersecciones[i + 1]) for i in range(0, len(intersecciones) - 1, 2)]

    @staticmethod
    def limites_verticales(x: float) -> tuple[float, float]:
        intersecciones = CalculosIndirectos.intersecciones_verticales_contorno(x)
        if not intersecciones:
            cercano = min(OSM_CONTORNO_KM, key=lambda punto: abs(punto[0] - x))
            return cercano[1], cercano[1]
        return min(intersecciones), max(intersecciones)

    @staticmethod
    def xs_segmentos(segmentos_por_lado: int) -> list[float]:
        return [
            CalculosIndirectos.X_MIN
            + (CalculosIndirectos.X_MAX - CalculosIndirectos.X_MIN) * i / segmentos_por_lado
            for i in range(segmentos_por_lado + 1)
        ]

    @staticmethod
    def construir_segmento(lado: str, indice: int, a: float, b: float) -> dict:
        puntos_control = []
        for x in [a, a + (b - a) / 3, a + 2 * (b - a) / 3, b]:
            y_inf, y_sup = CalculosIndirectos.limites_verticales(x)
            puntos_control.append((x, y_sup if lado == "superior" else y_inf))
        return {
            "lado": lado,
            "indice": indice,
            "a": a,
            "b": b,
            "coeficientes": CalculosDIRECTOS.interpolar_cubico(puntos_control),
            "puntos_control": tuple(puntos_control),
        }

    @staticmethod
    @lru_cache(maxsize=None)
    def crear_modelo(curvas: int = CURVAS_MINIMAS) -> dict:
        curvas = CalculosIndirectos.validar_curvas(curvas)
        xs = CalculosIndirectos.xs_segmentos(curvas // 2)
        superiores = [
            CalculosIndirectos.construir_segmento("superior", i, a, b)
            for i, (a, b) in enumerate(zip(xs, xs[1:]), start=1)
        ]
        inferiores = [
            CalculosIndirectos.construir_segmento("inferior", i, a, b)
            for i, (a, b) in enumerate(zip(xs, xs[1:]), start=1)
        ]
        return {"curvas": curvas, "superiores": tuple(superiores), "inferiores": tuple(inferiores)}

    @staticmethod
    def segmento_para_x(segmentos: tuple[dict, ...], x: float) -> dict:
        if x <= segmentos[0]["a"]:
            return segmentos[0]
        if x >= segmentos[-1]["b"]:
            return segmentos[-1]
        for segmento in segmentos:
            if segmento["a"] <= x <= segmento["b"]:
                return segmento
        return segmentos[-1]

    @staticmethod
    def km_a_geo(x_km: float, y_km: float) -> SimpleNamespace:
        km_por_grado_lon = KM_POR_GRADO_LAT * cos(radians(CalculosIndirectos.CENTRO_LAGO.lat))
        return SimpleNamespace(
            lat=CalculosIndirectos.CENTRO_LAGO.lat + y_km / KM_POR_GRADO_LAT,
            lon=CalculosIndirectos.CENTRO_LAGO.lon + x_km / km_por_grado_lon,
        )

    @staticmethod
    def punto_modelo_a_geo(punto: tuple[float, float]) -> tuple[float, float]:
        geo = CalculosIndirectos.km_a_geo(punto[0], punto[1])
        return geo.lat, geo.lon

    @staticmethod
    def puntos_contorno(curvas: int = CURVAS_MINIMAS, muestras_por_segmento: int = 22) -> list[tuple[float, float]]:
        modelo = CalculosIndirectos.crear_modelo(curvas)
        puntos_superiores = []
        puntos_inferiores = []
        muestras_por_segmento = max(6, muestras_por_segmento)
        for segmento in modelo["superiores"]:
            for i in range(muestras_por_segmento):
                x = segmento["a"] + (segmento["b"] - segmento["a"]) * i / muestras_por_segmento
                puntos_superiores.append((x, CalculosDIRECTOS.evaluar_polinomio(segmento["coeficientes"], x)))
        puntos_superiores.append(
            (CalculosIndirectos.X_MAX, CalculosDIRECTOS.polinomio_superior(CalculosIndirectos.X_MAX, curvas))
        )
        for segmento in reversed(modelo["inferiores"]):
            for i in range(muestras_por_segmento):
                x = segmento["b"] - (segmento["b"] - segmento["a"]) * i / muestras_por_segmento
                puntos_inferiores.append((x, CalculosDIRECTOS.evaluar_polinomio(segmento["coeficientes"], x)))
        puntos_inferiores.append(
            (CalculosIndirectos.X_MIN, CalculosDIRECTOS.polinomio_inferior(CalculosIndirectos.X_MIN, curvas))
        )
        return puntos_superiores + puntos_inferiores

    @staticmethod
    def puntos_contorno_base() -> list[tuple[float, float]]:
        return list(OSM_CONTORNO_KM)

    @staticmethod
    def lineas_riemann_contorno(n: int) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        if n <= 0:
            raise ValueError("n debe ser un entero positivo.")
        delta_x = (CalculosIndirectos.X_MAX - CalculosIndirectos.X_MIN) / n
        lineas = []
        for i in range(n):
            x = CalculosIndirectos.X_MIN + (i + 0.5) * delta_x
            for y_inferior, y_superior in CalculosIndirectos.intervalos_verticales_contorno(x):
                lineas.append(((x, y_inferior), (x, y_superior)))
        return lineas

    @staticmethod
    def puntos_control_modelo(curvas: int = CURVAS_MINIMAS) -> list[tuple[str, tuple[float, float]]]:
        modelo = CalculosIndirectos.crear_modelo(curvas)
        puntos: list[tuple[str, tuple[float, float]]] = []
        for segmento in modelo["superiores"]:
            for indice, punto in enumerate(segmento["puntos_control"], start=1):
                puntos.append((f"S{segmento['indice']}.{indice}", punto))
        for segmento in modelo["inferiores"]:
            for indice, punto in enumerate(segmento["puntos_control"], start=1):
                puntos.append((f"I{segmento['indice']}.{indice}", punto))
        return puntos

    @staticmethod
    def lineas_cuadricula_modelo() -> list[tuple[tuple[float, float], tuple[float, float], str]]:
        lineas: list[tuple[tuple[float, float], tuple[float, float], str]] = []
        xs = [x for x in (-10.0, -5.0, 0.0, 5.0, 10.0) if CalculosIndirectos.X_MIN <= x <= CalculosIndirectos.X_MAX]
        ys = [y for y in (-5.0, 0.0, 5.0) if CalculosIndirectos.Y_MIN <= y <= CalculosIndirectos.Y_MAX]
        for x in xs:
            lineas.append(((x, CalculosIndirectos.Y_MIN), (x, CalculosIndirectos.Y_MAX), "eje_y" if x == 0.0 else "grid"))
        for y in ys:
            lineas.append(((CalculosIndirectos.X_MIN, y), (CalculosIndirectos.X_MAX, y), "eje_x" if y == 0.0 else "grid"))
        return lineas

    @staticmethod
    def segmento_escala_modelo() -> tuple[tuple[float, float], tuple[float, float], str]:
        y = CalculosIndirectos.Y_MIN + 0.6
        return (CalculosIndirectos.X_MIN + 1.0, y), (CalculosIndirectos.X_MIN + 6.0, y), "5 km"


class CalculosDIRECTOS:
    """Calculos ligados directamente a calculo diferencial e integral."""

    CURVAS_MINIMAS = CalculosIndirectos.CURVAS_MINIMAS
    CURVAS_MAXIMAS = CalculosIndirectos.CURVAS_MAXIMAS
    AREA_OFICIAL_KM2 = CalculosIndirectos.AREA_OFICIAL_KM2
    FUENTE_OFICIAL = CalculosIndirectos.FUENTE_OFICIAL
    FUENTE_CONTORNO = CalculosIndirectos.FUENTE_CONTORNO

    @staticmethod
    def resolver_sistema(matriz: list[list[float]], vector: list[float]) -> list[float]:
        n = len(vector)
        a = [fila[:] + [vector[i]] for i, fila in enumerate(matriz)]
        for col in range(n):
            pivote = max(range(col, n), key=lambda fila: abs(a[fila][col]))
            if abs(a[pivote][col]) < 1e-12:
                raise ValueError("Los puntos no permiten interpolar un polinomio unico.")
            a[col], a[pivote] = a[pivote], a[col]
            divisor = a[col][col]
            for j in range(col, n + 1):
                a[col][j] /= divisor
            for fila in range(n):
                if fila == col:
                    continue
                factor = a[fila][col]
                for j in range(col, n + 1):
                    a[fila][j] -= factor * a[col][j]
        return [a[i][n] for i in range(n)]

    @staticmethod
    def interpolar_cubico(puntos: list[tuple[float, float]]) -> tuple[float, float, float, float]:
        matriz = [[x**potencia for potencia in range(4)] for x, _ in puntos]
        return tuple(CalculosDIRECTOS.resolver_sistema(matriz, [y for _, y in puntos]))

    @staticmethod
    def evaluar_polinomio(coeficientes: tuple[float, ...], x: float) -> float:
        return sum(coef * x**potencia for potencia, coef in enumerate(coeficientes))

    @staticmethod
    def integral_polinomio(coeficientes: tuple[float, ...], a: float, b: float) -> float:
        return sum(
            coef * (b ** (potencia + 1) - a ** (potencia + 1)) / (potencia + 1)
            for potencia, coef in enumerate(coeficientes)
        )

    @staticmethod
    def integral_x_polinomio(coeficientes: tuple[float, ...], a: float, b: float) -> float:
        return sum(
            coef * (b ** (potencia + 2) - a ** (potencia + 2)) / (potencia + 2)
            for potencia, coef in enumerate(coeficientes)
        )

    @staticmethod
    def coeficientes_cuadrado(coeficientes: tuple[float, ...]) -> tuple[float, ...]:
        resultado = [0.0] * (2 * len(coeficientes) - 1)
        for i, coef_i in enumerate(coeficientes):
            for j, coef_j in enumerate(coeficientes):
                resultado[i + j] += coef_i * coef_j
        return tuple(resultado)

    @staticmethod
    def polinomio_superior(x: float, curvas: int = CURVAS_MINIMAS) -> float:
        segmento = CalculosIndirectos.segmento_para_x(CalculosIndirectos.crear_modelo(curvas)["superiores"], x)
        return CalculosDIRECTOS.evaluar_polinomio(segmento["coeficientes"], x)

    @staticmethod
    def polinomio_inferior(x: float, curvas: int = CURVAS_MINIMAS) -> float:
        segmento = CalculosIndirectos.segmento_para_x(CalculosIndirectos.crear_modelo(curvas)["inferiores"], x)
        return CalculosDIRECTOS.evaluar_polinomio(segmento["coeficientes"], x)

    @staticmethod
    def ancho_vertical(x: float, curvas: int = CURVAS_MINIMAS) -> float:
        return CalculosDIRECTOS.polinomio_superior(x, curvas) - CalculosDIRECTOS.polinomio_inferior(x, curvas)

    @staticmethod
    def area_por_riemann(n: int, curvas: int = CURVAS_MINIMAS) -> float:
        curvas = CalculosIndirectos.validar_curvas(curvas)
        if n <= 0:
            raise ValueError("n debe ser un entero positivo.")
        delta_x = (CalculosIndirectos.X_MAX - CalculosIndirectos.X_MIN) / n
        return sum(
            CalculosDIRECTOS.ancho_vertical(CalculosIndirectos.X_MIN + (i + 0.5) * delta_x, curvas) * delta_x
            for i in range(n)
        )

    @staticmethod
    def area_por_integral(curvas: int = CURVAS_MINIMAS) -> float:
        modelo = CalculosIndirectos.crear_modelo(curvas)
        area = 0.0
        for superior, inferior in zip(modelo["superiores"], modelo["inferiores"]):
            area += CalculosDIRECTOS.integral_polinomio(superior["coeficientes"], superior["a"], superior["b"])
            area -= CalculosDIRECTOS.integral_polinomio(inferior["coeficientes"], inferior["a"], inferior["b"])
        return area

    @staticmethod
    def centroide_cartesiano(curvas: int = CURVAS_MINIMAS) -> tuple[float, float]:
        modelo = CalculosIndirectos.crear_modelo(curvas)
        area = CalculosDIRECTOS.area_por_integral(curvas)
        momento_y = 0.0
        momento_x = 0.0
        for superior, inferior in zip(modelo["superiores"], modelo["inferiores"]):
            momento_y += CalculosDIRECTOS.integral_x_polinomio(superior["coeficientes"], superior["a"], superior["b"])
            momento_y -= CalculosDIRECTOS.integral_x_polinomio(inferior["coeficientes"], inferior["a"], inferior["b"])
            sup2 = CalculosDIRECTOS.coeficientes_cuadrado(superior["coeficientes"])
            inf2 = CalculosDIRECTOS.coeficientes_cuadrado(inferior["coeficientes"])
            momento_x += 0.5 * (
                CalculosDIRECTOS.integral_polinomio(sup2, superior["a"], superior["b"])
                - CalculosDIRECTOS.integral_polinomio(inf2, inferior["a"], inferior["b"])
            )
        return momento_y / area, momento_x / area

    @staticmethod
    def volumen_modelo_km3() -> float:
        return 2 * pi * SEMIEJE_MAYOR_KM * SEMIEJE_MENOR_KM**2 / 3

    @staticmethod
    def calcular_modelo(n: int, curvas: int = CURVAS_MINIMAS) -> SimpleNamespace:
        curvas = CalculosIndirectos.validar_curvas(curvas)
        area_riemann = CalculosDIRECTOS.area_por_riemann(n, curvas)
        area_integral = CalculosDIRECTOS.area_por_integral(curvas)
        volumen = CalculosDIRECTOS.volumen_modelo_km3()
        centroide_x, centroide_y = CalculosDIRECTOS.centroide_cartesiano(curvas)
        return SimpleNamespace(
            n=n,
            curvas=curvas,
            area_riemann_km2=area_riemann,
            area_integral_km2=area_integral,
            error_riemann_pct=100 * (area_riemann - CalculosDIRECTOS.AREA_OFICIAL_KM2) / CalculosDIRECTOS.AREA_OFICIAL_KM2,
            error_integral_pct=100 * (area_integral - CalculosDIRECTOS.AREA_OFICIAL_KM2) / CalculosDIRECTOS.AREA_OFICIAL_KM2,
            volumen_km3=volumen,
            volumen_millones_m3=volumen * 1000,
            centroide_x_km=centroide_x,
            centroide_y_km=centroide_y,
            centroide_geo=CalculosIndirectos.km_a_geo(centroide_x, centroide_y),
        )
