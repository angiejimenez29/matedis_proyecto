"""Estilo de la app: colores, esquinas redondeadas y letra.

Se usa en main.py y también se puede usar en cualquier vista que se corra sola:
    import estilo
    estilo.aplicar_estilo(raiz)
"""
import tkinter as tk
from tkinter import font, ttk

# colores
LILA = "#d8c8ff"
LILA_OSCURO = "#7c5cc4"
FONDO = "#f4efff"
BLANCO = "#fdfcff"
MORADO = "#9d84e0"
BORDE = "#d6caf7"
TEXTO = "#4b3a5c"
VERDE = "#2e7d32"
ROJO = "#c62828"


def mezclar(c1, c2, t):
    # mezcla dos colores hex, t entre 0 y 1
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def imagen_redondeada(ancho, alto, radio, relleno, fondo, borde=None, grosor=0,
                      solo_arriba=False, recta_arriba_izq=False):
    """Dibuja un rectángulo con esquinas redondeadas pixel por pixel.

    Tkinter no tiene esquinas redondeadas, así que se usa esta imagen como
    fondo de los botones, campos y pestañas (ttk la estira sin deformar las esquinas).
    """
    img = tk.PhotoImage(width=ancho, height=alto)
    for y in range(alto):
        fila = []
        for x in range(ancho):
            # distancia a la esquina más cercana (si estamos en una esquina)
            cx = radio if x < radio else ancho - 1 - radio if x > ancho - 1 - radio else x
            cy = radio if y < radio else alto - 1 - radio if y > alto - 1 - radio else y
            if solo_arriba and y > radio:
                cy = y
            if recta_arriba_izq and x < radio and y < radio:
                cx, cy = x, y
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            dentro = min(max(radio + 0.5 - d, 0), 1)  # suaviza el borde
            color = relleno
            if borde and d > radio - grosor:
                color = borde
            if borde and (x < grosor or x >= ancho - grosor or y < grosor or
                          (y >= alto - grosor and not solo_arriba)):
                color = borde
            fila.append(mezclar(fondo, color, dentro))
        img.put("{" + " ".join(fila) + "}", to=(0, y))
    return img


