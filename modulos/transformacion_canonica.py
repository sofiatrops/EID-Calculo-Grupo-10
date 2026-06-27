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


def _num_latex(valor: float, decimales: int = 4) -> str:
    """Redondea un numero solo para mostrarlo dentro de una formula LaTeX (no altera el valor real)."""
    redondeado = round(float(valor), decimales)
    if redondeado == 0:
        redondeado = 0.0  # evita mostrar "-0"
    if redondeado == int(redondeado):
        return str(int(redondeado))
    return f"{redondeado:.{decimales}f}".rstrip("0").rstrip(".")


def _resta_latex(variable: str, valor: float) -> str:
    """'(x - 5)' o, si valor es negativo, '(x + 5)' -- evita el doble signo '- -5'."""
    if valor < 0:
        return f"({variable} + {_num_latex(-valor)})"
    return f"({variable} - {_num_latex(valor)})"


def _termino_latex(valor: float, sufijo: str = "") -> str:
    """' + 3x' o ' - 3x' (con el signo correcto) para encadenar terminos sin doble signo."""
    if valor < 0:
        return f" - {_num_latex(-valor)}{sufijo}"
    return f" + {_num_latex(valor)}{sufijo}"


def _completar_cuadrado_variable(coef: float, lineal: float, nombre_var: str):
    """
    Completa el cuadrado de la expresión: coef*var² + lineal*var
    Retorna (h, correccion, pasos) tales que:
        coef*var² + lineal*var = coef*(var - h)² - correccion
    """
    h = -lineal / (2 * coef)
    correccion = coef * h * h
    pasos = [
        f"${_num_latex(coef)}{nombre_var}^2 + ({_num_latex(lineal)}){nombre_var} = "
        rf"{_num_latex(coef)}\left({nombre_var}^2 + \frac{{{_num_latex(lineal)}}}{{{_num_latex(coef)}}}{nombre_var}\right)$",
        f"$= {_num_latex(coef)}{_resta_latex(nombre_var, h)}^2{_termino_latex(-correccion)}$",
    ]
    return h, correccion, pasos


def _transformar_centro(A: float, B: float, C: float, D: float, E: float):
    """
    Completa el cuadrado en x e y para A x² + B y² + C x + D y + E = 0
    (válido cuando A != 0 y B != 0: circunferencia, elipse o hipérbola).
    Retorna (h, k, F, pasos) tales que A(x-h)² + B(y-k)² = F.
    """
    pasos = [
        f"Ecuación general: ${_num_latex(A)}x^2{_termino_latex(B, 'y^2')} + ({_num_latex(C)})x + "
        f"({_num_latex(D)})y{_termino_latex(E)} = 0$",
        "Paso 1: Agrupar los términos en x y en y por separado:",
        f"$({_num_latex(A)}x^2 + ({_num_latex(C)})x) + ({_num_latex(B)}y^2 + ({_num_latex(D)})y){_termino_latex(E)} = 0$",
    ]

    h, corr_x, pasos_x = _completar_cuadrado_variable(A, C, "x")
    k, corr_y, pasos_y = _completar_cuadrado_variable(B, D, "y")

    pasos.append("Paso 2: Completar el cuadrado en x:")
    pasos.extend(pasos_x)
    pasos.append("Paso 3: Completar el cuadrado en y:")
    pasos.extend(pasos_y)

    F = corr_x + corr_y - E
    pasos.append(
        f"Paso 4: Sustituir y agrupar constantes: "
        f"${_num_latex(A)}{_resta_latex('x', h)}^2{_termino_latex(B, _resta_latex('y', k) + '^2')}"
        f"{_termino_latex(-corr_x)}{_termino_latex(-corr_y)}{_termino_latex(E)} = 0$"
    )
    pasos.append(
        f"${_num_latex(A)}{_resta_latex('x', h)}^2{_termino_latex(B, _resta_latex('y', k) + '^2')} = "
        f"{_num_latex(corr_x)}{_termino_latex(corr_y)}{_termino_latex(-E)} = {_num_latex(F)}$"
    )

    return h, k, F, pasos


