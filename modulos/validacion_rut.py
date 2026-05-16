def parsear_rut(rut_str: str) -> tuple[str, str]:
    """
    Separa el cuerpo y el dígito verificador desde un string con formato
    '12345678-9', '12345678-K' o '123456789' (sin guión).
    Retorna (cuerpo, dv) como strings, o lanza ValueError si el formato es inválido.
    """
    rut_limpio = rut_str.strip().upper().replace(".", "")

    if "-" in rut_limpio:
        partes = rut_limpio.split("-")
        if len(partes) != 2:
            raise ValueError("Formato de RUT inválido. Use: 12345678-9 o 12345678-K")
        cuerpo, dv = partes
    elif len(rut_limpio) >= 2:
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]
    else:
        raise ValueError("RUT demasiado corto.")

    if not cuerpo.isdigit():
        raise ValueError(f"El cuerpo del RUT debe contener solo dígitos. Se recibió: '{cuerpo}'")
    if dv not in "0123456789K":
        raise ValueError(f"Dígito verificador inválido: '{dv}'")
    if len(cuerpo) < 7 or len(cuerpo) > 8:
        raise ValueError(f"El cuerpo del RUT debe tener 7 u 8 dígitos. Se recibió: {len(cuerpo)}")

    return cuerpo.zfill(8), dv


def calcular_digito_verificador(cuerpo: str) -> tuple[str, list[dict]]:
    """
    aui se calcula el digito verificador esperado usando el algoritmo del módulo 11
     se retorna (dv_calculado, pasos) donde 'pasos' es una lista de dicts con
    el detalle de cada multiplicación para mostrar en pantalla.
    """
    # Secuencia de factores: 2, 3, 4, 5, 6, 7 (se repite si hay más de 6 dígitos)
    factores = [2, 3, 4, 5, 6, 7]

    digitos_invertidos = [int(d) for d in reversed(cuerpo)]
    pasos = []
    suma_total = 0

    for i, digito in enumerate(digitos_invertidos):
        factor = factores[i % len(factores)]
        producto = digito * factor
        suma_total += producto
        pasos.append({
            "posicion": i + 1,
            "digito": digito,
            "factor": factor,
            "producto": producto,
            "suma_acumulada": suma_total,
        })

    resto = suma_total % 11
    resultado = 11 - resto

    if resultado == 11:
        dv_calculado = "0"
    elif resultado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(resultado)

    return dv_calculado, pasos, suma_total, resto


def validar_rut(rut_str: str) -> dict:
    """
    Valida un RUT chileno completo.

    Retorna un dict con:
        - valido (bool)
        - cuerpo (str)
        - dv_ingresado (str)
        - dv_calculado (str)
        - digitos (list[int]): lista [d1, d2, ..., d8] (con ceros a la izquierda si aplica)
        - pasos (list[dict]): detalle del procedimiento
        - mensaje (str): descripción del resultado
        - suma_total (int)
        - resto (int)
    """
    try:
        cuerpo, dv_ingresado = parsear_rut(rut_str)
    except ValueError as e:
        return {
            "valido": False,
            "mensaje": str(e),
            "cuerpo": "",
            "dv_ingresado": "",
            "dv_calculado": "",
            "digitos": [],
            "pasos": [],
            "suma_total": 0,
            "resto": 0,
        }

    dv_calculado, pasos, suma_total, resto = calcular_digito_verificador(cuerpo)
    es_valido = dv_ingresado == dv_calculado

    # Normalizar cuerpo a 8 dígitos (rellenar con ceros a la izquierda)
    cuerpo_normalizado = cuerpo.zfill(8)
    digitos = [int(c) for c in cuerpo_normalizado]

    if es_valido:
        mensaje = f"RUT {cuerpo}-{dv_ingresado} es VÁLIDO."
    else:
        mensaje = (
            f"RUT {cuerpo}-{dv_ingresado} es INVÁLIDO. "
            f"El dígito verificador esperado es '{dv_calculado}', pero se ingresó '{dv_ingresado}'."
        )

    return {
        "valido": es_valido,
        "mensaje": mensaje,
        "cuerpo": cuerpo,
        "dv_ingresado": dv_ingresado,
        "dv_calculado": dv_calculado,
        "digitos": digitos,
        "pasos": pasos,
        "suma_total": suma_total,
        "resto": resto,
    }


def formatear_procedimiento(resultado: dict) -> str:
    """
    aqui se genera un string con el procedimiento completo del módulo 11,
    listo para mostrarse en la interfaz o en consola
    """
    if not resultado["cuerpo"]:
        return f"Error: {resultado['mensaje']}"

    cuerpo = resultado["cuerpo"]
    dv = resultado["dv_ingresado"]
    lineas = []

    lineas.append("=" * 50)
    lineas.append("  VALIDACIÓN DE RUT — ALGORITMO MÓDULO 11")
    lineas.append("=" * 50)
    lineas.append(f"\nRUT ingresado: {cuerpo}-{dv}")
    lineas.append(f"Cuerpo (normalizado a 8 dígitos): {cuerpo.zfill(8)}")
    lineas.append("\nPaso 1: Invertir el cuerpo del RUT y multiplicar")
    lineas.append("        por la secuencia 2, 3, 4, 5, 6, 7 (repetida)\n")
    lineas.append(f"  {'Pos':<5} {'Dígito':<10} {'Factor':<10} {'Producto':<10} {'Suma acum.'}")
    lineas.append("  " + "-" * 45)

    for p in resultado["pasos"]:
        lineas.append(
            f"  {p['posicion']:<5} {p['digito']:<10} {p['factor']:<10} "
            f"{p['producto']:<10} {p['suma_acumulada']}"
        )

    lineas.append(f"\nPaso 2: Suma total = {resultado['suma_total']}")
    lineas.append(f"Paso 3: Resto = {resultado['suma_total']} mod 11 = {resultado['resto']}")
    lineas.append(f"Paso 4: DV calculado = 11 - {resultado['resto']} = {11 - resultado['resto']}")

    dv_calc = resultado["dv_calculado"]
    if dv_calc == "0":
        lineas.append("        Como el resultado fue 11 → DV = 0")
    elif dv_calc == "K":
        lineas.append("        Como el resultado fue 10 → DV = K")
    else:
        lineas.append(f"        DV = {dv_calc}")

    lineas.append(f"\nPaso 5: Comparar DV calculado ('{dv_calc}') con DV ingresado ('{dv}')")
    lineas.append(f"\nResultado: {resultado['mensaje']}")
    lineas.append("=" * 50)

    return "\n".join(lineas)


# test
if __name__ == "__main__":
    ruts_prueba = [
        "12345678-9",   # inventado — puede ser inválido
        "76354771-K",   # ejemplo conocido
        "11111111-1",   # dígitos iguales
        "99999999-X",   # dv inválido
        "7635477-K",    # cuerpo de 7 digitos
    ]

    for rut in ruts_prueba:
        resultado = validar_rut(rut)
        print(formatear_procedimiento(resultado))
        print()