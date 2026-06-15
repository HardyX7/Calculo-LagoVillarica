"""Area/test_area.py

Script de prueba para los módulos de Area.

Uso:
    python Area/test_area.py

Ejecuta pruebas de:
- Integral usando la clase Integral y scipy.integrate.quad
- Suma de Riemann usando SumaRiemann y PuntoMedio
"""

import sys
from pathlib import Path
from scipy.integrate import quad

# Agregar el directorio raíz para importar el paquete functions y Area como paquete
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from functions.funciones import f, g
from Area.suma_riemann import SumaRiemann, h
from Area.metodos_riemann import PuntoMedio
from Area.Integral import Integral


def test_integral_scipy():
    integral_f = Integral(funcion=f, intervalo=f.dominio)
    integral_g = Integral(funcion=g, intervalo=g.dominio)
    area_entre_curvas = integral_f() - integral_g()
    print(f"Integral f: {integral_f()}")
    print(f"Integral g: {integral_g()}")
    print(f"Área entre curvas (SciPy directo): {area_entre_curvas}")


def test_riemann():
    riemann_area = SumaRiemann(
        funcion=h,
        intervalo=f.dominio,
        n=10000,
        metodo=PuntoMedio()
    )
    area_scipy = quad(h, *f.dominio)[0]
    print(f"Área (SciPy):   {area_scipy}")
    print(f"Área (Riemann): {riemann_area()}")


if __name__ == "__main__":
    test_integral_scipy()
    print()
    test_riemann()
