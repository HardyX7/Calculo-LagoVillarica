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
f.agregar_tramo(2.44, PolinomioGradoTres(0.20149, -1.078911, 2.334591, 3.42))
f.agregar_tramo(6.47, PolinomioGradoTres(0.116694, -2.156136, 13.096991, -15.195071))
f.agregar_tramo(10.5, PolinomioGradoTres(0.031336, -0.794419, 6.325312, -5.266804))
f.agregar_tramo(14.77, PolinomioGradoTres(-0.051494, 1.725714, -18.651005, 75.026711))
f.agregar_tramo(22.5, PolinomioGradoTres(-0.00186, 0.096355, -1.919372, 23.421961))

g = FuncionPorTramos("g")
g.agregar_tramo(2.44, PolinomioGradoTres(-0.217752, 1.543509, -2.998444, 3.42))
g.agregar_tramo(6.47, PolinomioGradoTres(-0.088105, 1.208477, -5.285527, 9.11178))
g.agregar_tramo(10.5, PolinomioGradoTres(0.088073, -2.045153, 15.29131, -35.536636))
g.agregar_tramo(14.77, PolinomioGradoTres(-0.086657, 3.353787, -43.204039, 185.703326))
g.agregar_tramo(22.5, PolinomioGradoTres(0.039951, -2.044563, 34.996752, -199.6006764))

elipse = Elipse(15, 7.5, 15, 7.5)

