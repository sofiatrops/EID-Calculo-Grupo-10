class TransformadorConicas:
    def __init__(self):
        pass

    def raiz_cuadrada(self, numero):
        if numero < 0:
            return 0.0
        if numero == 0:
            return 0.0
        estimacion = numero / 2.0
        tolerancia = 0.00001
        diferencia = 1.0
        while diferencia > tolerancia:
            nueva_estimacion = 0.5 * (estimacion + (numero / estimacion))
            diferencia = estimacion - nueva_estimacion
            if diferencia < 0:
                diferencia = diferencia * -1.0
            estimacion = nueva_estimacion
        return estimacion

    def valor_absoluto(self, numero):
        if numero < 0:
            return numero * -1.0
        return numero

    def completar_cuadrado(self, coeficiente_cuadrado, coeficiente_lineal, variable):
        pasos = []
        if coeficiente_cuadrado == 0:
            return 0.0, 0.0, 0.0, pasos
        
        termino_lineal_interno = coeficiente_lineal / coeficiente_cuadrado
        mitad_lineal = termino_lineal_interno / 2.0
        termino_sumar_restar = mitad_lineal * mitad_lineal
        
        pasos.append("Agrupamos los términos con " + variable + " y factorizamos el coeficiente cuadrático:")
        pasos.append(str(coeficiente_cuadrado) + "(" + variable + "^2 + " + str(termino_lineal_interno) + variable + ")")
        
        pasos.append("Calculamos la mitad del término lineal y lo elevamos al cuadrado:")
        pasos.append("(" + str(termino_lineal_interno) + " / 2)^2 = " + str(termino_sumar_restar))
        
        pasos.append("Sumamos y restamos este valor dentro del paréntesis:")
        pasos.append(str(coeficiente_cuadrado) + "(" + variable + "^2 + " + str(termino_lineal_interno) + variable + " + " + str(termino_sumar_restar) + " - " + str(termino_sumar_restar) + ")")
        
        constante_fuera = coeficiente_cuadrado * (termino_sumar_restar * -1.0)
        pasos.append("Extraemos el término negativo multiplicándolo por el factor externo:")
        pasos.append(str(coeficiente_cuadrado) + "(" + variable + " + " + str(mitad_lineal) + ")^2 " + str(constante_fuera))
        
        centro = mitad_lineal * -1.0
        return coeficiente_cuadrado, centro, constante_fuera, pasos

    def transformar_a_canonica(self, a, c, d, e, f):
        pasos_totales = []
        pasos_totales.append("Ecuación general original:")
        pasos_totales.append(str(a) + "x^2 + " + str(c) + "y^2 + " + str(d) + "x + " + str(e) + "y + " + str(f) + " = 0")
        
        constante_x = 0.0
        centro_x = 0.0
        factor_x = a
        if a != 0:
            factor_x, centro_x, constante_x, pasos_x = self.completar_cuadrado(a, d, "x")
            pasos_totales.extend(pasos_x)

        constante_y = 0.0
        centro_y = 0.0
        factor_y = c
        if c != 0:
            factor_y, centro_y, constante_y, pasos_y = self.completar_cuadrado(c, e, "y")
            pasos_totales.extend(pasos_y)

        termino_independiente = f + constante_x + constante_y
        termino_independiente_derecha = termino_independiente * -1.0
        
        pasos_totales.append("Agrupamos las constantes resultantes y las movemos al lado derecho:")
        texto_canonica_temp = ""
        if a != 0:
            texto_canonica_temp = texto_canonica_temp + str(factor_x) + "(x - " + str(centro_x) + ")^2 "
        if c != 0:
            texto_canonica_temp = texto_canonica_temp + "+ " + str(factor_y) + "(y - " + str(centro_y) + ")^2 "
        
        pasos_totales.append(texto_canonica_temp + "= " + str(termino_independiente_derecha))

        tipo = "Desconocido"
        parametros = {}

        if a == c and a != 0:
            tipo = "Circunferencia"
            radio_cuadrado = termino_independiente_derecha / factor_x
            pasos_totales.append("Dividimos ambos lados por " + str(factor_x) + " para obtener la forma de circunferencia:")
            pasos_totales.append("(x - " + str(centro_x) + ")^2 + (y - " + str(centro_y) + ")^2 = " + str(radio_cuadrado))
            parametros["h"] = centro_x
            parametros["k"] = centro_y
            parametros["r"] = self.raiz_cuadrada(radio_cuadrado)
            
        elif a != 0 and c != 0 and (a * c > 0):
            tipo = "Elipse"
            pasos_totales.append("Dividimos todo por " + str(termino_independiente_derecha) + " para igualar a 1:")
            denominador_x = termino_independiente_derecha / factor_x
            denominador_y = termino_independiente_derecha / factor_y
            pasos_totales.append("(x - " + str(centro_x) + ")^2 / " + str(denominador_x) + " + (y - " + str(centro_y) + ")^2 / " + str(denominador_y) + " = 1")
            parametros["h"] = centro_x
            parametros["k"] = centro_y
            parametros["a"] = self.raiz_cuadrada(denominador_x)
            parametros["b"] = self.raiz_cuadrada(denominador_y)

        elif a != 0 and c != 0 and (a * c < 0):
            tipo = "Hipérbola"
            pasos_totales.append("Dividimos todo por " + str(termino_independiente_derecha) + " para igualar a 1:")
            denominador_x = termino_independiente_derecha / factor_x
            denominador_y = termino_independiente_derecha / factor_y
            pasos_totales.append("(x - " + str(centro_x) + ")^2 / " + str(denominador_x) + " + (y - " + str(centro_y) + ")^2 / " + str(denominador_y) + " = 1")
            parametros["h"] = centro_x
            parametros["k"] = centro_y
            if denominador_x > 0:
                parametros["eje_real"] = "x"
                parametros["a"] = self.raiz_cuadrada(denominador_x)
                parametros["b"] = self.raiz_cuadrada(self.valor_absoluto(denominador_y))
            else:
                parametros["eje_real"] = "y"
                parametros["a"] = self.raiz_cuadrada(denominador_y)
                parametros["b"] = self.raiz_cuadrada(self.valor_absoluto(denominador_x))

        elif a == 0 and c != 0:
            tipo = "Parábola Horizontal"
            pasos_totales.append("Despejamos el término lineal de x hacia el lado derecho:")
            termino_independiente_derecha_sin_x = constante_y + f
            termino_independiente_derecha_sin_x = termino_independiente_derecha_sin_x * -1.0
            coeficiente_x_derecha = d * -1.0
            pasos_totales.append(str(factor_y) + "(y - " + str(centro_y) + ")^2 = " + str(coeficiente_x_derecha) + "x + " + str(termino_independiente_derecha_sin_x))
            
            pasos_totales.append("Factorizamos el coeficiente de x en el lado derecho:")
            centro_x_parabola = termino_independiente_derecha_sin_x / coeficiente_x_derecha
            centro_x_parabola = centro_x_parabola * -1.0
            pasos_totales.append(str(factor_y) + "(y - " + str(centro_y) + ")^2 = " + str(coeficiente_x_derecha) + "(x - " + str(centro_x_parabola) + ")")
            
            pasos_totales.append("Dividimos todo por " + str(factor_y) + ":")
            factor_derecha = coeficiente_x_derecha / factor_y
            pasos_totales.append("(y - " + str(centro_y) + ")^2 = " + str(factor_derecha) + "(x - " + str(centro_x_parabola) + ")")
            parametros["h"] = centro_x_parabola
            parametros["k"] = centro_y
            parametros["p"] = factor_derecha / 4.0

        elif c == 0 and a != 0:
            tipo = "Parábola Vertical"
            pasos_totales.append("Despejamos el término lineal de y hacia el lado derecho:")
            termino_independiente_derecha_sin_y = constante_x + f
            termino_independiente_derecha_sin_y = termino_independiente_derecha_sin_y * -1.0
            coeficiente_y_derecha = e * -1.0
            pasos_totales.append(str(factor_x) + "(x - " + str(centro_x) + ")^2 = " + str(coeficiente_y_derecha) + "y + " + str(termino_independiente_derecha_sin_y))
            
            pasos_totales.append("Factorizamos el coeficiente de y en el lado derecho:")
            centro_y_parabola = termino_independiente_derecha_sin_y / coeficiente_y_derecha
            centro_y_parabola = centro_y_parabola * -1.0
            pasos_totales.append(str(factor_x) + "(x - " + str(centro_x) + ")^2 = " + str(coeficiente_y_derecha) + "(y - " + str(centro_y_parabola) + ")")
            
            pasos_totales.append("Dividimos todo por " + str(factor_x) + ":")
            factor_derecha = coeficiente_y_derecha / factor_x
            pasos_totales.append("(x - " + str(centro_x) + ")^2 = " + str(factor_derecha) + "(y - " + str(centro_y_parabola) + ")")
            parametros["h"] = centro_x
            parametros["k"] = centro_y_parabola
            parametros["p"] = factor_derecha / 4.0

        return tipo, parametros, pasos_totales

    def transformar_a_general(self, tipo, parametros):
        pasos = []
        pasos.append("Transformación de canónica a general para: " + tipo)
        
        a = 0.0
        c = 0.0
        d = 0.0
        e = 0.0
        f = 0.0
        
        h = parametros["h"]
        k = parametros["k"]
        
        if tipo == "Circunferencia":
            r = parametros["r"]
            pasos.append("Ecuación canónica: (x - " + str(h) + ")^2 + (y - " + str(k) + ")^2 = " + str(r) + "^2")
            pasos.append("Expandimos los binomios al cuadrado:")
            pasos.append("x^2 - " + str(2*h) + "x + " + str(h*h) + " + y^2 - " + str(2*k) + "y + " + str(k*k) + " = " + str(r*r))
            pasos.append("Reagrupamos términos e igualamos a cero:")
            
            a = 1.0
            c = 1.0
            d = -2.0 * h
            e = -2.0 * k
            f = (h*h) + (k*k) - (r*r)
            pasos.append(str(a) + "x^2 + " + str(c) + "y^2 + " + str(d) + "x + " + str(e) + "y + " + str(f) + " = 0")
            
        elif tipo == "Elipse":
            param_a = parametros["a"]
            param_b = parametros["b"]
            a_cuad = param_a * param_a
            b_cuad = param_b * param_b
            pasos.append("Ecuación canónica: (x - " + str(h) + ")^2 / " + str(a_cuad) + " + (y - " + str(k) + ")^2 / " + str(b_cuad) + " = 1")
            pasos.append("Multiplicamos todo por " + str(a_cuad * b_cuad) + " para eliminar denominadores:")
            pasos.append(str(b_cuad) + "(x - " + str(h) + ")^2 + " + str(a_cuad) + "(y - " + str(k) + ")^2 = " + str(a_cuad * b_cuad))
            pasos.append("Expandimos los binomios al cuadrado:")
            
            a = b_cuad
            c = a_cuad
            d = -2.0 * h * b_cuad
            e = -2.0 * k * a_cuad
            f = (b_cuad * h * h) + (a_cuad * k * k) - (a_cuad * b_cuad)
            pasos.append(str(a) + "x^2 + " + str(c) + "y^2 + " + str(d) + "x + " + str(e) + "y + " + str(f) + " = 0")
            
        elif tipo == "Hipérbola":
            param_a = parametros["a"]
            param_b = parametros["b"]
            a_cuad = param_a * param_a
            b_cuad = param_b * param_b
            eje_real = parametros["eje_real"]
            
            if eje_real == "x":
                pasos.append("Ecuación canónica: (x - " + str(h) + ")^2 / " + str(a_cuad) + " - (y - " + str(k) + ")^2 / " + str(b_cuad) + " = 1")
                pasos.append("Multiplicamos todo por " + str(a_cuad * b_cuad) + ":")
                a = b_cuad
                c = -1.0 * a_cuad
                d = -2.0 * h * b_cuad
                e = 2.0 * k * a_cuad
                f = (b_cuad * h * h) - (a_cuad * k * k) - (a_cuad * b_cuad)
            else:
                pasos.append("Ecuación canónica: (y - " + str(k) + ")^2 / " + str(a_cuad) + " - (x - " + str(h) + ")^2 / " + str(b_cuad) + " = 1")
                pasos.append("Multiplicamos todo por " + str(a_cuad * b_cuad) + ":")
                c = b_cuad
                a = -1.0 * a_cuad
                e = -2.0 * k * b_cuad
                d = 2.0 * h * a_cuad
                f = (b_cuad * k * k) - (a_cuad * h * h) - (a_cuad * b_cuad)
                
            pasos.append(str(a) + "x^2 + " + str(c) + "y^2 + " + str(d) + "x + " + str(e) + "y + " + str(f) + " = 0")

        elif tipo == "Parábola Horizontal":
            p = parametros["p"]
            pasos.append("Ecuación canónica: (y - " + str(k) + ")^2 = " + str(4.0 * p) + "(x - " + str(h) + ")")
            pasos.append("Expandimos el binomio:")
            pasos.append("y^2 - " + str(2.0 * k) + "y + " + str(k * k) + " = " + str(4.0 * p) + "x - " + str(4.0 * p * h))
            
            a = 0.0
            c = 1.0
            d = -4.0 * p
            e = -2.0 * k
            f = (k * k) + (4.0 * p * h)
            pasos.append(str(a) + "x^2 + " + str(c) + "y^2 + " + str(d) + "x + " + str(e) + "y + " + str(f) + " = 0")

        elif tipo == "Parábola Vertical":
            p = parametros["p"]
            pasos.append("Ecuación canónica: (x - " + str(h) + ")^2 = " + str(4.0 * p) + "(y - " + str(k) + ")")
            pasos.append("Expandimos el binomio:")
            pasos.append("x^2 - " + str(2.0 * h) + "x + " + str(h * h) + " = " + str(4.0 * p) + "y - " + str(4.0 * p * k))
            
            c = 0.0
            a = 1.0
            e = -4.0 * p
            d = -2.0 * h
            f = (h * h) + (4.0 * p * k)
            pasos.append(str(a) + "x^2 + " + str(c) + "y^2 + " + str(d) + "x + " + str(e) + "y + " + str(f) + " = 0")

        coeficientes_general = {"a": a, "c": c, "d": d, "e": e, "f": f}
        return coeficientes_general, pasos

    def calcular_elementos(self, tipo, parametros):
        elementos = {}
        h = parametros.get("h", 0.0)
        k = parametros.get("k", 0.0)
        elementos["centro"] = (h, k)

        if tipo == "Circunferencia":
            r = parametros.get("r", 0.0)
            elementos["semiejes"] = "Radio = " + str(r)
            elementos["vertices"] = "N/A"
            elementos["focos"] = "N/A"

        elif tipo == "Elipse":
            a = parametros.get("a", 0.0)
            b = parametros.get("b", 0.0)
            elementos["semiejes"] = "Semieje mayor = " + str(a) + ", Semieje menor = " + str(b)
            if a > b:
                distancia_focal_cuad = (a * a) - (b * b)
                distancia_focal = self.raiz_cuadrada(distancia_focal_cuad)
                elementos["focos"] = "(" + str(h + distancia_focal) + ", " + str(k) + "), (" + str(h - distancia_focal) + ", " + str(k) + ")"
                elementos["vertices"] = "(" + str(h + a) + ", " + str(k) + "), (" + str(h - a) + ", " + str(k) + ")"
            else:
                distancia_focal_cuad = (b * b) - (a * a)
                distancia_focal = self.raiz_cuadrada(distancia_focal_cuad)
                elementos["focos"] = "(" + str(h) + ", " + str(k + distancia_focal) + "), (" + str(h) + ", " + str(k - distancia_focal) + ")"
                elementos["vertices"] = "(" + str(h) + ", " + str(k + b) + "), (" + str(h) + ", " + str(k - b) + ")"

        elif tipo == "Hipérbola":
            a = parametros.get("a", 0.0)
            b = parametros.get("b", 0.0)
            eje_real = parametros.get("eje_real", "x")
            elementos["semiejes"] = "Eje transversal = " + str(a) + ", Eje conjugado = " + str(b)
            distancia_focal_cuad = (a * a) + (b * b)
            distancia_focal = self.raiz_cuadrada(distancia_focal_cuad)
            
            if eje_real == "x":
                elementos["focos"] = "(" + str(h + distancia_focal) + ", " + str(k) + "), (" + str(h - distancia_focal) + ", " + str(k) + ")"
                elementos["vertices"] = "(" + str(h + a) + ", " + str(k) + "), (" + str(h - a) + ", " + str(k) + ")"
            else:
                elementos["focos"] = "(" + str(h) + ", " + str(k + distancia_focal) + "), (" + str(h) + ", " + str(k - distancia_focal) + ")"
                elementos["vertices"] = "(" + str(h) + ", " + str(k + a) + "), (" + str(h) + ", " + str(k - a) + ")"

        elif tipo == "Parábola Horizontal":
            p = parametros.get("p", 0.0)
            elementos["semiejes"] = "N/A"
            elementos["vertices"] = "(" + str(h) + ", " + str(k) + ")"
            elementos["focos"] = "(" + str(h + p) + ", " + str(k) + ")"

        elif tipo == "Parábola Vertical":
            p = parametros.get("p", 0.0)
            elementos["semiejes"] = "N/A"
            elementos["vertices"] = "(" + str(h) + ", " + str(k) + ")"
            elementos["focos"] = "(" + str(h) + ", " + str(k + p) + ")"

        return elementos
