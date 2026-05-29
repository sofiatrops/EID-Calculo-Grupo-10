import matplotlib.pyplot as plt

class UtilidadesMatematicas:
    def obtener_numero_pi(self):
        return 3.141592653589793

    def calcular_factorial(self, numero_entero):
        if numero_entero == 0:
            return 1
            
        resultado_factorial = 1
        for iterador in range(2, numero_entero + 1):
            resultado_factorial = resultado_factorial * iterador
            
        return resultado_factorial

    def calcular_potencia(self, numero_base, numero_exponente):
        resultado_potencia = 1
        for iterador in range(numero_exponente):
            resultado_potencia = resultado_potencia * numero_base
            
        return resultado_potencia

    def calcular_seno(self, angulo_en_radianes):
        numero_de_terminos = 15
        resultado_seno = 0
        
        for iterador in range(numero_de_terminos):
            exponente_actual = (2 * iterador) + 1
            termino_actual = self.calcular_potencia(angulo_en_radianes, exponente_actual) / self.calcular_factorial(exponente_actual)
            
            if iterador % 2 == 0:
                resultado_seno = resultado_seno + termino_actual
            else:
                resultado_seno = resultado_seno - termino_actual
                
        return resultado_seno

    def calcular_coseno(self, angulo_en_radianes):
        numero_de_terminos = 15
        resultado_coseno = 0
        
        for iterador in range(numero_de_terminos):
            exponente_actual = 2 * iterador
            termino_actual = self.calcular_potencia(angulo_en_radianes, exponente_actual) / self.calcular_factorial(exponente_actual)
            
            if iterador % 2 == 0:
                resultado_coseno = resultado_coseno + termino_actual
            else:
                resultado_coseno = resultado_coseno - termino_actual
                
        return resultado_coseno

    def calcular_seno_hiperbolico(self, valor_real):
        numero_de_terminos = 15
        resultado_seno_hiperbolico = 0
        
        for iterador in range(numero_de_terminos):
            exponente_actual = (2 * iterador) + 1
            termino_actual = self.calcular_potencia(valor_real, exponente_actual) / self.calcular_factorial(exponente_actual)
            resultado_seno_hiperbolico = resultado_seno_hiperbolico + termino_actual
            
        return resultado_seno_hiperbolico

    def calcular_coseno_hiperbolico(self, valor_real):
        numero_de_terminos = 15
        resultado_coseno_hiperbolico = 0
        
        for iterador in range(numero_de_terminos):
            exponente_actual = 2 * iterador
            termino_actual = self.calcular_potencia(valor_real, exponente_actual) / self.calcular_factorial(exponente_actual)
            resultado_coseno_hiperbolico = resultado_coseno_hiperbolico + termino_actual
            
        return resultado_coseno_hiperbolico

    def generar_rango_de_valores(self, valor_inicial, valor_final, tamano_del_paso):
        lista_de_valores = []
        valor_actual = valor_inicial
        
        while valor_actual <= valor_final:
            lista_de_valores.append(valor_actual)
            valor_actual = valor_actual + tamano_del_paso
            
        return lista_de_valores

class GraficadorDeConicas:
    def __init__(self):
        pass

    def graficar_circunferencia(self, centro_x, centro_y, radio):
        pass

    def graficar_elipse(self, centro_x, centro_y, semieje_a, semieje_b):
        pass

    def graficar_hiperbola(self, centro_x, centro_y, semieje_a, semieje_b, es_hiperbola_horizontal):
        pass

    def graficar_parabola(self, vertice_x, vertice_y, factor_apertura_a, es_parabola_vertical):
        pass

    def configurar_y_mostrar_grafico(self):
        pass