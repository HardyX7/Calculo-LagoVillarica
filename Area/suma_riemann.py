"""Suma de Riemann para aproximar una integral definida."""

from typing import Callable

from .metodos_riemann import MetodoRiemann


class SumaRiemann:
    """
    Clase que aproxima la integral definida de una funcion
    usando el metodo de Riemann indicado.
    """

    def __init__(
            self,
            funcion: Callable[[float], float],
            n: int,
            metodo: MetodoRiemann
        ) -> None:

        self.funcion = funcion
        self.n = n
        self.metodo = metodo
        self.intervalo = funcion.dominio

    def __call__(self) -> float:
        """
        Calcula la suma de Riemann en el dominio de la funcion.
        """
        a, b = self.intervalo
        dx = (b - a) / self.n

        return sum(
            self.funcion(self.metodo.obtener_x(a, dx, i))
            for i in range(self.n)
        ) * dx

    def __str__(self) -> str:
        a, b = self.intervalo
        nombre = getattr(self.funcion, "nombre", self.funcion.__class__.__name__)
        metodo = self.metodo.__class__.__name__

        datos = [
            f"Funcion: {nombre}",
            f"Intervalo: [{a}, {b}]",
            f"Subintervalos: {self.n}",
            f"Metodo: {metodo}",
        ]

        datos_unidos = "\n".join(datos)
        return f"Suma de Riemann:\n{datos_unidos}"
