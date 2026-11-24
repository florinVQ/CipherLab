"""Mini-aplicatia Afin: interfata. Criptarea se face in motor.cpp."""

from __future__ import annotations

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet  # noqa: E402
from fereastra_cifru import AplicatieCifru, Camp  # noqa: E402

if __name__ == "__main__":
    AplicatieCifru(
        FOLDER,
        campuri_cheie=[Camp("a", "5"), Camp("b", "8")],
        campuri_atac=[],
        chei_atac=[Camp("a"), Camp("b")],
        alfabet=alfabet.LATIN,
    ).mainloop()
