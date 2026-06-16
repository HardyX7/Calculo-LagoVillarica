"""Area/metodos_riemann.py

Define las estrategias de selección de puntos para la suma de Riemann.

Uso:
    from Area.metodos_riemann import PuntoMedio, ExtremoIzquierdo, ExtremoDerecho

    metodo = PuntoMedio()
    x = metodo.obtener_x(a, dx, i)

Estas clases se usan dentro de SumaRiemann para calcular el valor x de cada
subintervalo.
"""

from abc import ABC, abstractmethod


class MetodoRiemann(ABC):
    
    """
    Representa una estrategia para seleccionar el punto de evaluación
    de cada subintervalo.
    """
    
    @abstractmethod
    def obtener_x(self, a: float, dx: float, i: int) -> float:
        pass


class ExtremoIzquierdo(MetodoRiemann):
    
    def obtener_x(self, a: float, dx: float, i: int) -> float:
        x = a + i * dx
        return x


class ExtremoDerecho(MetodoRiemann):
    
    def obtener_x(self, a: float, dx: float, i: int) -> float:
        x = a + (i + 1) * dx
        return x


class PuntoMedio(MetodoRiemann):
    
    def obtener_x(self, a: float, dx: float, i: int) -> float:
        x = a + (i + 0.5) * dx
        return x
