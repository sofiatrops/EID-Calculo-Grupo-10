from funciones_tramos import generar_funcion_tramos


def _evaluar_caso_0(x, a, d1):
    return (x - a) * (x + d1) / (x - a)


def _evaluar_caso_1_izq(x, a, d2):
    return x + d2


def _evaluar_caso_1_der(x, a, d4):
    return x + d4


def _evaluar_caso_2(x, a, d5):
    return (d5 + 1) / (x - a)


def analizar_limites(rut_str: str) -> dict:
    resultado = generar_funcion_tramos(rut_str)
    if "error" in resultado:
        return resultado

    digitos = resultado["digitos"]
    d1, d2, d3, d4, d5, d8 = digitos[0], digitos[1], digitos[2], digitos[3], digitos[4], digitos[7]
    a = d3
    caso = resultado["caso"]

    tabla_valores = []
    pasos_justificacion = []

    if caso == 0:
        expresion_simplificada = f"f(x) = x + {d1},  x != {a}"

        pasos_justificacion.append(
            f"Paso 1: Factorizar el numerador. "
            f"f(x) = (x - {a})(x + {d1}) / (x - {a})"
        )
        pasos_justificacion.append(
            f"Paso 2: Cancelar el factor (x - {a}) del numerador y denominador, "
            f"válido para todo x != {a}. "
            f"Queda f(x) = x + {d1}"
        )

        lim_izq = a + d1
        lim_der = a + d1
        limite_existe = True
        f_a_definida = False
        razon_no_definida = f"f({a}) no está definida porque el denominador (x - {a}) se anula en x = {a}"
        continua = False
        tipo_discontinuidad = "removible"

        pasos_justificacion.append(
            f"Paso 3: Calcular límite lateral izquierdo. "
            f"lím x->{a}- f(x) = lím x->{a}- (x + {d1}) = {a} + {d1} = {lim_izq}"
        )
        pasos_justificacion.append(
            f"Paso 4: Calcular límite lateral derecho. "
            f"lím x->{a}+ f(x) = lím x->{a}+ (x + {d1}) = {a} + {d1} = {lim_der}"
        )
        pasos_justificacion.append(
            f"Paso 5: Como ambos límites laterales son iguales ({lim_izq}), "
            f"el límite existe y vale {lim_izq}."
        )
        pasos_justificacion.append(
            f"Paso 6: {razon_no_definida}. No se cumple que lím f(x) = f({a})."
        )
        pasos_justificacion.append(
            f"Paso 7: La discontinuidad es de tipo REMOVIBLE (evitable), "
            f"ya que el límite existe pero f({a}) no está definida. "
            f"Se puede redefinir f({a}) = {lim_izq} para hacer la función continua."
        )

        for delta in [1, 0.1, 0.01, 0.001]:
            for signo in [-1, 1]:
                x_val = a + signo * delta
                y_val = _evaluar_caso_0(x_val, a, d1)
                lado = "izquierdo" if signo == -1 else "derecho"
                tabla_valores.append({
                    "x": x_val, "f(x)": y_val, "lado": lado, "delta": delta
                })

    elif caso == 1:
        pasos_justificacion.append(
            f"Paso 1: Identificar la función por tramos. "
            f"f(x) = x + {d2}  si x < {a},  f(x) = x + {d4}  si x >= {a}"
        )

        lim_izq = a + d2
        lim_der = a + d4
        limite_existe = (lim_izq == lim_der)
        f_a_definida = True
        valor_f_a = a + d4
        continua = (limite_existe and lim_izq == valor_f_a)

        pasos_justificacion.append(
            f"Paso 2: Calcular límite lateral izquierdo (x -> {a}-). "
            f"Usamos la rama x < {a}: f(x) = x + {d2}. "
            f"lím x->{a}- f(x) = {a} + {d2} = {lim_izq}"
        )
        pasos_justificacion.append(
            f"Paso 3: Calcular límite lateral derecho (x -> {a}+). "
            f"Usamos la rama x >= {a}: f(x) = x + {d4}. "
            f"lím x->{a}+ f(x) = {a} + {d4} = {lim_der}"
        )

        if limite_existe:
            pasos_justificacion.append(
                f"Paso 4: Ambos límites laterales son iguales ({lim_izq}). "
                f"El límite existe y vale {lim_izq}."
            )
            if continua:
                pasos_justificacion.append(
                    f"Paso 5: lím f(x) = {lim_izq} = f({a}) = {valor_f_a}. "
                    f"La función es CONTINUA en x = {a}."
                )
                tipo_discontinuidad = "ninguna"
            else:
                pasos_justificacion.append(
                    f"Paso 5: lím f(x) = {lim_izq} != f({a}) = {valor_f_a}. "
                    f"Discontinuidad REMOVIBLE."
                )
                tipo_discontinuidad = "removible"
        else:
            pasos_justificacion.append(
                f"Paso 4: Los límites laterales son DISTINTOS "
                f"(izquierdo = {lim_izq}, derecho = {lim_der}). "
                f"El límite NO existe."
            )
            tipo_discontinuidad = "salto"
            pasos_justificacion.append(
                f"Paso 5: La discontinuidad es de tipo SALTO (de primera especie). "
                f"Diferencia: |{lim_izq} - ({lim_der})| = {abs(lim_izq - lim_der)}"
            )

        for delta in [1, 0.1, 0.01, 0.001]:
            for signo in [-1, 1]:
                x_val = a + signo * delta
                if x_val < a:
                    y_val = _evaluar_caso_1_izq(x_val, a, d2)
                else:
                    y_val = _evaluar_caso_1_der(x_val, a, d4)
                lado = "izquierdo" if signo == -1 else "derecho"
                tabla_valores.append({
                    "x": x_val, "f(x)": y_val, "lado": lado, "delta": delta
                })

    else:
        pasos_justificacion.append(
            f"Paso 1: Identificar la función. "
            f"f(x) = ({d5 + 1}) / (x - {a})"
        )

        lim_izq_cualitativo = None
        lim_der_cualitativo = None

        if (d5 + 1) > 0:
            lim_izq_cualitativo = "-inf"
            lim_der_cualitativo = "+inf"
        elif (d5 + 1) < 0:
            lim_izq_cualitativo = "+inf"
            lim_der_cualitativo = "-inf"
        else:
            lim_izq_cualitativo = "0"
            lim_der_cualitativo = "0"

        limite_existe = False
        f_a_definida = False
        razon_no_definida = f"f({a}) no está definida porque el denominador (x - {a}) se anula en x = {a}"
        continua = False
        tipo_discontinuidad = "infinita"

        signo_num = "+" if (d5 + 1) > 0 else "-"
        pasos_justificacion.append(
            f"Paso 2: El numerador ({d5 + 1}) es {signo_num}. "
            f"Al acercarnos a x = {a}, el denominador tiende a 0, "
            f"por lo que |f(x)| -> +inf."
        )
        pasos_justificacion.append(
            f"Paso 3: Calcular límite lateral izquierdo (x -> {a}-). "
            f"Si x < {a}, entonces (x - {a}) < 0. "
            f"Por lo tanto, f(x) -> {lim_izq_cualitativo}."
        )
        pasos_justificacion.append(
            f"Paso 4: Calcular límite lateral derecho (x -> {a}+). "
            f"Si x > {a}, entonces (x - {a}) > 0. "
            f"Por lo tanto, f(x) -> {lim_der_cualitativo}."
        )
        pasos_justificacion.append(
            f"Paso 5: Los límites laterales son distintos y al menos uno tiende a +/-inf. "
            f"El límite NO existe."
        )
        pasos_justificacion.append(
            f"Paso 6: {razon_no_definida}."
        )
        pasos_justificacion.append(
            f"Paso 7: La discontinuidad es de tipo INFINITA (de segunda especie), "
            f"con asíntota vertical en x = {a}."
        )

        for delta in [1, 0.1, 0.01, 0.001]:
            for signo in [-1, 1]:
                x_val = a + signo * delta
                y_val = _evaluar_caso_2(x_val, a, d5)
                lado = "izquierdo" if signo == -1 else "derecho"
                tabla_valores.append({
                    "x": x_val, "f(x)": y_val, "lado": lado, "delta": delta
                })

    resultado_analisis = {
        "rut": resultado["rut"],
        "digitos": digitos,
        "a": a,
        "caso": caso,
        "expresion": resultado["expresion"],
        "tramos": resultado["tramos"],
        "lim_izquierdo": lim_izq if caso != 2 else lim_izq_cualitativo,
        "lim_derecho": lim_der if caso != 2 else lim_der_cualitativo,
        "limite_existe": limite_existe,
        "f_a_definida": f_a_definida,
        "f_a": valor_f_a if caso == 1 else None,
        "continua": continua,
        "tipo_discontinuidad": tipo_discontinuidad,
        "tabla_valores": tabla_valores,
        "pasos_justificacion": pasos_justificacion,
    }

    if caso == 0:
        resultado_analisis["expresion_simplificada"] = expresion_simplificada

    return resultado_analisis


