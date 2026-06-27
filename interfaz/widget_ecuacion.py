import re

import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def _tokenizar_mixto(texto):
    """
    Separa un texto en tokens, tratando cada tramo $...$ (formula) como un
    bloque atomico que nunca se corta al envolver lineas.
    """
    tokens = []
    pos = 0
    for m in re.finditer(r"\$[^$]+\$", texto):
        if m.start() > pos:
            tokens.extend(texto[pos:m.start()].split())
        tokens.append(m.group(0))
        pos = m.end()
    if pos < len(texto):
        tokens.extend(texto[pos:].split())
    return tokens


def envolver_parrafo(texto, ancho=95):
    """Envuelve un parrafo (prosa + formulas $...$) en lineas de hasta `ancho` caracteres."""
    tokens = _tokenizar_mixto(texto)
    lineas = []
    actual = ""
    for tok in tokens:
        candidato = f"{actual} {tok}".strip()
        if len(candidato) > ancho and actual:
            lineas.append(actual)
            actual = tok
        else:
            actual = candidato
    if actual:
        lineas.append(actual)
    return lineas


class EcuacionLatex(customtkinter.CTkFrame):
    """
    Renderiza una formula matematica con tipografia tipo LaTeX (fracciones,
    exponentes y raices reales) usando el motor mathtext de matplotlib.
    Es solo visualizacion: no realiza ningun calculo matematico.
    """

    def __init__(self, master, altura_pulgadas=0.6, ancho_pulgadas=6, tamano_fuente=15, **kwargs):
        super().__init__(master, **kwargs)
        self.tamano_fuente_base = tamano_fuente
        self.ancho_pulgadas = ancho_pulgadas

        self.figura = Figure(figsize=(ancho_pulgadas, altura_pulgadas), dpi=100)
        self.eje = self.figura.add_axes([0, 0, 1, 1])
        self.eje.axis("off")

        self.canvas = FigureCanvasTkAgg(self.figura, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.mostrar("")

    def redimensionar(self, altura_pulgadas):
        self.figura.set_size_inches(self.ancho_pulgadas, altura_pulgadas)
        ancho_px = int(self.ancho_pulgadas * self.figura.dpi)
        alto_px = int(altura_pulgadas * self.figura.dpi)
        self.canvas.get_tk_widget().configure(width=ancho_px, height=alto_px)

    def mostrar(self, texto):
        """Muestra una formula corta (1-2 lineas), centrada verticalmente."""
        self.eje.clear()
        self.eje.axis("off")

        if texto:
            lineas = texto.split("\n")
            largo_max = max(len(linea) for linea in lineas)
            tamano = self.tamano_fuente_base
            if largo_max > 40:
                tamano = max(9, int(tamano * 40 / largo_max))

            self.eje.text(
                0.02, 0.5, texto, fontsize=tamano,
                ha="left", va="center",
            )

        self.canvas.draw()

    def mostrar_parrafos(self, parrafos, ancho_linea=95, tamano_fuente=12, alto_por_linea=0.225):
        """
        Muestra una lista de parrafos (prosa + formulas $...$), cada uno
        envuelto automaticamente en varias lineas. Ajusta la altura del
        widget segun la cantidad de lineas resultante.
        """
        bloques = []
        for parrafo in parrafos:
            bloques.extend(envolver_parrafo(parrafo, ancho_linea))
            bloques.append("")
        if bloques and bloques[-1] == "":
            bloques.pop()

        n_lineas = max(len(bloques), 1)
        altura = max(0.5, n_lineas * alto_por_linea + 0.3)
        self.redimensionar(altura)

        self.eje.clear()
        self.eje.axis("off")
        if bloques:
            self.eje.text(
                0.01, 0.98, "\n".join(bloques), fontsize=tamano_fuente,
                ha="left", va="top",
            )
        self.canvas.draw()
