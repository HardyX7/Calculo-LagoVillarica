from dataclasses import dataclass


@dataclass(frozen=True)
class Escala:
    factor: float

    def aplicar(self, valor: float) -> float:
        return valor * self.factor

    def quitar(self, valor: float) -> float:
        return valor / self.factor


escala_lago = Escala(factor=0.75705)
