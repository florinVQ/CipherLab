# CipherLab

An educational desktop app with 7 classic ciphers: **Caesar, Keyed Caesar, Affine, Polybius, Homophonic, Vigenère, Hill**.
The interface is written in **Python (tkinter)**; encryption, decryption and the brute-force attack are written in **C++**.
The app works in **Romanian, English and Russian**, in **light or dark mode** (buttons RO / EN / RU and the theme button in the top-right corner; your choice is remembered).

## 1. What you need

| Requirement | Windows | Linux | macOS |
|---|---|---|---|
| Python 3.9+ (tkinter is included) | python.org installer (tick "Add to PATH") | `sudo apt install python3 python3-tk` | python.org installer |
| A C++ compiler (`g++`) | install [MSYS2](https://www.msys2.org/) or WinLibs and add `g++` to PATH | `sudo apt install g++` | `xcode-select --install` |

Check in a terminal: `python --version` and `g++ --version` (use `python3` on Linux/macOS).

## 2. How to start

1. Unzip `CriptoLab.zip`.
2. Open a terminal in the `CriptoLab` folder and run:

       python main.py

3. Click a cipher card in the main menu. Its mini-app opens in a new window.
4. The first time, the cipher's `motor.cpp` is compiled automatically (about a second). It is recompiled by itself whenever you edit it.

Each mini-app can also be started alone, for example `python cezar/interfata.py`.

## 3. Project structure

    main.py                  main menu (cards, basic terminology)
    comun/                   Python code shared by all ciphers
        fereastra_cifru.py     window with tabs (theory, encryption, decryption, attack)
        traduceri.py           app texts in RO / EN / RU
        teorie.py              theory texts of every cipher in RO / EN / RU
        tema.py                the two themes (colors, fonts, style)
        setari.py, bara_setari.py   chosen language and theme
        motor_cpp.py           compiles and calls the C++ engine
    cezar/ cezar_cheie/ afin/ polibius/ homofonic/ vigenere/ hill/
        interfata.py           the cipher's interface (Python): only the key fields
        motor.cpp              the cipher algorithm (C++): simple, arrays only, no vector

Every cipher folder = exactly 2 files: `interfata.py` + `motor.cpp`.

## 4. How to use a mini-app

Every window has tabs:

- **Theoretical notions** – explanation of the cipher with formulas and examples.
- **Encryption** – type (or load from a .txt file) the plain text, fill in the key, press *Encrypt*. The result appears below and can be saved to a file.
- **Decryption** – the same, in reverse.
- **Brute-force attack** – only for Caesar, Keyed Caesar and Affine. Paste a ciphertext; the app lists all possible keys with the decrypted text. The most text-like line is shown first.

Text rules: diacritics are replaced automatically (ă→a, ș→s...) and text is made uppercase; only the letters A-Z are used.
Caesar, Keyed Caesar, Affine and Vigenère keep spaces and punctuation. Polybius, Homophonic and Hill keep only letters, so the result has no spaces.

### Keys of each cipher

| Cipher | Key | Notes |
|---|---|---|
| Caesar | shift `k` | any integer |
| Keyed Caesar | keyword + shift `k` | the new alphabet starts with the keyword (no repeated letters); the attack takes a comma-separated list of guessed words, e.g. `ION,MARIA`, and tries all 26 shifts for each |
| Affine | `a` and `b` | `a` must be coprime with 26 (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25); the attack tries all 312 keys |
| Vigenère | keyword | letters only |
| Polybius | keyword | 5×5 square, J = I; keyword `A` gives the standard square |
| Homophonic | number 0–9999 | the number decides how the 100 codes are shuffled and shared between letters |

## 5. Hill cipher – step by step

The Hill cipher encrypts **blocks of n characters** with an **n × n matrix**, all calculations being done **modulo m**.
In this app **you provide**: the alphabet, the modular number `m`, the size `n` and the matrix. The program does **not** compute the inverse matrix.

### What you enter

1. **Alphabet** – type it in the *Alphabet* box (default `ABCDEFGHIJKLMNOPQRSTUVWXYZ`) or press *Read alphabet from file* (a .txt file whose first line is the alphabet).
   It can contain any characters (for example the Russian alphabet), up to 90, with no repeated characters.
2. **Modular number m** – equal to the number of characters of the alphabet (26 for A-Z). It fills in by itself when you change the alphabet. If you change it by hand and it differs from the alphabet length, you get an error.
3. **Size n** – choose 2, 4, 6 or 8 (even numbers).
   - n = 2 or 4: the matrix is written in boxes.
   - n = 6 or 8: the matrix is written in a text area (numbers separated by spaces or commas, row by row).
   - Always possible: *Read matrix from file* – a .txt file with n × n numbers (n is detected from how many numbers there are).
4. **Matrix**
   - **Encryption tab:** the *key matrix K*.
   - **Decryption tab:** the *modular inverse matrix K⁻¹* – the matrix created with the same modular number m, so that `K · K⁻¹ = I (mod m)`.

Negative numbers are allowed (they are reduced modulo m).

### How to find K⁻¹ (done by you, outside the app)

    det = det(K) mod m
    d   = the number with  det · d = 1 (mod m)     (the inverse of det modulo m)
    K⁻¹ = d · adjugate(K)  (mod m)

K⁻¹ exists only if `det` is coprime with `m` (for m = 26: det is not even and not divisible by 13).
The adjugate is the transpose of the cofactor matrix.

### Formulas

    Encryption:  C = K  · P  (mod m)
    Decryption:  P = K⁻¹ · C  (mod m)

Every character gets its position in the alphabet (first = 0, ..., last = m − 1). If the number of characters is not divisible by n, the **last character of the alphabet** is added to complete the last block.
Only characters found in the alphabet are used; lowercase letters are converted to uppercase when the alphabet has uppercase letters.

### Worked examples (alphabet A-Z, m = 26)

**2 × 2**

    K   = [3 3 ; 2 5]          det = 9, d = 3 (9·3 = 27 = 1 mod 26)
    K⁻¹ = [15 17 ; 20 9]       check: 3·15 + 3·20 = 105 = 1 (mod 26)
    HELP --K--> HIAT --K⁻¹--> HELP

**4 × 4**

    K   = [4 1 3 5 ; 4 3 6 2 ; 3 4 3 2 ; 2 1 6 1]
    K⁻¹ = [9 16 23 7 ; 18 3 22 16 ; 3 22 8 3 ; 24 15 14 5]
    HELP --K--> KGWV

Choosing a new n fills in a valid example (for A-Z, m = 26) that you can edit. For n = 6 and 8 the example is built from 4×4 and 2×2 blocks; for another alphabet or another m you must enter your own matrix.

### Common errors

| Message | What to do |
|---|---|
| The alphabet must have 2 to 90 characters, with no repeated characters | remove duplicates / shorten the alphabet |
| The modular number m must equal the number of characters in the alphabet | set m = alphabet length |
| The matrix needs n × n numbers | write exactly n² numbers |
| The text contains no character from the alphabet | check the text against the alphabet |
| Garbled result after decryption | K⁻¹ is not the inverse of K modulo this m, or m / alphabet differ from those used for encryption |

## 6. The C++ engines in a terminal

Each engine reads its data from standard input (one item per line); the exact format is written in the comments at the top of every `motor.cpp`.

    g++ -o cezar/motor cezar/motor.cpp
    printf 'cripteaza\n3\nATAC LA ZORI\n' | ./cezar/motor        # Caesar, k = 3
    printf 'atac\nDWDF OD CRUL\n' | ./cezar/motor                # brute-force attack

Hill (encrypt, n = 2, m = 26, matrix `3 3 2 5`, then alphabet, then text):

    g++ -o hill/motor hill/motor.cpp
    printf 'cripteaza\n2\n26\n3\n3\n2\n5\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nHELP\n' | ./hill/motor     # prints HIAT

Errors are printed on stderr as short codes (for example `hill_modul`, `afin_a`).
