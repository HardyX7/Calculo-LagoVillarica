"""Vista principal: pantalla, widgets y botones."""

from __future__ import annotations

import tkinter as tk

from calculos import CalculosDIRECTOS, CalculosIndirectos
from cambios_visuales_mapa import LogicaMapa
from estilizacion.moldes_widgets import COLOR_ACENTO, COLOR_BARRA, COLOR_BOTON, COLOR_BOTON_ACTIVO, COLOR_FONDO, COLOR_MAPA, COLOR_PANEL, COLOR_TEXTO, COLOR_TEXTO_SUAVE, Crear

TEXTO_LIMITACIONES = "Limitaciones: imagen satelital y escala aproximadas; puntos de borde seleccionados manualmente; cuatro cubicas suavizan un contorno real irregular; Riemann mejora al aumentar n; el volumen usa secciones semicirculares idealizadas y no batimetria real."
class VistaPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modelo Lago Villarrica - Riemann, integral, volumen y centroide")
        self.root.geometry("1400x780")
        self.root.minsize(1180, 680)
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda _event: self.root.attributes("-fullscreen", False))
        self.root.configure(bg=COLOR_FONDO)
        self.crear = Crear()
        self.fuentes = self.crear.fuentes(self.root)
        self.fondo = self.crear.fondo(self.root)
        self.fondo.pack(fill="both", expand=True)
        self.n_var = tk.StringVar(value="15")
        self.curvas_var = tk.StringVar(value=str(CalculosIndirectos.CURVAS_MAXIMAS))
        self.estado_var = tk.StringVar(value="Elige opciones y presiona Calcular.")
        self.zoom_info_var = tk.StringVar(value="Escala: segmento blanco = 5 km")
        self.valores = {}
        self.ultimo_resultado = None
        self.map_widget = None
        self.al_presionar_boton = AL_PRESIONAR_BOTON(self)
        self.crear_widgets = CrearWidgets(self)
        self.crear_widgets.ejecutar()
        self.logica_mapa = LogicaMapa(self.root, self.map_widget, self.estado_var, self.zoom_info_var)

    def ejecutar(self) -> None:
        self.root.mainloop()

