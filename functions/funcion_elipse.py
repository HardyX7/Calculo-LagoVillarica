import math
class Elipse:
    
    """
    Clase que representa una elipse en el plano cartesiano.

    Su ecuación es:

        (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1

    La elipse se modela como una función que entrega la distancia
    entre la curva superior e inferior para un valor de x, lo que
    permite utilizarla directamente en los cálculos de integración.
    """

    def __init__(self, h: float, k: float, a: float, b: float):
        
        """
        Inicializa la elipse.

        Parámetros:
        - h: coordenada x del centro.
        - k: coordenada y del centro.
        - a: semieje horizontal.
        - b: semieje vertical.
        """
        
        self.h = h
        self.k = k
        self.a = a
        self.b = b

    @property
    def intervalo(self) -> tuple[float, float]:
        """Devuelve el intervalo horizontal en el que existe la elipse."""

        return (self.h - self.a, self.h + self.a)

    def y_superior(self, x: float) -> float:
        
        """
        Evalúa la rama superior de la elipse para un valor de x.
        """
        
        return self.k + self.b * math.sqrt(
            1 - ((x - self.h) ** 2) / (self.a ** 2)
        )

    def y_inferior(self, x: float) -> float:
        
        """
        Evalúa la rama inferior de la elipse para un valor de x.
        """
        
        return self.k - self.b * math.sqrt(
            1 - ((x - self.h) ** 2) / (self.a ** 2)
        )

    def __call__(self, x: float) -> float:
        
        """
        Evalúa la altura vertical de la elipse para un valor de x.

        Esta altura corresponde a la diferencia entre la función
        superior y la función inferior, permitiendo utilizar la
        elipse directamente como una función integrable.
        """
        
        return self.y_superior(x) - self.y_inferior(x)
