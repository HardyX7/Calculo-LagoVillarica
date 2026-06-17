from functions.funciones import f, g
from Area.area_entre_curvas_integral import AreaEntreCurvasIntegral
from Area.area_entre_curvas_riemann import AreaEntreCurvasRiemann
from Area.metodos_riemann import PuntoMedio
from constantes import AREA_REFERENCIA_KM2, INTERVALO, ESCALA_KM2, ESCALA

print("Resultados del modelo del Lago Villarrica:")
print(f"Area por Riemann (n=15): {AreaEntreCurvasRiemann(f, g, 15, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Riemann (n=30): {AreaEntreCurvasRiemann(f, g, 30, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Riemann (n=60): {AreaEntreCurvasRiemann(f, g, 60, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Riemann (n=100): {AreaEntreCurvasRiemann(f, g, 100, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Integral: {AreaEntreCurvasIntegral(f, g).area_escalada(INTERVALO):.3f} km2")

print(ESCALA, ESCALA_KM2)