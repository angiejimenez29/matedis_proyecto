"""Simulación de ruido en el canal (Valery).

Algunos bits llegan cambiados (0 -> 1 o 1 -> 0). Cambiar un bit es sumarle 1 en mod 2,
o sea, hacer XOR con 1. Los bits van en listas de 0 y 1, igual que en hamming.py.
"""
import random


def voltear(bits, posiciones):
    nuevos = list(bits)
    for i in posiciones:
        nuevos[i] ^= 1
    return nuevos


def ruido_por_bloque(bits, tam_bloque=7, semilla=None):
    # cambia 1 bit al azar en cada bloque de 7 (Hamming puede corregirlo)
    azar = random.Random(semilla)
    posiciones = []
    for inicio in range(0, len(bits) - tam_bloque + 1, tam_bloque):
        posiciones.append(inicio + azar.randrange(tam_bloque))
    return voltear(bits, posiciones), posiciones


def ruido_probabilidad(bits, p=0.05, semilla=None):
    # cada bit se cambia con probabilidad p; puede tocar 2 en un mismo bloque
    if p < 0 or p > 1:
        raise ValueError("La probabilidad debe estar entre 0 y 1")
    azar = random.Random(semilla)
    posiciones = [i for i in range(len(bits)) if azar.random() < p]
    return voltear(bits, posiciones), posiciones


def contar_diferencias(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


if __name__ == "__main__":
    original = [1, 0, 1, 1, 0, 0, 1] * 2
    con_ruido, pos = ruido_por_bloque(original, semilla=1)
    print("Original: ", original)
    print("Con ruido:", con_ruido, "posiciones:", pos)
    print("Bits distintos:", contar_diferencias(original, con_ruido))
