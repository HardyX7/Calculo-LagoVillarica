import math
from typing import Tuple

class Elipse:
    """
    Clase que representa una elipse en forma matemática:

        (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1

    Esta clase permite obtener:
    - Función superior y(x)
    - Función inferior y(x)
    - Intervalo válido en el eje x

    Se utiliza para modelar la elipse como dos funciones,
    compatibles con el sistema de integración y centroide.
    """

    def __init__(self, h: float, k: float, a: float, b: float):
        """
        Parámetros:
        - h: centro en eje x
        - k: centro en eje y
        - a: semieje horizontal
        - b: semieje vertical
        """
        self.h = h
        self.k = k
        self.a = a
        self.b = b

    def y_superior(self, x: float) -> float:
        """
        Retorna la función superior de la elipse en un punto x.

        Corresponde a la rama positiva de la ecuación:
        y = k + b * sqrt(1 - ((x - h)^2 / a^2))
        """
        return self.k + self.b * math.sqrt(
            1 - ((x - self.h) ** 2) / (self.a ** 2)
        )

    def y_inferior(self, x: float) -> float:
        """
        Retorna la función inferior de la elipse en un punto x.

        Corresponde a la rama negativa de la ecuación:
        y = k - b * sqrt(1 - ((x - h)^2 / a^2))
        """
        return self.k - self.b * math.sqrt(
            1 - ((x - self.h) ** 2) / (self.a ** 2)
        )

    def intervalo(self) -> Tuple[float, float]:
        """
        Retorna el intervalo válido de la elipse en el eje x.

        La elipse solo existe cuando:
        h - a ≤ x ≤ h + a
        """
        return (self.h - self.a, self.h + self.a)