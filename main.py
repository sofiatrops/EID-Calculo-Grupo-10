import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
_MODULOS_PATH = os.path.join(_PROJECT_ROOT, "modulos")
_INTERFAZ_PATH = os.path.join(_PROJECT_ROOT, "interfaz")
for _path in (_PROJECT_ROOT, _MODULOS_PATH, _INTERFAZ_PATH):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import customtkinter as ctk
from vista_conicas import VistaConicas
from vista_limites import VistaLimites


class AplicacionPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EID Cálculo — Cónicas y Límites a partir del RUT")
        self.geometry("1200x800")
        self.minsize(900, 600)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_navegacion()
        self._build_contenido()
        self.mostrar_conicas()

    def _build_navegacion(self):
        nav = ctk.CTkFrame(self)
        nav.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")

        ctk.CTkLabel(
            nav,
            text="Evaluación Integrada de Desempeño — MAT1186",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            nav, text="Módulo de Cónicas", command=self.mostrar_conicas
        ).pack(side="right", padx=5, pady=10)

        ctk.CTkButton(
            nav, text="Módulo de Límites", command=self.abrir_limites
        ).pack(side="right", padx=5, pady=10)

    def _build_contenido(self):
        self.contenido = ctk.CTkFrame(self)
        self.contenido.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(0, weight=1)

    def mostrar_conicas(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()
        vista = VistaConicas(self.contenido)
        vista.grid(row=0, column=0, sticky="nsew")

    def abrir_limites(self):
        VistaLimites(self)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")
    app = AplicacionPrincipal()
    app.mainloop()
