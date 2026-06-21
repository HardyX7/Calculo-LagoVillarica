import math
from typing import Tuple

class Elipse:
    """
    Representa una elipse:

        (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1

    Se modela como una función f(x) = altura de la elipse.
    """

    def __init__(self, h: float, k: float, a: float, b: float):
        self.h = h
        self.k = k
        self.a = a
        self.b = b

    def y_superior(self, x: float) -> float:
        return self.k + self.b * math.sqrt(
            1 - ((x - self.h) ** 2) / (self.a ** 2)
        )

    def y_inferior(self, x: float) -> float:
        return self.k - self.b * math.sqrt(
            1 - ((x - self.h) ** 2) / (self.a ** 2)
        )

    def __call__(self, x: float) -> float:
        """
        Permite usar la elipse como función:
            f(x) = y_superior(x) - y_inferior(x)
        """
        return self.y_superior(x) - self.y_inferior(x)