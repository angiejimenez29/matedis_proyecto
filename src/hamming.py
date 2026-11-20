"""Codificación y decodificación Hamming(7,4) (Angie).

Cada bloque de 4 bits de datos (d1 d2 d3 d4) se convierte en una palabra de
7 bits con 3 bits de paridad. Posiciones (1 a 7):

    pos:   1   2   3   4   5   6   7
           p1  p2  d1  p3  d2  d3  d4

    p1 = d1 + d2 + d4  (mod 2)   -> cubre posiciones 1, 3, 5, 7
    p2 = d1 + d3 + d4  (mod 2)   -> cubre posiciones 2, 3, 6, 7
    p3 = d2 + d3 + d4  (mod 2)   -> cubre posiciones 4, 5, 6, 7

Al recibir, se recalculan las 3 paridades. El síndrome (s3 s2 s1) leído como
número binario es la posición del bit dañado (0 = sin error). Corrige 1 error
por bloque de 7 bits.

Los bits se manejan como listas de enteros 0/1.
"""


# ---------- Conversión texto <-> bits ----------

def texto_a_bits(texto):
    """Convierte un texto (UTF-8) en una lista de bits."""
    bits = []
    for byte in texto.encode("utf-8"):
        bits.extend((byte >> i) & 1 for i in range(7, -1, -1))
    return bits


def bits_a_texto(bits):
    """Convierte una lista de bits (múltiplo de 8) de vuelta a texto."""
    if len(bits) % 8 != 0:
        raise ValueError("La cantidad de bits debe ser múltiplo de 8.")
    datos = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i + 8]:
            byte = (byte << 1) | b
        datos.append(byte)
    return datos.decode("utf-8", errors="replace")


# ---------- Un bloque ----------

def codificar_bloque(d):
    """Recibe [d1, d2, d3, d4] y devuelve la palabra de 7 bits."""
    if len(d) != 4:
        raise ValueError("Un bloque de datos debe tener 4 bits.")
    d1, d2, d3, d4 = d
    p1 = (d1 + d2 + d4) % 2
    p2 = (d1 + d3 + d4) % 2
    p3 = (d2 + d3 + d4) % 2
    return [p1, p2, d1, p3, d2, d3, d4]


def decodificar_bloque(w):
    """Recibe 7 bits (posiblemente dañados).

    Devuelve (datos, posicion_error): los 4 bits corregidos y la posición
    (1 a 7) del bit que se corrigió, o 0 si no se detectó error.
    """
    if len(w) != 7:
        raise ValueError("Una palabra Hamming(7,4) debe tener 7 bits.")
    w = list(w)
    s1 = (w[0] + w[2] + w[4] + w[6]) % 2
    s2 = (w[1] + w[2] + w[5] + w[6]) % 2
    s3 = (w[3] + w[4] + w[5] + w[6]) % 2
    posicion = s3 * 4 + s2 * 2 + s1
    if posicion != 0:
        w[posicion - 1] ^= 1  # voltear el bit dañado
    return [w[2], w[4], w[5], w[6]], posicion


# ---------- Mensajes completos ----------

def codificar(bits):
    """Codifica una lista de bits (múltiplo de 4) en bloques de 7 bits."""
    if len(bits) % 4 != 0:
        raise ValueError("La cantidad de bits debe ser múltiplo de 4.")
    salida = []
    for i in range(0, len(bits), 4):
        salida.extend(codificar_bloque(bits[i:i + 4]))
    return salida


def decodificar(bits):
    """Decodifica y corrige una lista de bits (múltiplo de 7).

    Devuelve (bits_datos, errores_corregidos).
    """
    if len(bits) % 7 != 0:
        raise ValueError("La cantidad de bits debe ser múltiplo de 7.")
    datos = []
    corregidos = 0
    for i in range(0, len(bits), 7):
        d, pos = decodificar_bloque(bits[i:i + 7])
        datos.extend(d)
        if pos != 0:
            corregidos += 1
    return datos, corregidos


if __name__ == "__main__":
    # Demo rápida: un error en un bloque
    original = [1, 0, 1, 1]
    palabra = codificar_bloque(original)
    print("Datos:           ", original)
    print("Palabra Hamming: ", palabra)
    recibida = palabra.copy()
    recibida[4] ^= 1
    print("Recibida (pos 5 dañada):", recibida)
    datos, pos = decodificar_bloque(recibida)
    print(f"Error detectado en la posición {pos}; datos corregidos: {datos}")
