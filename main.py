import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
_MODULOS_PATH = os.path.join(_PROJECT_ROOT, "modulos")
_INTERFAZ_PATH = os.path.join(_PROJECT_ROOT, "interfaz")
for _path in (_PROJECT_ROOT, _MODULOS_PATH, _INTERFAZ_PATH):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import customtkinter as ctk
from interfaz.vista_conicas import VistaConicas
from interfaz.vista_limites import VistaLimites
from modulos.validacion_rut import validar_rut


class AplicacionPrincipal(ctk.CTk):
    CARACTERES_RUT = set("0123456789.kK-")

    def __init__(self):
        super().__init__()
        self.title("EID Cálculo — Cónicas y Límites a partir del RUT")
        self.geometry("1300x900")
        self.minsize(1000, 700)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_entrada_rut()
        self._build_tabs()

    def _build_entrada_rut(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="ew")
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame,
            text="Evaluación Integrada de Desempeño — MAT1186",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 5), sticky="w")

        ctk.CTkLabel(frame, text="RUT:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=(10, 5), pady=10
        )

        self.entrada_rut = ctk.CTkEntry(frame, placeholder_text="Ej: 12345678-9")
        self.entrada_rut.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.entrada_rut.bind(
            "<KeyRelease>", lambda e: self._filtrar_entrada(self.entrada_rut, self.CARACTERES_RUT)
        )

        ctk.CTkButton(frame, text="Analizar RUT", command=self.analizar_rut).grid(
            row=1, column=2, padx=5, pady=10
        )
        ctk.CTkButton(frame, text="Limpiar Todo", command=self.limpiar_todo).grid(
            row=1, column=3, padx=(5, 10), pady=10
        )

        self.etiqueta_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.etiqueta_error.grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="w")

    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="nsew")

        tab_conicas = self.tabview.add("Cónicas")
        tab_limites = self.tabview.add("Límites")

        tab_conicas.grid_columnconfigure(0, weight=1)
        tab_conicas.grid_rowconfigure(0, weight=1)
        tab_limites.grid_columnconfigure(0, weight=1)
        tab_limites.grid_rowconfigure(0, weight=1)

        self.vista_conicas = VistaConicas(tab_conicas)
        self.vista_conicas.grid(row=0, column=0, sticky="nsew")

        self.vista_limites = VistaLimites(tab_limites)
        self.vista_limites.grid(row=0, column=0, sticky="nsew")

    def _filtrar_entrada(self, entrada, caracteres_permitidos):
        texto = entrada.get()
        filtrado = "".join(c for c in texto if c in caracteres_permitidos)
        if filtrado != texto:
            entrada.delete(0, "end")
            entrada.insert(0, filtrado)

    def analizar_rut(self):
        rut = self.entrada_rut.get().strip()
        if not rut:
            self.etiqueta_error.configure(text="El campo RUT no puede estar vacío.")
            return

        resultado_rut = validar_rut(rut)
        if not resultado_rut["valido"]:
            self.etiqueta_error.configure(text=resultado_rut["mensaje"])
            return

        self.etiqueta_error.configure(text="")
        self.vista_conicas.procesar_rut_valido(resultado_rut)
        self.vista_limites.procesar_rut_valido(resultado_rut)

    def limpiar_todo(self):
        self.entrada_rut.delete(0, "end")
        self.etiqueta_error.configure(text="")
        self.vista_conicas.limpiar_campos()
        self.vista_limites.limpiar_resultados()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")
    app = AplicacionPrincipal()
    app.mainloop()
