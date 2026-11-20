"""Vista Tkinter de Hamming(7,4) (Angie).

Se puede usar sola (py src/vista_hamming.py) o dentro de la ventana de Valery:

    from vista_hamming import VistaHamming
    VistaHamming(contenedor).pack(fill="both", expand=True)

Flujo de la demo:
  1. Escribir un mensaje y pulsar "Codificar".
  2. Dañar bits: clic en un bit para voltearlo, o "Ruido aleatorio".
  3. Pulsar "Decodificar y corregir".
"""
import os
import random
import sys
import tkinter as tk
from tkinter import ttk

sys.path.insert(0, os.path.dirname(__file__))
import hamming  # noqa: E402

MAX_BYTES = 8  # para que quepa en pantalla (8 bytes = 16 bloques)
BLOQUES_POR_FILA = 4
COLOR_OK = "#e8e8e8"
COLOR_ERROR = "#ff8a80"
COLOR_CORREGIDO = "#81c784"
ETIQUETAS = ["p1", "p2", "d1", "p3", "d2", "d3", "d4"]


class VistaHamming(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=12)
        self.original = ""
        self.enviado = []    # bits codificados (lo que se transmite)
        self.recibido = []   # bits tras el ruido
        self.botones = []
        self.corregidos = {}  # índice de bit global -> True
        self._construir()

    # ---------- Interfaz ----------
    def _construir(self):
        ttk.Label(self, text="Codificación Hamming(7,4)",
                  font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(self, text="Cada 4 bits de datos se envían con 3 bits de "
                  "paridad (p1, p2, p3). Corrige 1 error por bloque.").pack(anchor="w")

        fila = ttk.Frame(self)
        fila.pack(fill="x", pady=8)
        ttk.Label(fila, text=f"Mensaje (máx. {MAX_BYTES} bytes):").pack(side="left")
        self.entrada = ttk.Entry(fila, width=24)
        self.entrada.insert(0, "Hola")
        self.entrada.pack(side="left", padx=6)
        ttk.Button(fila, text="Codificar", command=self.codificar).pack(side="left")

        self.info_bits = ttk.Label(self, text="", wraplength=640, justify="left")
        self.info_bits.pack(anchor="w")

        self.marco_bits = ttk.Frame(self)
        self.marco_bits.pack(fill="x", pady=8)

        acciones = ttk.Frame(self)
        acciones.pack(fill="x")
        self.btn_ruido = ttk.Button(acciones, text="Ruido aleatorio (1 bit por bloque)",
                                    command=self.ruido_aleatorio, state="disabled")
        self.btn_ruido.pack(side="left")
        self.btn_decod = ttk.Button(acciones, text="Decodificar y corregir",
                                    command=self.decodificar, state="disabled")
        self.btn_decod.pack(side="left", padx=6)
        self.btn_reset = ttk.Button(acciones, text="Quitar ruido",
                                    command=self.quitar_ruido, state="disabled")
        self.btn_reset.pack(side="left")

        leyenda = ttk.Label(self, text="Gris: bit normal   Rojo: bit dañado   "
                            "Verde: bit corregido   (clic en un bit para voltearlo)")
        leyenda.pack(anchor="w", pady=(8, 0))

        self.resultado = ttk.Label(self, text="", font=("Segoe UI", 12, "bold"),
                                   wraplength=640, justify="left")
        self.resultado.pack(anchor="w", pady=8)

    # ---------- Acciones ----------
    def codificar(self):
        texto = self.entrada.get()
        if not texto:
            self.resultado.config(text="Escribe un mensaje primero.")
            return
        if len(texto.encode("utf-8")) > MAX_BYTES:
            self.resultado.config(text=f"El mensaje es muy largo (máx. {MAX_BYTES} bytes).")
            return
        self.original = texto
        datos = hamming.texto_a_bits(texto)
        self.enviado = hamming.codificar(datos)
        self.recibido = self.enviado.copy()
        self.corregidos = {}
        self.info_bits.config(
            text=f"Bits del mensaje ({len(datos)}): {''.join(map(str, datos))}\n"
                 f"Bits codificados ({len(self.enviado)}): se agregan "
                 f"{len(self.enviado) - len(datos)} bits de paridad.")
        self.resultado.config(text="")
        self._dibujar()
        for b in (self.btn_ruido, self.btn_decod, self.btn_reset):
            b.config(state="normal")

    def voltear(self, i):
        self.recibido[i] ^= 1
        self.corregidos = {}
        self.resultado.config(text="")
        self._dibujar()

    def ruido_aleatorio(self):
        self.recibido = self.enviado.copy()
        for k in range(0, len(self.recibido), 7):
            self.recibido[k + random.randrange(7)] ^= 1
        self.corregidos = {}
        self.resultado.config(text="")
        self._dibujar()

    def quitar_ruido(self):
        self.recibido = self.enviado.copy()
        self.corregidos = {}
        self.resultado.config(text="")
        self._dibujar()

    def decodificar(self):
        datos, n = hamming.decodificar(self.recibido)
        # marcar bits corregidos
        self.corregidos = {}
        for k in range(0, len(self.recibido), 7):
            _, pos = hamming.decodificar_bloque(self.recibido[k:k + 7])
            if pos:
                self.corregidos[k + pos - 1] = True
        self._dibujar()
        recuperado = hamming.bits_a_texto(datos)
        if recuperado == self.original:
            self.resultado.config(
                text=f"Mensaje recuperado: «{recuperado}»  ({n} bloques corregidos)",
                foreground="#2e7d32")
        else:
            self.resultado.config(
                text=f"Mensaje recuperado: «{recuperado}»  - no coincide con el "
                     f"original. Hamming(7,4) solo corrige 1 error por bloque.",
                foreground="#c62828")

    # ---------- Dibujo ----------
    def _dibujar(self):
        for w in self.marco_bits.winfo_children():
            w.destroy()
        self.botones = []
        for b in range(len(self.recibido) // 7):
            caja = ttk.LabelFrame(self.marco_bits, text=f"Bloque {b + 1}")
            caja.grid(row=b // BLOQUES_POR_FILA, column=b % BLOQUES_POR_FILA,
                      padx=4, pady=4, sticky="n")
            for j in range(7):
                i = b * 7 + j
                if i in self.corregidos:
                    color = COLOR_CORREGIDO
                elif self.recibido[i] != self.enviado[i]:
                    color = COLOR_ERROR
                else:
                    color = COLOR_OK
                celda = ttk.Frame(caja)
                celda.grid(row=0, column=j)
                ttk.Label(celda, text=ETIQUETAS[j], font=("Segoe UI", 7)).pack()
                btn = tk.Button(celda, text=str(self.recibido[i]), width=2,
                                bg=color, relief="flat",
                                command=lambda i=i: self.voltear(i))
                btn.pack()
                self.botones.append(btn)


if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.title("Hamming(7,4)")
    VistaHamming(raiz).pack(fill="both", expand=True)
    raiz.mainloop()
