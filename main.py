"""Punto de entrada principal de la aplicacion."""

import sys

sys.dont_write_bytecode = True

from vista import VistaPrincipal


def main() -> None:
    
    app = VistaPrincipal()
    app.ejecutar()


if __name__ == "__main__":
    main()