def _finalizar_circunferencia(A: float, h: float, k: float, F: float, pasos: list):
    if F == 0:
        pasos.append("F = 0 → la ecuación representa un único punto (caso degenerado), no una circunferencia real.")
        return {"tipo": "Circunferencia degenerada (punto)", "centro": (h, k), "pasos": pasos}

    r2 = F / A
    if r2 < 0:
        pasos.append(f"$F/A = {_num_latex(r2)} < 0$ → no existen puntos reales que satisfagan la ecuación.")
        return {"tipo": "Sin lugar geométrico real", "centro": (h, k), "pasos": pasos}

    r = raiz_cuadrada(r2)
    pasos.append(
        f"Paso 5: Dividir por $A = {_num_latex(A)}$: "
        f"${_resta_latex('x', h)}^2 + {_resta_latex('y', k)}^2 = {_num_latex(r2)}$"
    )
    pasos.append(
        f"Paso 6: $r = \\sqrt{{{_num_latex(r2)}}} = {_num_latex(r)}$ "
        f"(raíz calculada con Newton-Raphson, sin math.sqrt)"
    )

    return {
        "tipo": "Circunferencia",
        "centro": (h, k),
        "radio": r,
        "ecuacion_canonica": f"(x - {h})² + (y - {k})² = {r}²",
        "ecuacion_canonica_latex": (
            f"${_resta_latex('x', h)}^2 + {_resta_latex('y', k)}^2 = {_num_latex(r)}^2$"
        ),
        "pasos": pasos,
    }


