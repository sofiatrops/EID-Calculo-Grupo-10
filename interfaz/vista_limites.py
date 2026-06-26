import sys
import os

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


class VistaLimites(ctk.CTkToplevel):
    CARACTERES_RUT = set("0123456789.kK-")

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Análisis de Límites y Continuidad")
        self.geometry("1150x850")
        self.minsize(900, 600)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_rut_input()
        self._build_content()

        self.resultado = None

    def _build_header(self):
        header = ctk.CTkLabel(
            self,
            text="Módulo de Límites y Continuidad",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        header.grid(row=0, column=0, pady=(15, 5), padx=20, sticky="ew")

    def _build_rut_input(self):
        rut_frame = ctk.CTkFrame(self)
        rut_frame.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="ew")
        rut_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            rut_frame, text="RUT:", font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, padx=(10, 5), pady=10)

        self.rut_entry = ctk.CTkEntry(
            rut_frame, placeholder_text="12345678-9"
        )
        self.rut_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.rut_entry.bind("<KeyRelease>", lambda e: self._filtrar_entrada(self.rut_entry, self.CARACTERES_RUT))

        self.generar_btn = ctk.CTkButton(
            rut_frame, text="Generar", command=self._on_generar
        )
        self.generar_btn.grid(row=0, column=2, padx=(0, 10), pady=10)

        self.error_label = ctk.CTkLabel(
            rut_frame, text="", text_color="red", font=ctk.CTkFont(size=12)
        )
        self.error_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 5), sticky="w")

    def _build_content(self):
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="nsew")
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

        ctk.CTkLabel(
            self.func_frame, text="f(x) =", font=ctk.CTkFont(size=14)
        ).grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="ne")

        self.func_expresion = ctk.CTkLabel(
            self.func_frame,
            text="",
            font=ctk.CTkFont(size=14),
            justify="left",
            wraplength=700,
        )
        self.func_expresion.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="w")

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

        ctk.CTkLabel(
            self.proc_frame,
            text="Procedimiento paso a paso",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.proc_text = ctk.CTkTextbox(
            self.proc_frame, height=180, wrap="word", state="disabled"
        )
        self.proc_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Section 5: Campos de defensa ---
        self.defensa_frame = ctk.CTkFrame(self.main_frame)
        self.defensa_frame.grid(row=4, column=0, padx=5, pady=(10, 5), sticky="ew")
        self.defensa_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.defensa_frame,
            text="Defensa — Complete los campos (sin ayuda automática)",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="w")

        defensa_campos = [
            ("Límite por la izquierda:", "lim_izq"),
            ("Límite por la derecha:", "lim_der"),
            ("¿Existe el límite? (sí/no):", "limite_existe"),
            ("Valor de f(a), si existe:", "f_a"),
            ("¿Es continua en a? (sí/no):", "continua"),
            ("Tipo de discontinuidad:", "tipo_discontinuidad"),
        ]

        self.defensa_entries = {}
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

        ctk.CTkLabel(
            self.defensa_frame,
            text="Justificación escrita:",
            font=ctk.CTkFont(size=13),
            anchor="w",
        ).grid(row=len(defensa_campos) + 1, column=0, padx=(10, 5), pady=(8, 4), sticky="ne")

        self.defensa_justificacion = ctk.CTkTextbox(
            self.defensa_frame, height=80, wrap="word"
        )
        self.defensa_justificacion.grid(
            row=len(defensa_campos) + 1, column=1, padx=(0, 10), pady=(8, 10), sticky="ew"
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

    def _filtrar_entrada(self, entrada, caracteres_permitidos):
        """Elimina en tiempo real cualquier caracter que no este en caracteres_permitidos."""
        texto = entrada.get()
        filtrado = "".join(c for c in texto if c in caracteres_permitidos)
        if filtrado != texto:
            entrada.delete(0, "end")
            entrada.insert(0, filtrado)

    def _mostrar_error(self, mensaje):
        self.error_label.configure(text=mensaje)

    def _limpiar_error(self):
        self.error_label.configure(text="")

    def _limpiar_resultados(self):
        self.resultado = None
        self.func_expresion.configure(text="")
        for fila in self.tabla_labels:
            for lbl in fila:
                lbl.configure(text="—")
        self._mostrar_grafica_vacia()
        self.proc_text.configure(state="normal")
        self.proc_text.delete("1.0", "end")
        self.proc_text.configure(state="disabled")
        self._limpiar_defensa()

    def _on_generar(self):
        rut = self.rut_entry.get().strip()
        if not rut:
            self._mostrar_error("El campo RUT no puede estar vacío.")
            self._limpiar_resultados()
            return

        resultado = analizar_limites(rut)
        if "error" in resultado:
            self._mostrar_error(resultado["error"])
            self._limpiar_resultados()
            return

        self._limpiar_error()
        self.resultado = resultado
        self._actualizar_funcion()
        self._actualizar_tabla()
        self._actualizar_grafica()
        self._actualizar_procedimiento()
        self._limpiar_defensa()

    def _actualizar_funcion(self):
        r = self.resultado
        texto = r["expresion"]
        if "expresion_simplificada" in r:
            texto += f"\nSimplificada: {r['expresion_simplificada']}"
        self.func_expresion.configure(text=texto)

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
            self.ax.plot(xs_izq, ys_izq, color="steelblue", label=f"f(x) = x + {d1}")
            self.ax.plot(xs_der, ys_der, color="steelblue")
            punto_hueco_y = a + d1
            self.ax.plot(a, punto_hueco_y, "o", markersize=8,
                         markerfacecolor="white", markeredgecolor="red", markeredgewidth=2,
                         label=f"Discontinuidad removible en x = {a}")
        elif caso == 1:
            xs_izq = [x for x in xs_total if x < a]
            xs_der = [x for x in xs_total if x >= a]
            ys_izq = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_izq]
            ys_der = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_der]
            self.ax.plot(xs_izq, ys_izq, color="steelblue", label=f"x + {d2} (x < {a})")
            self.ax.plot(xs_der, ys_der, color="coral", label=f"x + {d4} (x >= {a})")
            self.ax.plot(a, a + d2, "o", markersize=8,
                         markerfacecolor="white", markeredgecolor="steelblue", markeredgewidth=2,
                         label=f"Lím izq: {a + d2}")
            self.ax.plot(a, a + d4, "o", markersize=8,
                         markerfacecolor="coral", markeredgecolor="coral",
                         label=f"f({a}) = {a + d4}")
            espacio = abs((a + d4) - (a + d2)) * 0.3
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
            self.ax.plot(xs_izq, ys_izq, color="steelblue", label=f"({d5 + 1})/(x - {a})")
            self.ax.plot(xs_der, ys_der, color="steelblue")
            self.ax.axvline(x=a, color="black", linestyle="--", linewidth=1.5,
                            label=f"Asíntota vertical x = {a}")
            self.ax.set_ylim(-100, 100)

        self.ax.axvline(x=a, color="gray", linestyle=":", alpha=0.5)
        self.ax.axhline(y=0, color="black", linewidth=0.5)
        self.ax.axvline(x=0, color="black", linewidth=0.5)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        tipo_discontinuidad = r["tipo_discontinuidad"]
        self.ax.set_title(f"Función por tramos - {r['rut']}  |  {tipo_discontinuidad}")
        self.ax.legend(fontsize=9)
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()

    def _actualizar_procedimiento(self):
        self.proc_text.configure(state="normal")
        self.proc_text.delete("1.0", "end")
        pasos = self.resultado["pasos_justificacion"]
        for paso in pasos:
            self.proc_text.insert("end", paso + "\n\n")
        self.proc_text.configure(state="disabled")

    def _limpiar_defensa(self):
        for entry in self.defensa_entries.values():
            entry.delete(0, "end")
        self.defensa_justificacion.delete("1.0", "end")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("EID Cálculo")
    app.geometry("400x200")

    ctk.CTkLabel(
        app,
        text="Evaluación Integrada de Desempeño\nMAT1186 - Introducción al Cálculo",
        font=ctk.CTkFont(size=16, weight="bold"),
        justify="center",
    ).pack(pady=30, padx=20)

    ctk.CTkButton(
        app,
        text="Abrir Módulo de Límites",
        command=lambda: VistaLimites(app),
        width=250,
        height=40,
    ).pack(pady=10)

    app.mainloop()
