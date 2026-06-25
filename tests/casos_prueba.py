"""
Casos de prueba end-to-end: RUT -> coeficientes -> clasificación -> forma canónica.

Documenta un RUT real (válido según el algoritmo módulo 11) para cada uno de
los 4 tipos de cónica, disparado explícitamente por la regla correspondiente
del enunciado, además de casos de manejo de errores con RUTs inválidos.

Ejecutar con: python3 tests/casos_prueba.py
"""

import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODULOS_PATH = os.path.join(_PROJECT_ROOT, "modulos")
if _MODULOS_PATH not in sys.path:
    sys.path.insert(0, _MODULOS_PATH)

from validacion_rut import validar_rut
from construccion_coeficientes import construir_coeficientes
from clasificador_conicas import ClasificadorDeConicas
from transformacion_canonica import transformar_a_canonica


# RUT real (pasa el algoritmo módulo 11) elegido para disparar explícitamente
# la regla de ajuste correspondiente. dígitos = [d1..d8].
CASOS_VALIDOS = [
    {
        "rut": "11000101-0",
        "tipo_esperado": "Circunferencia",
        "disparador": "d1 = d2 = 1 -> Ajuste 2 (B = A)",
    },
    {
        "rut": "01020100-4",
        "tipo_esperado": "Elipse",
        "disparador": "A y B mismo signo, A != B, sin ajustes especiales",
    },
    {
        "rut": "01010103-4",
        "tipo_esperado": "Hiperbola",
        "disparador": "d8 = 3 (impar) -> Ajuste 1 (B = -B)",
    },
    {
        "rut": "01000001-7",
        "tipo_esperado": "Parabola",
        "disparador": "d5+d6 = 0, 0 % 3 == 0 y d7 = 0 (par) -> Ajuste 3 (B = 0)",
    },
]

CASOS_INVALIDOS = [
    "12345678-9",      # dígito verificador incorrecto
    "123-9",            # cuerpo demasiado corto
    "ABCDEFGH-9",        # cuerpo no numérico
    "",                  # vacío
]

# RUT cuyos primeros 4 dígitos son 0 -> A = 0 y B = 0 (caso degenerado)
RUT_DEGENERADO = "00000010-8"


def ejecutar_caso_valido(caso):
    resultado_rut = validar_rut(caso["rut"])
    assert resultado_rut["valido"], f"El RUT {caso['rut']} debería ser válido"

    coeficientes = construir_coeficientes(resultado_rut["digitos"], resultado_rut["dv_ingresado"])
    clasificador = ClasificadorDeConicas(coeficientes)
    nombre, justificacion = clasificador.determinar_clasificacion_y_justificacion()

    assert nombre == caso["tipo_esperado"], (
        f"RUT {caso['rut']}: se esperaba {caso['tipo_esperado']}, se obtuvo {nombre}"
    )

    canonica = transformar_a_canonica(coeficientes)

    print(f"RUT: {caso['rut']}  ->  {nombre}")
    print(f"  Disparador: {caso['disparador']}")
    print(f"  Dígitos: {resultado_rut['digitos']}")
    print(f"  Ecuación general:  {coeficientes['ecuacion']}")
    print(f"  Justificación:     {justificacion}")
    print(f"  Tipo (canónica):   {canonica['tipo']}")
    if "ecuacion_canonica" in canonica:
        print(f"  Ecuación canónica: {canonica['ecuacion_canonica']}")
    print()


def ejecutar_caso_invalido(rut_str):
    resultado = validar_rut(rut_str)
    assert resultado["valido"] is False, f"El RUT '{rut_str}' debería marcarse como inválido"
    print(f"RUT inválido '{rut_str}' -> manejado correctamente: {resultado['mensaje']}")


def ejecutar_caso_degenerado():
    resultado_rut = validar_rut(RUT_DEGENERADO)
    assert resultado_rut["valido"], f"El RUT {RUT_DEGENERADO} debería ser válido"

    coeficientes = construir_coeficientes(resultado_rut["digitos"], resultado_rut["dv_ingresado"])
    assert coeficientes["A"] == 0 and coeficientes["B"] == 0

    clasificador = ClasificadorDeConicas(coeficientes)
    try:
        clasificador.comprobar_caso_degenerado()
        raise AssertionError("Se esperaba ValueError para el caso degenerado A=0, B=0")
    except ValueError as e:
        print(f"Caso degenerado (A=0, B=0) manejado correctamente: {e}")


def main():
    print("=" * 70)
    print("  CASOS DE PRUEBA — RUT -> COEFICIENTES -> CONICA -> CANONICA")
    print("=" * 70)
    print()

    print("--- Casos válidos (uno por tipo de cónica) ---\n")
    for caso in CASOS_VALIDOS:
        ejecutar_caso_valido(caso)

    print("--- Casos inválidos (manejo de errores) ---\n")
    for rut_str in CASOS_INVALIDOS:
        ejecutar_caso_invalido(rut_str)
    print()

    print("--- Caso degenerado (A=0 y B=0) ---\n")
    ejecutar_caso_degenerado()
    print()

    print("Todos los casos de prueba pasaron correctamente.")


if __name__ == "__main__":
    main()
