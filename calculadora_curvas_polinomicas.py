"""Calculadora de curvas polinómicas de grado 3 (interpolación).

Permite ingresar 4 puntos (x, y), calcula el polinomio que los interpola
mediante ajuste de polinomio de grado 3 (mínimos cuadrados exacto para 4 puntos),
muestra la fórmula y grafica la curva. Incluye botón para copiar la fórmula.

La ventana se implementa como un Toplevel que puede lanzarse desde la vista
principal. El estilo sigue la estética de la aplicación mediante los moldes
de widgets definidos en `estilizacion.moldes_widgets`.
"""

import sys
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constantes import (
            COLOR_FONDO, COLOR_PANEL, COLOR_TEXTO, COLOR_TEXTO_SUAVE,
            COLOR_BOTON, COLOR_BOTON_ACTIVO, COLOR_FONDO,
        )
from estilizacion.moldes_widgets import CrearWidget


class CalculadoraCurvasPolinomicas:
    """
    Ventana emergente (Toplevel) para interpolar puntos con un polinomio de grado 3
    y graficar el resultado.
    """

    def __init__(self, master: tk.Misc):
        """
        Parameters
        ----------
        master: tk.Misc
            Ventana padre (normalmente la raíz de la aplicación).
        """
        # Importar colores desde constantes (evitar ciclos) antes de usar
        

        # Ventana independiente
        self.top = tk.Toplevel(master)
        self.top.title("Interpolador de curvas cúbicas")
        self.top.configure(bg=COLOR_FONDO)
        self.top.resizable(False, False)
        self.top.transient(master)  # mantener encima de la ventana principal
        self.top.grab_set()        # bloquear interacción con la ventana principal mientras está abierta

        # Fuente y fábrica de widgets consistente con la vista principal
        self.crear = CrearWidget()
        self.fuentes = self.crear.fuentes(self.top)

        self.formula_actual = ""
        
        label_style = {'bg': COLOR_PANEL, 'fg': COLOR_TEXTO, 'font': self.fuentes['texto']}
        self.crear.etiqueta(
            self.top,
            "Ingrese los 4 puntos (x, y):",
            fuentes=self.fuentes,
            estilo="texto",
            fondo=COLOR_PANEL,
            color=COLOR_TEXTO,
        ).pack(pady=10, padx=10, anchor='w')

        self.entries = []
        for i in range(4):
            frame = self.crear.frame(self.top, fondo=COLOR_PANEL)
            frame.pack(pady=2, padx=10, fill='x')
            self.crear.etiqueta(
                frame,
                f"Punto {i+1}:",
                fuentes=self.fuentes,
                estilo="texto",
                fondo=COLOR_PANEL,
                color=COLOR_TEXTO,
            ).pack(side=tk.LEFT)
            # Entradas estilo personalizado (no hay molde específico)
            ex = tk.Entry(
                frame, width=8, bg="#0a2236", fg=COLOR_TEXTO,
                insertbackground=COLOR_TEXTO, relief="flat"
            )
            ex.pack(side=tk.LEFT, padx=5)
            ey = tk.Entry(
                frame, width=8, bg="#0a2236", fg=COLOR_TEXTO,
                insertbackground=COLOR_TEXTO, relief="flat"
            )
            ey.pack(side=tk.LEFT)
            self.entries.append((ex, ey))

        # Botón de cálculo
        self.crear.boton(
            self.top,
            texto="Calcular y Graficar",
            comando=self.procesar,
            fuentes=self.fuentes,
            fondo=COLOR_BOTON,
            fondo_activo=COLOR_BOTON_ACTIVO,
        ).pack(pady=10)

        # Resultado de la fórmula
        self.lbl_resultado = self.crear.etiqueta(
            self.top,
            texto="f(x) = ...",
            fuentes=self.fuentes,
            estilo="valor",
            fondo=COLOR_PANEL,
            color="#00ff00",  # verde mantenido del original
        )
        self.lbl_resultado.pack(pady=5)

        # Botón copiar
        self.crear.boton(
            self.top,
            texto="Copiar al portapapeles",
            comando=self.copiar_texto,
            fuentes=self.fuentes,
            pequeno=True,
            fondo=COLOR_BOTON,
            fondo_activo=COLOR_BOTON_ACTIVO,
        ).pack(pady=5)

        # ---- Gráfico ----
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.fig.patch.set_facecolor(COLOR_FONDO)
        self.ax.set_facecolor(COLOR_FONDO)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.top)
        self.canvas.get_tk_widget().pack(pady=10)

    # -----------------------------------------------------------------
    # Lógica de procesamiento (idéntica a la versión original)
    # -----------------------------------------------------------------
    def procesar(self):
        """Calcula el polinomio de grado 3 que interpola los 4 puntos y actualiza la UI."""
        try:
            puntos = [(float(ex.get()), float(ey.get())) for ex, ey in self.entries]
            x = [p[0] for p in puntos]
            y = [p[1] for p in puntos]

            # ---- INTERPOLACIÓN POLINÓMICA DE GRADO 3 ----
            # np.polyfit devuelve los coeficientes [a3, a2, a1, a0] del polinomio
            # a3*x^3 + a2*x^2 + a1*x + a0 que mejor se ajusta (mínimos cuadrados)
            # a los puntos (x, y). Con exactamente 4 puntos y grado 3, el ajuste
            # es una interpolación exacta (el polinomio pasa por todos los puntos).
            coefs = np.polyfit(x, y, 3)
            p = np.poly1d(coefs)   # crea un objeto polinomio evaluable

            # Formatear la fórmula para mostrarla
            self.formula_actual = (
                f"{coefs[0]:.6f}*x^3 + {coefs[1]:.6f}*x^2 + "
                f"{coefs[2]:.6f}*x + {coefs[3]:.6f}"
            )
            self.lbl_resultado.config(text=f"f(x) = {self.formula_actual}")

            # ---- GRÁFICO ----
            self.ax.clear()
            self.ax.set_facecolor(COLOR_FONDO)

            # Ejes fijos según la vista principal (0–30 en X, 0–15 en Y)
            self.ax.set_xlim(0, 30)
            self.ax.set_ylim(0, 15)

            x_plot = np.linspace(0, 30, 200)
            self.ax.plot(x, y, 'ro', label='Puntos')
            # Línea sólida color cian (como en el original)
            self.ax.plot(x_plot, p(x_plot), 'c-', linewidth=2, label='Polinomio')

            self.ax.legend(loc='upper right', fontsize='small')
            self.ax.grid(True, linestyle=':', alpha=0.6)
            self.canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Verifica que todos los campos contengan números válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def copiar_texto(self):
        """Copia la fórmula al portapapeles del sistema."""
        if self.formula_actual:
            self.top.clipboard_clear()
            self.top.clipboard_append(self.formula_actual)
            messagebox.showinfo("Éxito", "Fórmula copiada.")
        else:
            messagebox.showwarning("Advertencia", "No hay fórmula para copiar.")

    def mostrar(self):
        """Hace visible la ventana y la lleva al frente."""
        self.top.deiconify()
        self.top.lift()
