from Area.Integral import Integral
from constantes import M2_A_KM2, KM2_A_M2


class VolumenElipse:

    def __init__(self, elipse):
        self.elipse = elipse
        self.integral = Integral(elipse)

    def volumen(self, altura_m: float) -> float:
        intervalo = (self.elipse.h - self.elipse.a,
                     self.elipse.h + self.elipse.a)

        area_km2 = self.integral.area_escalada(intervalo)

        area_m2 = area_km2 * KM2_A_M2
        volumen_m3 = area_m2 * altura_m

        return volumen_m3 / M2_A_KM2

    def __call__(self, altura_m: float) -> float:
        return self.volumen(altura_m)
