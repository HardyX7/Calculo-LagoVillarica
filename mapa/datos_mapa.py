"""Prepara y almacena los valores numericos usados para dibujar el mapa."""

import numpy as np


class DatosMapa:
    """Calcula y conserva los datos necesarios para representar el lago visualmente."""
    def __init__(self, funcion_norte, funcion_sur, intervalo, muestras=600):
        self.funcion_norte = funcion_norte
        self.funcion_sur = funcion_sur
        self.intervalo = intervalo
        self.x, self.norte, self.sur = self._calcular_curvas(muestras)

    def _calcular_curvas(self, muestras):
        """Evalua una sola vez los contornos norte y sur del modelo."""
        # Las curvas no cambian al seleccionar n, por eso se calculan una sola vez.
        x = np.linspace(*self.intervalo, muestras)
        norte = np.array([self.funcion_norte(float(valor)) for valor in x])
        sur = np.array([self.funcion_sur(float(valor)) for valor in x])
        return x, norte, sur

    def rectangulos_riemann(self, n, metodo):
        # Obtiene la posicion, base y altura de todos los rectangulos de Riemann al presionar el boton de calcular.
        a, b = self.intervalo
        dx = (b - a) / n
        izquierdas = a + np.arange(n) * dx
        puntos = [metodo.obtener_x(a, dx, i) for i in range(n)]
        bases = np.array([self.funcion_sur(punto) for punto in puntos])
        alturas = np.array([self.funcion_norte(punto) for punto in puntos]) - bases
        return izquierdas, bases, alturas, dx
