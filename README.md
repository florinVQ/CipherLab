# CriptoLab

Aplicație pentru sisteme de criptare clasice: Cezar, Cezar cu cheie, afin, Polibius, homofonic, Vigenère, chei fluide, Hill, Playfair, cifrul cu permutare, Richelieu, criptarea exponențială și criptanaliza Vigenère. Interfața e în Python (tkinter), iar calculele se fac în C++ (`motor.cpp` din fiecare folder).

## Pornire din cod

```
py main.py
```

Ai nevoie de Python 3.7+ și de g++ (MinGW) în PATH. Fiecare motor se compilează singur la prima folosire.

## CriptoLab.exe pe calculatorul tău (Windows)

Dublu-clic pe `construieste.bat` sau, în terminal:

```
py construieste.py
```

Rezultatul e în `dist\CriptoLab\`. Pornești `CriptoLab.exe`. Folderul `_internal` de lângă el trebuie să rămână acolo. Tot în `dist\` apare și `CriptoLab-windows.zip`, cu tot folderul, gata de trimis.

Calculatorul pe care rulează exe-ul nu are nevoie de Python sau de g++: motoarele vin deja compilate.

## CriptoLab.exe făcut de GitHub

1. Pui proiectul pe GitHub (cu tot cu folderul `.github`).
2. La fiecare `push` pe `main`, GitHub construiește exe-ul singur. Îl poți porni și manual: **Actions → Construieste CriptoLab.exe → Run workflow**.
3. Când rularea are bifa verde, o deschizi și descarci **CriptoLab-windows** din secțiunea **Artifacts**.
4. Dacă faci un tag (de exemplu `v1.0`), arhiva apare și la **Releases**:

```
git tag v1.0
git push origin v1.0
```
