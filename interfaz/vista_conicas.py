import sys
import os
import re

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODULOS_PATH = os.path.join(_PROJECT_ROOT, "modulos")
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
if _MODULOS_PATH not in sys.path:
    sys.path.insert(0, _MODULOS_PATH)

import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modulos.validacion_rut import validar_rut, formatear_procedimiento
from modulos.construccion_coeficientes import construir_coeficientes, formatear_construccion
from modulos.clasificador_conicas import ClasificadorDeConicas
from modulos.transformacion_canonica import transformar_a_canonica, formatear_transformacion
from modulos.graficador import GraficadorDeConicas

class VistaConicas(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.graficador = GraficadorDeConicas()
        self.ultima_canonica = None
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
        self.frame_izquierdo.grid_rowconfigure(3, weight=1)
        self.frame_izquierdo.grid_columnconfigure(0, weight=1)

        self.etiqueta_ecuacion_general = customtkinter.CTkLabel(self.frame_izquierdo, text="Ecuación General:")
        self.etiqueta_ecuacion_general.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.etiqueta_ecuacion_canonica = customtkinter.CTkLabel(self.frame_izquierdo, text="Ecuación Canónica:")
        self.etiqueta_ecuacion_canonica.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.etiqueta_procedimiento = customtkinter.CTkLabel(
            self.frame_izquierdo, text="Procedimiento Paso a Paso",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.etiqueta_procedimiento.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.texto_procedimiento = customtkinter.CTkTextbox(
            self.frame_izquierdo, wrap="word",
            font=customtkinter.CTkFont(family="Courier", size=12),
        )
        self.texto_procedimiento.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.texto_procedimiento.configure(state="disabled")

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
        self.etiqueta_defensa.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.etiqueta_centro = customtkinter.CTkLabel(self.frame_defensa, text="Centro (h, k):")
        self.etiqueta_centro.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_centro = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_centro.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.feedback_centro = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_centro.grid(row=1, column=2, padx=5, pady=5)

        self.etiqueta_vertices = customtkinter.CTkLabel(self.frame_defensa, text="Vértices:")
        self.etiqueta_vertices.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entrada_vertices = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_vertices.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.feedback_vertices = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_vertices.grid(row=2, column=2, padx=5, pady=5)

        self.etiqueta_focos = customtkinter.CTkLabel(self.frame_defensa, text="Focos:")
        self.etiqueta_focos.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entrada_focos = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_focos.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.feedback_focos = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_focos.grid(row=3, column=2, padx=5, pady=5)

        self.etiqueta_semiejes = customtkinter.CTkLabel(self.frame_defensa, text="Semiejes:")
        self.etiqueta_semiejes.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entrada_semiejes = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_semiejes.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.feedback_semiejes = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_semiejes.grid(row=4, column=2, padx=5, pady=5)

        self.boton_comprobar = customtkinter.CTkButton(
            self.frame_defensa, text="Comprobar Respuestas", command=self.comprobar_respuestas
        )
        self.boton_comprobar.grid(row=5, column=0, columnspan=3, padx=10, pady=(10, 5))

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

        canonica = transformar_a_canonica(coeficientes)

        self.etiqueta_ecuacion_general.configure(
            text=f"Ecuación General: {coeficientes['ecuacion']}"
        )
        self.etiqueta_ecuacion_canonica.configure(
            text=f"Ecuación Canónica: {canonica.get('ecuacion_canonica', canonica['tipo'])}"
        )

        procedimiento = (
            formatear_procedimiento(resultado_rut)
            + "\n\n"
            + formatear_construccion(coeficientes)
            + "\n\n"
            + resumen_clasificacion
            + "\n\n"
            + formatear_transformacion(canonica)
        )
        self._mostrar_procedimiento(procedimiento)
        self._graficar_canonica(canonica)
        self.ultima_canonica = canonica
        self._limpiar_feedback_defensa()

    def _mostrar_procedimiento(self, texto):
        self.texto_procedimiento.configure(state="normal")
        self.texto_procedimiento.delete("1.0", "end")
        self.texto_procedimiento.insert("1.0", texto)
        self.texto_procedimiento.configure(state="disabled")

    def _graficar_canonica(self, canonica):
        self.eje.clear()
        tipo = canonica["tipo"]

        if tipo == "Circunferencia":
            h, k = canonica["centro"]
            self.graficador.graficar_circunferencia(self.eje, h, k, canonica["radio"])
        elif tipo == "Elipse":
            h, k = canonica["centro"]
            if canonica["eje_mayor"] == "x":
                semieje_x, semieje_y = canonica["semieje_mayor"], canonica["semieje_menor"]
            else:
                semieje_x, semieje_y = canonica["semieje_menor"], canonica["semieje_mayor"]
            self.graficador.graficar_elipse(self.eje, h, k, semieje_x, semieje_y)
        elif tipo == "Hipérbola":
            h, k = canonica["centro"]
            es_horizontal = canonica["eje_transverso"] == "x"
            self.graficador.graficar_hiperbola(
                self.eje, h, k,
                canonica["semieje_transverso"], canonica["semieje_conjugado"],
                es_horizontal,
            )
        elif tipo.startswith("Parábola") and "degenerada" not in tipo:
            h, k = canonica["vertice"]
            factor_apertura = 1 / (4 * canonica["p"])
            es_vertical = "vertical" in tipo
            self.graficador.graficar_parabola(self.eje, h, k, factor_apertura, es_vertical)
        else:
            self.eje.text(
                0.5, 0.5, "Caso degenerado: no se puede graficar",
                ha="center", va="center", transform=self.eje.transAxes,
            )

        self.graficador.configurar_grafico(self.eje)
        self.figura.tight_layout()
        self.canvas_grafica.draw()

    def _valores_esperados(self, canonica):
        """
        Determina, según el tipo de cónica, qué campos de defensa aplican
        y cuáles son los números que debería contener cada uno.
        Un valor None significa que ese campo no aplica para este tipo.
        """
        tipo = canonica["tipo"]

        if tipo == "Circunferencia":
            h, k = canonica["centro"]
            return {
                "centro": [h, k],
                "vertices": None,
                "focos": None,
                "semiejes": [canonica["radio"]],
            }
        if tipo == "Elipse":
            h, k = canonica["centro"]
            return {
                "centro": [h, k],
                "vertices": [coord for punto in canonica["vertices"] for coord in punto],
                "focos": [coord for punto in canonica["focos"] for coord in punto],
                "semiejes": [canonica["semieje_mayor"], canonica["semieje_menor"]],
            }
        if tipo == "Hipérbola":
            h, k = canonica["centro"]
            return {
                "centro": [h, k],
                "vertices": [coord for punto in canonica["vertices"] for coord in punto],
                "focos": [coord for punto in canonica["focos"] for coord in punto],
                "semiejes": [canonica["semieje_transverso"], canonica["semieje_conjugado"]],
            }
        if tipo.startswith("Parábola") and "degenerada" not in tipo:
            vh, vk = canonica["vertice"]
            fh, fk = canonica["foco"]
            return {
                "centro": None,
                "vertices": [vh, vk],
                "focos": [fh, fk],
                "semiejes": None,
            }
        return {"centro": None, "vertices": None, "focos": None, "semiejes": None}

    def _extraer_numeros(self, texto):
        return [float(n) for n in re.findall(r"-?\d+\.?\d*", texto)]

    def _numeros_coinciden(self, encontrados, esperados, tolerancia=0.1):
        restantes = list(encontrados)
        for valor_esperado in esperados:
            coincidencia = next(
                (c for c in restantes if abs(c - valor_esperado) <= tolerancia), None
            )
            if coincidencia is None:
                return False
            restantes.remove(coincidencia)
        return True

    def _limpiar_feedback_defensa(self):
        for feedback in (
            self.feedback_centro, self.feedback_vertices,
            self.feedback_focos, self.feedback_semiejes,
        ):
            feedback.configure(text="")

    def comprobar_respuestas(self):
        if self.ultima_canonica is None:
            self.mostrar_error("Primero valida un RUT para poder comprobar las respuestas.")
            return
        self.limpiar_error()

        esperados = self._valores_esperados(self.ultima_canonica)
        campos = {
            "centro": (self.entrada_centro, self.feedback_centro),
            "vertices": (self.entrada_vertices, self.feedback_vertices),
            "focos": (self.entrada_focos, self.feedback_focos),
            "semiejes": (self.entrada_semiejes, self.feedback_semiejes),
        }

        for clave, (entrada, feedback) in campos.items():
            valor_esperado = esperados[clave]

            if valor_esperado is None:
                feedback.configure(text="N/A", text_color="gray")
                continue

            texto = entrada.get().strip()
            if texto == "":
                feedback.configure(text="vacío", text_color="orange")
                continue

            encontrados = self._extraer_numeros(texto)
            if self._numeros_coinciden(encontrados, valor_esperado):
                feedback.configure(text="✓ Correcto", text_color="green")
            else:
                feedback.configure(text="✗ Revisar", text_color="red")

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
        self._mostrar_procedimiento("")
        self.etiqueta_ecuacion_general.configure(text="Ecuación General:")
        self.etiqueta_ecuacion_canonica.configure(text="Ecuación Canónica:")
        
        self.entrada_centro.delete(0, "end")
        self.entrada_vertices.delete(0, "end")
        self.entrada_focos.delete(0, "end")
        self.entrada_semiejes.delete(0, "end")
        self._limpiar_feedback_defensa()
        self.ultima_canonica = None

        self._mostrar_grafica_vacia()
