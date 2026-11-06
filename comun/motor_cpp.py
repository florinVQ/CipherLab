"""Apeleaza motoarele de criptare scrise in C++ (fisierul motor.cpp din fiecare folder)."""

import os
import subprocess
import unicodedata
from pathlib import Path

LUNGIME_MAXIMA = 10000  # aceeasi valoare ca MAX din fisierele motor.cpp


class EroareMotor(Exception):
    """Motorul C++ nu a putut fi compilat sau a raportat o eroare.

    `cod` este cheia mesajului tradus (de exemplu "afin_a" -> "eroare_afin_a").
    """

    def __init__(self, cod: str, detalii: str = ""):
        super().__init__(cod)
        self.cod = cod
        self.detalii = detalii


def pregateste(text: str) -> str:
    """Scoate diacriticele (ă, â, î, ș, ț) si scrie cu majuscule: cifrurile folosesc doar A-Z."""
    descompus = unicodedata.normalize("NFD", text)
    return "".join(c for c in descompus if not unicodedata.combining(c)).upper()


def _compileaza_daca_trebuie(folder: Path) -> Path:
    executabil = folder / ("motor.exe" if os.name == "nt" else "motor")
    sursa = folder / "motor.cpp"
    if executabil.exists() and executabil.stat().st_mtime >= sursa.stat().st_mtime:
        return executabil

    try:
        rezultat = subprocess.run(["g++", "-O2", "-o", str(executabil), str(sursa)],
                                  capture_output=True, text=True)
    except FileNotFoundError:
        raise EroareMotor("gpp")
    if rezultat.returncode != 0:
        raise EroareMotor("compilare", rezultat.stderr)
    return executabil


def ruleaza_motor(folder: Path, parametri: list[str], text: str, curata_text: bool = True) -> str:
    """Trimite motorului parametrii si textul (fiecare pe linia lui) si intoarce iesirea lui.

    `parametri` incepe cu comanda: "cripteaza", "decripteaza" sau "atac".
    `curata_text=False` trimite textul exact asa cum este (fara majuscule si fara diacritice).
    """
    executabil = _compileaza_daca_trebuie(folder)
    text_pe_o_linie = " ".join((pregateste(text) if curata_text else text).splitlines())
    intrare = "\n".join([*parametri, text_pe_o_linie]) + "\n"

    rezultat = subprocess.run(
        [str(executabil)], input=intrare, capture_output=True, text=True,
        encoding="utf-8", creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if rezultat.returncode != 0:
        raise EroareMotor(rezultat.stderr.strip() or "motor")
    return rezultat.stdout
