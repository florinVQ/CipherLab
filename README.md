# CriptoLab

A desktop app for classical cryptography. It covers the encryption systems from a university cryptography course: you type a text and a key, and the app shows the result together with the calculation step by step.

The interface is written in Python (tkinter) and available in Romanian, English and Russian, with a dark and a light theme. The calculations run in C++: every cipher has its own `motor.cpp`.

## What's inside

| Cipher | Type | Notes |
|---|---|---|
| Caesar | monoalphabetic | brute-force attack over all keys |
| Caesar with keyword | monoalphabetic | attack with a list of suspected keywords |
| Affine | monoalphabetic | C = (a·P + b) mod m, brute-force attack |
| Polybius square | monoalphabetic | square size follows the alphabet |
| Homophonic | homophonic | common letters get several numbers |
| Vigenère | polyalphabetic | |
| Keystreams | stream | synchronous (keyword, Fibonacci, number sequence) and asynchronous (self-synchronizing), with a step table |
| Hill | polygraphic | n×n matrix, n = 2–10 |
| Playfair | polygraphic | rectangle built from the keyword |
| Permutation cipher | transposition | |
| Richelieu | transposition | segments with their own permutations, e.g. (2 3 1)(4 1 5 3 2)(2 1) |
| Exponential encryption | exponential | Y = M^e mod p, modular exponentiation shown step by step |
| Vigenère cryptanalysis | cryptanalysis | Kasiski test, index of coincidence, frequencies per line, every possible key ranked |

Every cipher works with an alphabet you choose (A-Z, Romanian letters, Cyrillic, digits, symbols), typed in or read from a file. `m` is counted automatically and all calculations are done modulo `m`.

## Download

Ready-made Windows builds are on the [Releases](https://github.com/florinVQ/CipherLab/releases) page. Unzip, then run `CriptoLab.exe`. Keep the `_internal` folder next to it. The computer running it needs neither Python nor a C++ compiler.

## Running from source

```
git clone https://github.com/florinVQ/CipherLab.git
cd CipherLab
py main.py
```

Requirements: Python 3.7+ with tkinter, and `g++` (MinGW-w64 on Windows) in `PATH`. Each C++ engine is compiled the first time its cipher is used.

## Building CriptoLab.exe

On Windows, double-click `construieste.bat`, or run:

```
py construieste.py
```

The script compiles every engine statically (`-static`, so no MinGW DLLs are needed), installs PyInstaller if missing and packages the app. The output:

- `dist/CriptoLab/CriptoLab.exe` together with its `_internal` folder
- `dist/CriptoLab-windows.zip`, the same folder zipped

### GitHub Actions

`.github/workflows/construieste-exe.yml` builds the exe on a Windows runner on every push to `main`. You can also start it by hand from **Actions → Construieste CriptoLab.exe → Run workflow**. The result is in the run's **Artifacts** (`CriptoLab-windows`).

Pushing a tag starting with `v` also publishes the zip on the Releases page:

```
git tag v1.0
git push origin v1.0
```

## Project layout

```
main.py                  main menu
comun/                   shared code: window, alphabet, themes, translations, theory texts
<cipher>/interfata.py    the window of one cipher
<cipher>/motor.cpp       its C++ engine (reads stdin, writes stdout)
construieste.py          builds the exe
```

The Python side sends the engine the command, the key, the alphabet and the text, one per line. Each alphabet character is passed as a one-byte code (the first character is `chr(33)`, the second `chr(34)` and so on), so the engines handle Romanian or Cyrillic letters the same way as A-Z.
