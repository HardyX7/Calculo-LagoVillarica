"""Punto de entrada principal de la aplicacion."""

import sys
from vista import VistaPrincipal


def main() -> None:
    
    sys.dont_write_bytecode = True
    app = VistaPrincipal()
    app.ejecutar()


if __name__ == "__main__":
    main()
