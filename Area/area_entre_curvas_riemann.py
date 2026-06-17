from typing import Tuple
from constantes import ESCALA_KM2
from functions.funcion_por_tramos import FuncionPorTramos
from Area.suma_riemann import SumaRiemann
from Area.metodos_riemann import MetodoRiemann

class AreaEntreCurvasRiemann:
    """
    Representa el área entre dos curvas f y g utilizando la suma de Riemann. 
    El área se calcula como la suma de las áreas de los rectángulos formados 
    por la diferencia entre f y g en cada subintervalo.
    Uso:
    
    - area = AreaEntreCurvasRiemann(f, g, n, metodo)(intervalo)
    - area_km2 = AreaEntreCurvasRiemann(f, g, n, metodo).area_escalada(intervalo)
    
    Donde:
    
    - f: la primera curva, debe ser una FuncionPorTramos
    - g: la segunda curva, debe ser una FuncionPorTramos
    - n: el numero de subintervalos a usar para la suma de Riemann
    - metodo: una instancia de MetodoRiemann que indica la estrategia de seleccion de puntos
    - intervalo: una tupla (a, b) que indica el intervalo de integracion
    """
    
    def __init__(
            self,
            f: FuncionPorTramos,
            g: FuncionPorTramos,
            n: int,
            metodo: MetodoRiemann
        ) -> None:
        
        self.f = f
        self.g = g
        self.n = n
        self.metodo = metodo
    
    def area_escalada(self, intervalo: Tuple[float, float]) -> float:
        """
        Calcula el área entre las curvas f y g en el intervalo dado utilizando la suma de Riemann,
        y luego la escala a km2.
        """
        area = self(intervalo)
        return area * ESCALA_KM2
    
    def __call__(self, intervalo: Tuple[float, float]) -> float:
        """
        Calcula el área entre las curvas f y g en el intervalo dado utilizando la suma de Riemann.
        El área se aproxima como la suma de las áreas de los rectángulos formados por la diferencia
        entre f y g en cada subintervalo.
        """
        
        return abs(
                SumaRiemann(self.f, self.n, self.metodo)(intervalo) 
                - SumaRiemann(self.g, self.n, self.metodo)(intervalo)
            )