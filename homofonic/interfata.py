"""Mini-aplicatia Homofonic: interfata. Criptarea se face in motor.cpp."""

from __future__ import annotations

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet  # noqa: E402
from fereastra_cifru import AplicatieCifru, Camp  # noqa: E402

# Cate numere primeste fiecare litera A-Z, dupa frecventa ei (suma = 100).
OMOFOANE_LATIN = dict(zip(alfabet.LATIN, [11, 1, 5, 4, 12, 1, 1, 1, 11, 1, 1, 4, 3,
                                          6, 4, 3, 1, 7, 5, 6, 6, 2, 1, 1, 1, 1]))


class AplicatieHomofonic(AplicatieCifru):
    def _parametri_din_alfabet(self, caractere: str) -> list[str]:
        """Literele A-Z primesc omofoanele din tabel; orice alt caracter primeste unul."""
        omofoane = [OMOFOANE_LATIN.get(c.upper(), 1) for c in caractere]
        return [" ".join(str(x) for x in [len(omofoane), *omofoane])]


if __name__ == "__main__":
    AplicatieHomofonic(
        FOLDER,
        campuri_cheie=[Camp("cheia_homofonic", "1234")],
        alfabet=alfabet.LATIN,
        pastreaza_restul=False,
        text_cifrat_numeric=True,
    ).mainloop()
