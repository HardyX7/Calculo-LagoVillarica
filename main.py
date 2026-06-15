"""Punto de entrada principal de la aplicacion."""

import sys
from vista import VistaPrincipal
from functions.funciones import *

print(f(0))
print(g(0))
print(f(0) == g(0))

print(f(30))
print(g(30))
print(f(30) == g(30))

sys.dont_write_bytecode = True

def main() -> None:
    app = VistaPrincipal()
    app.ejecutar()


if __name__ == "__main__":
    main()