class CrearWidgets:
    def __init__(self, vista):
        self.vista = vista
        self.crear = vista.crear
        self.botones_n = {}
        self.botones_curvas = {}
        self.contenido_izquierdo = None

    def ejecutar(self) -> None:
        self.panel_izquierdo()
        self.panel_mapa()

    def panel_izquierdo(self) -> None:
        v = self.vista
        panel = self.crear.frame(v.fondo, fondo=COLOR_PANEL, borde=True)
        panel.place(relx=0.03, rely=0.055, relwidth=0.245, relheight=0.89)
        self.contenido_izquierdo = self.crear.frame(panel, fondo=COLOR_PANEL)
        self.contenido_izquierdo.pack(fill="both", expand=True)
        self.mostrar_inicio()

    def limpiar_panel_izquierdo(self) -> None:
        for widget in self.contenido_izquierdo.winfo_children():
            widget.destroy()

    def mostrar_inicio(self) -> None:
        v = self.vista
        contenido = self.contenido_izquierdo
        self.botones_n = {}
        self.botones_curvas = {}
        v.valores = {}
        self.limpiar_panel_izquierdo()
        self.crear.etiqueta(contenido, "Lago Villarrica\nmodelo de calculo", fuentes=v.fuentes, estilo="titulo", fondo=COLOR_PANEL, color=COLOR_TEXTO, justify="left", anchor="w").pack(fill="x", padx=16, pady=(14, 2))
        self.crear.etiqueta(contenido, "Area, integral, volumen, centroide y punto de abastecimiento", fuentes=v.fuentes, estilo="subtitulo", fondo=COLOR_PANEL, color=COLOR_TEXTO_SUAVE, justify="left", wraplength=310, anchor="w").pack(fill="x", padx=16, pady=(0, 10))
        self.controles(contenido)
        self.tarjetas(contenido)
        self.crear.etiqueta(contenido, fuentes=v.fuentes, estilo="texto", fondo=COLOR_PANEL, color=COLOR_ACENTO, textvariable=v.estado_var, wraplength=310, justify="left", anchor="w").pack(fill="x", padx=16, pady=(0, 12))
        if v.ultimo_resultado is not None and hasattr(v, "logica_mapa"):
            v.logica_mapa.actualizar_resultados(v.ultimo_resultado, v.valores)

    def mostrar_detalle(self, titulo: str, cuerpo: str) -> None:
        v = self.vista
        contenido = self.contenido_izquierdo
        self.limpiar_panel_izquierdo()
        self.crear.boton(contenido, "Volver", self.mostrar_inicio, fuentes=v.fuentes, pequeno=True).pack(fill="x", padx=16, pady=(14, 10))
        self.crear.etiqueta(contenido, titulo, fuentes=v.fuentes, estilo="titulo", fondo=COLOR_PANEL, color=COLOR_TEXTO, justify="left", anchor="w", wraplength=310).pack(fill="x", padx=16, pady=(0, 8))
        self.crear.etiqueta(contenido, cuerpo, fuentes=v.fuentes, estilo="texto", fondo=COLOR_PANEL, color=COLOR_TEXTO, justify="left", anchor="nw", wraplength=320).pack(fill="both", expand=True, padx=16, pady=(0, 14))

    def controles(self, panel) -> None:
        v = self.vista
        controles = self.crear.frame(panel, fondo=COLOR_PANEL)
        controles.pack(fill="x", padx=16, pady=(0, 8))
        self.crear.etiqueta(controles, "n para suma de Riemann", fuentes=v.fuentes, estilo="etiqueta", fondo=COLOR_PANEL, color=COLOR_TEXTO, anchor="w").pack(fill="x")
        fila_n = self.crear.frame(controles, fondo=COLOR_PANEL)
        fila_n.pack(fill="x", pady=(6, 8))
        for n in (15, 30, 60, 100):
            boton = self.crear.boton(fila_n, str(n), lambda valor=n: self.seleccionar_n(valor), fuentes=v.fuentes)
            boton.pack(side="left", expand=True, fill="x", padx=(0, 6))
            self.botones_n[str(n)] = boton
        self.crear.etiqueta(controles, "curvas polinomiales cubicas", fuentes=v.fuentes, estilo="etiqueta", fondo=COLOR_PANEL, color=COLOR_TEXTO, anchor="w").pack(fill="x", pady=(8, 0))
        fila_curvas = self.crear.frame(controles, fondo=COLOR_PANEL)
        fila_curvas.pack(fill="x", pady=(6, 8))
        for curvas in (4, 8, 12, 20):
            boton = self.crear.boton(fila_curvas, str(curvas), lambda valor=curvas: self.seleccionar_curvas(valor), fuentes=v.fuentes)
            boton.pack(side="left", expand=True, fill="x", padx=(0, 6))
            self.botones_curvas[str(curvas)] = boton
        self.crear.boton(controles, "Calcular", lambda: v.al_presionar_boton.Presionar_buscar(v.n_var.get(), v.curvas_var.get()), fuentes=v.fuentes).pack(fill="x", pady=(2, 0))
        self.marcar_seleccionados()

    def seleccionar_n(self, valor: int) -> None:
        self.vista.n_var.set(str(valor))
        self.marcar_seleccionados()

    def seleccionar_curvas(self, valor: int) -> None:
        self.vista.curvas_var.set(str(valor))
        self.marcar_seleccionados()

    def marcar_seleccionados(self) -> None:
        self.marcar_grupo(self.botones_n, self.vista.n_var.get())
        self.marcar_grupo(self.botones_curvas, self.vista.curvas_var.get())

    def marcar_grupo(self, botones: dict, seleccionado: str) -> None:
        for valor, boton in botones.items():
            activo = valor == seleccionado
            boton.configure(bg=COLOR_ACENTO if activo else COLOR_BOTON, fg="#03101a" if activo else COLOR_TEXTO, activebackground=COLOR_ACENTO if activo else COLOR_BOTON_ACTIVO)

    def tarjetas(self, panel) -> None:
        datos = [
            ("Curvas cubicas", "Pendiente\npresiona Calcular", self.vista.al_presionar_boton.Presionar_profundizar_curvas_cubicas),
            ("Area Riemann", "Pendiente\npresiona Calcular", self.vista.al_presionar_boton.Presionar_profundizar_riemman),
            ("Area por integral", "Pendiente\npresiona Calcular", self.vista.al_presionar_boton.Presionar_profundizar_integral),
            ("Datos", f"Oficial: {CalculosIndirectos.AREA_OFICIAL_KM2:.1f} km2\nver discusion critica", self.vista.al_presionar_boton.Presionar_profundizar_datos),
        ]
        for titulo, valor, comando in datos:
            tarjeta, etiqueta_valor = self.crear.tarjeta(panel, titulo=titulo, valor_inicial=valor, fuentes=self.vista.fuentes, comando_profundizar=comando)
            tarjeta.pack(fill="x", padx=16, pady=(0, 6))
            self.vista.valores[titulo] = etiqueta_valor

    def panel_mapa(self) -> None:
        v = self.vista
        panel = self.crear.frame(v.fondo, fondo=COLOR_MAPA, borde=True)
        panel.place(relx=0.30, rely=0.055, relwidth=0.665, relheight=0.89)
        encabezado = self.crear.frame(panel, fondo=COLOR_BARRA)
        encabezado.pack(fill="x")
        self.crear.etiqueta(encabezado, "Imagen satelital del Lago Villarrica", fuentes=v.fuentes, estilo="etiqueta", fondo=COLOR_BARRA, color=COLOR_TEXTO, anchor="w").pack(side="left", padx=14, pady=8)
        self.crear.etiqueta(encabezado, fuentes=v.fuentes, estilo="texto", fondo=COLOR_BARRA, color=COLOR_TEXTO_SUAVE, textvariable=v.zoom_info_var, anchor="e").pack(side="right", padx=14, pady=8)
        v.map_widget = self.crear.mapa(panel, fuentes=v.fuentes)


