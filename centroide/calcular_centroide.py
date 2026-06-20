from typing import Tuple
from functions.funcion_por_tramos import FuncionPorTramos
from centroide.calcular_coordenada_x import CalcularCoordenadaXCentroide
from centroide.calcular_coordenada_y import CalcularCoordenadaYCentroide

class CalcularCentroide:
    """
    Clase que calcula el centroide (coordenadas x, y) de la región entre dos curvas f y g
    en el intervalo dado.
    
    Uso:
    
    - from centroide.calcular_centroide import CalcularCentroide
    - centroide = CalcularCentroide(f, g, intervalo).calcular()
    
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
    
    def calcular(self) -> Tuple[float, float]:
        
        """
        Calcula y devuelve el centroide como una tupla (x, y).
        """
        
        x = CalcularCoordenadaXCentroide(self.f, self.g, self.intervalo).calcular()
        y = CalcularCoordenadaYCentroide(self.f, self.g, self.intervalo).calcular()
        return (x, y)