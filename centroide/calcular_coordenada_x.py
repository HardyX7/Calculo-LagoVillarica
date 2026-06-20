from typing import Tuple
from functions.funcion_por_tramos import FuncionPorTramos
from scipy.integrate import quad
from Area.area_entre_curvas_integral import AreaEntreCurvasIntegral

class CalcularCoordenadaXCentroide:
    def __init__(
            self,
            f: FuncionPorTramos,
            g: FuncionPorTramos,
            intervalo: Tuple[float, float]
        ) -> None:

        self.f = f
        self.g = g
        self.intervalo = intervalo

    def area(self) -> float:
        """Calcula el área entre las curvas f y g en el intervalo dado."""
        return AreaEntreCurvasIntegral(self.f, self.g)(self.intervalo)

    def momento_y(self) -> float:
        """Calcula el momento alrededor del eje y: integral de x*(f(x)-g(x)) dx en el intervalo."""
        def integrando(x: float) -> float:
            return x * (self.f(x) - self.g(x))
        a, b = self.intervalo
        resultado, _ = quad(integrando, a, b)
        return resultado

    def calcular(self) -> float:
        """Calcula el centroide en el intervalo dado."""
        
        a = self.area()
        if a == 0:
            raise ValueError("El área entre las curvas es cero, no se puede calcular el centroide.")
        return self.momento_y() / a