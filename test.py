from functions.funciones import f, g
from Area.area_entre_curvas_integral import AreaEntreCurvasIntegral
from Area.area_entre_curvas_riemann import AreaEntreCurvasRiemann
from Area.metodos_riemann import PuntoMedio
from constantes import AREA_REFERENCIA_KM2, INTERVALO, ESCALA_KM2, ESCALA
from centroide.calcular_centroide import CalcularCentroide

print("Resultados del modelo del Lago Villarrica:")
print(f"Area por Riemann (n=15): {AreaEntreCurvasRiemann(f, g, 15, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Riemann (n=30): {AreaEntreCurvasRiemann(f, g, 30, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Riemann (n=60): {AreaEntreCurvasRiemann(f, g, 60, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Riemann (n=100): {AreaEntreCurvasRiemann(f, g, 100, PuntoMedio()).area_escalada(INTERVALO):.3f} km2")
print(f"Area por Integral: {AreaEntreCurvasIntegral(f, g).area_escalada(INTERVALO):.3f} km2")
calculadora = CalcularCentroide(f, g, INTERVALO)
centroide = calculadora.calcular()  # Devuelve (x, y)
print(f"Centroide: {centroide}")

print(ESCALA, ESCALA_KM2)
import tkinter as tk
from tkinter import font

ventana = tk.Tk()
ventana.geometry("500x300")
ventana.configure(bg="#1e1e2e") # Fondo oscuro para la ventana
ventana.title("Deslizador Personalizado")

# Definir una fuente bonita
fuente_cool = font.Font(family="Helvetica", size=10, weight="bold")

# Función para obtener el valor EN TIEMPO REAL (Método 1)
def actualizar_valor(val):
    etiqueta_dinamica.config(text=f"Volumen: {val}%")


deslizador = tk.Scale(
    ventana,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    resolution=1,          # Solo enteros
    
    # 🎨 COLORES
    bg="#1e1e2e",          # Fondo del canal del deslizador
    fg="#cdd6f4",          # Color de los números de texto
    troughcolor="#313244", # Color de la barra por donde corre el botón
    activebackground="#b4befe", # Color del botón cuando pasas el mouse por encima
    
    # 📐 DISEÑO Y BORDES
    sliderrelief=tk.FLAT,  # Hace que el botón sea plano (más moderno)
    bd=0,                  # Quita el borde de la caja contenedora
    highlightthickness=0,  # Quita el molesto borde de enfoque al hacer clic
    sliderlength=25,       # Ancho del botón deslizante
    width=15,              # Grosor de la barra
    length=350,            # Largo total en píxeles
    
    # 🔤 TEXTOS Y REGLA
    font=fuente_cool,
    tickinterval=25,       # Muestra marcas cada 25 unidades (0, 25, 50, 75, 100)
    showvalue=False,       # Oculta el número flotante clásico sobre el botón (lo haremos más limpio)
    
    # ⚡ ACCIÓN
    command=actualizar_valor
)

deslizador.set(50) # Valor inicial por defecto
deslizador.pack(pady=40)

# Etiqueta moderna para mostrar el valor
etiqueta_dinamica = tk.Label(ventana, text="Volumen: 50%", bg="#1e1e2e", fg="#b4befe", font=fuente_cool)
etiqueta_dinamica.pack(pady=10)

# --- OBTENER EL VALOR BAJO DEMANDA (Método 2) ---
def presionar_boton():
    # .get() obtiene el entero exacto en este instante
    valor_actual = deslizador.get()
    print(f"Valor guardado al presionar el botón: {valor_actual}")

boton = tk.Button(ventana, text="Guardar Configuración", command=presionar_boton, bg="#b4befe", fg="#1e1e2e", font=fuente_cool)
boton.pack(pady=10)

ventana.mainloop()