"""Suma de Riemann para aproximar una integral definida."""
from typing import Tuple
from constantes import ESCALA_KM2
from Area.metodos_riemann import MetodoRiemann
from functions.funcion_por_tramos import FuncionPorTramos

class SumaRiemann:
    
    """
    Clase que aproxima la integral definida de una funcion
    usando el metodo de Riemann indicado.
    Uso:
    
    - area = SumaRiemann(f, n, metodo)(intervalo)
    - area_km2 = SumaRiemann(f, n, metodo).area_escalada(intervalo)
    
    Donde:
    
    - f: la funcion a integrar, debe ser una FuncionPorTramos
    - n: el numero de subintervalos a usar
    - metodo: una instancia de MetodoRiemann que indica la estrategia de seleccion de puntos
    - intervalo: una tupla (a, b) que indica el intervalo de integracion
    """
    
    def __init__(
            self,
            f: FuncionPorTramos,
            n: int,
            metodo: MetodoRiemann
        ) -> None:
        
        self.f = f
        self.n = n
        self.metodo = metodo
    
    def area_escalada(self, intervalo: Tuple[float, float]) -> float:
        
        """
        Calcula la suma de Riemann en el dominio de la funcion, y luego la escala a km2.
        """
        
        area = self(intervalo)
        return area * ESCALA_KM2
    
    def __call__(self, intervalo: Tuple[float, float]) -> float:
        """
        Calcula la suma de Riemann en el dominio de la funcion.
        """
        a, b = intervalo
        dx = (b - a) / self.n
        suma = 0
        
        for i in range(self.n):
            x_i = self.metodo.obtener_x(a, dx, i)
            f_evaluada_en_x_i = self.f(x_i)
            suma += f_evaluada_en_x_i * dx
        
        return suma
