class ClasificadorDeConicas:
    def __init__(self, coeficientes):
        self.coeficientes = coeficientes
        self.coeficiente_a = coeficientes.get('A')
        self.coeficiente_c = coeficientes.get('C')
        
        if self.coeficiente_a is None or self.coeficiente_c is None:
            raise ValueError("El diccionario proporcionado no contiene los coeficientes 'A' y 'C'.")

    def comprobar_caso_degenerado(self):
        if self.coeficiente_a == 0 and self.coeficiente_c == 0:
            raise ValueError("No existen los terminos cuadraticos: la ecuacion no representa una conica.")

    def determinar_clasificacion_y_justificacion(self):
        if self.coeficiente_a == self.coeficiente_c:
            nombreConica = "Circunferencia"
            justificacion = "A (" + str(self.coeficiente_a) + ") es igual a C (" + str(self.coeficiente_c) + ") y ambos son distintos de cero."
            
        elif self.coeficiente_a == 0 or self.coeficiente_c == 0:
            nombreConica = "Parabola"
            justificacion = "Exactamente uno de los coeficientes principales es cero (A = " + str(self.coeficiente_a) + ", C = " + str(self.coeficiente_c) + ")."
            
        elif (self.coeficiente_a > 0 and self.coeficiente_c > 0) or (self.coeficiente_a < 0 and self.coeficiente_c < 0):
            nombreConica = "Elipse"
            justificacion = "Los coeficientes A (" + str(self.coeficiente_a) + ") y C (" + str(self.coeficiente_c) + ") tienen el mismo signo y son distintos entre si."
            
        else:
            nombreConica = "Hiperbola"
            justificacion = "Los coeficientes A (" + str(self.coeficiente_a) + ") y C (" + str(self.coeficiente_c) + ") tienen signos opuestos."
            
        return nombreConica, justificacion

    def ejecutar_clasificacion(self):
        self.comprobar_caso_degenerado()
        
        nombreConica, justificacion = self.determinar_clasificacion_y_justificacion()
        
        self.coeficientes['nombreConica'] = nombreConica
        self.coeficientes['justificacion'] = justificacion

        resultadoFinal = nombreConica + ": " + justificacion

        return resultadoFinal

