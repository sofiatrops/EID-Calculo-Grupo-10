import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODULOS_PATH = os.path.join(_PROJECT_ROOT, "modulos")
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
if _MODULOS_PATH not in sys.path:
    sys.path.insert(0, _MODULOS_PATH)

import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from validacion_rut import validar_rut, formatear_procedimiento
from construccion_coeficientes import construir_coeficientes, formatear_construccion
from clasificador_conicas import ClasificadorDeConicas

class VistaConicas(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configurar_layout()
        self.crear_widgets()
        self._mostrar_grafica_vacia()

    def configurar_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def crear_widgets(self):
        self.crear_panel_superior()
        self.crear_panel_izquierdo()
        self.crear_panel_derecho()

    def crear_panel_superior(self):
        self.frame_entrada = customtkinter.CTkFrame(self)
        self.frame_entrada.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.etiqueta_rut = customtkinter.CTkLabel(self.frame_entrada, text="Ingrese RUT:")
        self.etiqueta_rut.grid(row=0, column=0, padx=10, pady=10)
        
        self.entrada_rut = customtkinter.CTkEntry(self.frame_entrada, placeholder_text="Ej: 12345678-9")
        self.entrada_rut.grid(row=0, column=1, padx=10, pady=10)
        
        self.boton_validar = customtkinter.CTkButton(self.frame_entrada, text="Validar RUT", command=self.validar_rut_presionado)
        self.boton_validar.grid(row=0, column=2, padx=10, pady=10)

        self.boton_limpiar = customtkinter.CTkButton(self.frame_entrada, text="Limpiar Todo", command=self.limpiar_campos)
        self.boton_limpiar.grid(row=0, column=3, padx=10, pady=10)

        self.etiqueta_error = customtkinter.CTkLabel(self.frame_entrada, text="", text_color="red")
        self.etiqueta_error.grid(row=1, column=0, columnspan=4, padx=10, pady=5)

    def crear_panel_izquierdo(self):
        self.frame_izquierdo = customtkinter.CTkFrame(self)
        self.frame_izquierdo.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_izquierdo.grid_rowconfigure(2, weight=1)
        self.frame_izquierdo.grid_columnconfigure(0, weight=1)

        self.etiqueta_ecuacion_general = customtkinter.CTkLabel(self.frame_izquierdo, text="Ecuación General:")
        self.etiqueta_ecuacion_general.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.etiqueta_ecuacion_canonica = customtkinter.CTkLabel(self.frame_izquierdo, text="Ecuación Canónica:")
        self.etiqueta_ecuacion_canonica.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.panel_procedimiento = customtkinter.CTkScrollableFrame(self.frame_izquierdo, label_text="Procedimiento Paso a Paso")
        self.panel_procedimiento.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.texto_procedimiento = customtkinter.CTkLabel(
            self.panel_procedimiento, text="", justify="left", wraplength=600
        )
        self.texto_procedimiento.pack(padx=10, pady=10, anchor="w")

    def crear_panel_derecho(self):
        self.frame_derecho = customtkinter.CTkFrame(self)
        self.frame_derecho.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_derecho.grid_rowconfigure(0, weight=1)
        self.frame_derecho.grid_columnconfigure(0, weight=1)

        self.frame_grafica = customtkinter.CTkFrame(self.frame_derecho)
        self.frame_grafica.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.eje = self.figura.add_subplot(111)
        
        self.canvas_grafica = FigureCanvasTkAgg(self.figura, master=self.frame_grafica)
        self.widget_grafica = self.canvas_grafica.get_tk_widget()
        self.widget_grafica.pack(fill="both", expand=True)

        self.crear_campos_defensa()

    def crear_campos_defensa(self):
        self.frame_defensa = customtkinter.CTkFrame(self.frame_derecho)
        self.frame_defensa.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.etiqueta_defensa = customtkinter.CTkLabel(self.frame_defensa, text="Campos para Defensa Oral", font=("Arial", 14, "bold"))
        self.etiqueta_defensa.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        self.etiqueta_centro = customtkinter.CTkLabel(self.frame_defensa, text="Centro (h, k):")
        self.etiqueta_centro.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_centro = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_centro.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.etiqueta_vertices = customtkinter.CTkLabel(self.frame_defensa, text="Vértices:")
        self.etiqueta_vertices.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entrada_vertices = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_vertices.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.etiqueta_focos = customtkinter.CTkLabel(self.frame_defensa, text="Focos:")
        self.etiqueta_focos.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entrada_focos = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_focos.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.etiqueta_semiejes = customtkinter.CTkLabel(self.frame_defensa, text="Semiejes:")
        self.etiqueta_semiejes.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entrada_semiejes = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_semiejes.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.frame_defensa.grid_columnconfigure(1, weight=1)

    def validar_rut_presionado(self):
        rut_ingresado = self.entrada_rut.get().strip()
        if rut_ingresado == "":
            self.mostrar_error("El campo RUT no puede estar vacío")
            return

        resultado_rut = validar_rut(rut_ingresado)
        if not resultado_rut["valido"]:
            self.mostrar_error(resultado_rut["mensaje"])
            return

        self.limpiar_error()
        self.procesar_rut_valido(resultado_rut)

    def procesar_rut_valido(self, resultado_rut):
        coeficientes = construir_coeficientes(resultado_rut["digitos"], resultado_rut["dv_ingresado"])

        try:
            clasificador = ClasificadorDeConicas(coeficientes)
            resumen_clasificacion = clasificador.ejecutar_clasificacion()
        except ValueError as e:
            self.mostrar_error(str(e))
            return

        self.etiqueta_ecuacion_general.configure(
            text=f"Ecuación General: {coeficientes['ecuacion']}"
        )
        self.etiqueta_ecuacion_canonica.configure(
            text="Ecuación Canónica: (pendiente — ver KAN-9)"
        )

        procedimiento = (
            formatear_procedimiento(resultado_rut)
            + "\n\n"
            + formatear_construccion(coeficientes)
            + "\n\n"
            + resumen_clasificacion
        )
        self.texto_procedimiento.configure(text=procedimiento)

    def mostrar_error(self, mensaje):
        self.etiqueta_error.configure(text=mensaje)

    def limpiar_error(self):
        self.etiqueta_error.configure(text="")

    def _mostrar_grafica_vacia(self):
        self.eje.clear()
        self.eje.set_xlabel("x")
        self.eje.set_ylabel("y")
        self.eje.axhline(y=0, color="gray", linewidth=0.5)
        self.eje.axvline(x=0, color="gray", linewidth=0.5)
        self.eje.grid(True, alpha=0.3)
        self.figura.tight_layout()
        self.canvas_grafica.draw()

    def limpiar_campos(self):
        self.entrada_rut.delete(0, "end")
        self.limpiar_error()
        self.texto_procedimiento.configure(text="")
        self.etiqueta_ecuacion_general.configure(text="Ecuación General:")
        self.etiqueta_ecuacion_canonica.configure(text="Ecuación Canónica:")
        
        self.entrada_centro.delete(0, "end")
        self.entrada_vertices.delete(0, "end")
        self.entrada_focos.delete(0, "end")
        self.entrada_semiejes.delete(0, "end")

        self._mostrar_grafica_vacia()
