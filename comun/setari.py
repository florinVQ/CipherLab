"""Retine limba si tema alese, ca sa le aiba si ferestrele deschise mai tarziu."""

import json
from pathlib import Path

import tema
import traduceri

FISIER = Path.home() / ".criptolab_setari.json"


def incarca() -> None:
    try:
        date = json.loads(FISIER.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    if date.get("limba") in traduceri.LIMBI:
        traduceri.seteaza_limba(date["limba"])
    if date.get("tema") in tema.PALETE:
        tema.seteaza_tema(date["tema"])


def salveaza() -> None:
    date = {"limba": traduceri.limba, "tema": tema.nume_tema}
    try:
        FISIER.write_text(json.dumps(date), encoding="utf-8")
    except OSError:
        pass  # setarile raman valabile cat timp fereastra este deschisa
