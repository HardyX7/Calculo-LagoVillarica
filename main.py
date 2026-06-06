"""Punto de entrada principal de la aplicacion."""

import sys


def main() -> None:
    #esta cosita no genera pycaches, 676767
    sys.dont_write_bytecode = True
    from vista import VistaPrincipal

    VistaPrincipal().ejecutar()


if __name__ == "__main__":
    main()