def aplicar_estilo(raiz):
    raiz.configure(bg=FONDO)
    # letra un poco más grande en toda la app (campos de texto incluidos)
    for nombre in ("TkDefaultFont", "TkTextFont"):
        font.nametofont(nombre).configure(family="Segoe UI", size=11)
    img = {
        "boton": imagen_redondeada(24, 24, 9, MORADO, BLANCO),
        "boton2": imagen_redondeada(24, 24, 9, LILA_OSCURO, BLANCO),
        "boton3": imagen_redondeada(24, 24, 9, "#dcd2f5", BLANCO),
        "campo": imagen_redondeada(24, 24, 8, "#ffffff", BLANCO, BORDE, 2),
        "campo2": imagen_redondeada(24, 24, 8, "#ffffff", BLANCO, MORADO, 2),
        "bloque": imagen_redondeada(30, 30, 9, "#ffffff", BLANCO, "#e4d9ff", 2),
        "pestana": imagen_redondeada(30, 24, 9, "#e9e0ff", FONDO, solo_arriba=True),
        "pestana2": imagen_redondeada(30, 24, 9, LILA_OSCURO, FONDO, solo_arriba=True),
        "tarjeta": imagen_redondeada(40, 40, 14, BLANCO, FONDO, LILA_OSCURO, 2,
                                     recta_arriba_izq=True),
    }
    raiz.imagenes = img  # si no se guardan, Python las borra

    st = ttk.Style(raiz)
    st.theme_use("clam")
    st.configure(".", background=BLANCO, foreground=TEXTO, font=("Segoe UI", 11))
    st.configure("TFrame", background=BLANCO)
    st.configure("TLabel", background=BLANCO, foreground=TEXTO)
    st.configure("TRadiobutton", background=BLANCO, foreground=TEXTO)
    st.map("TRadiobutton", background=[("active", BLANCO)],
           indicatorcolor=[("selected", MORADO), ("!selected", "white")])

    # botones
    st.element_create("boton", "image", img["boton"], ("disabled", img["boton3"]),
                      ("active", img["boton2"]), border=9, sticky="nsew")
    st.layout("TButton", [("boton", {"sticky": "nsew", "children": [
        ("Button.padding", {"sticky": "nsew", "children": [
            ("Button.label", {"sticky": "nsew"})]})]})])
    st.configure("TButton", foreground="white", padding=(18, 5),
                 font=("Segoe UI", 11, "bold"), anchor="center")
    st.map("TButton", foreground=[("disabled", "white")])

    # campos de texto
    st.element_create("campo", "image", img["campo"], ("focus", img["campo2"]),
                      border=8, sticky="nsew")
    st.layout("TEntry", [("campo", {"sticky": "nsew", "children": [
        ("Entry.padding", {"sticky": "nsew", "children": [
            ("Entry.textarea", {"sticky": "nsew"})]})]})])
    st.configure("TEntry", padding=(8, 2))

    # marco para las cajas grandes de texto
    st.element_create("caja", "image", img["campo"], border=8, sticky="nsew")
    st.layout("Caja.TFrame", [("caja", {"sticky": "nsew"})])

    # bloques de la vista de Angie
    st.element_create("bloque", "image", img["bloque"], border=10, sticky="nsew")
    st.layout("TLabelframe", [("bloque", {"sticky": "nsew"})])
    st.configure("TLabelframe", padding=4)
    st.configure("TLabelframe.Label", foreground=LILA_OSCURO, font=("Segoe UI", 10, "bold"))

    # tarjeta donde va cada pestaña
    st.element_create("tarjeta", "image", img["tarjeta"], border=16, sticky="nsew")
    st.layout("Tarjeta.TFrame", [("tarjeta", {"sticky": "nsew"})])
    st.configure("Tarjeta.TFrame", background=FONDO)

    # pestañas
    st.element_create("pestana", "image", img["pestana"], ("selected", img["pestana2"]),
                      border=9, sticky="nsew")
    st.layout("TNotebook.Tab", [("pestana", {"sticky": "nsew", "children": [
        ("Notebook.padding", {"sticky": "nsew", "children": [
            ("Notebook.label", {"sticky": ""})]})]})])
    st.configure("TNotebook", background=FONDO, borderwidth=0, tabmargins=(2, 4, 0, 0),
                 bordercolor=FONDO, lightcolor=FONDO, darkcolor=FONDO)
    st.configure("TNotebook.Tab", background=FONDO, padding=(24, 9),
                 font=("Segoe UI", 12, "bold"))
    st.map("TNotebook.Tab", foreground=[("selected", "white")],
           background=[("selected", FONDO)], expand=[("selected", (0, 0, 0, 0))],
           padding=[("selected", (24, 9))])

    raiz.option_add("*Text.background", "white")
    raiz.option_add("*Text.foreground", TEXTO)
    raiz.option_add("*Text.relief", "flat")
    raiz.option_add("*Text.borderWidth", 0)
    raiz.option_add("*Text.highlightThickness", 0)
    raiz.option_add("*Text.padX", 6)
    raiz.option_add("*Text.padY", 4)


def caja_texto(padre, **opciones):
    # tk.Text dentro de un marco redondeado
    marco = ttk.Frame(padre, style="Caja.TFrame", padding=6)
    texto = tk.Text(marco, **opciones)
    texto.pack(fill="both", expand=True)
    return marco, texto


class Tarjeta(ttk.Frame):
    # recuadro blanco con bordes redondeados
    def __init__(self, padre):
        super().__init__(padre, style="Tarjeta.TFrame", padding=16)
        self.cuerpo = ttk.Frame(self)
        self.cuerpo.pack(fill="both", expand=True)
