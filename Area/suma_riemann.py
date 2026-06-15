"""Area/suma_riemann.py

Contiene la clase SumaRiemann que aproxima una integral definida mediante
una suma de Riemann.

Uso:
    from Area.suma_riemann import SumaRiemann, h
    from Area.metodos_riemann import PuntoMedio
    from functions.funciones import f

    riemann = SumaRiemann(funcion=h, intervalo=f.dominio, n=10000, metodo=PuntoMedio())
    area = riemann()

También define la función h(x) = f(x) - g(x), que representa el área entre
las curvas f y g.
"""

from typing import Callable, Tuple
from .metodos_riemann import MetodoRiemann, PuntoMedio

from functions.funciones import f, g

class SumaRiemann:
    
    """
    Clase que aproxima la integral definida de una función
    mediante una suma de Riemann.
    """
    
    def __init__(
            self,
            funcion: Callable[[float], float],
            intervalo: Tuple[float, float],
            n: int,
            metodo: MetodoRiemann
        ) -> None:
        
        self.funcion = funcion
        self.intervalo = intervalo
        self.n = n
        self.metodo = metodo
    
    def __call__(self) -> float:
        
        """
        Calcula la suma de Riemann usando la estrategia indicada.
        """
        
        a, b = self.intervalo
        dx = (b - a) / self.n
        
        suma = 0
        for i in range(self.n):
            x = self.metodo.obtener_x(a, dx, i)
            suma += self.funcion(x)
        
        return suma * dx


def h(x: float) -> float:
    return f(x) - g(x)

