from validacion_rut import validar_rut


def generar_funcion_tramos(rut_str: str) -> dict:
    resultado_rut = validar_rut(rut_str)

    if not resultado_rut["valido"]:
        return {"error": f"RUT inválido: {resultado_rut['mensaje']}"}

    digitos = resultado_rut["digitos"]
    d1, d2, d3, d4, d5, d8 = digitos[0], digitos[1], digitos[2], digitos[3], digitos[4], digitos[7]
    a = d3
    residuo = d8 % 3

    caso = None
    tramos = []
    puntos_criticos = []
    expresion = ""

    if residuo == 0:
        caso = 0
        expresion = f"f(x) = (x - {a})(x + {d1}) / (x - {a})"
        tramos = [
            {"tramo": "x != a", "expresion": f"(x - {a})(x + {d1}) / (x - {a})"},
        ]
        puntos_criticos = [
            {"punto": a, "tipo": "discontinuidad removible", "razon": f"Denominador (x - {a}) se anula, pero el factor se cancela"},
        ]
    elif residuo == 1:
        caso = 1
        expresion = f"f(x) = x + {d2}  si x < {a},  f(x) = x + {d4}  si x >= {a}"
        tramos = [
            {"tramo": f"x < {a}", "expresion": f"x + {d2}"},
            {"tramo": f"x >= {a}", "expresion": f"x + {d4}"},
        ]
        puntos_criticos = [
            {"punto": a, "tipo": "discontinuidad de salto", "razon": f"Límite lateral izquierdo: {d2 + a}, límite lateral derecho: {d4 + a}"},
        ]
    else:
        caso = 2
        expresion = f"f(x) = ({d5 + 1}) / (x - {a})"
        tramos = [
            {"tramo": f"x != {a}", "expresion": f"({d5 + 1}) / (x - {a})"},
        ]
        puntos_criticos = [
            {"punto": a, "tipo": "discontinuidad infinita",             "razon": f"Denominador (x - {a}) se anula -> asíntota vertical"},
        ]

    return {
        "rut": resultado_rut["cuerpo"] + "-" + resultado_rut["dv_ingresado"],
        "digitos": digitos,
        "d1": d1,
        "d2": d2,
        "d3": d3,
        "d4": d4,
        "d5": d5,
        "d8": d8,
        "punto_analisis": a,
        "d8_mod_3": residuo,
        "caso": caso,
        "expresion": expresion,
        "tramos": tramos,
        "puntos_criticos": puntos_criticos,
    }


def mostrar_funcion_tramos(resultado: dict):
    if "error" in resultado:
        print(resultado["error"])
        return

    print("=" * 55)
    print("  FUNCIÓN POR TRAMOS — ANÁLISIS")
    print("=" * 55)
    print(f"\nRUT: {resultado['rut']}")
    print(f"Dígitos: d1={resultado['d1']}, d2={resultado['d2']}, "
          f"d3={resultado['d3']}, d4={resultado['d4']}, "
          f"d5={resultado['d5']}, d8={resultado['d8']}")
    print(f"Punto de análisis: a = d3 = {resultado['punto_analisis']}")

    print(f"\nCaso seleccionado: d8 % 3 = {resultado['d8']} % 3 = {resultado['d8_mod_3']}")

    if resultado["caso"] == 0:
        print("  => Discontinuidad removible")
    elif resultado["caso"] == 1:
        print("  => Discontinuidad de salto")
    else:
        print("  => Discontinuidad infinita")

    print(f"\nExpresión: {resultado['expresion']}")

    print("\nTramos:")
    for t in resultado["tramos"]:
        print(f"  - {t['tramo']}: {t['expresion']}")

    print("\nPuntos críticos:")
    for pc in resultado["puntos_criticos"]:
        print(f"  - x = {pc['punto']}: {pc['tipo']}")
        print(f"    Razón: {pc['razon']}")

    print("=" * 55)


if __name__ == "__main__":
    ruts_prueba = [
        "12345670-K",
        "76354771-K",
        "12345672-6",
    ]

    for rut in ruts_prueba:
        resultado = generar_funcion_tramos(rut)
        if "error" not in resultado:
            mostrar_funcion_tramos(resultado)
            print()
