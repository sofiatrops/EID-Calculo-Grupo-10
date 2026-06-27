# MAT1186 — Evaluación Integrada de Desempeño N°1
### Análisis y Modelamiento de Secciones Cónicas y Funciones por Tramos a partir del RUT

> Proyecto académico correspondiente al curso **MAT1186 - Introducción al Cálculo**  
> Universidad Católica de Temuco — Ingeniería Civil en Informática  
> Versión 2026 | Peso evaluativo: 25% de la nota final

---

## Equipo de trabajo

| Nombre | Rol | Responsabilidades |
|---|---|---|
| Denys Rodríguez | **Líder** | Validación de RUT, construcción de coeficientes, coordinación general |
| Paulo Villalobos | **Suplente** | Clasificación de cónicas, transformación canónica, graficación |
| Joaquín Valenzuela | **Integrante** | Funciones por tramos, análisis de límites y discontinuidades |

---

## Descripción del proyecto

Aplicación en Python con interfaz gráfica **unificada en una sola ventana**: se ingresa **un único RUT chileno válido**
y ese mismo RUT alimenta simultáneamente los dos módulos del proyecto, organizados en pestañas
("Cónicas" y "Límites"). No es necesario volver a ingresar el RUT al cambiar de módulo.

A partir del RUT, el sistema realiza automáticamente:

- Validación del RUT mediante el algoritmo oficial del módulo 11
- Construcción de una ecuación general de segundo grado: `Ax² + By² + Cx + Dy + E = 0`
- Clasificación de la sección cónica resultante (circunferencia, elipse, hipérbola o parábola)
- Transformación paso a paso a la forma canónica y procedimiento inverso
- Graficación de la cónica en el plano cartesiano
- Análisis de funciones por tramos generadas desde el RUT: límites laterales, continuidad y clasificación de discontinuidades

Además, ambos módulos incluyen:

- **Campos de defensa oral** inicialmente vacíos (centro, vértices, focos, semiejes, directriz, asíntotas / límites
  laterales, existencia del límite, f(a), continuidad, tipo de discontinuidad, justificación escrita) que el
  estudiante completa manualmente.
- Un botón **"Comprobar Respuestas"** que evalúa lo escrito por el estudiante contra el resultado real, sin
  completar los campos por sí mismo.
- Un botón **"Mostrar/Ocultar Respuestas"** pensado solo para practicar de forma autónoma antes de la defensa:
  revela los valores correctos y los elementos geométricos en el gráfico, y se oculta de nuevo con el mismo botón.
  Se resetea a oculto automáticamente con cada RUT nuevo, ya que durante la defensa oral real estos elementos
  **no deben ser visibles** en el gráfico (el objetivo es que el estudiante los identifique por sí mismo).
- Un **buscador de puntos** (solo en cónicas) para verificar si un punto ingresado pertenece a la cónica, y si
  coincide con su centro, vértice o foco.

> ⚠️ **Restricción técnica**: todos los cálculos matemáticos están implementados manualmente.  
> No se utilizan librerías como `numpy`, `math`, `sympy`, `scipy` ni `pandas`.

---

## Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| CustomTkinter | Interfaz gráfica |
| Matplotlib | Visualización de gráficas (solo display) |
| GitHub | Control de versiones y evidencia de participación |

---

## Estructura del proyecto

```
EID-Calculo/
│
├── main.py                              # Punto de entrada de la aplicación
├── requirements.txt                     # Dependencias del proyecto
├── README.md                            # Este archivo
│
├── modulos/
│   ├── validacion_rut.py                # Algoritmo módulo 11, parseo y validación
│   ├── construccion_coeficientes.py     # Construcción de A, B, C, D, E desde el RUT
│   ├── clasificador_conicas.py          # Clasificación automática de la cónica
│   ├── transformacion_canonica.py       # Transformación general ↔ canónica, paso a paso
│   ├── funciones_tramos.py              # Construcción de la función por tramos desde el RUT
│   └── analisis_limites.py              # Límites laterales, continuidad y discontinuidades
│
├── interfaz/
│   ├── vista_conicas.py                 # Pestaña "Cónicas": ecuaciones, gráfico, defensa, buscador de puntos
│   └── vista_limites.py                 # Pestaña "Límites": función, tabla, gráfico, defensa
│
└── tests/
    └── casos_prueba.py                  # RUTs de prueba para las 4 cónicas + manejo de errores
```

`main.py` contiene la única entrada de RUT de toda la aplicación (`AplicacionPrincipal`). Al presionar
"Analizar RUT" valida el RUT una sola vez y llama a `vista_conicas.procesar_rut_valido(...)` y
`vista_limites.procesar_rut_valido(...)` con el mismo resultado, mostrando ambos módulos como pestañas
de un `CTkTabview`.

---

## Instalación y ejecución

