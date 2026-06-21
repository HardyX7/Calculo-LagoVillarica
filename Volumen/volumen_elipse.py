from Area.Integral import Integral
from constantes import M2_A_KM2, KM2_A_M2

class VolumenElipse:

    """
    Calcula el volumen de una elipse extruida a una altura constante.

    Modelo utilizado:

        V = Área(elipse) × altura

    El área de la elipse se obtiene mediante integración numérica y luego
    se multiplica por la altura para estimar el volumen.
    """

    def __init__(self, elipse):
        """
        Recibe el objeto Elipse y crea el objeto encargado
        de calcular su área mediante integración.
        """
        self.elipse = elipse
        self.integral = Integral(elipse)

    def volumen(self, altura_m: float) -> float:
        """
        Calcula el volumen de la elipse extruida.

        Pasos:
        1. Calcula el área de la elipse (km²).
        2. Convierte el área a m².
        3. Multiplica por la altura para obtener el volumen en m³.
        4. Convierte el resultado a km³.
        """
        intervalo = (
            self.elipse.h - self.elipse.a,
            self.elipse.h + self.elipse.a
        )
        area_km2 = self.integral.area_escalada(intervalo)
        area_m2 = area_km2 * KM2_A_M2
        volumen_m3 = area_m2 * altura_m
        return volumen_m3 / M2_A_KM2

    def __call__(self, altura_m: float) -> float:
        """
        Permite calcular el volumen llamando al objeto como una función.
        """
        return self.volumen(altura_m)



