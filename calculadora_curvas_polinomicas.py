import sys
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BG_COLOR = "#2d2d2d"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#4a90e2"

class InterpoladorApp:
    
    """
    Aplicación para interpolar puntos con un polinomio de grado 3 y graficar el resultado.
    Permite ingresar 4 puntos (x, y), calcula el polinomio que los interpola, muestra la 
    fórmula y grafica la curva. También incluye un botón para copiar la fórmula al portapapeles. 
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Modelador de Contornos - Lago Villarrica")
        self.root.configure(bg=BG_COLOR)
        self.formula_actual = ""
        
        # Estilo para etiquetas
        label_style = {'bg': BG_COLOR, 'fg': FG_COLOR, 'font': ('Arial', 10)}
        
        tk.Label(root, text="Ingrese los 4 puntos (x, y):", **label_style).pack(pady=10)
        
        self.entries = []
        for i in range(4):
            frame = tk.Frame(root, bg=BG_COLOR)
            frame.pack()
            tk.Label(frame, text=f"Punto {i+1}:", **label_style).pack(side=tk.LEFT)
            ex = tk.Entry(frame, width=8, bg="#3d3d3d", fg=FG_COLOR, insertbackground=FG_COLOR); ex.pack(side=tk.LEFT, padx=5)
            ey = tk.Entry(frame, width=8, bg="#3d3d3d", fg=FG_COLOR, insertbackground=FG_COLOR); ey.pack(side=tk.LEFT)
            self.entries.append((ex, ey))

        tk.Button(root, text="Calcular y Graficar", command=self.procesar, bg=ACCENT_COLOR, fg=FG_COLOR).pack(pady=10)
        
        self.lbl_resultado = tk.Label(root, text="f(x) = ...", fg="#00ff00", bg=BG_COLOR, font=('Courier', 10))
        self.lbl_resultado.pack(pady=5)
        
        tk.Button(root, text="Copiar al portapapeles", command=self.copiar_texto, bg="#555555", fg=FG_COLOR).pack(pady=5)

        # Configuración del gráfico en modo oscuro
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.fig.patch.set_facecolor(BG_COLOR)
        self.ax.set_facecolor(BG_COLOR)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

    def procesar(self):
        try:
            puntos = [(float(ex.get()), float(ey.get())) for ex, ey in self.entries]
            x = [p[0] for p in puntos]
            y = [p[1] for p in puntos]

            coefs = np.polyfit(x, y, 3)
            p = np.poly1d(coefs)
            
            self.formula_actual = f"{coefs[0]:.6f}*x^3 + {coefs[1]:.6f}*x^2 + {coefs[2]:.6f}*x + {coefs[3]:.6f}"
            self.lbl_resultado.config(text=f"f(x) = {self.formula_actual}")

            # Graficar
            self.ax.clear()
            self.ax.set_facecolor(BG_COLOR)
            
            # Ejes fijos 0 a 30 y 0 a 15
            self.ax.set_xlim(0, 30)
            self.ax.set_ylim(0, 15)
            
            x_plot = np.linspace(0, 30, 200)
            self.ax.plot(x, y, 'ro', label='Puntos')
            # Línea sólida
            self.ax.plot(x_plot, p(x_plot), 'c-', linewidth=2, label='Polinomio')
            
            self.ax.legend(loc='upper right', fontsize='small')
            self.ax.grid(True, linestyle=':', alpha=0.6)
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Verifica los números: {e}")

    def copiar_texto(self):
        if self.formula_actual:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.formula_actual)
            messagebox.showinfo("Éxito", "Fórmula copiada.")

if __name__ == "__main__":
    
    sys.dont_write_bytecode = True
    root = tk.Tk()
    app = InterpoladorApp(root)
    root.mainloop()