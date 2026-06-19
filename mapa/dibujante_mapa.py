"""Contiene el estilo y las operaciones de dibujo realizadas con Matplotlib."""

from constantes import COLOR_MAPA_AREA, COLOR_MAPA_FONDO, COLOR_MAPA_LEYENDA, COLOR_MAPA_NORTE, COLOR_MAPA_SUR


class DibujanteMapa:
    """Dibuja el mapa, las curvas y los rectangulos sobre los ejes."""

    def __init__(self, ejes):
        self.ejes = ejes

    def dibujar_base(self, imagen, intervalo):
        # La imagen y los ejes se configuran una sola vez al iniciar el mapa, esto crea 
        # el fondo sobre el que se dibujaran las curvas y los rectangulos de Riemann.
        a, b = intervalo
        self.ejes.set_position((0.035, 0.045, 0.95, 0.94))
        self.ejes.set_facecolor(COLOR_MAPA_FONDO)
        self.ejes.imshow(imagen, extent=(a, b, 0, 15), origin="upper", aspect="equal", alpha=0.82)
        self.ejes.set(xlim=(a, b), ylim=(0, 15))
        self.ejes.set_aspect("equal", adjustable="box")
        self.ejes.tick_params(colors=COLOR_MAPA_SUR, labelsize=9)
        self.ejes.grid(color=COLOR_MAPA_SUR, linestyle=":", alpha=0.18)
        for borde in self.ejes.spines.values():
            borde.set_color(COLOR_MAPA_AREA)

    def dibujar_curvas(self, datos):
        # Las curvas se agregan una sola vez durante el primer calculo.
        if self.ejes.lines:
            return
        self.ejes.fill_between(datos.x, datos.sur, datos.norte, color=COLOR_MAPA_AREA, alpha=0.18, label="Area integral")
        self.ejes.plot(datos.x, datos.norte, color=COLOR_MAPA_NORTE, linewidth=2, label="f(x) norte")
        self.ejes.plot(datos.x, datos.sur, color=COLOR_MAPA_SUR, linewidth=2, label="g(x) sur")
        self.ejes.legend(facecolor=COLOR_MAPA_LEYENDA, labelcolor=COLOR_MAPA_SUR, loc="upper right")

    def dibujar_riemann(self, rectangulos):
        # Al cambiar n se elimina el grupo anterior y se dibuja el nuevo.
        for barras in list(self.ejes.containers):
            barras.remove()
        izquierdas, bases, alturas, dx = rectangulos
        self.ejes.bar(izquierdas, alturas, width=dx, bottom=bases, align="edge", color=COLOR_MAPA_NORTE, edgecolor=COLOR_MAPA_NORTE, alpha=0.20, linewidth=0.6)
