
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

from Area.area_entre_curvas import h

class Integral:
    
    """
    Clase que representa la integral definida de una función.
    
    La función debe ser invocable y poseer un atributo
    `dominio` de la forma (a, b).
    """
    
    def __init__(
            self,
            funcion: Callable[[float], float]
        ) -> None:
        
        self.funcion = funcion
        self.intervalo = funcion.dominio
    
    def __call__(self) -> float:
        
        """
        Evalúa numéricamente la integral definida
        utilizando scipy.integrate.quad.
        """
        
        a, b = self.intervalo
        resultado, _ = quad(self.funcion, a, b)
        return resultado

    def __str__(self) -> str:
        a, b = self.intervalo
        nombre = getattr(self.funcion, "nombre", self.funcion.__class__.__name__)

        datos = [
            f"Funcion: {nombre}",
            f"Intervalo: [{a}, {b}]",
        ]

        datos_unidos = "\n".join(datos)
        return f"Integral:\n{datos_unidos}"

integral_area = Integral(funcion=h)
    
