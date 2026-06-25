def raiz_cuadrada(x: float, iteraciones: int = 25) -> float:
    """
    Calcula la raíz cuadrada de x mediante el método de Newton-Raphson,
    sin usar math.sqrt ni librerías externas.
    """
    if x < 0:
        raise ValueError(f"No existe raíz cuadrada real de un número negativo: {x}")
    if x == 0:
        return 0.0

    estimado = x
    for _ in range(iteraciones):
        estimado = 0.5 * (estimado + x / estimado)
    return estimado


def _completar_cuadrado_variable(coef: float, lineal: float, nombre_var: str):
    """
    Completa el cuadrado de la expresión: coef*var² + lineal*var
    Retorna (h, correccion, pasos) tales que:
        coef*var² + lineal*var = coef*(var - h)² - correccion
    """
    h = -lineal / (2 * coef)
    correccion = coef * h * h
    pasos = [
        f"{coef}{nombre_var}² + ({lineal}){nombre_var} = {coef}({nombre_var}² + ({lineal}/{coef}){nombre_var})",
        f"= {coef}({nombre_var} - ({h}))² - {coef}·({h})²",
        f"= {coef}({nombre_var} - {h})² - {correccion}",
    ]
    return h, correccion, pasos


def _transformar_centro(A: float, B: float, C: float, D: float, E: float):
    """
    Completa el cuadrado en x e y para A x² + B y² + C x + D y + E = 0
    (válido cuando A != 0 y B != 0: circunferencia, elipse o hipérbola).
    Retorna (h, k, F, pasos) tales que A(x-h)² + B(y-k)² = F.
    """
    pasos = [
        f"Ecuación general: {A}x² + {B}y² + ({C})x + ({D})y + {E} = 0",
        "Paso 1: Agrupar los términos en x y en y por separado.",
        f"  ({A}x² + ({C})x) + ({B}y² + ({D})y) + {E} = 0",
    ]

    h, corr_x, pasos_x = _completar_cuadrado_variable(A, C, "x")
    k, corr_y, pasos_y = _completar_cuadrado_variable(B, D, "y")

    pasos.append("Paso 2: Completar el cuadrado en x:")
    pasos.extend(f"  {p}" for p in pasos_x)
    pasos.append("Paso 3: Completar el cuadrado en y:")
    pasos.extend(f"  {p}" for p in pasos_y)

    F = corr_x + corr_y - E
    pasos.append(
        f"Paso 4: Sustituir y agrupar constantes:\n"
        f"  {A}(x - {h})² + {B}(y - {k})² - {corr_x} - {corr_y} + {E} = 0\n"
        f"  {A}(x - {h})² + {B}(y - {k})² = {corr_x} + {corr_y} - {E} = {F}"
    )

    return h, k, F, pasos


def _finalizar_circunferencia(A: float, h: float, k: float, F: float, pasos: list):
    if F == 0:
        pasos.append("F = 0 → la ecuación representa un único punto (caso degenerado), no una circunferencia real.")
        return {"tipo": "Circunferencia degenerada (punto)", "centro": (h, k), "pasos": pasos}

    r2 = F / A
    if r2 < 0:
        pasos.append(f"F/A = {r2} < 0 → no existen puntos reales que satisfagan la ecuación.")
        return {"tipo": "Sin lugar geométrico real", "centro": (h, k), "pasos": pasos}

    r = raiz_cuadrada(r2)
    pasos.append(f"Paso 5: Dividir por A = {A}: (x - {h})² + (y - {k})² = {r2}")
    pasos.append(f"Paso 6: r = √{r2} = {r}  (raíz calculada con Newton-Raphson, sin math.sqrt)")

    return {
        "tipo": "Circunferencia",
        "centro": (h, k),
        "radio": r,
        "ecuacion_canonica": f"(x - {h})² + (y - {k})² = {r}²",
        "pasos": pasos,
    }


def _finalizar_elipse_o_hiperbola(A: float, B: float, h: float, k: float, F: float, pasos: list):
    if F == 0:
        pasos.append("F = 0 → caso degenerado: el lugar geométrico se reduce a un punto o a un par de rectas.")
        return {"tipo": "Cónica degenerada", "centro": (h, k), "pasos": pasos}

    denom_x = F / A
    denom_y = F / B
    pasos.append(
        f"Paso 5: Dividir ambos lados por F = {F}:\n"
        f"  (x - {h})²/{denom_x} + (y - {k})²/{denom_y} = 1"
    )

    if denom_x > 0 and denom_y > 0:
        return _finalizar_elipse(h, k, denom_x, denom_y, pasos)
    elif denom_x * denom_y < 0:
        return _finalizar_hiperbola(h, k, denom_x, denom_y, pasos)
    else:
        pasos.append("Uno de los denominadores es cero → caso degenerado (par de rectas).")
        return {"tipo": "Cónica degenerada", "centro": (h, k), "pasos": pasos}


