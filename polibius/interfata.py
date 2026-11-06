"""Mini-aplicatia Polibius: interfata. Criptarea se face in motor.cpp."""

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

from fereastra_cifru import AplicatieCifru, Camp  # noqa: E402

if __name__ == "__main__":
    AplicatieCifru(
        FOLDER,
        campuri_cheie=[Camp("cuvant_cheie", "A")],
    ).mainloop()
