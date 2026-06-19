"""Define la conversion entre unidades del modelo y kilometros reales."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Escala:
    """Aplica o revierte un factor de escala sin modificarlo accidentalmente."""

    factor: float

    def aplicar(self, valor: float) -> float:
        return valor * self.factor

    def quitar(self, valor: float) -> float:
        return valor / self.factor


# Escala especifica utilizada por el modelo del Lago Villarrica.
escala_lago = Escala(factor=0.766)