def _finalizar_elipse(h: float, k: float, denom_x: float, denom_y: float, pasos: list):
    if denom_x >= denom_y:
        a2, b2, eje_mayor = denom_x, denom_y, "x"
    else:
        a2, b2, eje_mayor = denom_y, denom_x, "y"

    a = raiz_cuadrada(a2)
    b = raiz_cuadrada(b2)
    c = raiz_cuadrada(a2 - b2) if a2 != b2 else 0.0

    pasos.append(f"Paso 6: a = √{a2} = {a},  b = √{b2} = {b},  c = √(a² - b²) = √{a2 - b2} = {c}")
    pasos.append(f"Eje mayor: {eje_mayor}")

    if eje_mayor == "x":
        vertices = [(h - a, k), (h + a, k)]
        co_vertices = [(h, k - b), (h, k + b)]
        focos = [(h - c, k), (h + c, k)]
    else:
        vertices = [(h, k - a), (h, k + a)]
        co_vertices = [(h - b, k), (h + b, k)]
        focos = [(h, k - c), (h, k + c)]

    return {
        "tipo": "Elipse",
        "centro": (h, k),
        "semieje_mayor": a,
        "semieje_menor": b,
        "c": c,
        "eje_mayor": eje_mayor,
        "vertices": vertices,
        "co_vertices": co_vertices,
        "focos": focos,
        "ecuacion_canonica": f"(x - {h})²/{a2} + (y - {k})²/{b2} = 1" if eje_mayor == "x"
                              else f"(x - {h})²/{b2} + (y - {k})²/{a2} = 1",
        "pasos": pasos,
    }


def _finalizar_hiperbola(h: float, k: float, denom_x: float, denom_y: float, pasos: list):
    if denom_x > 0:
        a2, b2, eje_transverso = denom_x, -denom_y, "x"
    else:
        a2, b2, eje_transverso = denom_y, -denom_x, "y"

    a = raiz_cuadrada(a2)
    b = raiz_cuadrada(b2)
    c = raiz_cuadrada(a2 + b2)

    pasos.append(f"Paso 6: a = √{a2} = {a},  b = √{b2} = {b},  c = √(a² + b²) = √{a2 + b2} = {c}")
    pasos.append(f"Eje transverso: {eje_transverso}")

    if eje_transverso == "x":
        vertices = [(h - a, k), (h + a, k)]
        focos = [(h - c, k), (h + c, k)]
        ecuacion_canonica = f"(x - {h})²/{a2} - (y - {k})²/{b2} = 1"
    else:
        vertices = [(h, k - a), (h, k + a)]
        focos = [(h, k - c), (h, k + c)]
        ecuacion_canonica = f"(y - {k})²/{a2} - (x - {h})²/{b2} = 1"

    return {
        "tipo": "Hipérbola",
        "centro": (h, k),
        "semieje_transverso": a,
        "semieje_conjugado": b,
        "c": c,
        "eje_transverso": eje_transverso,
        "vertices": vertices,
        "focos": focos,
        "ecuacion_canonica": ecuacion_canonica,
        "pasos": pasos,
    }


def _transformar_parabola(A: float, B: float, C: float, D: float, E: float):
    pasos = [f"Ecuación general: {A}x² + {B}y² + ({C})x + ({D})y + {E} = 0"]

    if B == 0:
        return _parabola_vertical(A, C, D, E, pasos)
    else:
        return _parabola_horizontal(B, C, D, E, pasos)


