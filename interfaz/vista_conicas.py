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
from modulos.validacion_rut import formatear_procedimiento
from modulos.construccion_coeficientes import construir_coeficientes, formatear_construccion
from modulos.clasificador_conicas import ClasificadorDeConicas
from modulos.transformacion_canonica import transformar_a_canonica, formatear_transformacion
from modulos.graficador import GraficadorDeConicas
from interfaz.widget_ecuacion import EcuacionLatex

class VistaConicas(customtkinter.CTkFrame):
    CARACTERES_NUMERICOS = set("0123456789.,()- ")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.graficador = GraficadorDeConicas()
        self.ultima_canonica = None
        self.ultimos_coeficientes = None
        self.punto_verificado = None
        self.mostrar_respuestas = False
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
        self.etiqueta_error = customtkinter.CTkLabel(self, text="", text_color="red")
        self.etiqueta_error.grid(row=0, column=0, columnspan=2, padx=15, pady=(5, 0), sticky="w")

    def crear_panel_izquierdo(self):
        self.frame_izquierdo = customtkinter.CTkFrame(self)
        self.frame_izquierdo.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_izquierdo.grid_rowconfigure(5, weight=1)
        self.frame_izquierdo.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(
            self.frame_izquierdo, text="Ecuación General:",
            font=customtkinter.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.widget_ecuacion_general = EcuacionLatex(self.frame_izquierdo, altura_pulgadas=0.55)
        self.widget_ecuacion_general.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        customtkinter.CTkLabel(
            self.frame_izquierdo, text="Ecuación Canónica:",
            font=customtkinter.CTkFont(size=13, weight="bold"),
        ).grid(row=2, column=0, padx=10, pady=(0, 0), sticky="w")
        self.widget_ecuacion_canonica = EcuacionLatex(self.frame_izquierdo, altura_pulgadas=0.55)
        self.widget_ecuacion_canonica.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.etiqueta_procedimiento = customtkinter.CTkLabel(
            self.frame_izquierdo, text="Procedimiento Paso a Paso",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.etiqueta_procedimiento.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")

        self.frame_procedimiento_scroll = customtkinter.CTkScrollableFrame(self.frame_izquierdo)
        self.frame_procedimiento_scroll.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.frame_procedimiento_scroll.grid_columnconfigure(0, weight=1)

        self.widget_procedimiento = EcuacionLatex(
            self.frame_procedimiento_scroll, altura_pulgadas=2.0, ancho_pulgadas=6.8,
        )
        self.widget_procedimiento.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

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
        self.crear_buscador_puntos()

    def crear_buscador_puntos(self):
        self.frame_punto = customtkinter.CTkFrame(self.frame_derecho)
        self.frame_punto.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.frame_punto.grid_columnconfigure(1, weight=1)

        self.etiqueta_buscador = customtkinter.CTkLabel(
            self.frame_punto, text="Verificar si un Punto Pertenece a la Cónica",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.etiqueta_buscador.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.etiqueta_punto = customtkinter.CTkLabel(self.frame_punto, text="Punto (x, y):")
        self.etiqueta_punto.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_punto = customtkinter.CTkEntry(self.frame_punto, placeholder_text="Ej: 5.85, 2.75")
        self.entrada_punto.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.entrada_punto.bind("<KeyRelease>", lambda e: self._filtrar_entrada(self.entrada_punto, self.CARACTERES_NUMERICOS))

        self.boton_verificar_punto = customtkinter.CTkButton(
            self.frame_punto, text="Verificar Punto", command=self.verificar_punto
        )
        self.boton_verificar_punto.grid(row=1, column=2, padx=10, pady=5)

        self.feedback_punto = customtkinter.CTkLabel(
            self.frame_punto, text="", justify="left", wraplength=320
        )
        self.feedback_punto.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="w")

    def crear_campos_defensa(self):
        self.frame_defensa = customtkinter.CTkFrame(self.frame_derecho)
        self.frame_defensa.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.etiqueta_defensa = customtkinter.CTkLabel(self.frame_defensa, text="Campos para Defensa Oral", font=("Arial", 14, "bold"))
        self.etiqueta_defensa.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.etiqueta_centro = customtkinter.CTkLabel(self.frame_defensa, text="Centro (h, k):")
        self.etiqueta_centro.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_centro = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_centro.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.entrada_centro.bind("<KeyRelease>", lambda e: self._filtrar_entrada(self.entrada_centro, self.CARACTERES_NUMERICOS))
        self.feedback_centro = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_centro.grid(row=1, column=2, padx=5, pady=5)

        self.etiqueta_vertices = customtkinter.CTkLabel(self.frame_defensa, text="Vértices:")
        self.etiqueta_vertices.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entrada_vertices = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_vertices.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.entrada_vertices.bind("<KeyRelease>", lambda e: self._filtrar_entrada(self.entrada_vertices, self.CARACTERES_NUMERICOS))
        self.feedback_vertices = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_vertices.grid(row=2, column=2, padx=5, pady=5)

        self.etiqueta_focos = customtkinter.CTkLabel(self.frame_defensa, text="Focos:")
        self.etiqueta_focos.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entrada_focos = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_focos.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.entrada_focos.bind("<KeyRelease>", lambda e: self._filtrar_entrada(self.entrada_focos, self.CARACTERES_NUMERICOS))
        self.feedback_focos = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_focos.grid(row=3, column=2, padx=5, pady=5)

        self.etiqueta_semiejes = customtkinter.CTkLabel(self.frame_defensa, text="Semiejes:")
        self.etiqueta_semiejes.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entrada_semiejes = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_semiejes.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.entrada_semiejes.bind("<KeyRelease>", lambda e: self._filtrar_entrada(self.entrada_semiejes, self.CARACTERES_NUMERICOS))
        self.feedback_semiejes = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_semiejes.grid(row=4, column=2, padx=5, pady=5)

        self.etiqueta_directriz = customtkinter.CTkLabel(self.frame_defensa, text="Directriz:")
        self.etiqueta_directriz.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.entrada_directriz = customtkinter.CTkEntry(self.frame_defensa)
        self.entrada_directriz.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        self.entrada_directriz.bind("<KeyRelease>", lambda e: self._filtrar_entrada(self.entrada_directriz, self.CARACTERES_NUMERICOS))
        self.feedback_directriz = customtkinter.CTkLabel(self.frame_defensa, text="", width=70)
        self.feedback_directriz.grid(row=5, column=2, padx=5, pady=5)

        self.boton_comprobar = customtkinter.CTkButton(
            self.frame_defensa, text="Comprobar Respuestas", command=self.comprobar_respuestas
        )
        self.boton_comprobar.grid(row=6, column=0, columnspan=2, padx=10, pady=(10, 5))

        self.boton_mostrar_respuestas = customtkinter.CTkButton(
            self.frame_defensa, text="Mostrar Respuestas", command=self.alternar_respuestas,
            fg_color="gray40", hover_color="gray30",
        )
        self.boton_mostrar_respuestas.grid(row=6, column=2, padx=10, pady=(10, 5))

        self.etiqueta_advertencia_respuestas = customtkinter.CTkLabel(
            self.frame_defensa,
            text="⚠ Solo para practicar — no usar durante la defensa oral",
            font=customtkinter.CTkFont(size=10), text_color="gray60",
        )
        self.etiqueta_advertencia_respuestas.grid(row=7, column=0, columnspan=3, padx=10, pady=(0, 10))

        self.frame_defensa.grid_columnconfigure(1, weight=1)

    def procesar_rut_valido(self, resultado_rut):
        coeficientes = construir_coeficientes(resultado_rut["digitos"], resultado_rut["dv_ingresado"])

        try:
            clasificador = ClasificadorDeConicas(coeficientes)
            resumen_clasificacion = clasificador.ejecutar_clasificacion()
        except ValueError as e:
            self.mostrar_error(str(e))
            return

        canonica = transformar_a_canonica(coeficientes)

        self.widget_ecuacion_general.mostrar(coeficientes["ecuacion_latex"])
        self.widget_ecuacion_canonica.mostrar(
            canonica.get("ecuacion_canonica_latex", canonica["tipo"])
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
        self.ultima_canonica = canonica
        self.ultimos_coeficientes = coeficientes
        self.punto_verificado = None
        self.entrada_punto.delete(0, "end")
        self.feedback_punto.configure(text="")
        self.mostrar_respuestas = False
        self.boton_mostrar_respuestas.configure(text="Mostrar Respuestas")

        self._mostrar_procedimiento(procedimiento)
        self._graficar_canonica(canonica)
        self._limpiar_feedback_defensa()

    def _mostrar_procedimiento(self, texto):
        self.widget_procedimiento.mostrar_parrafos(texto.split("\n"), ancho_linea=80)

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

        if self.mostrar_respuestas:
            self._dibujar_respuestas_grafico(canonica)

        if self.punto_verificado is not None:
            x, y, pertenece = self.punto_verificado
            color_punto = "lime" if pertenece else "red"
            self.eje.plot(
                x, y, marker="*", markersize=16, color=color_punto,
                markeredgecolor="black", markeredgewidth=1, linestyle="None",
                label=f"Punto evaluado ({x}, {y})",
            )

        self.graficador.configurar_grafico(self.eje)
        self.figura.tight_layout()
        self.canvas_grafica.draw()

    def _dibujar_respuestas_grafico(self, canonica):
        centro = canonica.get("centro")
        if centro:
            self.eje.scatter([centro[0]], [centro[1]], color="red", zorder=5, label="Centro")

        for clave, color in (("vertice", "orange"), ("foco", "purple")):
            punto = canonica.get(clave)
            if punto:
                self.eje.scatter(
                    [punto[0]], [punto[1]], color=color, marker="s", zorder=5,
                    label=clave.capitalize(),
                )

        for clave, color, etiqueta in (
            ("vertices", "orange", "Vértices"),
            ("focos", "purple", "Focos"),
            ("co_vertices", "brown", "Co-vértices"),
        ):
            puntos = canonica.get(clave)
            if puntos:
                self.eje.scatter(
                    [p[0] for p in puntos], [p[1] for p in puntos],
                    color=color, marker="s", zorder=5, label=etiqueta,
                )

        directriz_valor = canonica.get("directriz_valor")
        if directriz_valor is not None:
            if canonica.get("directriz_eje") == "horizontal":
                self.eje.axhline(y=directriz_valor, color="brown", linestyle="--", label="Directriz")
            else:
                self.eje.axvline(x=directriz_valor, color="brown", linestyle="--", label="Directriz")

    def _identificar_punto_especial(self, x, y, canonica, tolerancia=0.3):
        def cerca(punto):
            return punto is not None and abs(punto[0] - x) <= tolerancia and abs(punto[1] - y) <= tolerancia

        if cerca(canonica.get("centro")):
            return "Centro"
        if cerca(canonica.get("vertice")):
            return "Vértice"
        if cerca(canonica.get("foco")):
            return "Foco"
        for punto in canonica.get("vertices") or []:
            if cerca(punto):
                return "Vértice"
        for punto in canonica.get("focos") or []:
            if cerca(punto):
                return "Foco"
        for punto in canonica.get("co_vertices") or []:
            if cerca(punto):
                return "Co-vértice (semieje menor)"
        return None

    def verificar_punto(self):
        if self.ultima_canonica is None or self.ultimos_coeficientes is None:
            self.mostrar_error("Primero valida un RUT para poder verificar un punto.")
            return
        self.limpiar_error()

        numeros = self._extraer_numeros(self.entrada_punto.get())
        if len(numeros) < 2:
            self.feedback_punto.configure(
                text="Ingresa un punto válido, ej: 5.85, 2.75", text_color="orange"
            )
            return

        x, y = numeros[0], numeros[1]
        coef = self.ultimos_coeficientes
        valor = coef["A"] * x**2 + coef["B"] * y**2 + coef["C"] * x + coef["D"] * y + coef["E"]
        escala = (
            abs(coef["A"]) * x**2 + abs(coef["B"]) * y**2
            + abs(coef["C"]) * x + abs(coef["D"]) * y + abs(coef["E"])
        )
        tolerancia = max(0.5, 0.05 * escala)
        pertenece = abs(valor) <= tolerancia

        if pertenece:
            texto = f"✓ El punto ({x}, {y}) SÍ pertenece a la cónica.\nA·x² + B·y² + C·x + D·y + E = {valor:.4f} ≈ 0"
            color = "green"
        else:
            texto = f"✗ El punto ({x}, {y}) NO pertenece a la cónica.\nA·x² + B·y² + C·x + D·y + E = {valor:.4f} ≠ 0"
            color = "red"

        especial = self._identificar_punto_especial(x, y, self.ultima_canonica)
        if especial:
            texto += f"\n★ Coincide con: {especial}"

        self.feedback_punto.configure(text=texto, text_color=color)
        self.punto_verificado = (x, y, pertenece)
        self._graficar_canonica(self.ultima_canonica)

    def _filtrar_entrada(self, entrada, caracteres_permitidos):
        """Elimina en tiempo real cualquier caracter que no este en caracteres_permitidos."""
        texto = entrada.get()
        filtrado = "".join(c for c in texto if c in caracteres_permitidos)
        if filtrado != texto:
            entrada.delete(0, "end")
            entrada.insert(0, filtrado)

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
                "directriz": None,
            }
        if tipo == "Elipse":
            h, k = canonica["centro"]
            return {
                "centro": [h, k],
                "vertices": [coord for punto in canonica["vertices"] for coord in punto],
                "focos": [coord for punto in canonica["focos"] for coord in punto],
                "semiejes": [canonica["semieje_mayor"], canonica["semieje_menor"]],
                "directriz": None,
            }
        if tipo == "Hipérbola":
            h, k = canonica["centro"]
            return {
                "centro": [h, k],
                "vertices": [coord for punto in canonica["vertices"] for coord in punto],
                "focos": [coord for punto in canonica["focos"] for coord in punto],
                "semiejes": [canonica["semieje_transverso"], canonica["semieje_conjugado"]],
                "directriz": None,
            }
        if tipo.startswith("Parábola") and "degenerada" not in tipo:
            vh, vk = canonica["vertice"]
            fh, fk = canonica["foco"]
            return {
                "centro": None,
                "vertices": [vh, vk],
                "focos": [fh, fk],
                "semiejes": None,
                "directriz": [canonica["directriz_valor"]],
            }
        return {"centro": None, "vertices": None, "focos": None, "semiejes": None, "directriz": None}

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
            self.feedback_focos, self.feedback_semiejes, self.feedback_directriz,
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
            "directriz": (self.entrada_directriz, self.feedback_directriz),
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

    def alternar_respuestas(self):
        if self.ultima_canonica is None:
            self.mostrar_error("Primero valida un RUT para poder mostrar las respuestas.")
            return
        self.limpiar_error()

        self.mostrar_respuestas = not self.mostrar_respuestas
        self.boton_mostrar_respuestas.configure(
            text="Ocultar Respuestas" if self.mostrar_respuestas else "Mostrar Respuestas"
        )
        self._actualizar_feedback_respuestas()
        self._graficar_canonica(self.ultima_canonica)

    def _formatear_valor_esperado(self, clave, valores):
        if clave in ("semiejes", "directriz"):
            return ", ".join(f"{round(v, 4)}" for v in valores)
        puntos = [valores[i:i + 2] for i in range(0, len(valores), 2)]
        return ", ".join(f"({round(p[0], 4)}, {round(p[1], 4)})" for p in puntos)

    def _actualizar_feedback_respuestas(self):
        if not self.mostrar_respuestas:
            self._limpiar_feedback_defensa()
            return

        esperados = self._valores_esperados(self.ultima_canonica)
        feedbacks = {
            "centro": self.feedback_centro, "vertices": self.feedback_vertices,
            "focos": self.feedback_focos, "semiejes": self.feedback_semiejes,
            "directriz": self.feedback_directriz,
        }
        for clave, feedback in feedbacks.items():
            valor = esperados[clave]
            if valor is None:
                feedback.configure(text="N/A", text_color="gray")
            else:
                feedback.configure(
                    text=f"→ {self._formatear_valor_esperado(clave, valor)}", text_color="#1e6fd9"
                )

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
        self.limpiar_error()
        self._mostrar_procedimiento("")
        self.widget_ecuacion_general.mostrar("")
        self.widget_ecuacion_canonica.mostrar("")

        self.entrada_centro.delete(0, "end")
        self.entrada_vertices.delete(0, "end")
        self.entrada_focos.delete(0, "end")
        self.entrada_semiejes.delete(0, "end")
        self.entrada_directriz.delete(0, "end")
        self._limpiar_feedback_defensa()
        self.ultima_canonica = None
        self.ultimos_coeficientes = None
        self.punto_verificado = None
        self.mostrar_respuestas = False
        self.boton_mostrar_respuestas.configure(text="Mostrar Respuestas")
        self.entrada_punto.delete(0, "end")
        self.feedback_punto.configure(text="")

        self._mostrar_grafica_vacia()
