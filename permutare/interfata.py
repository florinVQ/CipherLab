"""Mini-aplicatia Cifrul cu permutare: interfata. Criptarea se face in motor.cpp."""

from __future__ import annotations

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet  # noqa: E402
import teorie  # noqa: E402
from fereastra_cifru import NUMERE, AplicatieCifru, Camp  # noqa: E402

TEORIE_PERMUTARE = {
    "ro": """
# Ce este?
Cifrul cu permutare (o transpoziție) nu schimbă caracterele, doar ordinea lor. Textul se taie în blocuri de câte n caractere, iar în fiecare bloc caracterele se reașază după o permutare π a numerelor 1, 2, ..., n.

# Criptarea
Pe poziția i din blocul criptat ajunge caracterul de pe poziția π(i) din blocul clar:
    e(x1, x2, ..., xn) = (xπ(1), xπ(2), ..., xπ(n))
Dacă ultimul bloc are mai puțin de n caractere, se completează cu ultimul caracter al alfabetului.

# Decriptarea
Se aplică permutarea inversă π⁻¹: dacă π(i) = j, atunci π⁻¹(j) = i. Aplicația o calculează singură, așa că la decriptare scrii aceeași permutare ca la criptare.

# Exemplu
π = (3 1 4 2), deci π⁻¹ = (2 4 1 3).
    CRIP TARE  ->  ICPR RTEA
În primul bloc poziția 1 primește x3 = I, poziția 2 primește x1 = C, poziția 3 primește x4 = P, iar poziția 4 primește x2 = R.

# Securitate
Frecvențele literelor rămân exact cele din textul clar, deci un criptanalist vede repede că are de-a face cu o transpoziție. Pentru blocuri de n caractere există n! chei; pentru n = 4 sunt doar 24.

# Cum folosești aplicația
Scrii permutarea ca numere despărțite prin spațiu, de exemplu 3 1 4 2. Din text rămân doar caracterele care sunt în alfabet.
""",
    "en": """
# What is it?
The permutation cipher (a transposition) does not change the characters, only their order. The text is cut into blocks of n characters, and inside every block the characters are rearranged by a permutation π of the numbers 1, 2, ..., n.

# Encryption
Position i of the encrypted block receives the character from position π(i) of the plain block:
    e(x1, x2, ..., xn) = (xπ(1), xπ(2), ..., xπ(n))
If the last block is shorter than n, it is filled with the last character of the alphabet.

# Decryption
The inverse permutation π⁻¹ is applied: if π(i) = j, then π⁻¹(j) = i. The app works it out, so for decryption you type the same permutation as for encryption.

# Example
π = (3 1 4 2), so π⁻¹ = (2 4 1 3).
    CRIP TARE  ->  ICPR RTEA
In the first block position 1 gets x3 = I, position 2 gets x1 = C, position 3 gets x4 = P and position 4 gets x2 = R.

# Security
Letter frequencies stay exactly as in the plain text, so a cryptanalyst quickly sees it is a transposition. Blocks of n characters give n! keys; for n = 4 that is only 24.

# How to use the app
Type the permutation as numbers separated by spaces, for example 3 1 4 2. Only the characters found in the alphabet are kept from the text.
""",
    "ru": """
# Что это?
Шифр перестановки не меняет символы, а только их порядок. Текст разбивается на блоки по n символов, и в каждом блоке символы переставляются согласно перестановке π чисел 1, 2, ..., n.

# Шифрование
На позицию i зашифрованного блока ставится символ с позиции π(i) открытого блока:
    e(x1, x2, ..., xn) = (xπ(1), xπ(2), ..., xπ(n))
Если в последнем блоке меньше n символов, он дополняется последним символом алфавита.

# Расшифровка
Применяется обратная перестановка π⁻¹: если π(i) = j, то π⁻¹(j) = i. Приложение вычисляет её само, поэтому для расшифровки вводится та же перестановка, что и для шифрования.

# Пример
π = (3 1 4 2), значит π⁻¹ = (2 4 1 3).
    CRIP TARE  ->  ICPR RTEA
В первом блоке позиция 1 получает x3 = I, позиция 2 — x1 = C, позиция 3 — x4 = P, позиция 4 — x2 = R.

# Стойкость
Частоты букв остаются такими же, как в открытом тексте, поэтому криптоаналитик быстро видит, что это перестановка. Для блоков по n символов существует n! ключей; при n = 4 их всего 24.

# Как пользоваться приложением
Введите перестановку числами через пробел, например 3 1 4 2. Из текста остаются только символы, которые есть в алфавите.
""",
}

teorie.TEORIE["permutare"] = TEORIE_PERMUTARE

if __name__ == "__main__":
    AplicatieCifru(
        FOLDER,
        campuri_cheie=[Camp("permutarea", "3 1 4 2", tip=NUMERE)],
        alfabet=alfabet.LATIN,
        pastreaza_restul=False,
    ).mainloop()
