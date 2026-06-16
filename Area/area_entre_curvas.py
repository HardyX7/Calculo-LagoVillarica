from functions.escala import escala_lago
from functions.funciones import f, g


def h(x: float) -> float:
    x_modelo = escala_lago.quitar(x)
    return escala_lago.aplicar(f(x_modelo) - g(x_modelo))


h.nombre = "f - g escalada"
h.dominio = (
    escala_lago.aplicar(f.dominio[0]),
    escala_lago.aplicar(f.dominio[1]),
)