def _parabola_vertical(A: float, C: float, D: float, E: float, pasos: list):
    pasos.append("B = 0 → parábola de eje vertical. Se completa el cuadrado en x.")
    h, corr_x, pasos_x = _completar_cuadrado_variable(A, C, "x")
    pasos.extend(f"  {p}" for p in pasos_x)
    pasos.append(f"Sustituyendo: {A}(x - {h})² - {corr_x} + ({D})y + {E} = 0")

    if D == 0:
        pasos.append("D = 0 → no hay término lineal en y; la ecuación no define una parábola estándar (caso degenerado).")
        return {"tipo": "Parábola degenerada", "vertice": (h, None), "pasos": pasos}

    k = (corr_x - E) / D
    pasos.append(f"({D})y = -{A}(x - {h})² + {corr_x} - {E}")
    pasos.append(f"y - ({k}) = ({-A}/{D})(x - {h})²")

    p = -D / (4 * A)
    pasos.append(f"Forma estándar (x - h)² = 4p(y - k):  4p = {-D}/{A} → p = {p}")

    foco = (h, k + p)
    directriz = k - p
    apertura = "hacia arriba" if p > 0 else "hacia abajo"
    pasos.append(f"p = {p} ({apertura}). Vértice = ({h}, {k}). Foco = {foco}. Directriz: y = {directriz}")

    return {
        "tipo": "Parábola (eje vertical)",
        "vertice": (h, k),
        "foco": foco,
        "directriz": f"y = {directriz}",
        "p": p,
        "ecuacion_canonica": f"(x - {h})² = {4 * p}(y - {k})",
        "pasos": pasos,
    }


def _parabola_horizontal(B: float, C: float, D: float, E: float, pasos: list):
    pasos.append("A = 0 → parábola de eje horizontal. Se completa el cuadrado en y.")
    k, corr_y, pasos_y = _completar_cuadrado_variable(B, D, "y")
    pasos.extend(f"  {p}" for p in pasos_y)
    pasos.append(f"Sustituyendo: {B}(y - {k})² - {corr_y} + ({C})x + {E} = 0")

    if C == 0:
        pasos.append("C = 0 → no hay término lineal en x; la ecuación no define una parábola estándar (caso degenerado).")
        return {"tipo": "Parábola degenerada", "vertice": (None, k), "pasos": pasos}

    h = (corr_y - E) / C
    pasos.append(f"({C})x = -{B}(y - {k})² + {corr_y} - {E}")
    pasos.append(f"x - ({h}) = ({-B}/{C})(y - {k})²")

    p = -C / (4 * B)
    pasos.append(f"Forma estándar (y - k)² = 4p(x - h):  4p = {-C}/{B} → p = {p}")

    foco = (h + p, k)
    directriz = h - p
    apertura = "hacia la derecha" if p > 0 else "hacia la izquierda"
    pasos.append(f"p = {p} ({apertura}). Vértice = ({h}, {k}). Foco = {foco}. Directriz: x = {directriz}")

    return {
        "tipo": "Parábola (eje horizontal)",
        "vertice": (h, k),
        "foco": foco,
        "directriz": f"x = {directriz}",
        "p": p,
        "ecuacion_canonica": f"(y - {k})² = {4 * p}(x - {h})",
        "pasos": pasos,
    }


def expandir_forma_canonica(resultado: dict) -> list:
    """
    Procedimiento inverso: expande la forma canónica y reagrupa los términos
    para reobtener la ecuación general, mostrando cada paso algebraico.
    """
    tipo = resultado["tipo"]
    pasos = []

    if tipo == "Circunferencia":
        h, k = resultado["centro"]
        r = resultado["radio"]
        pasos.append(f"Partimos de la forma canónica: (x - {h})² + (y - {k})² = {r}²")
        pasos.append(f"Expandimos los cuadrados de binomio:")
        pasos.append(f"  x² - {2*h}x + {h*h} + y² - {2*k}y + {k*k} = {r*r}")
        pasos.append("Reagrupamos todos los términos al lado izquierdo:")
        pasos.append(
            f"  x² + y² + ({-2*h})x + ({-2*k})y + ({h*h + k*k - r*r}) = 0"
        )
        pasos.append("Esta es la ecuación general equivalente (A = B = 1 tras normalizar).")

    elif tipo in ("Elipse", "Hipérbola"):
        h, k = resultado["centro"]
        signo = "+" if tipo == "Elipse" else "-"
        eje = resultado.get("eje_mayor") or resultado.get("eje_transverso")
        if eje == "x":
            a2 = resultado.get("semieje_mayor", resultado.get("semieje_transverso")) ** 2
            b2 = resultado.get("semieje_menor", resultado.get("semieje_conjugado")) ** 2
            pasos.append(f"Partimos de: (x - {h})²/{a2} {signo} (y - {k})²/{b2} = 1")
            pasos.append(f"Multiplicamos por {a2}·{b2}: {b2}(x - {h})² {signo} {a2}(y - {k})² = {a2*b2}")
        else:
            a2 = resultado.get("semieje_mayor", resultado.get("semieje_transverso")) ** 2
            b2 = resultado.get("semieje_menor", resultado.get("semieje_conjugado")) ** 2
            pasos.append(f"Partimos de: (y - {k})²/{a2} {signo} (x - {h})²/{b2} = 1")
            pasos.append(f"Multiplicamos por {a2}·{b2}: {b2}(y - {k})² {signo} {a2}(x - {h})² = {a2*b2}")
        pasos.append("Se expanden los binomios al cuadrado y se reagrupan los términos para llegar a la forma Ax² + By² + Cx + Dy + E = 0.")

    elif tipo.startswith("Parábola") and "degenerada" not in tipo:
        h, k = resultado["vertice"]
        p = resultado["p"]
        if "vertical" in tipo:
            pasos.append(f"Partimos de: (x - {h})² = {4*p}(y - {k})")
            pasos.append(f"Expandimos: x² - {2*h}x + {h*h} = {4*p}y - {4*p*k}")
            pasos.append(f"Reagrupamos: x² + ({-2*h})x + ({-4*p})y + ({h*h + 4*p*k}) = 0")
        else:
            pasos.append(f"Partimos de: (y - {k})² = {4*p}(x - {h})")
            pasos.append(f"Expandimos: y² - {2*k}y + {k*k} = {4*p}x - {4*p*h}")
            pasos.append(f"Reagrupamos: y² + ({-2*k})y + ({-4*p})x + ({k*k + 4*p*h}) = 0")
        pasos.append("Esta es la ecuación general equivalente.")

    return pasos


