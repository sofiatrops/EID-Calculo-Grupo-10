import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class EcuacionLatex(customtkinter.CTkFrame):
    """
    Renderiza una formula matematica con tipografia tipo LaTeX (fracciones,
    exponentes y raices reales) usando el motor mathtext de matplotlib.
    Es solo visualizacion: no realiza ningun calculo matematico.
    """

    def __init__(self, master, altura_pulgadas=0.6, tamano_fuente=15, **kwargs):
        super().__init__(master, **kwargs)
        self.tamano_fuente_base = tamano_fuente

        self.figura = Figure(figsize=(6, altura_pulgadas), dpi=100)
        self.eje = self.figura.add_axes([0, 0, 1, 1])
        self.eje.axis("off")

        self.canvas = FigureCanvasTkAgg(self.figura, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.mostrar("")

    def mostrar(self, texto):
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
