"""Cambios visuales del mapa: dibujo sobre imagen satelital fija."""

from __future__ import annotations

from calculos import CalculosIndirectos
from estilizacion.moldes_widgets import COLOR_ACENTO, COLOR_BORDE, COLOR_TEXTO


class LogicaMapa:
    def __init__(self, root, map_widget, estado_var, zoom_info_var):
        self.root = root
        self.map_widget = map_widget
        self.estado_var = estado_var
        self.zoom_info_var = zoom_info_var
        self.resultado_actual = None
        self.zoom_info_var.set("Escala: segmento blanco = 5 km")
        if self.map_widget is not None:
            self.map_widget.bind("<Configure>", lambda _event: self._redibujar_actual(), add="+")
        self.marcar_posicion_inicial()

    def marcar_posicion_inicial(self) -> None:
        self.estado_var.set("Imagen satelital local cargada. Presiona Calcular para dibujar el modelo.")

    def actualizar_resultados(self, resultado, valores: dict) -> None:
        valores["Curvas cubicas"].configure(text=f"{resultado.curvas} curvas\n{resultado.curvas // 2} superiores + {resultado.curvas // 2} inferiores")
        valores["Area Riemann"].configure(text=f"{resultado.area_riemann_km2:.3f} km2\nerror {resultado.error_riemann_pct:+.2f}%")
        valores["Area por integral"].configure(text=f"{resultado.area_integral_km2:.3f} km2\nerror {resultado.error_integral_pct:+.2f}%")
        valores["Datos"].configure(text=f"Oficial: {CalculosIndirectos.AREA_OFICIAL_KM2:.1f} km2\nVolumen: {resultado.volumen_km3:.3f} km3")
        self.dibujar_modelo(resultado)

    def dibujar_modelo(self, resultado) -> None:
        if self.map_widget is None:
            return
        self.resultado_actual = resultado
        self.map_widget.update_idletasks()
        self.map_widget.delete("modelo")
        self._dibujar_area_lago_real()
        self._dibujar_cuadricula()
        self._dibujar_contorno_base()
        self._dibujar_contorno_modelado(resultado.curvas)
        salto, cantidad_lineas = self._dibujar_riemann(resultado.n, resultado.curvas)
        self._dibujar_ejes_escala_y_puntos(resultado.curvas)
        self._dibujar_centroide(resultado)
        self._actualizar_estado(resultado.n, resultado.curvas, salto, cantidad_lineas)

    def _redibujar_actual(self) -> None:
        if self.resultado_actual is not None:
            self.root.after_idle(lambda: self.dibujar_modelo(self.resultado_actual))

    def _pixel_modelo(self, punto: tuple[float, float]) -> tuple[float, float]:
        lat, lon = CalculosIndirectos.punto_modelo_a_geo(punto)
        return self.map_widget.geo_a_pixel(lat, lon)

    def _linea(self, puntos: list[tuple[float, float]], color: str, ancho: int) -> None:
        coords = []
        for punto in puntos:
            coords.extend(self._pixel_modelo(punto))
        self.map_widget.create_line(*coords, fill=color, width=ancho, tags="modelo", capstyle="round", joinstyle="round")

    def _coords(self, puntos: list[tuple[float, float]]) -> list[float]:
        coords = []
        for punto in puntos:
            coords.extend(self._pixel_modelo(punto))
        return coords

    def _texto(self, punto: tuple[float, float], texto: str, color: str = COLOR_TEXTO) -> None:
        x, y = self._pixel_modelo(punto)
        self.map_widget.create_text(x, y, text=texto, fill=color, font=("Segoe UI", 10, "bold"), tags="modelo")

    def _punto(self, punto: tuple[float, float], color: str, radio: int = 3) -> None:
        x, y = self._pixel_modelo(punto)
        self.map_widget.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color, outline="", tags="modelo")

    def _dibujar_area_lago_real(self) -> None:
        contorno = CalculosIndirectos.puntos_contorno_base()
        self.map_widget.create_polygon(
            *self._coords(contorno),
            outline="",
            fill="#0fd3ff",
            stipple="gray25",
            tags="modelo",
        )

    def _dibujar_cuadricula(self) -> None:
        for inicio, fin, tipo in CalculosIndirectos.lineas_cuadricula_modelo():
            color = "#ffffff" if tipo in ("eje_x", "eje_y") else "#7fdcff"
            self._linea([inicio, fin], color, 3 if tipo in ("eje_x", "eje_y") else 1)

    def _dibujar_contorno_base(self) -> None:
        contorno = CalculosIndirectos.puntos_contorno_base()
        self._linea(contorno + [contorno[0]], "#ffffff", 3)
        for punto in contorno[::5]:
            self._punto(punto, "#ffffff", 2)

    def _dibujar_contorno_modelado(self, curvas: int) -> None:
        coords = self._coords(CalculosIndirectos.puntos_contorno(curvas, 32))
        self.map_widget.create_polygon(*coords, outline=COLOR_BORDE, fill="", width=2, tags="modelo")

    def _dibujar_riemann(self, n: int, curvas: int) -> tuple[int, int]:
        lineas = CalculosIndirectos.lineas_riemann_contorno(n)
        salto = max(1, len(lineas) // 160)
        for punto_inferior, punto_superior in lineas[::salto]:
            self._linea([punto_inferior, punto_superior], COLOR_ACENTO, 1)
        return salto, len(lineas[::salto])

    def _dibujar_ejes_escala_y_puntos(self, curvas: int) -> None:
        inicio, fin, etiqueta = CalculosIndirectos.segmento_escala_modelo()
        self._linea([inicio, fin], "#ffffff", 5)
        self._texto(((inicio[0] + fin[0]) / 2, inicio[1] + 0.35), etiqueta)
        self._texto((10.5, 0.35), "x km")
        self._texto((0.45, 5.0), "y km")
        for _etiqueta_punto, punto in CalculosIndirectos.puntos_control_modelo(curvas):
            self._dibujar_cruz_control(punto)

    def _dibujar_cruz_control(self, punto: tuple[float, float]) -> None:
        x, y = punto
        tamano = 0.11
        self._linea([(x - tamano, y - tamano), (x + tamano, y + tamano)], COLOR_ACENTO, 3)
        self._linea([(x - tamano, y + tamano), (x + tamano, y - tamano)], COLOR_ACENTO, 3)

    def _dibujar_centroide(self, resultado) -> None:
        x = resultado.centroide_x_km
        y = resultado.centroide_y_km
        tamano = 0.22
        self._linea([(x - tamano, y), (x + tamano, y)], COLOR_ACENTO, 4)
        self._linea([(x, y - tamano), (x, y + tamano)], COLOR_ACENTO, 4)
        self._texto((x, y + 0.45), "Centroide / abastecimiento")

    def _actualizar_estado(self, n: int, curvas: int, salto: int, cantidad_lineas: int) -> None:
        texto = f"Modelo con {curvas} curvas cubicas y {cantidad_lineas} lineas de Riemann." if salto == 1 else f"Calculo con n={n} y {curvas} curvas; se muestran {cantidad_lineas} lineas."
        self.estado_var.set(texto)
