"""Mini-aplicatia Polibius: interfata. Criptarea se face in motor.cpp."""

from __future__ import annotations

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet  # noqa: E402
from fereastra_cifru import TEXT, AplicatieCifru, Camp  # noqa: E402

if __name__ == "__main__":
    AplicatieCifru(
        FOLDER,
        campuri_cheie=[Camp("cuvant_cheie", "A", tip=TEXT)],
        alfabet=alfabet.LATIN_FARA_J,
        pastreaza_restul=False,
        text_cifrat_numeric=True,
        inlocuiri={"J": "I"},
    ).mainloop()
