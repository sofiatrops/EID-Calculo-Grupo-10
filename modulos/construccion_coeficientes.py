def calcular_variable_v(dv: str) -> tuple[int, str]:
    if dv == "K":
        return 10, "DV = K  →  v = 10"
    elif dv == "0":
        return 11, "DV = 0  →  v = 11"
    else:
        v = int(dv)
        return v, f"DV = {dv}  →  v = {dv}"


def division_exacta(numerador: int, denominador: int) -> tuple[float, str]:
    if denominador == 0:
        raise ZeroDivisionError("El denominador v no puede ser cero.")

    # MCD con algoritmo de Euclides (sin math.gcd)
    a, b = abs(numerador), abs(denominador)
    while b:
        a, b = b, a % b
    mcd = a

    num_reducido = numerador // mcd
    den_reducido = denominador // mcd

    if den_reducido == 1:
        representacion = str(num_reducido)
    else:
        representacion = f"{num_reducido}/{den_reducido}"

    return numerador / denominador, representacion


def construir_coeficientes(digitos: list[int], dv: str) -> dict:
    if len(digitos) != 8:
        raise ValueError(f"Se esperaban 8 dígitos, se recibieron {len(digitos)}.")

    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    pasos = []
    ajustes = []

    #calculamos la variable v
    v, desc_v = calcular_variable_v(dv)
    pasos.append(f"Paso 1 — Variable auxiliar v:\n  {desc_v}")

    #calculamos los coeficientes base
    A_val, A_frac = division_exacta(d1 + d2, v)
    B_val, B_frac = division_exacta(d3 + d4, v)
    C_val = -(d5 + d6)
    D_val = -(d7 + d8)
    E_val = d1 + d3 + d5 + d7

    pasos.append(
        f"Paso 2 — Coeficientes base:\n"
        f"  A = (d1 + d2) / v = ({d1} + {d2}) / {v} = {d1+d2}/{v} = {A_frac}\n"
        f"  B = (d3 + d4) / v = ({d3} + {d4}) / {v} = {d3+d4}/{v} = {B_frac}\n"
        f"  C = -(d5 + d6)    = -({d5} + {d6}) = {C_val}\n"
        f"  D = -(d7 + d8)    = -({d7} + {d8}) = {D_val}\n"
        f"  E = d1+d3+d5+d7   = {d1}+{d3}+{d5}+{d7} = {E_val}"
    )

   #calculamos los ajustes

    pasos.append("Paso 3 — Aplicación de ajustes:")

    #hipérbola
    if d8 % 2 != 0:
        B_val = -B_val
        B_frac = f"-({B_frac})" if "/" in B_frac else f"-{B_frac}"
        ajuste = f"  • d8 = {d8} es IMPAR → B se reemplaza por -B = {B_frac}"
        ajustes.append("d8 impar → B = -B (posible hipérbola)")
        pasos.append(ajuste)
    else:
        pasos.append(f"  • d8 = {d8} es PAR → no se aplica la regla de hipérbola")

    #circunferencia
    if d1 == d2:
        B_val = A_val
        B_frac = A_frac
        ajuste = f"  • d1 = d2 = {d1} → se impone B = A = {A_frac} (posible circunferencia)"
        ajustes.append("d1 = d2 → B = A (posible circunferencia)")
        pasos.append(ajuste)
    else:
        pasos.append(f"  • d1 ({d1}) ≠ d2 ({d2}) → no se aplica la regla de circunferencia")

    # parabola
    suma_d5_d6 = d5 + d6
    if suma_d5_d6 % 3 == 0:
        if d7 % 2 == 0:
            B_val = 0.0
            B_frac = "0"
            ajuste = (
                f"  • d5+d6 = {suma_d5_d6} es múltiplo de 3 Y d7 = {d7} es PAR\n"
                f"    → B = 0 (parábola de eje vertical)"
            )
            ajustes.append("(d5+d6) % 3 == 0 y d7 par → B = 0 (parábola vertical)")
        else:
            A_val = 0.0
            A_frac = "0"
            ajuste = (
                f"  • d5+d6 = {suma_d5_d6} es múltiplo de 3 Y d7 = {d7} es IMPAR\n"
                f"    → A = 0 (parábola de eje horizontal)"
            )
            ajustes.append("(d5+d6) % 3 == 0 y d7 impar → A = 0 (parábola horizontal)")
        pasos.append(ajuste)
    else:
        pasos.append(
            f"  • d5+d6 = {suma_d5_d6}, residuo al dividir por 3 = {suma_d5_d6 % 3} "
            f"→ no se aplica la regla de parábola"
        )

    # clasificacion de la conica
    tipo = _clasificar_conica(A_val, B_val)
    pasos.append(
        f"Paso 4 — Clasificación de la cónica:\n"
        f"  A = {A_frac}, B = {B_frac}\n"
        f"  → {tipo}"
    )

    #ecuacion final
    ecuacion = _formatear_ecuacion(A_frac, B_frac, C_val, D_val, E_val)
    pasos.append(f"Ecuación general obtenida:\n  {ecuacion} = 0")

    return {
        "A": A_val,
        "B": B_val,
        "C": C_val,
        "D": D_val,
        "E": E_val,
        "A_frac": A_frac,
        "B_frac": B_frac,
        "v": v,
        "ajustes_aplicados": ajustes,
        "tipo_conica": tipo,
        "ecuacion": ecuacion + " = 0",
        "pasos": pasos,
        "digitos": digitos,
        "dv": dv,
    }


