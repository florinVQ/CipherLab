"""Alfabetul ales de utilizator.

Motoarele C++ lucreaza cu octeti, iar un alfabet poate avea litere romanesti sau rusesti
(mai multi octeti in UTF-8). De aceea fiecare caracter al alfabetului primeste un cod de
un octet: primul caracter devine chr(33), al doilea chr(34) si tot asa. Motorul primeste
alfabetul si textul deja codate, iar rezultatul lui se decodeaza aici.
"""

from __future__ import annotations

import unicodedata

from traduceri import t

LATIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LATIN_FARA_J = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # pentru patratele 5 x 5 (J se scrie ca I)
MAX_CARACTERE = 90                           # codurile 33 ... 122 sunt toate caractere vizibile
PRIMUL_COD = 33


def fara_diacritice(text: str) -> str:
    descompus = unicodedata.normalize("NFD", text)
    return "".join(c for c in descompus if not unicodedata.combining(c))


def valideaza(alfabet: str, minim: int = 2, maxim: int = MAX_CARACTERE) -> str:
    """Intoarce alfabetul daca are intre `minim` si `maxim` caractere, fara repetari."""
    if not minim <= len(alfabet) <= maxim or len(set(alfabet)) != len(alfabet):
        raise ValueError(t("eroare_alfabet", min=minim, max=maxim))
    return alfabet


def pozitia(caracter: str, alfabet: str, inlocuiri: dict[str, str] | None = None) -> int:
    """Pozitia caracterului in alfabet (-1 daca lipseste).

    Se incearca si varianta cu litera mare / mica si fara diacritice, ca „ă” sa fie
    gasit ca „A” atunci cand alfabetul este A-Z. `inlocuiri` (de exemplu J -> I)
    se aplica doar caracterelor care nu sunt in alfabet.
    """
    simplu = fara_diacritice(caracter)
    for varianta in (caracter, caracter.upper(), caracter.lower(),
                     simplu, simplu.upper(), simplu.lower()):
        if len(varianta) == 1 and varianta in alfabet:
            return alfabet.index(varianta)
    if inlocuiri and caracter.upper() in inlocuiri:
        return pozitia(inlocuiri[caracter.upper()], alfabet)
    return -1


def codifica(text: str, alfabet: str, inlocuiri: dict[str, str] | None = None) -> str:
    """Doar caracterele din alfabet, fiecare scris ca un cod de un octet."""
    pozitii = (pozitia(c, alfabet, inlocuiri) for c in text)
    return "".join(chr(PRIMUL_COD + p) for p in pozitii if p >= 0)


def decodifica(coduri: str, alfabet: str) -> str:
    return "".join(alfabet[ord(c) - PRIMUL_COD] for c in coduri)


def coduri_alfabet(alfabet: str) -> str:
    return "".join(chr(PRIMUL_COD + i) for i in range(len(alfabet)))


def sablon(text: str, alfabet: str, inlocuiri: dict[str, str] | None = None) -> list[str | None]:
    """None pe locul fiecarui caracter din alfabet; celelalte caractere raman asa cum sunt."""
    return [None if pozitia(c, alfabet, inlocuiri) >= 0 else c for c in text]


def completeaza(sablon_text: list[str | None], caractere: str) -> str:
    """Pune caracterele (in ordine) pe locurile libere din sablon."""
    urmatorul = iter(caractere)
    return "".join(next(urmatorul, "") if loc is None else loc for loc in sablon_text)
