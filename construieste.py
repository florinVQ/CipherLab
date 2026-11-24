"""Construieste CriptoLab.exe (Windows) intr-un folder, cu tot ce ii trebuie.

    py construieste.py

1. compileaza fiecare motor.cpp intr-un motor.exe legat static (nu cere g++ sau DLL-uri
   pe calculatorul pe care ruleaza aplicatia);
2. impacheteaza aplicatia cu PyInstaller in dist/CriptoLab/ (CriptoLab.exe + folderul _internal);
3. face si arhiva dist/CriptoLab-windows.zip, gata de trimis.

Cere: Python 3.8+, g++ (MinGW) in PATH; PyInstaller se instaleaza singur daca lipseste.
Merge si pe Linux (pentru verificare): atunci rezulta un executabil Linux.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

RADACINA = Path(__file__).resolve().parent
NUME = "CriptoLab"
PE_WINDOWS = os.name == "nt"
# Modulele din comun/ si din biblioteca standard pe care le folosesc ferestrele cifrurilor.
# PyInstaller vede doar ce importa main.py, iar ferestrele se incarca abia la deschidere.
MODULE_ASCUNSE = ["fereastra_cifru", "alfabet", "motor_cpp", "teorie", "bara_setari", "setari",
                  "tema", "traduceri", "collections", "re", "unicodedata", "json", "runpy",
                  "tkinter.filedialog", "tkinter.ttk"]


def foldere_cifruri() -> list[Path]:
    return sorted(f for f in RADACINA.iterdir() if (f / "interfata.py").exists())


def compileaza_motoarele() -> None:
    if shutil.which("g++") is None:
        sys.exit("Nu gasesc g++. Instaleaza MinGW-w64 si adauga folderul lui bin in PATH.")
    for folder in foldere_cifruri():
        executabil = folder / ("motor.exe" if PE_WINDOWS else "motor")
        comanda = ["g++", "-O2", "-o", str(executabil), str(folder / "motor.cpp")]
        if PE_WINDOWS:
            comanda.insert(2, "-static")  # libstdc++ inclus in exe, nu ca DLL separat
        print("compilez", folder.name)
        subprocess.run(comanda, check=True)


def asigura_pyinstaller() -> None:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)


def impacheteaza() -> Path:
    date = [f"{folder}{os.pathsep}{folder.name}" for folder in [*foldere_cifruri(), RADACINA / "comun"]]
    comanda = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed",
               "--name", NUME, "--paths", str(RADACINA / "comun"),
               "--distpath", str(RADACINA / "dist"), "--workpath", str(RADACINA / "build"),
               "--specpath", str(RADACINA / "build")]
    for modul in MODULE_ASCUNSE:
        comanda += ["--hidden-import", modul]
    for pereche in date:
        comanda += ["--add-data", pereche]
    comanda.append(str(RADACINA / "main.py"))
    subprocess.run(comanda, check=True)

    folder = RADACINA / "dist" / NUME
    arhiva = shutil.make_archive(str(RADACINA / "dist" / f"{NUME}-windows"), "zip", folder.parent, NUME)
    print(f"\nGata: {folder / (NUME + ('.exe' if PE_WINDOWS else ''))}\nArhiva: {arhiva}")
    return folder


if __name__ == "__main__":
    compileaza_motoarele()
    asigura_pyinstaller()
    impacheteaza()
