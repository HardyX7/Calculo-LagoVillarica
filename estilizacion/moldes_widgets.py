"""Moldes base y fabrica de widgets Tkinter."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import font
from typing import Callable
from PIL import Image, ImageTk
from constantes import (
    RUTA_FONDO, COLOR_BORDE, COLOR_PANEL_CLARO,
    COLOR_BOTON, COLOR_BOTON_ACTIVO, COLOR_FONDO, COLOR_PANEL, COLOR_TEXTO, 
    COLOR_TEXTO_SUAVE
)

class FondoEscalable(tk.Canvas):
    """Canvas base para mostrar la imagen de fondo ajustada a la ventana."""

    def __init__(self, master: tk.Misc, ruta: Path = RUTA_FONDO, **kwargs):
        super().__init__(master, highlightthickness=0, bd=0, **kwargs)
        self._imagen_original = Image.open(ruta) if ruta.exists() else None
        self._imagen_tk = None
        self.bind("<Configure>", self._redibujar)

    def _redibujar(self, event: tk.Event) -> None:
        self.delete("fondo")
        if self._imagen_original is None:
            self.configure(bg=COLOR_FONDO)
            return

        ancho = max(1, event.width)
        alto = max(1, event.height)
        imagen = self._imagen_original.resize((ancho, alto), Image.Resampling.LANCZOS)
        self._imagen_tk = ImageTk.PhotoImage(imagen)
        self.create_image(0, 0, image=self._imagen_tk, anchor="nw", tags="fondo")
        self.lower("fondo")


class MoldeFrame(tk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        fondo: str = COLOR_PANEL,
        borde: bool = False,
        **kwargs,
    ):
        super().__init__(
            master,
            bg=fondo,
            highlightbackground=COLOR_BORDE if borde else fondo,
            highlightthickness=1 if borde else 0,
            **kwargs,
        )


class MoldeEtiqueta(tk.Label):
    def __init__(
        self,
        master: tk.Misc,
        texto: str = "",
        *,
        fuentes: dict[str, font.Font],
        estilo: str = "texto",
        fondo: str = COLOR_PANEL,
        color: str = COLOR_TEXTO,
        **kwargs,
    ):
        super().__init__(
            master,
            text=texto,
            bg=fondo,
            fg=color,
            font=fuentes[estilo],
            **kwargs,
        )


class MoldeBoton(tk.Button):
    def __init__(
        self,
        master: tk.Misc,
        texto: str,
        comando: Callable,
        *,
        fuentes: dict[str, font.Font],
        pequeno: bool = False,
        fondo: str = COLOR_BOTON,
        fondo_activo: str = COLOR_BOTON_ACTIVO,
        **kwargs,
    ):
        super().__init__(
            master,
            text=texto,
            command=comando,
            bg=fondo,
            fg=COLOR_TEXTO,
            activebackground=fondo_activo,
            activeforeground=COLOR_TEXTO,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=fuentes["texto" if pequeno else "boton"],
            padx=6 if pequeno else 10,
            pady=2 if pequeno else 8,
            **kwargs,
        )


# --- NUEVO MOLDE PARA EL DESLIZADOR ---
class MoldeDeslizador(tk.Scale):
    """Molde estilizado y plano para controles deslizantes numéricos."""
    
    def __init__(
        self,
        master: tk.Misc,
        *,
        desde: int = 0,
        hasta: int = 100,
        comando: Callable[[str], None] | None = None,
        fuentes: dict[str, font.Font],
        estilo_fuente: str = "valor",
        fondo: str = COLOR_PANEL,
        color_barra: str = COLOR_BORDE,
        **kwargs,
    ):
        super().__init__(
            master,
            from_=desde,
            to=hasta,
            command=comando,
            orient=tk.HORIZONTAL,
            resolution=1,                  # Forzado a enteros por defecto
            bg=fondo,                      # Fondo del contenedor
            fg=COLOR_TEXTO_SUAVE,          # Color de los números del intervalo
            troughcolor=color_barra,       # Color de la línea/riel
            activebackground=COLOR_BOTON_ACTIVO, # Color del botón al pasar el mouse
            sliderrelief="flat",           # Estilo plano moderno sin 3D
            bd=0,                          # Quita bordes de ventana antigua
            highlightthickness=0,          # Elimina el recuadro de foco
            font=fuentes[estilo_fuente],
            **kwargs,
        )

class MoldeDesplegable(tk.OptionMenu):
    """Menú desplegable estilizado y plano para selección de opciones."""

    def __init__(
        self,
        master: tk.Misc,
        variable: tk.StringVar,
        opciones: list[str],
        *,
        fuentes: dict[str, font.Font],
        comando: Callable[[str], None] | None = None,
        fondo: str = COLOR_BOTON,
        fondo_activo: str = COLOR_BOTON_ACTIVO,
        **kwargs,
    ):
        
        if not variable.get() and opciones:
            variable.set(opciones[0])

        super().__init__(
            master,
            variable,
            *opciones,
            command=comando,
            **kwargs,
        )
        
        self.configure(
            bg=fondo,
            fg=COLOR_TEXTO,
            activebackground=fondo_activo,
            activeforeground=COLOR_TEXTO,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            font=fuentes["texto"],
            padx=10,
            pady=5,
        )
        
        self["menu"].configure(
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            activebackground=COLOR_BOTON_ACTIVO,
            activeforeground=COLOR_TEXTO,
            font=fuentes["texto"],
            bd=1,
            relief="flat"
        )

class CrearWidget:
    """Fabrica unica para crear widgets desde la vista."""

    def fuentes(self, root: tk.Tk) -> dict[str, font.Font]:
        return {
            "titulo": font.Font(root, family="Segoe UI", size=20, weight="bold"),
            "titulo_mapa": font.Font(root, family="Segoe UI", size=34, weight="bold"),
            "proporcion": font.Font(root, family="Segoe UI", size=17, weight="bold"),
            "estado": font.Font(root, family="Segoe UI", size=12, weight="bold"),
            "subtitulo": font.Font(root, family="Segoe UI", size=8),
            "etiqueta": font.Font(root, family="Segoe UI", size=8, weight="bold"),
            "valor": font.Font(root, family="Consolas", size=10, weight="bold"),
            "texto": font.Font(root, family="Segoe UI", size=9),
            "boton": font.Font(root, family="Segoe UI", size=10, weight="bold"),
        }

    def fondo(self, master: tk.Misc) -> FondoEscalable:
        return FondoEscalable(master, bg=COLOR_FONDO)

    def frame(
        self,
        master: tk.Misc,
        *,
        fondo: str = COLOR_PANEL,
        borde: bool = False,
        **kwargs,
    ) -> MoldeFrame:
        return MoldeFrame(master, fondo=fondo, borde=borde, **kwargs)

    def etiqueta(
        self,
        master: tk.Misc,
        texto: str = "",
        *,
        fuentes: dict[str, font.Font],
        estilo: str = "texto",
        fondo: str = COLOR_PANEL,
        color: str = COLOR_TEXTO,
        **kwargs,
    ) -> MoldeEtiqueta:
        return MoldeEtiqueta(
            master,
            texto,
            fuentes=fuentes,
            estilo=estilo,
            fondo=fondo,
            color=color,
            **kwargs,
        )

    def boton(
        self,
        master: tk.Misc,
        texto: str,
        comando: Callable,
        *,
        fuentes: dict[str, font.Font],
        pequeno: bool = False,
        fondo: str = COLOR_BOTON,
        fondo_activo: str = COLOR_BOTON_ACTIVO,
        **kwargs,
    ) -> MoldeBoton:
        return MoldeBoton(
            master,
            texto,
            comando,
            fuentes=fuentes,
            pequeno=pequeno,
            fondo=fondo,
            fondo_activo=fondo_activo,
            **kwargs,
        )

    def deslizador(
        self,
        master: tk.Misc,
        *,
        desde: int = 0,
        hasta: int = 100,
        comando: Callable[[str], None] | None = None,
        fuentes: dict[str, font.Font],
        estilo_fuente: str = "valor",
        fondo: str = COLOR_PANEL,
        color_barra: str = COLOR_BORDE,
        **kwargs,
    ) -> MoldeDeslizador:
        return MoldeDeslizador(
            master,
            desde=desde,
            hasta=hasta,
            comando=comando,
            fuentes=fuentes,
            estilo_fuente=estilo_fuente,
            fondo=fondo,
            color_barra=color_barra,
            **kwargs,
        )
    
    def desplegable(
        self,
        master: tk.Misc,
        variable: tk.StringVar,
        opciones: list[str],
        *,
        fuentes: dict[str, font.Font],
        comando: Callable[[str], None] | None = None,
        fondo: str = COLOR_BOTON,
        fondo_activo: str = COLOR_BOTON_ACTIVO,
        **kwargs,
    ) -> MoldeDesplegable:
        return MoldeDesplegable(
            master,
            variable=variable,
            opciones=opciones,
            fuentes=fuentes,
            comando=comando,
            fondo=fondo,
            fondo_activo=fondo_activo,
            **kwargs,
        )

    def tarjeta(
        self,
        master: tk.Misc,
        *,
        titulo: str,
        valor_inicial: str,
        fuentes: dict[str, font.Font],
        comando_profundizar: Callable | None = None,
    ) -> tuple[tk.Frame, tk.Label]:
        tarjeta = self.frame(master, fondo=COLOR_PANEL_CLARO, borde=True)
        encabezado = self.frame(tarjeta, fondo=COLOR_PANEL_CLARO)
        encabezado.pack(fill="x", padx=12, pady=(8, 0))

        self.etiqueta(
            encabezado,
            titulo,
            fuentes=fuentes,
            estilo="texto",
            fondo=COLOR_PANEL_CLARO,
            color=COLOR_TEXTO_SUAVE,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        if comando_profundizar is not None:
            self.boton(
                encabezado,
                "Profundizar",
                comando_profundizar,
                fuentes=fuentes,
                pequeno=True,
            ).pack(side="right")

        valor = self.etiqueta(
            tarjeta,
            valor_inicial,
            fuentes=fuentes,
            estilo="valor",
            fondo=COLOR_PANEL_CLARO,
            color=COLOR_TEXTO,
            anchor="w",
            justify="left",
            wraplength=310,
            height=2,
        )
        valor.pack(fill="x", padx=12, pady=(2, 9))
        return tarjeta, valor