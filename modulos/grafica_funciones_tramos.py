from funciones_tramos import generar_funcion_tramos
import matplotlib.pyplot as plt


def _generar_puntos(inicio, fin, paso):
    # Si en el futuro se permite numpy, reemplazar por:
    # import numpy as np
    # return np.arange(inicio, fin + paso, paso)
    puntos = []
    i = inicio
    while i <= fin:
        puntos.append(i)
        i += paso
    return puntos


def _evaluar_funcion(x, caso, a, d1, d2, d4, d5):
    if caso == 0:
        return (x - a) * (x + d1) / (x - a)
    elif caso == 1:
        if x < a:
            return x + d2
        else:
            return x + d4
    else:
        return (d5 + 1) / (x - a)


def graficar_funcion_tramos(rut_str: str, guardar: str = None):
    resultado = generar_funcion_tramos(rut_str)
    if "error" in resultado:
        print(resultado["error"])
        return

    digitos = resultado["digitos"]
    d1, d2, d3, d4, d5, d8 = digitos[0], digitos[1], digitos[2], digitos[3], digitos[4], digitos[7]
    a = d3
    caso = resultado["caso"]

    rango = 5
    paso = 0.05
    xs_total = _generar_puntos(a - rango, a + rango, paso)
    # Con numpy: xs_total = np.linspace(a - rango, a + rango, 400)

    plt.figure(figsize=(10, 6))

    if caso == 0:
        xs_izq = [x for x in xs_total if x < a]
        xs_der = [x for x in xs_total if x > a]
        # Con numpy (más limpio):
        # mask_izq = xs_total < a
        # mask_der = xs_total > a
        # xs_izq, xs_der = xs_total[mask_izq], xs_total[mask_der]

        ys_izq = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_izq]
        ys_der = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_der]
        # Con numpy: ys_izq = _evaluar_funcion(xs_izq, caso, a, d1, d2, d4, d5)

        plt.plot(xs_izq, ys_izq, color="steelblue", label=f"f(x) = x + {d1}")
        plt.plot(xs_der, ys_der, color="steelblue")

        punto_hueco_y = a + d1
        plt.plot(a, punto_hueco_y, "o", markersize=8,
                 markerfacecolor="white", markeredgecolor="red", markeredgewidth=2,
                 label=f"Discontinuidad removible en x = {a}")

    elif caso == 1:
        xs_izq = [x for x in xs_total if x < a]
        xs_der = [x for x in xs_total if x >= a]
        # Con numpy:
        # mask_izq = xs_total < a
        # mask_der = xs_total >= a
        # xs_izq, xs_der = xs_total[mask_izq], xs_total[mask_der]

        ys_izq = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_izq]
        ys_der = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_der]
        # Con numpy: ys_izq = xs_izq + d2; ys_der = xs_der + d4

        plt.plot(xs_izq, ys_izq, color="steelblue", label=f"x + {d2} (x < {a})")
        plt.plot(xs_der, ys_der, color="coral", label=f"x + {d4} (x >= {a})")

        plt.plot(a, a + d2, "o", markersize=8,
                 markerfacecolor="white", markeredgecolor="steelblue", markeredgewidth=2,
                 label=f"Lim izq: {a + d2}")
        plt.plot(a, a + d4, "o", markersize=8,
                 markerfacecolor="coral", markeredgecolor="coral",
                 label=f"f({a}) = {a + d4}")

        espacio = abs((a + d4) - (a + d2)) * 0.3
        ym = min(a + d2, a + d4) + abs((a + d4) - (a + d2)) / 2
        plt.annotate("", xy=(a, a + d4), xytext=(a, a + d2),
                     arrowprops=dict(arrowstyle="<->", color="gray", lw=1.5))
        plt.text(a + 0.2, ym, f"Salto = {abs((a + d4) - (a + d2))}",
                 fontsize=9, color="gray", va="center")

    else:
        xs_izq = [x for x in xs_total if x < a and x != a]
        xs_der = [x for x in xs_total if x > a]
        # Con numpy: mask_izq = xs_total < a; mask_der = xs_total > a
        # xs_izq, xs_der = xs_total[mask_izq], xs_total[mask_der]

        ys_izq = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_izq]
        ys_der = [_evaluar_funcion(x, caso, a, d1, d2, d4, d5) for x in xs_der]
        # Con numpy: ys_izq = (d5 + 1) / (xs_izq - a); ys_der = (d5 + 1) / (xs_der - a)

        plt.plot(xs_izq, ys_izq, color="steelblue", label=f"({d5 + 1})/(x - {a})")
        plt.plot(xs_der, ys_der, color="steelblue")

        plt.axvline(x=a, color="black", linestyle="--", linewidth=1.5,
                    label=f"Asintota vertical x = {a}")

        plt.ylim(-100, 100)

    plt.axvline(x=a, color="gray", linestyle=":", alpha=0.5)
    plt.axhline(y=0, color="black", linewidth=0.5)
    plt.axvline(x=0, color="black", linewidth=0.5)

    plt.text(a, plt.ylim()[0] + 0.05 * (plt.ylim()[1] - plt.ylim()[0]),
             f"a = {a}", fontsize=10, ha="center", color="gray")

    tipo_discontinuidad = resultado["puntos_criticos"][0]["tipo"]
    plt.title(f"Funcion por tramos - {resultado['rut']}  |  {tipo_discontinuidad}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if guardar:
        plt.savefig(guardar, dpi=150)
        print(f"Grafico guardado en: {guardar}")
    else:
        plt.show()


def mostrar_grafico(rut_str: str):
    graficar_funcion_tramos(rut_str)


if __name__ == "__main__":
    ruts_prueba = [
        "12345670-K",
        "76354771-K",
        "12345672-6",
    ]

    for rut in ruts_prueba:
        print(f"Graficando RUT: {rut}")
        graficar_funcion_tramos(rut)
