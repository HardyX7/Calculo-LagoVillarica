class VolumenEntreCurvas:
    """
    V = área entre curvas * altura
    """

    def __init__(self, area_entre_curvas):
        self.area_entre_curvas = area_entre_curvas

    def volumen(self, intervalo, altura_km: float) -> float:
        area_km2 = self.area_entre_curvas.area_escalada(intervalo)
        return area_km2 * altura_km

    def __call__(self, intervalo, altura_km: float) -> float:
        return self.volumen(intervalo, altura_km)
