from Area.Integral import Integral
from functions.funcion_por_tramos import FuncionPorTramos
from constantes import ESCALA_KM2

class AreaEntreCurvasIntegral:
    
    """
    Representa el área entre dos curvas f y g. El área se calcula como la integral de f 
    menos la integral de g en un intervalo dado.
    Uso:
    
    - area = AreaEntreCurvasIntegral(f, g)(intervalo)
    - area_km2 = AreaEntreCurvasIntegral(f, g).area_escalada(intervalo)
    
    Donde:
    
    - f: la primera curva, debe ser una FuncionPorTramos
    - g: la segunda curva, debe ser una FuncionPorTramos
    - intervalo: una tupla (a, b) que indica el intervalo de integración
    """
    
    def __init__(
            self, 
            f: FuncionPorTramos, 
            g: FuncionPorTramos, 
        ) -> None:
        
        self.f = f
        self.g = g
        
    def area_escalada(self, intervalo: tuple[float, float]) -> float:
        
        """
        Calcula el área entre las curvas f y g en el intervalo dado, 
        y luego la escala a km2.
        """
        
        area = self(intervalo)
        return area * ESCALA_KM2
    
    def __call__(self, intervalo: tuple[float, float]) -> float:
        """
        Calcula el área entre las curvas f y g en el intervalo dado.
        """
        
        return abs(Integral(self.f)(intervalo) - Integral(self.g)(intervalo))