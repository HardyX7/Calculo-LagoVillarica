from typing import Tuple

class PolinomioGradoTres:
    
    """
    Clase que representa un polinomio de grado tres de la forma:
    P(x) = c3 * (x ** 3) + c2 * (x ** 2) + c1 * x + c0
    Donde c3, c2, c1 y c0 son los coeficientes del polinomio.
    """
    
    def __init__(
            self, 
            c3: float, 
            c2: float, 
            c1: float, 
            c0: float
        ) -> None:
        
        self.coeficientes: Tuple[float, float, float, float] = (c3, c2, c1, c0)
    
    def evaluar(self, x: float) -> float:
        
        """
        Evalúa el polinomio en un valor x dado.
        """
        
        c3, c2, c1, c0 = self.coeficientes
        return c3 * (x ** 3) + c2 * (x ** 2) + c1 * x + c0

    def __str__(self) -> str:
        
        """
        Devuelve una representación en cadena del polinomio, mostrando los coeficientes y el formato del polinomio.
        """
        
        c3, c2, c1, c0 = self.coeficientes
        return f"{c3} * x^3 + {c2} * x^2 + {c1} * x + {c0}"