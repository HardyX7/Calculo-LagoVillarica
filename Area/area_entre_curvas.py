from Area.Integral import Integral
from functions.funcion_por_tramos import FuncionPorTramos
from constantes import ESCALA_KM2

class AreaEntreCurvas:
    def __init__(
            self, 
            f: FuncionPorTramos, 
            g: FuncionPorTramos, 
        ) -> None:
        
        self.f = f
        self.g = g
        
    def area_escalada(self, intervalo: tuple[float, float]) -> float:
        area = self(intervalo)
        return area * ESCALA_KM2
    
    def __call__(self, intervalo: tuple[float, float]) -> float:
        a, b = intervalo
        return Integral(self.f)(a, b) - Integral(self.g)(a, b)