def mostrar_analisis_limites(resultado: dict):
    if "error" in resultado:
        print(resultado["error"])
        return

    print("=" * 60)
    print("  ANÁLISIS DE LÍMITES Y CONTINUIDAD")
    print("=" * 60)
    print(f"\nRUT: {resultado['rut']}")
    print(f"Punto de análisis: a = {resultado['a']}")
    print(f"Caso: {resultado['caso']}")
    print(f"Expresión: {resultado['expresion']}")

    if "expresion_simplificada" in resultado:
        print(f"Simplificada: {resultado['expresion_simplificada']}")

    print("\n--- LIMITES LATERALES ---")
    a = resultado['a']
    print(f"  lim x->{a}- f(x) = {resultado['lim_izquierdo']}")
    print(f"  lim x->{a}+ f(x) = {resultado['lim_derecho']}")

    print("\n--- EXISTENCIA DEL LIMITE ---")
    if resultado["limite_existe"]:
        print("  El limite EXISTE (ambos laterales coinciden)")
    else:
        print("  El limite NO EXISTE (laterales distintos o tienden a infinito)")

    print("\n--- EVALUACION EN f(a) ---")
    if resultado["f_a_definida"]:
        print(f"  f({a}) esta definida = {resultado['f_a']}")
    else:
        print(f"  f({a}) NO esta definida")

    print("\n--- CONTINUIDAD ---")
    if resultado["continua"]:
        print(f"  La funcion es CONTINUA en x = {a}")
    else:
        print(f"  La funcion NO es continua en x = {a}")

    print("\n--- TIPO DE DISCONTINUIDAD ---")
    print(f"  {resultado['tipo_discontinuidad'].upper()}")

    print("\n--- TABLA DE VALORES ---")
    print(f"{'x':>12} {'f(x)':>16} {'Lado':>12} {'Delta':>8}")
    print("-" * 50)
    for fila in resultado["tabla_valores"]:
        fx = fila["f(x)"]
        if isinstance(fx, float):
            fx_str = f"{fx:.6f}"
        else:
            fx_str = str(fx)
        print(f"{fila['x']:>12.6f} {fx_str:>16} {fila['lado']:>12} {fila['delta']:>8}")

    print("\n--- JUSTIFICACIÓN MATEMÁTICA ---")
    for paso in resultado["pasos_justificacion"]:
        print(f"  {paso}")

    print("=" * 60)


if __name__ == "__main__":
    ruts_prueba = [
        "12345670-K",
        "76354771-K",
        "12345672-6",
    ]

    for rut in ruts_prueba:
        analisis = analizar_limites(rut)
        mostrar_analisis_limites(analisis)
        print()