def _finalizar_elipse_o_hiperbola(A: float, B: float, h: float, k: float, F: float, pasos: list):
    if F == 0:
        pasos.append("F = 0 → caso degenerado: el lugar geométrico se reduce a un punto o a un par de rectas.")
        return {"tipo": "Cónica degenerada", "centro": (h, k), "pasos": pasos}

    denom_x = F / A
    denom_y = F / B
    pasos.append(
        f"Paso 5: Dividir ambos lados por $F = {_num_latex(F)}$: "
        rf"$\frac{{{_resta_latex('x', h)}^2}}{{{_num_latex(denom_x)}}} + "
        rf"\frac{{{_resta_latex('y', k)}^2}}{{{_num_latex(denom_y)}}} = 1$"
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

    pasos.append(
        f"Paso 6: $a = \\sqrt{{{_num_latex(a2)}}} = {_num_latex(a)}$, "
        f"$b = \\sqrt{{{_num_latex(b2)}}} = {_num_latex(b)}$, "
        f"$c = \\sqrt{{a^2 - b^2}} = \\sqrt{{{_num_latex(a2 - b2)}}} = {_num_latex(c)}$"
    )
    pasos.append(f"Eje mayor: ${eje_mayor}$")

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
        "ecuacion_canonica_latex": (
            rf"$\frac{{{_resta_latex('x', h)}^2}}{{{_num_latex(a2)}}} + "
            rf"\frac{{{_resta_latex('y', k)}^2}}{{{_num_latex(b2)}}} = 1$"
            if eje_mayor == "x" else
            rf"$\frac{{{_resta_latex('x', h)}^2}}{{{_num_latex(b2)}}} + "
            rf"\frac{{{_resta_latex('y', k)}^2}}{{{_num_latex(a2)}}} = 1$"
        ),
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

    pasos.append(
        f"Paso 6: $a = \\sqrt{{{_num_latex(a2)}}} = {_num_latex(a)}$, "
        f"$b = \\sqrt{{{_num_latex(b2)}}} = {_num_latex(b)}$, "
        f"$c = \\sqrt{{a^2 + b^2}} = \\sqrt{{{_num_latex(a2 + b2)}}} = {_num_latex(c)}$"
    )
    pasos.append(f"Eje transverso: ${eje_transverso}$")

    if eje_transverso == "x":
        vertices = [(h - a, k), (h + a, k)]
        focos = [(h - c, k), (h + c, k)]
        ecuacion_canonica = f"(x - {h})²/{a2} - (y - {k})²/{b2} = 1"
        ecuacion_canonica_latex = (
            rf"$\frac{{{_resta_latex('x', h)}^2}}{{{_num_latex(a2)}}} - "
            rf"\frac{{{_resta_latex('y', k)}^2}}{{{_num_latex(b2)}}} = 1$"
        )
        pendiente = b / a
        pendiente_simbolo = "b/a"
    else:
        vertices = [(h, k - a), (h, k + a)]
        focos = [(h, k - c), (h, k + c)]
        ecuacion_canonica = f"(y - {k})²/{a2} - (x - {h})²/{b2} = 1"
        ecuacion_canonica_latex = (
            rf"$\frac{{{_resta_latex('y', k)}^2}}{{{_num_latex(a2)}}} - "
            rf"\frac{{{_resta_latex('x', h)}^2}}{{{_num_latex(b2)}}} = 1$"
        )
        pendiente = a / b
        pendiente_simbolo = "a/b"

    intercepto_1 = k - pendiente * h
    intercepto_2 = k + pendiente * h
    pasos.append(
        f"Paso 7: Asíntotas. Pendiente $m = {pendiente_simbolo} = {_num_latex(pendiente)}$. "
        f"Rectas que pasan por el centro: "
        f"$y = {_num_latex(pendiente)}x{_termino_latex(intercepto_1)}$ y "
        f"$y = {_num_latex(-pendiente)}x{_termino_latex(intercepto_2)}$"
    )
    asintotas = [
        f"y = {_num_latex(pendiente)}x{_termino_latex(intercepto_1)}",
        f"y = {_num_latex(-pendiente)}x{_termino_latex(intercepto_2)}",
    ]

    return {
        "tipo": "Hipérbola",
        "centro": (h, k),
        "semieje_transverso": a,
        "semieje_conjugado": b,
        "c": c,
        "eje_transverso": eje_transverso,
        "vertices": vertices,
        "focos": focos,
        "asintotas": asintotas,
        "asintotas_valores": [pendiente, intercepto_1, -pendiente, intercepto_2],
        "ecuacion_canonica": ecuacion_canonica,
        "ecuacion_canonica_latex": ecuacion_canonica_latex,
        "pasos": pasos,
    }


def _transformar_parabola(A: float, B: float, C: float, D: float, E: float):
    pasos = [
        f"Ecuación general: ${_num_latex(A)}x^2{_termino_latex(B, 'y^2')} + ({_num_latex(C)})x + "
        f"({_num_latex(D)})y{_termino_latex(E)} = 0$"
    ]

    if B == 0:
        return _parabola_vertical(A, C, D, E, pasos)
    else:
        return _parabola_horizontal(B, C, D, E, pasos)


def _parabola_vertical(A: float, C: float, D: float, E: float, pasos: list):
    pasos.append("B = 0 → parábola de eje vertical. Se completa el cuadrado en x.")
    h, corr_x, pasos_x = _completar_cuadrado_variable(A, C, "x")
    pasos.extend(pasos_x)
    pasos.append(
        f"Sustituyendo: ${_num_latex(A)}{_resta_latex('x', h)}^2{_termino_latex(-corr_x)} + "
        f"({_num_latex(D)})y{_termino_latex(E)} = 0$"
    )

    if D == 0:
        pasos.append("D = 0 → no hay término lineal en y; la ecuación no define una parábola estándar (caso degenerado).")
        return {"tipo": "Parábola degenerada", "vertice": (h, None), "pasos": pasos}

    k = (corr_x - E) / D
    pasos.append(
        f"${_num_latex(D)}y = {_num_latex(-A)}{_resta_latex('x', h)}^2{_termino_latex(corr_x)}{_termino_latex(-E)}$"
    )
    pasos.append(
        f"$y - ({_num_latex(k)}) = \\frac{{{_num_latex(-A)}}}{{{_num_latex(D)}}}{_resta_latex('x', h)}^2$"
    )

    p = -D / (4 * A)
    pasos.append(
        f"Forma estándar $(x-h)^2 = 4p(y-k)$: "
        rf"$4p = \frac{{{_num_latex(-D)}}}{{{_num_latex(A)}}} \to p = {_num_latex(p)}$"
    )

    foco = (h, k + p)
    directriz = k - p
    apertura = "hacia arriba" if p > 0 else "hacia abajo"
    pasos.append(
        f"$p = {_num_latex(p)}$ ({apertura}). Vértice $= ({_num_latex(h)}, {_num_latex(k)})$. "
        f"Foco $= ({_num_latex(foco[0])}, {_num_latex(foco[1])})$. Directriz: $y = {_num_latex(directriz)}$"
    )

    return {
        "tipo": "Parábola (eje vertical)",
        "vertice": (h, k),
        "foco": foco,
        "directriz": f"y = {directriz}",
        "directriz_valor": directriz,
        "directriz_eje": "horizontal",
        "p": p,
        "ecuacion_canonica": f"(x - {h})² = {4 * p}(y - {k})",
        "ecuacion_canonica_latex": (
            f"${_resta_latex('x', h)}^2 = {_num_latex(4 * p)}{_resta_latex('y', k)}$"
        ),
        "pasos": pasos,
    }


def _parabola_horizontal(B: float, C: float, D: float, E: float, pasos: list):
    pasos.append("A = 0 → parábola de eje horizontal. Se completa el cuadrado en y.")
    k, corr_y, pasos_y = _completar_cuadrado_variable(B, D, "y")
    pasos.extend(pasos_y)
    pasos.append(
        f"Sustituyendo: ${_num_latex(B)}{_resta_latex('y', k)}^2{_termino_latex(-corr_y)} + "
        f"({_num_latex(C)})x{_termino_latex(E)} = 0$"
    )

    if C == 0:
        pasos.append("C = 0 → no hay término lineal en x; la ecuación no define una parábola estándar (caso degenerado).")
        return {"tipo": "Parábola degenerada", "vertice": (None, k), "pasos": pasos}

    h = (corr_y - E) / C
    pasos.append(
        f"${_num_latex(C)}x = {_num_latex(-B)}{_resta_latex('y', k)}^2{_termino_latex(corr_y)}{_termino_latex(-E)}$"
    )
    pasos.append(
        f"$x - ({_num_latex(h)}) = \\frac{{{_num_latex(-B)}}}{{{_num_latex(C)}}}{_resta_latex('y', k)}^2$"
    )

    p = -C / (4 * B)
    pasos.append(
        f"Forma estándar $(y-k)^2 = 4p(x-h)$: "
        rf"$4p = \frac{{{_num_latex(-C)}}}{{{_num_latex(B)}}} \to p = {_num_latex(p)}$"
    )

    foco = (h + p, k)
    directriz = h - p
    apertura = "hacia la derecha" if p > 0 else "hacia la izquierda"
    pasos.append(
        f"$p = {_num_latex(p)}$ ({apertura}). Vértice $= ({_num_latex(h)}, {_num_latex(k)})$. "
        f"Foco $= ({_num_latex(foco[0])}, {_num_latex(foco[1])})$. Directriz: $x = {_num_latex(directriz)}$"
    )

    return {
        "tipo": "Parábola (eje horizontal)",
        "vertice": (h, k),
        "foco": foco,
        "directriz": f"x = {directriz}",
        "directriz_valor": directriz,
        "directriz_eje": "vertical",
        "p": p,
        "ecuacion_canonica": f"(y - {k})² = {4 * p}(x - {h})",
        "ecuacion_canonica_latex": (
            f"${_resta_latex('y', k)}^2 = {_num_latex(4 * p)}{_resta_latex('x', h)}$"
        ),
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
        pasos.append(
            f"Partimos de la forma canónica: ${_resta_latex('x', h)}^2 + {_resta_latex('y', k)}^2 = {_num_latex(r)}^2$"
        )
        pasos.append(
            f"Expandimos los cuadrados de binomio: "
            f"$x^2{_termino_latex(-2*h, 'x')} + {_num_latex(h*h)} + y^2{_termino_latex(-2*k, 'y')} + "
            f"{_num_latex(k*k)} = {_num_latex(r*r)}$"
        )
        pasos.append(
            f"Reagrupamos todos los términos al lado izquierdo: "
            f"$x^2 + y^2 + ({_num_latex(-2*h)})x + ({_num_latex(-2*k)})y + "
            f"({_num_latex(h*h + k*k - r*r)}) = 0$"
        )
        pasos.append("Esta es la ecuación general equivalente (A = B = 1 tras normalizar).")

    elif tipo in ("Elipse", "Hipérbola"):
        h, k = resultado["centro"]
        signo = "+" if tipo == "Elipse" else "-"
        eje = resultado.get("eje_mayor") or resultado.get("eje_transverso")
        a2 = resultado.get("semieje_mayor", resultado.get("semieje_transverso")) ** 2
        b2 = resultado.get("semieje_menor", resultado.get("semieje_conjugado")) ** 2
        if eje == "x":
            pasos.append(
                rf"Partimos de: $\frac{{{_resta_latex('x', h)}^2}}{{{_num_latex(a2)}}} {signo} "
                rf"\frac{{{_resta_latex('y', k)}^2}}{{{_num_latex(b2)}}} = 1$"
            )
            pasos.append(
                f"Multiplicamos por ${_num_latex(a2)} \\cdot {_num_latex(b2)}$: "
                f"${_num_latex(b2)}{_resta_latex('x', h)}^2 {signo} {_num_latex(a2)}{_resta_latex('y', k)}^2 = {_num_latex(a2*b2)}$"
            )
        else:
            pasos.append(
                rf"Partimos de: $\frac{{{_resta_latex('y', k)}^2}}{{{_num_latex(a2)}}} {signo} "
                rf"\frac{{{_resta_latex('x', h)}^2}}{{{_num_latex(b2)}}} = 1$"
            )
            pasos.append(
                f"Multiplicamos por ${_num_latex(a2)} \\cdot {_num_latex(b2)}$: "
                f"${_num_latex(b2)}{_resta_latex('y', k)}^2 {signo} {_num_latex(a2)}{_resta_latex('x', h)}^2 = {_num_latex(a2*b2)}$"
            )
        pasos.append(
            "Se expanden los binomios al cuadrado y se reagrupan los términos para llegar "
            "a la forma $Ax^2 + By^2 + Cx + Dy + E = 0$."
        )

    elif tipo.startswith("Parábola") and "degenerada" not in tipo:
        h, k = resultado["vertice"]
        p = resultado["p"]
        if "vertical" in tipo:
            pasos.append(f"Partimos de: ${_resta_latex('x', h)}^2 = {_num_latex(4*p)}{_resta_latex('y', k)}$")
            pasos.append(
                f"Expandimos: $x^2{_termino_latex(-2*h, 'x')} + {_num_latex(h*h)} = "
                f"{_num_latex(4*p)}y{_termino_latex(-4*p*k)}$"
            )
            pasos.append(
                f"Reagrupamos: $x^2 + ({_num_latex(-2*h)})x + ({_num_latex(-4*p)})y + "
                f"({_num_latex(h*h + 4*p*k)}) = 0$"
            )
        else:
            pasos.append(f"Partimos de: ${_resta_latex('y', k)}^2 = {_num_latex(4*p)}{_resta_latex('x', h)}$")
            pasos.append(
                f"Expandimos: $y^2{_termino_latex(-2*k, 'y')} + {_num_latex(k*k)} = "
                f"{_num_latex(4*p)}x{_termino_latex(-4*p*h)}$"
            )
            pasos.append(
                f"Reagrupamos: $y^2 + ({_num_latex(-2*k)})y + ({_num_latex(-4*p)})x + "
                f"({_num_latex(k*k + 4*p*h)}) = 0$"
            )
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


def _formatear_valor_geometrico(valor) -> str:
    """Formatea para pantalla un elemento geometrico: numero, punto (tupla) o lista de puntos."""
    if isinstance(valor, str):
        return valor
    if isinstance(valor, (int, float)):
        return _num_latex(valor)
    if isinstance(valor, tuple) and len(valor) == 2:
        return f"({_num_latex(valor[0])}, {_num_latex(valor[1])})"
    if isinstance(valor, list):
        return ", ".join(_formatear_valor_geometrico(v) for v in valor)
    return str(valor)


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
        lineas.append(
            f"\nEcuación canónica: {resultado.get('ecuacion_canonica_latex', resultado['ecuacion_canonica'])}"
        )

    if resultado.get("pasos_inversos"):
        lineas.append("\nProcedimiento inverso (canónica → general):")
        for paso in resultado["pasos_inversos"]:
            lineas.append(f"  {paso}")

    lineas.append("\nElementos geométricos:")
    for clave in ("centro", "vertice", "vertices", "co_vertices", "focos", "foco",
                  "radio", "semieje_mayor", "semieje_menor",
                  "semieje_transverso", "semieje_conjugado", "asintotas", "directriz"):
        if clave in resultado:
            lineas.append(f"  {clave}: {_formatear_valor_geometrico(resultado[clave])}")

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
