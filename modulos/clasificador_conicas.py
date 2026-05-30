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
        if self.coeficiente_a == self.coeficiente_b:
            nombreConica = "Circunferencia"
            justificacion = "A (" + str(self.coeficiente_a) + ") es igual a B (" + str(self.coeficiente_b) + ") y ambos son distintos de cero."

        elif self.coeficiente_a == 0 or self.coeficiente_b == 0:
            nombreConica = "Parabola"
            justificacion = "Exactamente uno de los coeficientes principales es cero (A = " + str(self.coeficiente_a) + ", B = " + str(self.coeficiente_b) + ")."

        elif (self.coeficiente_a > 0 and self.coeficiente_b > 0) or (self.coeficiente_a < 0 and self.coeficiente_b < 0):
            nombreConica = "Elipse"
            justificacion = "Los coeficientes A (" + str(self.coeficiente_a) + ") y B (" + str(self.coeficiente_b) + ") tienen el mismo signo y son distintos entre si."

        else:
            nombreConica = "Hiperbola"
            justificacion = "Los coeficientes A (" + str(self.coeficiente_a) + ") y B (" + str(self.coeficiente_b) + ") tienen signos opuestos."

        return nombreConica, justificacion

    def ejecutar_clasificacion(self):
        self.comprobar_caso_degenerado()

        nombreConica, justificacion = self.determinar_clasificacion_y_justificacion()

        self.coeficientes['nombreConica'] = nombreConica
        self.coeficientes['justificacion'] = justificacion

        resultadoFinal = nombreConica + ": " + justificacion

        return resultadoFinal
