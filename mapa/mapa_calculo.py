"""Fachada que conecta el panel de Tkinter con los datos y el dibujo del mapa."""
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.image import imread
from Area.metodos_riemann import PuntoMedio, ExtremoIzquierdo, ExtremoDerecho
from constantes import COLOR_MAPA_FONDO, INTERVALO
from functions.funciones import f, g
from mapa.datos_mapa import DatosMapa
from mapa.dibujante_mapa import DibujanteMapa
# La ruta se calcula desde este archivo para no depender de la carpeta de ejecucion.
RUTA_IMAGEN = Path(__file__).parent.parent / "images" / "villarica_lake.png"

class MapaCalculo:
    """Fachada que conecta la vista con los datos y el dibujo del mapa."""
    def __init__(self, panel, ):
        # Crea y conecta las dependencias internas que la vista no necesita conocer.
        self.datos = DatosMapa(f, g, INTERVALO)
        
        figura = Figure(figsize=(7, 6), dpi=100, facecolor=COLOR_MAPA_FONDO)
        self.canvas = FigureCanvasTkAgg(figura, master=panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.dibujante = DibujanteMapa(figura.add_subplot(111))
        self.mostrar_mapa_base()

    def mostrar_mapa_base(self):
        # Antes de calcular solo se muestra la imagen con sus coordenadas.
        self.dibujante.dibujar_base(imread(RUTA_IMAGEN), self.datos.intervalo)

    def mostrar_calculo_en_mapa(self, n, metodo):
        # Las curvas permanecen y solo se reemplaza la aproximacion de Riemann.
        self.metodo = PuntoMedio()
        if metodo == "Punto medio":
            self.metodo = PuntoMedio()
        elif metodo == "Extremo izquierdo":
            self.metodo = ExtremoIzquierdo()
        elif metodo == "Extremo derecho":
            self.metodo = ExtremoDerecho()
        self.dibujante.dibujar_curvas(self.datos)
        self.dibujante.dibujar_riemann(self.datos.rectangulos_riemann(n, self.metodo))
        self.canvas.draw_idle()
