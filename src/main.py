"""Ventana principal del proyecto (Valery).

Junta las tres partes en pestañas: cifrado, Hamming (de Angie) y el flujo completo.
Se ejecuta con: py src/main.py
"""
import tkinter as tk
from tkinter import ttk

import cifrado
import hamming
import ruido
from estilo import (FONDO, LILA, LILA_OSCURO, TEXTO, VERDE, ROJO, Tarjeta,
                    aplicar_estilo, caja_texto)
from vista_hamming import VistaHamming, COLOR_ERROR, COLOR_CORREGIDO


def separar_bits(bits, n=7):
    s = "".join(map(str, bits))
    return " ".join(s[i:i + n] for i in range(0, len(s), n))


class SelectorMetodo(ttk.Frame):
    # para elegir César (con un número) o Vigenère (con una palabra)
    def __init__(self, padre):
        super().__init__(padre)
        self.metodo = tk.StringVar(value="cesar")
        ttk.Radiobutton(self, text="César", value="cesar", variable=self.metodo,
                        command=self.cambiar).pack(side="left")
        ttk.Radiobutton(self, text="Vigenère", value="vigenere", variable=self.metodo,
                        command=self.cambiar).pack(side="left", padx=6)
        self.etiqueta = ttk.Label(self, text="Desplazamiento k:")
        self.etiqueta.pack(side="left", padx=(12, 4))
        self.clave = ttk.Entry(self, width=12)
        self.clave.insert(0, "3")
        self.clave.pack(side="left")

    def cambiar(self):
        self.clave.delete(0, "end")
        if self.metodo.get() == "cesar":
            self.etiqueta.config(text="Desplazamiento k:")
            self.clave.insert(0, "3")
        else:
            self.etiqueta.config(text="Clave (letras):")
            self.clave.insert(0, "CLAVE")

    def valores(self):
        return self.metodo.get(), self.clave.get().strip()


