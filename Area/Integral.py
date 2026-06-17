"""Area/Integral.py

Define la clase Integral para calcular integrales definidas numéricamente.

Uso:
    from Area.Integral import Integral
    from functions.funciones import f

    integral_f = Integral(funcion=f, intervalo=f.dominio)
    resultado = integral_f()

Esta clase usa scipy.integrate.quad internamente y sirve para calcular
una integral definida de cualquier función que se pase como callable.
"""

from typing import Tuple
from functions.funcion_por_tramos import FuncionPorTramos
from constantes import ESCALA_KM2
from scipy.integrate import quad

class Integral:
    
    """
    Clase para calcular la integral definida de una función dada en un intervalo específico.
    """
    
    def __init__(
            self,
            funcion: FuncionPorTramos,
        ) -> None:
        
        self.funcion = funcion
    
    def area_escalada(self, intervalo: Tuple[float, float]) -> float:
        """
        Calcula el área bajo la curva de la función en el intervalo dado y la escala
        para convertirla a km2.
        """
        area = self(intervalo)
        return area * ESCALA_KM2
    
    def __call__(self, intervalo: Tuple[float, float]) -> float:
        
        """
        Evalúa numéricamente la integral definida
        utilizando scipy.integrate.quad.
        """
        a, b = intervalo
        resultado, _ = quad(self.funcion, a, b)
        return resultado