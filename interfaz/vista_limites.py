import sys
import os
import re
import unicodedata

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODULOS_PATH = os.path.join(_PROJECT_ROOT, "modulos")
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
if _MODULOS_PATH not in sys.path:
    sys.path.insert(0, _MODULOS_PATH)

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modulos.analisis_limites import analizar_limites
from modulos.grafica_funciones_tramos import _generar_puntos, _evaluar_funcion
from interfaz.widget_ecuacion import EcuacionLatex


class VistaLimites(ctk.CTkFrame):
    SINONIMOS_TIPO_DISCONTINUIDAD = {
        "removible": {"removible", "evitable"},
        "salto": {"salto", "de salto", "primera especie"},
        "infinita": {"infinita", "segunda especie", "asintotica"},
        "ninguna": {"ninguna", "continua", "no hay discontinuidad", "sin discontinuidad"},
    }

    PALABRAS_CLAVE_JUSTIFICACION = {
        "removible": ["factoriz", "cancel", "indetermin", "no esta definid"],
        "salto": ["lateral", "distint", "no existe", "salto"],
        "infinita": ["asintota", "denominador", "infinit"],
        "ninguna": ["continua", "existe", "igual"],
    }

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.resultado = None
        self.mostrar_respuestas = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_content()

    def _build_header(self):
        header = ctk.CTkLabel(
            self,
            text="Módulo de Límites y Continuidad",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        header.grid(row=0, column=0, pady=(15, 5), padx=20, sticky="ew")

    def _build_content(self):
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # --- Section 1: Función ---
        self.func_frame = ctk.CTkFrame(self.main_frame)
        self.func_frame.grid(row=0, column=0, padx=5, pady=(5, 10), sticky="ew")
        self.func_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.func_frame,
            text="Función generada",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        self.widget_func_expresion = EcuacionLatex(self.func_frame, altura_pulgadas=0.9)
        self.widget_func_expresion.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # --- Section 2: Tabla de valores ---
        self.tabla_frame = ctk.CTkFrame(self.main_frame)
        self.tabla_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.tabla_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.tabla_frame,
            text="Tabla de valores cercanos a x = a",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.tabla_grid = ctk.CTkFrame(self.tabla_frame)
        self.tabla_grid.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.tabla_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["x", "f(x)", "Lado", "Delta"]
        for j, h in enumerate(headers):
            ctk.CTkLabel(
                self.tabla_grid,
                text=h,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="center",
            ).grid(row=0, column=j, padx=2, pady=2, sticky="ew")

        self.tabla_labels = []
        for i in range(8):
            row_labels = []
            for j in range(4):
                lbl = ctk.CTkLabel(
                    self.tabla_grid,
                    text="—",
                    font=ctk.CTkFont(size=12),
                    anchor="center",
                )
                lbl.grid(row=i + 1, column=j, padx=2, pady=1, sticky="ew")
                row_labels.append(lbl)
            self.tabla_labels.append(row_labels)

        # --- Section 3: Gráfica ---
        self.graf_frame = ctk.CTkFrame(self.main_frame)
        self.graf_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            self.graf_frame,
            text="Gráfica de la función",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.fig = Figure(figsize=(8, 4.5), dpi=80)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graf_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self._mostrar_grafica_vacia()

        # --- Section 4: Procedimiento ---
        self.proc_frame = ctk.CTkFrame(self.main_frame)
        self.proc_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.proc_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.proc_frame,
            text="Procedimiento paso a paso",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.widget_procedimiento = EcuacionLatex(self.proc_frame, altura_pulgadas=2.5, ancho_pulgadas=8.5)
        self.widget_procedimiento.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Section 5: Campos de defensa ---
        self.defensa_frame = ctk.CTkFrame(self.main_frame)
        self.defensa_frame.grid(row=4, column=0, padx=5, pady=(10, 5), sticky="ew")
        self.defensa_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.defensa_frame,
            text="Defensa — Complete los campos (sin ayuda automática)",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 10), sticky="w")

        defensa_campos = [
            ("Límite por la izquierda:", "lim_izq"),
            ("Límite por la derecha:", "lim_der"),
            ("¿Existe el límite? (sí/no):", "limite_existe"),
            ("Valor de f(a), si existe:", "f_a"),
            ("¿Es continua en a? (sí/no):", "continua"),
            ("Tipo de discontinuidad:", "tipo_discontinuidad"),
        ]

        self.defensa_entries = {}
        self.defensa_feedback = {}
        for i, (label, key) in enumerate(defensa_campos):
            ctk.CTkLabel(
                self.defensa_frame,
                text=label,
                font=ctk.CTkFont(size=13),
                anchor="w",
            ).grid(row=i + 1, column=0, padx=(10, 5), pady=4, sticky="w")

            entry = ctk.CTkEntry(self.defensa_frame, placeholder_text="")
            entry.grid(row=i + 1, column=1, padx=(0, 10), pady=4, sticky="ew")
            self.defensa_entries[key] = entry

            feedback = ctk.CTkLabel(self.defensa_frame, text="", width=80)
            feedback.grid(row=i + 1, column=2, padx=(0, 10), pady=4)
            self.defensa_feedback[key] = feedback

        self.boton_comprobar = ctk.CTkButton(
            self.defensa_frame, text="Comprobar Respuestas", command=self.comprobar_respuestas
        )
        self.boton_comprobar.grid(
            row=len(defensa_campos) + 1, column=0, columnspan=2, padx=10, pady=(10, 5)
        )

        self.boton_mostrar_respuestas = ctk.CTkButton(
            self.defensa_frame, text="Mostrar Respuestas", command=self.alternar_respuestas,
            fg_color="gray40", hover_color="gray30",
        )
        self.boton_mostrar_respuestas.grid(
            row=len(defensa_campos) + 1, column=2, padx=10, pady=(10, 5)
        )

        ctk.CTkLabel(
            self.defensa_frame,
            text="⚠ Solo para practicar — no usar durante la defensa oral",
            font=ctk.CTkFont(size=10), text_color="gray60",
        ).grid(row=len(defensa_campos) + 2, column=0, columnspan=3, padx=10, pady=(0, 8))

        ctk.CTkLabel(
            self.defensa_frame,
            text="Justificación escrita:",
            font=ctk.CTkFont(size=13),
            anchor="w",
        ).grid(row=len(defensa_campos) + 3, column=0, padx=(10, 5), pady=(8, 4), sticky="ne")

        self.defensa_justificacion = ctk.CTkTextbox(
            self.defensa_frame, height=80, wrap="word"
        )
        self.defensa_justificacion.grid(
            row=len(defensa_campos) + 3, column=1, columnspan=2, padx=(0, 10), pady=(8, 10), sticky="ew"
        )

        self.feedback_justificacion = ctk.CTkLabel(
            self.defensa_frame, text="", justify="left", wraplength=600, anchor="w",
        )
        self.feedback_justificacion.grid(
            row=len(defensa_campos) + 4, column=1, columnspan=2, padx=(0, 10), pady=(0, 4), sticky="w"
        )

        self.feedback_respuesta_modelo = ctk.CTkLabel(
            self.defensa_frame, text="", justify="left", wraplength=600, anchor="w",
        )
        self.feedback_respuesta_modelo.grid(
            row=len(defensa_campos) + 5, column=1, columnspan=2, padx=(0, 10), pady=(0, 10), sticky="w"
        )

    def _mostrar_grafica_vacia(self):
        self.ax.clear()
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Gráfica de la función")
        self.ax.axhline(y=0, color="gray", linewidth=0.5)
        self.ax.axvline(x=0, color="gray", linewidth=0.5)
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()

    def procesar_rut_valido(self, resultado_rut):
        rut_str = f"{resultado_rut['cuerpo']}-{resultado_rut['dv_ingresado']}"
        self.resultado = analizar_limites(rut_str)
        self.mostrar_respuestas = False
        self.boton_mostrar_respuestas.configure(text="Mostrar Respuestas")
        self._actualizar_funcion()
        self._actualizar_tabla()
        self._actualizar_grafica()
        self._actualizar_procedimiento()
        self._limpiar_defensa()

    def limpiar_resultados(self):
        self.resultado = None
        self.mostrar_respuestas = False
        self.boton_mostrar_respuestas.configure(text="Mostrar Respuestas")
        self.widget_func_expresion.mostrar("")
        for fila in self.tabla_labels:
            for lbl in fila:
                lbl.configure(text="—")
        self._mostrar_grafica_vacia()
        self.widget_procedimiento.mostrar_parrafos([])
        self._limpiar_defensa()

    def _actualizar_funcion(self):
        r = self.resultado
        lineas = [r["expresion_latex"]]
        if "expresion_simplificada_latex" in r:
            lineas.append(r["expresion_simplificada_latex"])
        self.widget_func_expresion.mostrar("\n".join(lineas))

    def _actualizar_tabla(self):
        tabla = self.resultado["tabla_valores"]
        for i in range(8):
            if i < len(tabla):
                fila = tabla[i]
                fx = fila["f(x)"]
                fx_str = f"{fx:.6f}" if isinstance(fx, float) else str(fx)
                self.tabla_labels[i][0].configure(text=f"{fila['x']:.6f}")
                self.tabla_labels[i][1].configure(text=fx_str)
                self.tabla_labels[i][2].configure(text=fila["lado"])
                self.tabla_labels[i][3].configure(text=str(fila["delta"]))
            else:
                for j in range(4):
                    self.tabla_labels[i][j].configure(text="—")

    def _actualizar_grafica(self):
        self.ax.clear()
        r = self.resultado
        a = r["a"]
        caso = r["caso"]
        digitos = r["digitos"]
        d1, d2, d4, d5 = digitos[0], digitos[1], digitos[3], digitos[4]

        rango = 5
        paso = 0.05
        xs_total = _generar_puntos(a - rango, a + rango, paso)

        if caso == 0:
            xs_izq = [x for x in xs_total if x < a]
            xs_der = [x for x in xs_total if x > a]
            ys_izq = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_izq]
            ys_der = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_der]
            self.ax.plot(xs_izq, ys_izq, color="steelblue")
            self.ax.plot(xs_der, ys_der, color="steelblue")
            if self.mostrar_respuestas:
                self.ax.plot(a, a + d1, "o", markersize=8,
                             markerfacecolor="white", markeredgecolor="red", markeredgewidth=2,
                             label=f"Discontinuidad removible en x = {a}")
        elif caso == 1:
            xs_izq = [x for x in xs_total if x < a]
            xs_der = [x for x in xs_total if x >= a]
            ys_izq = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_izq]
            ys_der = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_der]
            self.ax.plot(xs_izq, ys_izq, color="steelblue", label="f(x), x < a")
            self.ax.plot(xs_der, ys_der, color="coral", label="f(x), x >= a")
            if self.mostrar_respuestas:
                self.ax.plot(a, a + d2, "o", markersize=8,
                             markerfacecolor="white", markeredgecolor="steelblue", markeredgewidth=2,
                             label=f"Lím izq: {a + d2}")
                self.ax.plot(a, a + d4, "o", markersize=8,
                             markerfacecolor="coral", markeredgecolor="coral",
                             label=f"f({a}) = {a + d4}")
                ym = min(a + d2, a + d4) + abs((a + d4) - (a + d2)) / 2
                self.ax.annotate("", xy=(a, a + d4), xytext=(a, a + d2),
                                 arrowprops=dict(arrowstyle="<->", color="gray", lw=1.5))
                self.ax.text(a + 0.2, ym, f"Salto = {abs((a + d4) - (a + d2))}",
                             fontsize=9, color="gray", va="center")
        else:
            xs_izq = [x for x in xs_total if x < a and x != a]
            xs_der = [x for x in xs_total if x > a]
            ys_izq = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_izq]
            ys_der = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_der]
            self.ax.plot(xs_izq, ys_izq, color="steelblue")
            self.ax.plot(xs_der, ys_der, color="steelblue")
            etiqueta_asintota = f"Asíntota vertical x = {a}" if self.mostrar_respuestas else "Asíntota vertical"
            self.ax.axvline(x=a, color="black", linestyle="--", linewidth=1.5, label=etiqueta_asintota)
            self.ax.set_ylim(-100, 100)

        self.ax.axvline(x=a, color="gray", linestyle=":", alpha=0.5)
        self.ax.axhline(y=0, color="black", linewidth=0.5)
        self.ax.axvline(x=0, color="black", linewidth=0.5)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        titulo = f"Función por tramos — RUT {r['rut']}"
        if self.mostrar_respuestas:
            titulo += f"  |  {r['tipo_discontinuidad']}"
        self.ax.set_title(titulo)
        if caso != 0 or self.mostrar_respuestas:
            self.ax.legend(fontsize=9)
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()

    def _actualizar_procedimiento(self):
        self.widget_procedimiento.mostrar_parrafos(self.resultado["pasos_justificacion_latex"])

    def alternar_respuestas(self):
        if self.resultado is None:
            return

        self.mostrar_respuestas = not self.mostrar_respuestas
        self.boton_mostrar_respuestas.configure(
            text="Ocultar Respuestas" if self.mostrar_respuestas else "Mostrar Respuestas"
        )
        self._actualizar_feedback_respuestas()
        self._actualizar_grafica()

    def _actualizar_feedback_respuestas(self):
        if not self.mostrar_respuestas:
            for feedback in self.defensa_feedback.values():
                feedback.configure(text="")
            self.feedback_respuesta_modelo.configure(text="")
            return

        r = self.resultado
        valores = {
            "lim_izq": r["lim_izquierdo"],
            "lim_der": r["lim_derecho"],
            "limite_existe": "Sí" if r["limite_existe"] else "No",
            "f_a": r["f_a"] if r["f_a_definida"] else "No definida",
            "continua": "Sí" if r["continua"] else "No",
            "tipo_discontinuidad": r["tipo_discontinuidad"],
        }
        for clave, valor in valores.items():
            self.defensa_feedback[clave].configure(text=f"→ {valor}", text_color="#1e6fd9")

        self.feedback_respuesta_modelo.configure(
            text=self._respuesta_modelo_justificacion(), text_color="#1e6fd9"
        )

    def _limpiar_defensa(self):
        for entry in self.defensa_entries.values():
            entry.delete(0, "end")
        for feedback in self.defensa_feedback.values():
            feedback.configure(text="")
        self.feedback_justificacion.configure(text="")
        self.feedback_respuesta_modelo.configure(text="")
        self.defensa_justificacion.delete("1.0", "end")

    def _normalizar(self, texto):
        texto = texto.strip().lower()
        return "".join(
            c for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )

    def _comparar_limite(self, texto, esperado):
        texto_norm = self._normalizar(texto)
        if texto_norm == "":
            return None
        if isinstance(esperado, str):
            sinonimos = {
                "+inf": {"+inf", "infinito", "+infinito", "mas infinito"},
                "-inf": {"-inf", "-infinito", "menos infinito"},
                "0": {"0"},
            }
            return texto_norm in sinonimos.get(esperado, {esperado})
        numeros = re.findall(r"-?\d+\.?\d*", texto)
        if not numeros:
            return False
        return abs(float(numeros[0]) - esperado) <= 0.1

    def _comparar_si_no(self, texto, esperado_bool):
        texto_norm = self._normalizar(texto)
        if texto_norm == "":
            return None
        afirmativos = {"si", "true", "verdadero", "existe"}
        negativos = {"no", "false", "falso", "no existe"}
        if texto_norm in afirmativos:
            return esperado_bool is True
        if texto_norm in negativos:
            return esperado_bool is False
        return False

    def _comparar_f_a(self, texto, definida, valor):
        texto_norm = self._normalizar(texto)
        if texto_norm == "":
            return None
        if not definida:
            negativos = {
                "no definida", "indefinida", "no existe", "n/a", "no aplica",
                "no esta definida",
            }
            return texto_norm in negativos
        numeros = re.findall(r"-?\d+\.?\d*", texto)
        if not numeros:
            return False
        return abs(float(numeros[0]) - valor) <= 0.1

    def _comparar_tipo_discontinuidad(self, texto, esperado):
        texto_norm = self._normalizar(texto)
        if texto_norm == "":
            return None
        aceptados = self.SINONIMOS_TIPO_DISCONTINUIDAD.get(esperado, {esperado})
        return any(s in texto_norm for s in aceptados)

    def comprobar_respuestas(self):
        if self.resultado is None:
            return
        r = self.resultado

        comparaciones = {
            "lim_izq": self._comparar_limite(self.defensa_entries["lim_izq"].get(), r["lim_izquierdo"]),
            "lim_der": self._comparar_limite(self.defensa_entries["lim_der"].get(), r["lim_derecho"]),
            "limite_existe": self._comparar_si_no(
                self.defensa_entries["limite_existe"].get(), r["limite_existe"]
            ),
            "f_a": self._comparar_f_a(
                self.defensa_entries["f_a"].get(), r["f_a_definida"], r["f_a"]
            ),
            "continua": self._comparar_si_no(self.defensa_entries["continua"].get(), r["continua"]),
            "tipo_discontinuidad": self._comparar_tipo_discontinuidad(
                self.defensa_entries["tipo_discontinuidad"].get(), r["tipo_discontinuidad"]
            ),
        }

        for clave, es_correcto in comparaciones.items():
            feedback = self.defensa_feedback[clave]
            if es_correcto is None:
                feedback.configure(text="vacío", text_color="orange")
            elif es_correcto:
                feedback.configure(text="✓ Correcto", text_color="green")
            else:
                feedback.configure(text="✗ Revisar", text_color="red")

        self.comprobar_justificacion()

    def comprobar_justificacion(self):
        """
        No puede juzgar si la justificacion esta "bien" o "mal" (es texto
        libre), pero revisa si menciona los conceptos clave esperados segun
        el tipo de discontinuidad, a modo de chequeo de cobertura referencial.
        """
        if self.resultado is None:
            return

        texto = self._normalizar(self.defensa_justificacion.get("1.0", "end"))
        claves = self.PALABRAS_CLAVE_JUSTIFICACION.get(self.resultado["tipo_discontinuidad"], [])

        if texto == "":
            self.feedback_justificacion.configure(text="vacío", text_color="orange")
            return
        if not claves:
            self.feedback_justificacion.configure(text="", text_color="gray")
            return

        encontradas = [c for c in claves if c in texto]
        faltantes = [c for c in claves if c not in texto]

        if len(encontradas) == len(claves):
            self.feedback_justificacion.configure(
                text=f"✓ Menciona los {len(claves)} conceptos clave esperados para este caso.",
                text_color="green",
            )
        else:
            self.feedback_justificacion.configure(
                text=(
                    f"Menciona {len(encontradas)}/{len(claves)} conceptos clave esperados. "
                    f"Podrías mencionar también: {', '.join(faltantes)}. "
                    f"(Este chequeo solo verifica cobertura de conceptos, no corrige el contenido.)"
                ),
                text_color="orange",
            )

    def _respuesta_modelo_justificacion(self):
        r = self.resultado
        a = r["a"]
        tipo = r["tipo_discontinuidad"]

        if tipo == "removible":
            return (
                f"Respuesta modelo: al evaluar f({a}) por sustitución directa se obtiene una forma "
                f"indeterminada 0/0. Factorizando y cancelando el factor común se simplifica la "
                f"expresión y se calcula el límite, que existe y vale {r['lim_izquierdo']}. Sin embargo, "
                f"f({a}) no está definida porque el denominador original se anula ahí, por lo que la "
                f"discontinuidad es removible."
            )
        if tipo == "salto":
            return (
                f"Respuesta modelo: los límites laterales en x={a} son distintos "
                f"(izquierdo={r['lim_izquierdo']}, derecho={r['lim_derecho']}), por lo que el límite no "
                f"existe. Como ambos límites laterales son finitos pero diferentes, la discontinuidad "
                f"es de tipo salto."
            )
        if tipo == "infinita":
            return (
                f"Respuesta modelo: al sustituir x={a} el denominador se anula y el numerador no, por "
                f"lo que esta NO es una forma indeterminada. El valor de f(x) crece o decrece sin límite "
                f"cerca de x={a}, lo que indica una asíntota vertical y una discontinuidad infinita."
            )
        return (
            f"Respuesta modelo: los límites laterales en x={a} son iguales y coinciden con "
            f"f({a})={r['f_a']}, por lo que la función es continua en ese punto (no hay discontinuidad)."
        )
