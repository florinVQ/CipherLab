"""Butoanele de limba (RO / EN / RU) si de tema (luminos / intunecat) din coltul ferestrei."""

import tkinter as tk
from tkinter import ttk

import setari
import tema
import traduceri
from traduceri import t


def construieste_bara_setari(parinte: tk.Misc, dupa_schimbare) -> tk.Frame:
    """Intoarce bara cu butoane; `dupa_schimbare()` reconstruieste fereastra in noua limba/tema."""
    bara = tk.Frame(parinte, bg=tema.FUNDAL)

    def alege_limba(cod: str) -> None:
        traduceri.seteaza_limba(cod)
        setari.salveaza()
        dupa_schimbare()

    def schimba_tema() -> None:
        tema.seteaza_tema("luminos" if tema.nume_tema == "intunecat" else "intunecat")
        setari.salveaza()
        dupa_schimbare()

    for cod in traduceri.LIMBI:
        stil = "Accent.TButton" if cod == traduceri.limba else "TButton"
        ttk.Button(bara, text=cod.upper(), style=stil, width=4, cursor="hand2",
                   command=lambda c=cod: alege_limba(c)).pack(side="left", padx=(0, 4))

    spre_luminos = tema.nume_tema == "intunecat"
    ttk.Button(bara, text=t("tema_spre_luminos" if spre_luminos else "tema_spre_intunecat"),
               cursor="hand2", command=schimba_tema).pack(side="left", padx=(8, 0))
    return bara
