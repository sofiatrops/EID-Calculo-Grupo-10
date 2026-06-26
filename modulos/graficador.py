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
        self.utilidades = UtilidadesMatematicas()

    def graficar_circunferencia(self, ax, centro_x, centro_y, radio):
        pi = self.utilidades.obtener_numero_pi()
        rango_t = self.utilidades.generar_rango_de_valores(0, 2 * pi, 0.1)

        coordenadas_x = []
        coordenadas_y = []

        for t in rango_t:
            coseno_t = self.utilidades.calcular_coseno(t)
            seno_t = self.utilidades.calcular_seno(t)

            x = centro_x + (radio * coseno_t)
            y = centro_y + (radio * seno_t)

            coordenadas_x.append(x)
            coordenadas_y.append(y)

        ax.plot(coordenadas_x, coordenadas_y, label="Circunferencia", color="blue")
        ax.scatter([centro_x], [centro_y], color="red", zorder=5, label="Centro")

    def graficar_elipse(self, ax, centro_x, centro_y, semieje_a, semieje_b):
        pi = self.utilidades.obtener_numero_pi()
        rango_t = self.utilidades.generar_rango_de_valores(0, 2 * pi, 0.1)

        coordenadas_x = []
        coordenadas_y = []

        for t in rango_t:
            coseno_t = self.utilidades.calcular_coseno(t)
            seno_t = self.utilidades.calcular_seno(t)

            x = centro_x + (semieje_a * coseno_t)
            y = centro_y + (semieje_b * seno_t)

            coordenadas_x.append(x)
            coordenadas_y.append(y)

        ax.plot(coordenadas_x, coordenadas_y, label="Elipse", color="green")
        ax.scatter([centro_x], [centro_y], color="red", zorder=5, label="Centro")

        vertice_derecho_x = centro_x + semieje_a
        vertice_izquierdo_x = centro_x - semieje_a
        vertice_superior_y = centro_y + semieje_b
        vertice_inferior_y = centro_y - semieje_b

        lista_vertices_x = [vertice_derecho_x, vertice_izquierdo_x, centro_x, centro_x]
        lista_vertices_y = [centro_y, centro_y, vertice_superior_y, vertice_inferior_y]

        ax.scatter(lista_vertices_x, lista_vertices_y, color="orange", marker="s", zorder=5, label="Vértices")

    def graficar_hiperbola(self, ax, centro_x, centro_y, semieje_a, semieje_b, es_hiperbola_horizontal):
        rango_t = self.utilidades.generar_rango_de_valores(-2.5, 2.5, 0.1)

        rama_positiva_x = []
        rama_positiva_y = []
        rama_negativa_x = []
        rama_negativa_y = []

        for t in rango_t:
            coseno_h = self.utilidades.calcular_coseno_hiperbolico(t)
            seno_h = self.utilidades.calcular_seno_hiperbolico(t)

            if es_hiperbola_horizontal:
                x_positivo = centro_x + (semieje_a * coseno_h)
                x_negativo = centro_x - (semieje_a * coseno_h)
                y_valor = centro_y + (semieje_b * seno_h)

                rama_positiva_x.append(x_positivo)
                rama_positiva_y.append(y_valor)
                rama_negativa_x.append(x_negativo)
                rama_negativa_y.append(y_valor)
            else:
                x_valor = centro_x + (semieje_a * seno_h)
                y_positivo = centro_y + (semieje_b * coseno_h)
                y_negativo = centro_y - (semieje_b * coseno_h)

                rama_positiva_x.append(x_valor)
                rama_positiva_y.append(y_positivo)
                rama_negativa_x.append(x_valor)
                rama_negativa_y.append(y_negativo)

        ax.plot(rama_positiva_x, rama_positiva_y, color="purple", label="Hipérbola")
        ax.plot(rama_negativa_x, rama_negativa_y, color="purple")
        ax.scatter([centro_x], [centro_y], color="red", zorder=5, label="Centro")

        if es_hiperbola_horizontal:
            vertice_derecho_x = centro_x + semieje_a
            vertice_izquierdo_x = centro_x - semieje_a
            lista_vertices_x = [vertice_derecho_x, vertice_izquierdo_x]
            lista_vertices_y = [centro_y, centro_y]
        else:
            vertice_superior_y = centro_y + semieje_b
            vertice_inferior_y = centro_y - semieje_b
            lista_vertices_x = [centro_x, centro_x]
            lista_vertices_y = [vertice_superior_y, vertice_inferior_y]

        ax.scatter(lista_vertices_x, lista_vertices_y, color="orange", marker="s", zorder=5, label="Vértices")

    def graficar_parabola(self, ax, vertice_x, vertice_y, factor_apertura_a, es_parabola_vertical):
        rango_t = self.utilidades.generar_rango_de_valores(-10.0, 10.0, 0.2)

        coordenadas_x = []
        coordenadas_y = []

        for t in rango_t:
            if es_parabola_vertical:
                x = vertice_x + t
                y = vertice_y + (factor_apertura_a * (t * t))
            else:
                y = vertice_y + t
                x = vertice_x + (factor_apertura_a * (t * t))

            coordenadas_x.append(x)
            coordenadas_y.append(y)

        ax.plot(coordenadas_x, coordenadas_y, color="cyan", label="Parábola")
        ax.scatter([vertice_x], [vertice_y], color="orange", marker="s", zorder=5, label="Vértice")

    def configurar_grafico(self, ax):
        ax.axhline(0, color="black", linewidth=1.5)
        ax.axvline(0, color="black", linewidth=1.5)
        ax.grid(color="gray", linestyle="--", linewidth=0.5)
        ax.legend()
        ax.set_aspect("equal", adjustable="datalim")


if __name__ == "__main__":
    graficador = GraficadorDeConicas()
    fig, ax = plt.subplots(figsize=(6, 6))
    graficador.graficar_elipse(ax, centro_x=1.0, centro_y=-2.0, semieje_a=2.0, semieje_b=1.0)
    graficador.configurar_grafico(ax)
    plt.show()