class VistaCifrado(ttk.Frame):
    def __init__(self, padre=None):
        super().__init__(padre, padding=12)
        ttk.Label(self, text="Cifrado César y Vigenère",
                  font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(self, text="Cada letra se mueve en el alfabeto: "
                  "C = (P + k) mod 26").pack(anchor="w")

        self.selector = SelectorMetodo(self)
        self.selector.pack(anchor="w", pady=8)

        ttk.Label(self, text="Texto:").pack(anchor="w")
        marco, self.entrada = caja_texto(self, height=3, width=60, font=("Segoe UI", 12))
        self.entrada.insert("1.0", "Nota final: 18")
        marco.pack(anchor="w")

        botones = ttk.Frame(self)
        botones.pack(anchor="w", pady=8)
        ttk.Button(botones, text="Cifrar", command=self.cifrar).pack(side="left")
        ttk.Button(botones, text="Descifrar", command=self.descifrar).pack(side="left", padx=6)

        ttk.Label(self, text="Resultado:").pack(anchor="w")
        marco, self.salida = caja_texto(self, height=3, width=60, font=("Segoe UI", 12),
                                        state="disabled")
        marco.pack(anchor="w")
        self.mensaje = ttk.Label(self, text="")
        self.mensaje.pack(anchor="w", pady=6)

    def cifrar(self):
        self.procesar(cifrado.cifrar)

    def descifrar(self):
        self.procesar(cifrado.descifrar)

    def procesar(self, funcion):
        texto = self.entrada.get("1.0", "end-1c")
        metodo, clave = self.selector.valores()
        try:
            resultado = funcion(texto, metodo, clave)
        except ValueError:
            self.mensaje.config(text="Clave inválida: César usa un número y "
                                "Vigenère una palabra.", foreground=ROJO)
            return
        self.salida.config(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.insert("1.0", resultado)
        self.salida.config(state="disabled")
        self.mensaje.config(text="Listo.", foreground=VERDE)


class VistaFlujo(ttk.Frame):
    def __init__(self, padre=None):
        super().__init__(padre, padding=12)
        ttk.Label(self, text="Flujo completo del envío",
                  font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(self, text="cifrar → codificar → ruido → corregir → descifrar").pack(anchor="w")

        fila = ttk.Frame(self)
        fila.pack(anchor="w", pady=(8, 0))
        ttk.Label(fila, text="Mensaje:").pack(side="left")
        self.entrada = ttk.Entry(fila, width=36)
        self.entrada.insert(0, "Hola Angie")
        self.entrada.pack(side="left", padx=6)

        self.selector = SelectorMetodo(self)
        self.selector.pack(anchor="w", pady=6)

        fila = ttk.Frame(self)
        fila.pack(anchor="w")
        ttk.Label(fila, text="Ruido:").pack(side="left")
        self.tipo_ruido = tk.StringVar(value="bloque")
        for texto, valor in [("1 bit por bloque (se corrige)", "bloque"),
                             ("Aleatorio 5% (puede fallar)", "prob"),
                             ("Sin ruido", "nada")]:
            ttk.Radiobutton(fila, text=texto, value=valor,
                            variable=self.tipo_ruido).pack(side="left", padx=4)

        ttk.Button(self, text="Enviar mensaje", command=self.enviar).pack(anchor="w", pady=8)

        marco, self.texto = caja_texto(self, height=16, width=90, font=("Consolas", 11),
                                       wrap="word", state="disabled")
        self.texto.tag_config("titulo", font=("Segoe UI", 11, "bold"))
        self.texto.tag_config("error", background=COLOR_ERROR)
        self.texto.tag_config("corregido", background=COLOR_CORREGIDO)
        marco.pack(fill="both", expand=True)

        self.resultado = ttk.Label(self, text="", font=("Segoe UI", 13, "bold"),
                                   wraplength=750)
        self.resultado.pack(anchor="w", pady=6)

    def escribir(self, titulo, contenido, marcados=(), tag=None):
        self.texto.insert("end", titulo + "\n", "titulo")
        if marcados:
            # se escribe bit por bit para pintar los que cambiaron
            for i, b in enumerate(contenido):
                if i > 0 and i % 7 == 0:
                    self.texto.insert("end", " ")
                self.texto.insert("end", str(b), tag if i in marcados else ())
        else:
            self.texto.insert("end", contenido)
        self.texto.insert("end", "\n\n")

    def enviar(self):
        mensaje = self.entrada.get()
        metodo, clave = self.selector.valores()
        if not mensaje:
            self.resultado.config(text="Escribe un mensaje.", foreground=ROJO)
            return
        try:
            texto_cifrado = cifrado.cifrar(mensaje, metodo, clave)
        except ValueError:
            self.resultado.config(text="Clave inválida.", foreground=ROJO)
            return

        # lo que se envía
        enviado = hamming.codificar(hamming.texto_a_bits(texto_cifrado))

        # lo que pasa en el camino
        tipo = self.tipo_ruido.get()
        if tipo == "bloque":
            recibido, danados = ruido.ruido_por_bloque(enviado)
        elif tipo == "prob":
            recibido, danados = ruido.ruido_probabilidad(enviado, 0.05)
        else:
            recibido, danados = list(enviado), []

        # lo que hace el que recibe
        datos, n_corregidos = hamming.decodificar(recibido)
        corregidos = set()
        for k in range(0, len(recibido), 7):
            _, pos = hamming.decodificar_bloque(recibido[k:k + 7])
            if pos:
                corregidos.add(k + pos - 1)
        texto_recibido = hamming.bits_a_texto(datos)
        try:
            final = cifrado.descifrar(texto_recibido, metodo, clave)
        except ValueError:
            final = texto_recibido

        self.texto.config(state="normal")
        self.texto.delete("1.0", "end")
        self.escribir("1. Mensaje original", mensaje)
        self.escribir("2. Cifrado", texto_cifrado)
        self.escribir(f"3. Bits codificados con Hamming ({len(enviado)} bits)",
                      separar_bits(enviado))
        self.escribir(f"4. Bits recibidos: {len(danados)} dañados (rojo)",
                      recibido, set(danados), "error")
        self.escribir(f"5. Bits corregidos: {n_corregidos} bloques (verde)",
                      hamming.codificar(datos), corregidos, "corregido")
        self.escribir("6. Texto recibido (cifrado)", texto_recibido)
        self.escribir("7. Mensaje descifrado", final)
        self.texto.config(state="disabled")

        if final == mensaje:
            self.resultado.config(text=f"Llegó bien: «{final}»", foreground=VERDE)
        else:
            self.resultado.config(text=f"Llegó dañado: «{final}». Hubo 2 o más errores "
                                  "en un mismo bloque y Hamming(7,4) solo corrige 1.",
                                  foreground=ROJO)


def main():
    raiz = tk.Tk()
    raiz.title("Envío seguro y confiable de mensajes")
    raiz.geometry("940x900")
    aplicar_estilo(raiz)

    cabecera = tk.Frame(raiz, bg=LILA, pady=16)
    cabecera.pack(fill="x")
    tk.Label(cabecera, text="Envío seguro y confiable de mensajes", bg=LILA,
             fg=LILA_OSCURO, font=("Segoe UI", 24, "bold")).pack()
    tk.Label(cabecera, text="Matemática Discreta  ·  Valery y Angie", bg=LILA,
             fg=TEXTO, font=("Segoe UI", 12)).pack()

    pestanas = ttk.Notebook(raiz)
    pestanas.pack(fill="both", expand=True, padx=16, pady=(12, 16))
    for Vista, nombre in [(VistaCifrado, "Cifrado"), (VistaHamming, "Hamming(7,4)"),
                          (VistaFlujo, "Flujo completo")]:
        fondo = tk.Frame(pestanas, bg=FONDO)
        tarjeta = Tarjeta(fondo)
        tarjeta.pack(fill="both", expand=True)
        Vista(tarjeta.cuerpo).pack(anchor="n")
        pestanas.add(fondo, text=nombre)

    raiz.mainloop()


if __name__ == "__main__":
    main()
