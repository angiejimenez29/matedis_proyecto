import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import hamming  # noqa: E402


class TestHamming(unittest.TestCase):
    def test_ida_y_vuelta_sin_error(self):
        for n in range(16):
            d = [(n >> i) & 1 for i in (3, 2, 1, 0)]
            datos, pos = hamming.decodificar_bloque(hamming.codificar_bloque(d))
            self.assertEqual(datos, d)
            self.assertEqual(pos, 0)

    def test_corrige_cualquier_error_de_un_bit(self):
        for n in range(16):
            d = [(n >> i) & 1 for i in (3, 2, 1, 0)]
            w = hamming.codificar_bloque(d)
            for i in range(7):
                dañada = w.copy()
                dañada[i] ^= 1
                datos, pos = hamming.decodificar_bloque(dañada)
                self.assertEqual(datos, d)
                self.assertEqual(pos, i + 1)

    def test_mensaje_completo_con_un_error_por_bloque(self):
        random.seed(1)
        texto = "Hola, mundo! Ñandú 123"
        bits = hamming.texto_a_bits(texto)
        codificado = hamming.codificar(bits)
        for i in range(0, len(codificado), 7):
            codificado[i + random.randrange(7)] ^= 1
        datos, corregidos = hamming.decodificar(codificado)
        self.assertEqual(corregidos, len(codificado) // 7)
        self.assertEqual(hamming.bits_a_texto(datos), texto)

    def test_longitudes_invalidas(self):
        with self.assertRaises(ValueError):
            hamming.codificar([1, 0, 1])
        with self.assertRaises(ValueError):
            hamming.decodificar([1] * 8)


if __name__ == "__main__":
    unittest.main()
