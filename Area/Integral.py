
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

from typing import Callable, Tuple
from scipy.integrate import quad

class Integral:
    
    """
    Clase que representa la integral definida de una función
    en un intervalo dado. La aproximación numérica se realiza
    utilizando el método `quad` de scipy.
    """
    
    def __init__(
            self,
            funcion: Callable[[float], float],
            intervalo: Tuple[float, float]
        ) -> None:
        
        self.funcion = funcion
        self.intervalo = intervalo
    
    def __call__(self) -> float:
        
        """
        Evalúa numéricamente la integral definida.
        """
        
        a, b = self.intervalo
        resultado, _ = quad(self.funcion, a, b)
        return resultado
    
    def __str__(self) -> str:
        
        """
        Devuelve una representación en cadena de la integral.
        """
        
        a, b = self.intervalo
        nombre = getattr(self.funcion, "nombre", self.funcion.__class__.__name__)
        
        return (
            f"Integral de {nombre} "
            f"en el intervalo [{a}, {b}]"
        )
    
