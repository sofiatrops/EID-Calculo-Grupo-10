def _fmt(valor: float, decimales: int = 4) -> str:
    """Redondea un numero solo para mostrarlo en la justificacion (no altera el valor real)."""
    redondeado = round(float(valor), decimales)
    if redondeado == 0:
        redondeado = 0.0  # evita mostrar "-0"
    if redondeado == int(redondeado):
        return str(int(redondeado))
    return f"{redondeado:.{decimales}f}".rstrip("0").rstrip(".")


class ClasificadorDeConicas:
    def __init__(self, coeficientes):
        self.coeficientes = coeficientes
        self.coeficiente_a = coeficientes.get('A')
        self.coeficiente_b = coeficientes.get('B')

        if self.coeficiente_a is None or self.coeficiente_b is None:
            raise ValueError("El diccionario proporcionado no contiene los coeficientes 'A' y 'B'.")

    def comprobar_caso_degenerado(self):
        if self.coeficiente_a == 0 and self.coeficiente_b == 0:
            raise ValueError("No existen los terminos cuadraticos: la ecuacion no representa una conica.")

    def determinar_clasificacion_y_justificacion(self):
        a_str, b_str = _fmt(self.coeficiente_a), _fmt(self.coeficiente_b)

        if self.coeficiente_a == self.coeficiente_b:
            nombreConica = "Circunferencia"
            justificacion = f"$A = {a_str}$ es igual a $B = {b_str}$ y ambos son distintos de cero."

        elif self.coeficiente_a == 0 or self.coeficiente_b == 0:
            nombreConica = "Parabola"
            justificacion = f"Exactamente uno de los coeficientes principales es cero ($A = {a_str}$, $B = {b_str}$)."

        elif (self.coeficiente_a > 0 and self.coeficiente_b > 0) or (self.coeficiente_a < 0 and self.coeficiente_b < 0):
            nombreConica = "Elipse"
            justificacion = f"Los coeficientes $A = {a_str}$ y $B = {b_str}$ tienen el mismo signo y son distintos entre si."

        else:
            nombreConica = "Hiperbola"
            justificacion = f"Los coeficientes $A = {a_str}$ y $B = {b_str}$ tienen signos opuestos."

        return nombreConica, justificacion

    def ejecutar_clasificacion(self):
        self.comprobar_caso_degenerado()

        nombreConica, justificacion = self.determinar_clasificacion_y_justificacion()

        self.coeficientes['nombreConica'] = nombreConica
        self.coeficientes['justificacion'] = justificacion

        resultadoFinal = nombreConica + ": " + justificacion

        return resultadoFinal
