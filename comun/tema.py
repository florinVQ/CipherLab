"""Culorile, fonturile si stilul comun al aplicatiei, in doua teme: intunecat si luminos.

Dupa `seteaza_tema(...)`, numele din paleta (FUNDAL, PANOU, TEXT, ACCENT ...) sunt
disponibile ca `tema.FUNDAL`, `tema.TEXT` etc. Ferestrele se reconstruiesc dupa schimbare.
"""

import tkinter as tk
from tkinter import ttk

PALETE = {
    "intunecat": {
        "FUNDAL": "#0B1220",
        "PANOU": "#111B30",
        "PANOU_HOVER": "#192645",
        "INPUT": "#0D1526",
        "BORDURA": "#24324F",
        "TEXT": "#E6EDF7",
        "TEXT_SLAB": "#9AA8C0",
        "ACCENT": "#2DD4BF",
        "ACCENT_HOVER": "#5EEAD4",
        "PE_ACCENT": "#04201C",
        "SELECTIE": "#0F766E",
        "EROARE": "#FF8A8A",
        "SUCCES": "#5EEAD4",
        "TIP_MONOALFABETIC": "#2DD4BF",
        "TIP_POLIALFABETIC": "#FBBF24",
        "TIP_OMOFONIC": "#60A5FA",
        "TIP_POLIGRAFIC": "#C4B5FD",
    },
    "luminos": {
        "FUNDAL": "#EEF2F8",
        "PANOU": "#FFFFFF",
        "PANOU_HOVER": "#E3EAF5",
        "INPUT": "#F7F9FC",
        "BORDURA": "#C5D0E0",
        "TEXT": "#0F172A",
        "TEXT_SLAB": "#475569",
        "ACCENT": "#0F766E",
        "ACCENT_HOVER": "#115E59",
        "PE_ACCENT": "#FFFFFF",
        "SELECTIE": "#0F766E",
        "EROARE": "#B91C1C",
        "SUCCES": "#047857",
        "TIP_MONOALFABETIC": "#0F766E",
        "TIP_POLIALFABETIC": "#B45309",
        "TIP_OMOFONIC": "#1D4ED8",
        "TIP_POLIGRAFIC": "#6D28D9",
    },
}

FONT_UI = ("Segoe UI", 11)
FONT_UI_BOLD = ("Segoe UI", 11, "bold")
FONT_TITLU = ("Segoe UI", 20, "bold")
FONT_MIC = ("Segoe UI", 10)
FONT_COD = ("Consolas", 12)

nume_tema = "intunecat"


def seteaza_tema(nume: str) -> None:
    """Alege tema ("intunecat" sau "luminos") si pune culorile ei in acest modul."""
    global nume_tema
    nume_tema = nume
    globals().update(PALETE[nume])


seteaza_tema(nume_tema)


def aplica_stilul(fereastra: tk.Misc) -> None:
    """Configureaza toate widgeturile ttk (butoane, taburi, tabele) in tema curenta."""
    stil = ttk.Style(fereastra)
    stil.theme_use("clam")
    stil.configure(".", background=PANOU, foreground=TEXT, font=FONT_UI,
                   bordercolor=BORDURA, lightcolor=BORDURA, darkcolor=BORDURA,
                   focuscolor=ACCENT)

    stil.configure("TFrame", background=PANOU)
    stil.configure("TLabel", background=PANOU, foreground=TEXT)

    stil.configure("TNotebook", background=FUNDAL, borderwidth=0)
    stil.configure("TNotebook.Tab", background=FUNDAL, foreground=TEXT_SLAB,
                   padding=(18, 10), font=FONT_UI_BOLD, borderwidth=0)
    stil.map("TNotebook.Tab",
             background=[("selected", PANOU), ("active", PANOU_HOVER)],
             foreground=[("selected", ACCENT), ("active", TEXT)])

    stil.configure("TButton", background=PANOU_HOVER, foreground=TEXT,
                   padding=(14, 8), borderwidth=1)
    stil.map("TButton", background=[("active", BORDURA)])
    stil.configure("Accent.TButton", background=ACCENT, foreground=PE_ACCENT,
                   font=FONT_UI_BOLD, borderwidth=0)
    stil.map("Accent.TButton", background=[("active", ACCENT_HOVER)])

    stil.configure("Vertical.TScrollbar", background=PANOU_HOVER, troughcolor=INPUT,
                   arrowcolor=TEXT, bordercolor=INPUT)
    stil.map("Vertical.TScrollbar", background=[("active", BORDURA)])

    stil.configure("TEntry", fieldbackground=INPUT, foreground=TEXT,
                   insertcolor=TEXT, padding=6)
    stil.map("TEntry", bordercolor=[("focus", ACCENT)])

    stil.configure("Treeview", background=INPUT, fieldbackground=INPUT,
                   foreground=TEXT, rowheight=28, borderwidth=0, font=FONT_COD)
    stil.configure("Treeview.Heading", background=PANOU_HOVER, foreground=TEXT,
                   font=FONT_UI_BOLD, padding=6)
    stil.map("Treeview", background=[("selected", SELECTIE)],
             foreground=[("selected", "#FFFFFF")])


def zona_text(parinte: tk.Misc, inaltime: int, doar_citire: bool = False) -> tk.Text:
    """O casuta de text multi-linie, in stilul aplicatiei."""
    zona = tk.Text(parinte, height=inaltime, wrap="word", font=FONT_COD,
                   bg=INPUT, fg=TEXT, insertbackground=TEXT, relief="flat",
                   padx=10, pady=8, highlightthickness=1,
                   highlightbackground=BORDURA, highlightcolor=ACCENT,
                   selectbackground=SELECTIE, selectforeground="#FFFFFF", undo=True)
    if doar_citire:
        zona.configure(state="disabled")
    return zona


def scrie_in_zona(zona: tk.Text, continut: str) -> None:
    """Inlocuieste tot textul dintr-o zona (si o lasa doar-citire daca asa era)."""
    stare_initiala = str(zona.cget("state"))
    zona.configure(state="normal")
    zona.delete("1.0", "end")
    zona.insert("1.0", continut)
    zona.configure(state=stare_initiala)
