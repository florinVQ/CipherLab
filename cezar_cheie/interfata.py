"""Mini-aplicatia Cezar cu cheie: interfata. Criptarea se face in motor.cpp."""

from __future__ import annotations

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet  # noqa: E402
from fereastra_cifru import LISTA, TEXT, AplicatieCifru, Camp  # noqa: E402

if __name__ == "__main__":
    AplicatieCifru(
        FOLDER,
        campuri_cheie=[Camp("cuvant_cheie", "CODE", tip=TEXT), Camp("k", "3")],
        campuri_atac=[Camp("cuvinte_banuite", "code,ion,maria", tip=LISTA)],
        chei_atac=[Camp("cuvant_cheie", tip=TEXT), Camp("k")],
        alfabet=alfabet.LATIN,
    ).mainloop()