def _clasificar_conica(A: float, B: float) -> str:
    """Clasifica la cónica según los coeficientes A y B."""
    if A == 0 and B == 0:
        return "Caso degenerado (A = 0 y B = 0): no es una cónica estándar."
    if A == 0 or B == 0:
        return "Parábola (exactamente uno de A o B es cero)"
    if A == B:
        return "Circunferencia (A = B ≠ 0)"
    if (A > 0 and B > 0) or (A < 0 and B < 0):
        return "Elipse (A y B tienen el mismo signo y A ≠ B)"
    return "Hipérbola (A y B tienen signos opuestos)"


def _formatear_ecuacion(A_frac: str, B_frac: str, C: int, D: int, E: int) -> str:
    terminos = []

    def agregar_termino(coef_str: str, variable: str):
        try:
            val = float(eval(coef_str))  # solo fracciones simples a/b
        except Exception:
            val = 0.0
        if val == 0:
            return
        if val == 1:
            terminos.append(variable)
        elif val == -1:
            terminos.append(f"-{variable}")
        else:
            terminos.append(f"({coef_str}){variable}")

    agregar_termino(A_frac, "x²")
    agregar_termino(B_frac, "y²")

    if C != 0:
        terminos.append(f"{C}x")
    if D != 0:
        terminos.append(f"{D}y")
    if E != 0:
        terminos.append(str(E))

    if not terminos:
        return "0"

    resultado = terminos[0]
    for t in terminos[1:]:
        if t.startswith("-"):
            resultado += f" {t}"
        else:
            resultado += f" + {t}"
    return resultado


def formatear_construccion(resultado: dict) -> str:
    d = resultado["digitos"]
    lineas = []
    lineas.append("=" * 55)
    lineas.append("  CONSTRUCCIÓN DE ECUACIÓN GENERAL DESDE EL RUT")
    lineas.append("=" * 55)
    lineas.append(f"\nDígitos extraídos del RUT:")
    lineas.append(
        f"  d1={d[0]}, d2={d[1]}, d3={d[2]}, d4={d[3]}, "
        f"d5={d[4]}, d6={d[5]}, d7={d[6]}, d8={d[7]}"
    )
    lineas.append(f"  DV = {resultado['dv']},  v = {resultado['v']}\n")

    for paso in resultado["pasos"]:
        lineas.append(paso)
        lineas.append("")

    if resultado["ajustes_aplicados"]:
        lineas.append("Ajustes aplicados:")
        for aj in resultado["ajustes_aplicados"]:
            lineas.append(f"  ✔ {aj}")
        lineas.append("")

    lineas.append(f"Tipo de cónica:  {resultado['tipo_conica']}")
    lineas.append(f"Ecuación final:  {resultado['ecuacion']}")
    lineas.append("=" * 55)

    return "\n".join(lineas)



# test

if __name__ == "__main__":
    # Ejemplo con dígitos ficticios para verificar la lógica
    digitos_ejemplo = [1, 2, 3, 4, 5, 6, 7, 8]
    dv_ejemplo = "K"

    resultado = construir_coeficientes(digitos_ejemplo, dv_ejemplo)
    print(formatear_construccion(resultado))
