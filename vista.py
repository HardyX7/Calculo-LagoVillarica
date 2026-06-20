import tkinter as tk
from estilizacion.moldes_widgets import  CrearWidget
from mapa.mapa_calculo import MapaCalculo
from resultados_lago import CalcularResultados
from functions.funciones import f, g
from constantes import (
    AREA_REFERENCIA_KM2, ESCALA, ESCALA_KM2,
    COLOR_ACENTO, COLOR_BOTON, COLOR_BOTON_ACTIVO,
    COLOR_FONDO, COLOR_PANEL, COLOR_TEXTO, COLOR_TEXTO_SUAVE, INTERVALO
)

class VistaPrincipal:
    
    """
    Vista principal: controles y resultados.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modelo Lago Villarrica - Riemann e integral")
        self.root.geometry("1180x720")
        self.root.minsize(980, 640)
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda _event: self.root.attributes("-fullscreen", False))
        self.root.configure(bg=COLOR_FONDO)
        
        self.crear = CrearWidget()
        self.fuentes = self.crear.fuentes(self.root)
        self.fondo = self.crear.fondo(self.root)
        self.fondo.pack(fill="both", expand=True)
        
        self.n_var = tk.StringVar(value="15")
        self.estado_var = tk.StringVar(value="Elige n y presiona Calcular.")
        self.valores = {}
        self.ultimo_resultado = None
        self.botones_n = {}
        self.tocar_boton_calcular = TOCAR_BOTON_CALCULAR(self)

        self.crear_panel_resultados()
        self.crear_espacio_imagen()

    def ejecutar(self):
        self.root.mainloop()

    def crear_panel_resultados(self):
        panel = self.crear.frame(self.fondo, fondo=COLOR_PANEL, borde=True)
        panel.place(relx=0.03, rely=0.06, relwidth=0.21, relheight=0.88)

        self.crear.etiqueta(panel, "Lago Villarrica\nmodelo de calculo", fuentes=self.fuentes, estilo="titulo", fondo=COLOR_PANEL, color=COLOR_TEXTO, justify="left", anchor="w").pack(fill="x", padx=16, pady=(14, 2))
        self.crear.etiqueta(panel, "Área por Riemann e integral", fuentes=self.fuentes, estilo="subtitulo", fondo=COLOR_PANEL, color=COLOR_TEXTO_SUAVE, justify="left", wraplength=330, anchor="w").pack(fill="x", padx=16, pady=(0, 10))

        self.crear_controles(panel)
        self.crear_tarjetas(panel)
        self.crear.etiqueta(panel, fuentes=self.fuentes, estilo="estado", fondo=COLOR_PANEL, color=COLOR_ACENTO, textvariable=self.estado_var, wraplength=280, justify="center", anchor="center").pack(fill="both", expand=True, padx=12, pady=(2, 10))

    def crear_espacio_imagen(self):
        panel = self.crear.frame(self.fondo, fondo=COLOR_PANEL, borde=True)
        panel.place(relx=0.285, rely=0.06, relwidth=0.68, relheight=0.88)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1, uniform="margen_mapa")
        panel.grid_rowconfigure(2, weight=1, uniform="margen_mapa")

        encabezado = self.crear.frame(panel, fondo=COLOR_PANEL)
        encabezado.grid(row=0, column=0, sticky="nsew")
        self.crear.etiqueta(encabezado, "MODELO DEL LAGO VILLARRICA", fuentes=self.fuentes, estilo="titulo_mapa", fondo=COLOR_PANEL, color=COLOR_TEXTO, anchor="center").pack(fill="both", expand=True)

        contenedor_mapa = self.crear.frame(panel, fondo=COLOR_PANEL, height=500)
        contenedor_mapa.grid(row=1, column=0, sticky="ew")
        contenedor_mapa.pack_propagate(False)
        self.panel_mapa = contenedor_mapa

        pie = self.crear.frame(panel, fondo=COLOR_PANEL)
        pie.grid(row=2, column=0, sticky="nsew")
        self.crear.etiqueta(pie, f"PROPORCIÓN • 1u = {ESCALA:.3f}km • 1u² = {ESCALA_KM2:.6f}km²", fuentes=self.fuentes, estilo="proporcion", fondo=COLOR_PANEL, color=COLOR_ACENTO, anchor="center").pack(fill="both", expand=True)
        panel.bind("<Configure>", lambda e: contenedor_mapa.configure(height=max(260, min(e.height - 120, int(e.width / 2)))))
        self.mapa_calculo = MapaCalculo(self.panel_mapa)

    def crear_controles(self, panel):
        controles = self.crear.frame(panel, fondo=COLOR_PANEL)
        controles.pack(fill="x", padx=16, pady=(0, 8))
        self.crear.etiqueta(controles, "n para suma de Riemann", fuentes=self.fuentes, estilo="etiqueta", fondo=COLOR_PANEL, color=COLOR_TEXTO, anchor="w").pack(fill="x")

        fila_n = self.crear.frame(controles, fondo=COLOR_PANEL)
        fila_n.pack(fill="x", pady=(6, 8))
        for n in (15, 30, 60, 100):
            boton = self.crear.boton(fila_n, str(n), lambda valor=n: self.seleccionar_n(valor), fuentes=self.fuentes)
            boton.pack(side="left", expand=True, fill="x", padx=(0, 6))
            self.botones_n[str(n)] = boton

        self.crear.boton(controles, "Calcular", self.tocar_boton_calcular.ejecutar, fuentes=self.fuentes).pack(fill="x", pady=(2, 0))
        self.marcar_n_seleccionado()

    def crear_tarjetas(self, panel):
        tarjetas = [
            ("Curvas cubicas", "Pendiente\npresiona Calcular"),
            ("Area", "Riemann: pendiente\nIntegral: pendiente"),
            ("Centroide", "Ubicación: pendiente"),
            ("Volumen", "Volumen: pendiente"),
            ("Datos", f"Referencia: {AREA_REFERENCIA_KM2:.1f} km2\npendiente"),
        ]
        for titulo, valor in tarjetas:
            tarjeta, etiqueta_valor = self.crear.tarjeta(panel, titulo=titulo, valor_inicial=valor, fuentes=self.fuentes)
            tarjeta.pack(fill="x", padx=16, pady=(0, 6))
            self.valores[titulo] = etiqueta_valor
            if titulo == "Datos":
                etiqueta_valor.configure(height=3)

    def seleccionar_n(self, valor):
        self.n_var.set(str(valor))
        self.marcar_n_seleccionado()

    def marcar_n_seleccionado(self):
        for valor, boton in self.botones_n.items():
            activo = valor == self.n_var.get()
            boton.configure(bg=COLOR_ACENTO if activo else COLOR_BOTON, fg="#03101a" if activo else COLOR_TEXTO, activebackground=COLOR_ACENTO if activo else COLOR_BOTON_ACTIVO)


class TOCAR_BOTON_CALCULAR:
    def __init__(self, vista):
        self.vista = vista

    def ejecutar(self):
        resultado = CalcularResultados(f, g, INTERVALO, int(self.vista.n_var.get())).calcular()
        self.vista.ultimo_resultado = resultado
        self.vista.valores["Curvas cubicas"].configure(text=f"{resultado.curvas} curvas\n{resultado.curvas_por_lado} superiores + {resultado.curvas_por_lado} inferiores")
        self.vista.valores["Area"].configure(text=f"Riemann: {resultado.area_riemann_km2:.3f} km2\nIntegral: {resultado.area_integral_km2:.3f} km2")
        self.vista.valores["Centroide"].configure(text=f"Ubicación: X = {resultado.centroide_x:.2f} KM\nY = {resultado.centroide_y:.2f} KM")
        self.vista.valores["Volumen"].configure()
        self.vista.valores["Datos"].configure(text=f"Referencia: {AREA_REFERENCIA_KM2:.1f} km2\nerror integral {resultado.error_integral_pct:+.2f}%\nerror Riemann {resultado.error_riemann_pct:+.2f}%")
        self.vista.estado_var.set(f"Calculo listo con n={resultado.n}.")
        self.vista.mapa_calculo.mostrar_calculo_en_mapa(resultado.n)