class AL_PRESIONAR_BOTON:
    def __init__(self, vista):
        self.vista = vista

    def Presionar_buscar(self, n, cantidad_curvas_polinomiales) -> None:
        n = int(n)
        curvas = int(cantidad_curvas_polinomiales)

        self.vista.ultimo_resultado = CalculosDIRECTOS.calcular_modelo(n, curvas)
        self.vista.logica_mapa.actualizar_resultados(self.vista.ultimo_resultado, self.vista.valores)

    def Presionar_profundizar_curvas_cubicas(self) -> None:
        resultado = self.vista.ultimo_resultado or CalculosDIRECTOS.calcular_modelo(int(self.vista.n_var.get()), int(self.vista.curvas_var.get()))
        cuerpo = (
            f"Modelo actual: {resultado.curvas} curvas cubicas.\n\n"
            "Cumplimiento de la rubrica: se construyen al menos 4 curvas polinomiales de grado 3, "
            "con 2 curvas superiores y 2 curvas inferiores. Cuando se eligen 8, 12 o 20 curvas, "
            "se mantiene el mismo metodo pero con mas tramos.\n\n"
            f"Se usan {resultado.curvas // 2} curvas para el borde superior y {resultado.curvas // 2} para el borde inferior.\n\n"
            "El borde real del lago no es recto ni perfectamente ovalado. Por eso se divide en tramos y en cada tramo "
            "se ajusta una curva cubica.\n\n"
            "Una funcion cubica se ensena como una expresion formada por cuatro partes: una constante, una parte con equis, "
            "otra con equis al cuadrado y otra con equis al cubo. Con cuatro puntos de control se determina una curva "
            "suave que pasa por el tramo elegido.\n\n"
            "Mientras mas curvas se usan, menor es la distancia que cubre cada tramo. Asi el modelo sigue mejor las "
            "irregularidades del contorno de OpenStreetMap."
        )
        self.vista.crear_widgets.mostrar_detalle("Curvas polinomiales cubicas", cuerpo)

    def Presionar_profundizar_riemman(self) -> None:
        resultado = self.vista.ultimo_resultado or CalculosDIRECTOS.calcular_modelo(int(self.vista.n_var.get()), int(self.vista.curvas_var.get()))
        tabla = "n     area km2     error\n"
        for n_tabla in (15, 30, 60, 100):
            calculo = CalculosDIRECTOS.calcular_modelo(n_tabla, resultado.curvas)
            tabla += f"{n_tabla:<5} {calculo.area_riemann_km2:>8.3f}   {calculo.error_riemann_pct:>+6.2f}%\n"
        cuerpo = (
            f"Entrada usada: n = {resultado.n} subintervalos.\n"
            f"Contorno usado: {resultado.curvas} curvas cubicas por tramos.\n\n"
            "La suma de Riemann aproxima el area usando rectangulos delgados.\n\n"
            "Primero se divide el ancho total del lago en n partes iguales. En el centro de cada parte se mide la distancia "
            "vertical entre el borde superior y el borde inferior. Esa distancia es la altura del rectangulo.\n\n"
            "En clase se diria asi: el area aproximada es la suma de varios rectangulos. Cada rectangulo se obtiene "
            "multiplicando el ancho de la division por la altura entre ambos bordes.\n\n"
            f"Resultado actual:\n"
            f"Area aproximada por Riemann: {resultado.area_riemann_km2:.3f} kilometros cuadrados.\n"
            f"Area oficial usada para comparar: 175.9 kilometros cuadrados.\n"
            f"Error porcentual: {resultado.error_riemann_pct:+.2f} por ciento.\n\n"
            "Comparacion pedida por la rubrica:\n"
            f"{tabla}\n"
            "Mientras mayor sea n, los rectangulos son mas delgados y la aproximacion sigue mejor la forma del lago."
        )
        self.vista.crear_widgets.mostrar_detalle("Area por sumas de Riemann", cuerpo)

    def Presionar_profundizar_integral(self) -> None:
        resultado = self.vista.ultimo_resultado or CalculosDIRECTOS.calcular_modelo(int(self.vista.n_var.get()), int(self.vista.curvas_var.get()))
        cuerpo = (
            f"Contorno usado: {resultado.curvas} curvas cubicas por tramos.\n\n"
            "La integral calcula el area entre dos curvas: el borde superior y el borde inferior del lago.\n\n"
            "La idea de clase es esta: para cada posicion horizontal se observa cuanta distancia hay entre ambos bordes. "
            "La integral suma todas esas distancias de manera continua a lo largo del lago.\n\n"
            "Por eso la integral es la version continua de la suma de Riemann. Riemann suma rectangulos; la integral "
            "suma el ancho real entre las curvas sin partirlo en rectangulos visibles.\n\n"
            f"Area por integral: {resultado.area_integral_km2:.3f} kilometros cuadrados.\n"
            f"Area oficial: 175.9 kilometros cuadrados.\n"
            f"Error porcentual: {resultado.error_integral_pct:+.2f} por ciento."
        )
        self.vista.crear_widgets.mostrar_detalle("Area por integral", cuerpo)

    def Presionar_profundizar_datos(self) -> None:
        resultado = self.vista.ultimo_resultado or CalculosDIRECTOS.calcular_modelo(int(self.vista.n_var.get()), int(self.vista.curvas_var.get()))
        cuerpo = (
            f"Fuente oficial para comparar area: {CalculosIndirectos.FUENTE_OFICIAL}\n\n"
            f"Fuente del contorno: {CalculosIndirectos.FUENTE_CONTORNO}\n\n"
            f"Fuente de imagen satelital: {CalculosIndirectos.FUENTE_IMAGEN}\n\n"
            f"Volumen idealizado: {resultado.volumen_km3:.3f} kilometros cubicos, equivalente a "
            f"{resultado.volumen_millones_m3:.1f} millones de metros cubicos.\n\n"
            "El volumen se aproxima usando un modelo idealizado, no una medicion batimetrica real. Sirve para aplicar "
            "la idea de un solido matematico, no para afirmar el volumen exacto del lago.\n\n"
            f"Centroide cartesiano: equis = {resultado.centroide_x_km:.3f} kilometros, "
            f"y = {resultado.centroide_y_km:.3f} kilometros.\n\n"
            f"Coordenadas aproximadas del centroide: latitud {resultado.centroide_geo.lat:.6f}, "
            f"longitud {resultado.centroide_geo.lon:.6f}.\n\n"
            "Ese punto se interpreta como centro geometrico del modelo y se usa como referencia para el punto de "
            "abastecimiento.\n\n"
            "Discusion critica:\n"
            f"{TEXTO_LIMITACIONES}\n\n"
            "Limitaciones practicas: un punto central geometrico no garantiza profundidad adecuada, seguridad de navegacion, "
            "proteccion frente al viento, permisos ambientales, cercania a rutas nauticas ni facilidad de acceso desde la costa."
        )
        self.vista.crear_widgets.mostrar_detalle("Datos del modelo", cuerpo)
