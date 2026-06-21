from functions.polinomio_grado_tres import PolinomioGradoTres
from functions.funcion_por_tramos import FuncionPorTramos
from functions.funcion_elipse import Elipse

"""
Funciones f y g que modelan el contorno del lago Villarica, donde f corresponde al contorno norte y g al 
contorno sur. Cada función está definida por tramos, donde usando interpolacion polinomica de grado tres 
obtenemos los polinomios que modelan cada tramo.

Como usar:
1.- Importar las funciones f y g desde este módulo. (from function.funciones import f, g)
2.- Evaluar las funciones en cualquier punto dentro del dominio [0, 30]. Por ejemplo:
    valor_f = f(5)  # Evalúa la función f en x = 5
    valor_g = g(5)  # Evalúa la función g en x = 5

Donde:
f: [0, 30] -> R tal que: 
0 <= x < 3.53: 
    f(x) = 0.129235x^3 - 0.987254x^2 + 2.653156x + 4.64
3.53 <= x < 10.75: 
    f(x) = 0.041567x^3 - 1.209839x^2 + 11.261291x - 19.115071
10.75 <= x < 19.81: 
    f(x) = -0.023132x^3 + 1.035955x^2 - 15.013535x + 84.18492
x <= 30: 
    f(x) = -0.00214x^3 + 0.163131x^2 - 4.393378x + 53.134089

g: [0, 30] -> R tal que:
0 <= x < 3.53: 
    g(x) = -0.133677x^3 + 1.218880x^2 - 3.126997x + 4.64
3.53 <= x < 10.75: 
    g(x) = -0.016647x^3 + 0.353668x^2 - 2.468833x + 7.95023
10.75 <= x < 19.81: 
    g(x) = -0.002032x^3 + 0.096148x^2 - 1.650198x + 10.752381
x <= 30: 
    g(x) = 0.015282x^3 - 0.999939x^2 + 21.990029x - 162.01717

Nota importante: Asegúrate de que el punto de evaluación esté dentro del dominio [0, 30], ya que las funciones 
están definidas solo para ese rango. Si se intenta evaluar fuera del dominio, se lanzará un error.

"""

f = FuncionPorTramos("f")
f.agregar_tramo(3.53, PolinomioGradoTres(0.129235, -0.987254, 2.653156, 4.64))
f.agregar_tramo(10.75, PolinomioGradoTres(0.041567, -1.209839, 11.261291, -19.115071))
f.agregar_tramo(19.81, PolinomioGradoTres(-0.023132, 1.035955, -15.013535, 84.18492))
f.agregar_tramo(30, PolinomioGradoTres(-0.00214, 0.163131, -4.393378, 53.134089))

g = FuncionPorTramos("g")
g.agregar_tramo(3.53, PolinomioGradoTres(-0.133677, 1.21888, -3.126997, 4.64))
g.agregar_tramo(10.75, PolinomioGradoTres(-0.016647, 0.353668, -2.468833, 7.95023))
g.agregar_tramo(19.81, PolinomioGradoTres(-0.002032, 0.096148, -1.650198, 10.752381))
g.agregar_tramo(30, PolinomioGradoTres(0.015282, -0.999939, 21.990029, -162.01717))

elipse = Elipse(15, 7.5, 15, 7.5)