### Requisitos previos
- Python 3.10 o superior instalado
- Git instalado

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/sofiatrops/EID-Calculo-Grupo-10.git
cd EID-Calculo-Grupo-10

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python main.py
```

---

## Funcionamiento del sistema

### Módulo 1 — Validación de RUT
Ingresa un RUT chileno en formato `12345678-9` o `12345678-K`. El sistema aplica el algoritmo del módulo 11 y muestra cada multiplicación, suma acumulada y cálculo del dígito verificador.

### Módulo 2 — Ecuación general
A partir de los dígitos `d1...d8` y el dígito verificador, construye:

```
A = (d1 + d2) / v      B = (d3 + d4) / v
C = -(d5 + d6)         D = -(d7 + d8)
E = d1 + d3 + d5 + d7
```

Con ajustes automáticos según paridad de `d8`, igualdad `d1 = d2` y divisibilidad de `d5 + d6` por 3.

### Módulo 3 — Clasificación y forma canónica
| Condición | Cónica |
|---|---|
| A = B ≠ 0 | Circunferencia |
| mismo signo, A ≠ B | Elipse |
| signos opuestos | Hipérbola |
| A = 0 o B = 0 | Parábola |
| A = 0 y B = 0 | Caso degenerado (error controlado) |

A partir de ahí, `transformacion_canonica.py` completa el cuadrado en x e y para
llevar la ecuación general a su forma canónica, paso a paso, identificando
centro/vértice, focos, vértices y semiejes. La raíz cuadrada necesaria para
calcular radios, semiejes y distancia focal se implementa manualmente con el
**método de Newton-Raphson** (sin `math.sqrt`). También se muestra el
procedimiento inverso: expandir la forma canónica y reagrupar para reobtener
la ecuación general.

### Módulo 4 — Funciones por tramos y límites
Genera una función por tramos según `d8 % 3`, con punto de análisis `a = d3`. Calcula límites laterales, evalúa continuidad y clasifica la discontinuidad (removible, salto o infinita).

---

## Estrategia de ramas Git

| Rama | Propósito |
|---|---|
| `main` | Versión estable y entregable |
| `dev` | Integración continua del equipo |
| `feature/KAN-5-*`, `feature/KAN-6-*`, `feature/KAN-7-*` | Validación de RUT y construcción de coeficientes (Denys) |
| `feature/KAN-8-*`, `feature/KAN-9-*`, `feature/KAN-10-*`, `feature/KAN-14-*` | Clasificación, forma canónica, graficación e interfaz de cónicas (Paulo) |
| `feature/KAN-11-*`, `feature/KAN-12-*`, `feature/KAN-13-*`, `feature/KAN-15-*` | Funciones por tramos, límites e interfaz de límites (Joaquín) |

### Convención de commits

```
feat:   nueva funcionalidad
fix:    corrección de errores
docs:   cambios en documentación
test:   casos de prueba
refactor: mejoras sin cambio de funcionalidad
```

---

## Código de ética del equipo

El equipo se compromete a:

- Distribuir el trabajo de forma justa y verificable mediante commits reales
- Mantener comunicación honesta sobre avances y dificultades
- No simular participación ni utilizar trabajo ajeno sin reconocimiento
- Resolver conflictos internos con respeto y profesionalismo
- Cumplir los plazos acordados por el equipo

**Líder responsable:** Denys Rodríguez — coordinación general y comunicación con el docente.

---

## Casos de prueba

El sistema demuestra las cuatro cónicas con RUTs reales (válidos según el
algoritmo del módulo 11), cada uno disparando explícitamente la regla de
ajuste correspondiente. Verificados y documentados en `tests/casos_prueba.py`
(ejecutar con `python3 tests/casos_prueba.py`):

| Cónica | RUT | Disparador |
|---|---|---|
| Circunferencia | `11000101-0` | d1 = d2 = 1 → Ajuste 2 (B = A) |
| Elipse | `01020100-4` | A y B mismo signo, A ≠ B, sin ajustes |
| Hipérbola | `01010103-4` | d8 = 3 (impar) → Ajuste 1 (B = −B) |
| Parábola | `01000001-7` | (d5+d6) % 3 = 0, d7 par → Ajuste 3 (B = 0) |

El archivo de pruebas también cubre RUTs inválidos (dígito verificador
incorrecto, cuerpo corto, no numérico, vacío) y el caso degenerado
A = 0 y B = 0, verificando que el sistema responde con errores controlados
en vez de fallar.

---

## Preguntas frecuentes para la defensa oral

- **¿Cómo funciona el algoritmo módulo 11?** Se invierten los dígitos del
  cuerpo del RUT, se multiplican por la secuencia 2,3,4,5,6,7 (repetida), se
  suman los productos y se calcula el resto al dividir por 11. El dígito
  verificador es `11 − resto` (con `11→0` y `10→K`). Ver `validacion_rut.py`.
- **¿Por qué se aplica el ajuste de d8 impar?** Es una regla del enunciado
  para forzar que A y B tengan signos opuestos en algunos casos y así poder
  demostrar la construcción de una hipérbola a partir del RUT.
- **¿Cómo se completa el cuadrado para una elipse?** Se agrupan los términos
  en x y en y, se suma y resta el cuadrado de la mitad del coeficiente lineal
  de cada variable, y se divide todo por la constante resultante hasta dejar
  la ecuación igualada a 1. Ver `transformacion_canonica.py`.
- **¿Cómo se calcula la raíz cuadrada sin `math`?** Con el método de
  Newton-Raphson: partiendo de una estimación inicial, se itera
  `estimado = 0.5 * (estimado + x / estimado)` hasta converger.
- **¿Por qué hay discontinuidad en x = a?** Porque el punto de análisis
  `a = d3` coincide siempre con un valor que anula un denominador o separa
  dos tramos de la función generada desde el RUT (ver `funciones_tramos.py`).
- **¿Qué pasa si los límites laterales son iguales pero f(a) no existe?**
  El límite existe, pero la función no es continua en `a`: se clasifica como
  discontinuidad removible, ya que redefiniendo `f(a)` igual al límite la
  función se vuelve continua.