def transformar_a_canonica(coeficientes: dict) -> dict:
    """
    Transforma la ecuación general Ax² + By² + Cx + Dy + E = 0 a su forma
    canónica, completando el cuadrado paso a paso. Identifica centro/vértice,
    focos, vértices y semiejes según el tipo de cónica.
    """
    A, B, C, D, E = (
        coeficientes["A"], coeficientes["B"],
        coeficientes["C"], coeficientes["D"], coeficientes["E"],
    )

    if A == 0 and B == 0:
        raise ValueError("A = 0 y B = 0: no es una cónica, no se puede transformar a forma canónica.")

    if A == 0 or B == 0:
        resultado = _transformar_parabola(A, B, C, D, E)
    else:
        h, k, F, pasos = _transformar_centro(A, B, C, D, E)
        if A == B:
            resultado = _finalizar_circunferencia(A, h, k, F, pasos)
        else:
            resultado = _finalizar_elipse_o_hiperbola(A, B, h, k, F, pasos)

    resultado["pasos_inversos"] = expandir_forma_canonica(resultado)
    return resultado


def formatear_transformacion(resultado: dict) -> str:
    """Devuelve un string con el procedimiento completo, listo para mostrar en pantalla."""
    lineas = []
    lineas.append("=" * 55)
    lineas.append("  TRANSFORMACIÓN A FORMA CANÓNICA")
    lineas.append("=" * 55)
    lineas.append(f"\nTipo de cónica: {resultado['tipo']}\n")

    lineas.append("Procedimiento — completar el cuadrado:")
    for paso in resultado["pasos"]:
        lineas.append(f"  {paso}")

    if "ecuacion_canonica" in resultado:
        lineas.append(f"\nEcuación canónica: {resultado['ecuacion_canonica']}")

    if resultado.get("pasos_inversos"):
        lineas.append("\nProcedimiento inverso (canónica → general):")
        for paso in resultado["pasos_inversos"]:
            lineas.append(f"  {paso}")

    lineas.append("\nElementos geométricos:")
    for clave in ("centro", "vertice", "vertices", "co_vertices", "focos", "foco",
                  "radio", "semieje_mayor", "semieje_menor",
                  "semieje_transverso", "semieje_conjugado", "directriz"):
        if clave in resultado:
            lineas.append(f"  {clave}: {resultado[clave]}")

    lineas.append("=" * 55)
    return "\n".join(lineas)


if __name__ == "__main__":
    casos = [
        {"A": 1.0, "B": 1.0, "C": -4.0, "D": 6.0, "E": 4.0},       # circunferencia
        {"A": 1.0, "B": 4.0, "C": -2.0, "D": 16.0, "E": 13.0},     # elipse
        {"A": 1.0, "B": -4.0, "C": -2.0, "D": -16.0, "E": -19.0},  # hipérbola
        {"A": 1.0, "B": 0.0, "C": -2.0, "D": -8.0, "E": 9.0},      # parábola vertical
        {"A": 0.0, "B": 1.0, "C": -8.0, "D": -2.0, "E": 9.0},      # parábola horizontal
    ]
    for c in casos:
        r = transformar_a_canonica(c)
        print(formatear_transformacion(r))
        print()
