from typing import Tuple
from functions.funcion_por_tramos import FuncionPorTramos
from .calcular_coordenada_x import CalcularCoordenadaXCentroide
from .calcular_coordenada_y import CalcularCoordenadaYCentroide

class CalcularCentroide:
    """
    Clase que calcula el centroide (coordenadas x, y) de la región entre dos curvas f y g.
    El centroide se calcula como:
        x_bar = (1/A) * ∫_a^b x * (f(x) - g(x)) dx
        y_bar = (1/(2*A)) * ∫_a^b [f(x)^2 - g(x)^2] dx
    donde A es el área entre las curvas f y g en el intervalo [a, b].

    Uso:
        - calculadora = CalcularCentroide(f, g, intervalo)
        - centroide = calculadora.calcular()  # Devuelve (x_bar, y_bar)

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
        # Calculadoras reutilizables para x y y
        self.calculadora_x = CalcularCoordenadaXCentroide(f, g, intervalo)
        self.calculadora_y = CalcularCoordenadaYCentroide(f, g, intervalo)

    def calcular(self) -> Tuple[float, float]:
        """Calcula y devuelve el centroide como una tupla (x_centroide, y_centroide)."""
        x = self.calculadora_x.calcular()
        y = self.calculadora_y.calcular()
        return (x, y)

    def area(self) -> float:
        """Devuelve el área entre las curvas f y g en el intervalo dado."""
        return self.calculadora_x.area()  # o self.calculadora_y.area(), son iguales