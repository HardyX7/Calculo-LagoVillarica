from typing import List, Tuple
from functions.polinomio_grado_tres import PolinomioGradoTres

class FuncionPorTramos:
    
    """
    Clase que representa una función definida por tramos, donde cada tramo es un polinomio de grado tres.
    Permite agregar tramos con sus respectivos límites y evaluar la función en cualquier punto dentro del
    dominio especificado.
    """
    
    def __init__(
            self, 
            nombre: str, 
            dominio: Tuple[float, float] = (0, 30)
        ) -> None:
        
        self.nombre = nombre
        self.dominio = dominio
        self.tramos: List[Tuple[float, PolinomioGradoTres]] = []
    
    def agregar_tramo(self, limite: float, poly: PolinomioGradoTres) -> None:
        
        """
        Agrega un tramo a la función por tramos. El tramo se define por un límite superior
        y un polinomio de grado tres. Los tramos se almacenan en una lista y se ordenan por su límite.
        """
        
        self.tramos.append((limite, poly))
        self.tramos.sort()
    
    def __call__(self, x: float) -> float:
        
        """
        Evalúa la función por tramos en un valor x dado. Verifica en qué tramo se encuentra x 
        y evalúa el polinomio correspondiente.
        """
        
        if not (self.dominio[0] <= x <= self.dominio[1]):
            raise ValueError(f"x={x} fuera del dominio {self.dominio}")
            
        for limite, poly in self.tramos:
            if x < limite:
                return poly.evaluar(x)
        
        return self.tramos[-1][1].evaluar(x)
    
    def __str__(self) -> str:
        
        """
        Devuelve una representación en cadena de la función por tramos, mostrando cada tramo con su límite
        y polinomio.
        """
        
        tramos_str = []
        for limite, poly in self.tramos:
            tramos_str.append(f"x < {limite}: \n  {self.nombre}(x) = {poly}")
        
        tramos_unidos = "\n".join(tramos_str)
        return f"""
                {self.nombre}: [{self.dominio[0]}, {self.dominio[1]}] -> R tal que: \n {tramos_unidos}
                """.strip()