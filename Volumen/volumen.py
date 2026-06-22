class Volumen:
    """Calcula el volumen de una superficie con altura constante.

    El calculador de area debe implementar ``area_escalada(intervalo)`` y
    devolver km2. La altura se recibe en km y el volumen se devuelve en km3.
    Es un caso particular de secciones transversales, que al tener una profundidad constrante solo es necesario
    integrar para obtener area y multiplicarlo por la altura.
    """

    def __init__(self, calculador_area):
        self.calculador_area = calculador_area

    def volumen(self, intervalo: tuple[float, float], altura_km: float) -> float:
        area_km2 = self.calculador_area.area_escalada(intervalo)
        return area_km2 * altura_km

    def __call__(self, intervalo: tuple[float, float], altura_km: float) -> float:
        return self.volumen(intervalo, altura_km)
