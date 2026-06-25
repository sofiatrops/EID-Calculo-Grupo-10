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

Aplicación en Python con interfaz gráfica que, a partir de un **RUT chileno válido**, realiza automáticamente:

- Validación del RUT mediante el algoritmo oficial del módulo 11
- Construcción de una ecuación general de segundo grado: `Ax² + By² + Cx + Dy + E = 0`
- Clasificación de la sección cónica resultante (circunferencia, elipse, hipérbola o parábola)
- Transformación paso a paso a la forma canónica y procedimiento inverso
- Graficación de la cónica en el plano cartesiano
- Análisis de funciones por tramos generadas desde el RUT: límites laterales, continuidad y clasificación de discontinuidades

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
│   ├── app_principal.py                 # Ventana raíz y navegación
│   ├── vista_conicas.py                 # Módulo visual de cónicas
│   └── vista_limites.py                 # Módulo visual de límites
│
└── tests/
    └── casos_prueba.py                  # RUTs de prueba para las 4 cónicas
```

---

## Instalación y ejecución

### Requisitos previos
- Python 3.10 o superior instalado
- Git instalado

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/USUARIO/EID-Calculo.git
cd EID-Calculo

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

### Módulo 4 — Funciones por tramos y límites
Genera una función por tramos según `d8 % 3`, con punto de análisis `a = d3`. Calcula límites laterales, evalúa continuidad y clasifica la discontinuidad (removible, salto o infinita).

---

## Estrategia de ramas Git

| Rama | Propósito |
|---|---|
| `main` | Versión estable y entregable |
| `dev` | Integración continua del equipo |
| `feature/validacion-del-rut` | Trabajo de Denys |
| `feature/conicas-graficacion` | Trabajo de Paulo |
| `feature/funciones-tramos` | Trabajo de Joaquín |

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

El sistema debe poder demostrar las cuatro cónicas con RUTs válidos reales. Los casos se documentan en `tests/casos_prueba.py`.

| Cónica | Condición del RUT requerida |
|---|---|
| Circunferencia | d1 = d2 |
| Elipse | A y B mismo signo, A ≠ B |
| Hipérbola | d8 impar, d1 ≠ d2, d5+d6 no múltiplo de 3 |
| Parábola | (d5 + d6) múltiplo de 3 |
