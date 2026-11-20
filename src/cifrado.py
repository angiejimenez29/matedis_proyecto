"""Cifrado César y Vigenère (Valery).

César:    C = (P + k) mod 26
Vigenère: C = (P + letra de la clave) mod 26, la clave se repite
Solo se cifran las letras A-Z; lo demás (espacios, números, tildes) queda igual.
"""

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def es_letra(c):
    return c.upper() in ALFABETO


def mover(letra, k):
    # mueve la letra k posiciones, respetando si es mayúscula o minúscula
    base = ord("A") if letra.isupper() else ord("a")
    return chr((ord(letra) - base + k) % 26 + base)


def cesar_cifrar(texto, k):
    resultado = ""
    for c in texto:
        resultado += mover(c, k) if es_letra(c) else c
    return resultado


def cesar_descifrar(texto, k):
    return cesar_cifrar(texto, -k)


def vigenere(texto, clave, signo):
    clave = "".join(c for c in clave.upper() if c in ALFABETO)
    if clave == "":
        raise ValueError("La clave debe tener al menos una letra")
    resultado = ""
    j = 0
    for c in texto:
        if es_letra(c):
            k = ALFABETO.index(clave[j % len(clave)])
            resultado += mover(c, signo * k)
            j += 1  # la clave solo avanza con las letras
        else:
            resultado += c
    return resultado


def vigenere_cifrar(texto, clave):
    return vigenere(texto, clave, 1)


def vigenere_descifrar(texto, clave):
    return vigenere(texto, clave, -1)


# las usa main.py
def cifrar(texto, metodo, clave):
    if metodo == "cesar":
        return cesar_cifrar(texto, int(clave))
    return vigenere_cifrar(texto, clave)


def descifrar(texto, metodo, clave):
    if metodo == "cesar":
        return cesar_descifrar(texto, int(clave))
    return vigenere_descifrar(texto, clave)


if __name__ == "__main__":
    msg = "Nota final: 18"
    c = cesar_cifrar(msg, 3)
    print("César k=3:", c, "->", cesar_descifrar(c, 3))
    v = vigenere_cifrar(msg, "CLAVE")
    print("Vigenère CLAVE:", v, "->", vigenere_descifrar(v, "CLAVE"))
