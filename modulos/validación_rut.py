"""
Módulo: validacion_rut.py
Descripción: Validación de RUT chileno usando el algoritmo oficial del módulo 11.
             Muestra el procedimiento paso a paso y retorna los dígitos extraídos.
Autor: Denys Rodríguez (Líder)
"""


def parsear_rut(rut_str: str) -> tuple[str, str]:
    """
    Separa el cuerpo y el dígito verificador desde un string con formato
    '12345678-9', '12345678-K' o '123456789' (sin guión).
    Retorna (cuerpo, dv) como strings, o lanza ValueError si el formato es inválido.
    """
    rut_limpio = rut_str.strip().upper().replace(".", "")

    if "-" in rut_limpio:
        partes = rut_limpio.split("-")
        if len(partes) != 2:
            raise ValueError("Formato de RUT inválido. Use: 12345678-9 o 12345678-K")
        cuerpo, dv = partes
    elif len(rut_limpio) >= 2:
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]
    else:
        raise ValueError("RUT demasiado corto.")

    if not cuerpo.isdigit():
        raise ValueError(f"El cuerpo del RUT debe contener solo dígitos. Se recibió: '{cuerpo}'")
    if dv not in "0123456789K":
        raise ValueError(f"Dígito verificador inválido: '{dv}'")
    if len(cuerpo) < 7 or len(cuerpo) > 8:
        raise ValueError(f"El cuerpo del RUT debe tener 7 u 8 dígitos. Se recibió: {len(cuerpo)}")

    return cuerpo, dv

