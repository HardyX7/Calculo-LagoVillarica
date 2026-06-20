
from typing import Tuple
from functions.funcion_por_tramos import FuncionPorTramos
from scipy.integrate import quad
from Area.area_entre_curvas_integral import AreaEntreCurvasIntegral

class CalcularCoordenadaYCentroide:
    """
    Calcula la coordenada y del centroide de la región entre dos curvas f y g.
    
    Uso:
    
    - from centroide.calcular_coordenada_y import CalcularCoordenadaYCentroide
    - posicion_y = CalcularCoordenadaYCentroide(f, g, intervalo).calcular()
    
    Donde:
        - f: la curva superior, debe ser una FuncionPorTramos
        - g: la curva inferior, debe ser una FuncionPorTramos
        - intervalo: una tupla (a, b) que indica el intervalo de integración
    """

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

    def momento_x(self) -> float:
        """Calcula el momento alrededor del eje x: integral de 0.5*(f(x)^2 - g(x)^2) dx en el intervalo."""
        def integrando(x: float) -> float:
            return 0.5 * (self.f(x) ** 2 - self.g(x) ** 2)
        a, b = self.intervalo
        resultado, _ = quad(integrando, a, b)
        return resultado

    def calcular(self) -> float:
        """Calcula y devuelve la coordenada y del centroide."""
        a = self.area()
        if a == 0:
            raise ValueError("El área entre las curvas es cero, no se puede calcular el centroide.")
        return self.momento_x() / a