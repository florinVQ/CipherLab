"""Mini-aplicatia Cifrul Richelieu: interfata. Criptarea se face in motor.cpp."""

from __future__ import annotations

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet  # noqa: E402
import teorie  # noqa: E402
from fereastra_cifru import PERMUTARI, AplicatieCifru, Camp  # noqa: E402

TEORIE_RICHELIEU = {
    "ro": """
# Ce este?
Cifrul Richelieu, numit după cardinalul Richelieu (secolul al XVII-lea), este o transpoziție cu mai multe permutări. Cheia este un șir de permutări de lungimi diferite, scrise între paranteze, de exemplu (2 3 1)(4 1 5 3 2)(2 1).

# Criptarea
Textul se împarte în segmente: primul are lungimea primei permutări, al doilea lungimea celei de-a doua și așa mai departe. Fiecare segment se reașază cu permutarea lui, la fel ca la cifrul cu permutare:
    y[i] = x[π(i)]
Când textul e mai lung decât suma lungimilor, permutările se reiau de la prima. Ultimul segment se completează cu ultimul caracter al alfabetului.

# Decriptarea
Fiecare segment se reașază cu inversa permutării lui. Scrii aceeași cheie ca la criptare; inversarea o face aplicația.

# Exemplu
Cheia (2 3 1)(4 1 5 3 2)(2 1) are lungimile 3 + 5 + 2 = 10.
    PRO FESOR UL  ->  ROP OFRSE LU
Segmentul FESOR cu (4 1 5 3 2): x4 = O, x1 = F, x5 = R, x3 = S, x2 = E.

# Securitate
Literele rămân aceleași, deci analiza frecvențelor arată imediat că e o transpoziție. Cheia se ghicește mai greu decât o singură permutare, pentru că segmentele au lungimi diferite.

# Cum folosești aplicația
Scrii cheia ca permutări între paranteze. În paranteză numerele se despart prin spațiu sau virgulă; (2314) scris fără spații se citește cifră cu cifră.
""",
    "en": """
# What is it?
The Richelieu cipher, named after Cardinal Richelieu (17th century), is a transposition with several permutations. The key is a sequence of permutations of different lengths, written in brackets, for example (2 3 1)(4 1 5 3 2)(2 1).

# Encryption
The text is cut into segments: the first one as long as the first permutation, the second as long as the second one, and so on. Every segment is rearranged with its own permutation, as in the permutation cipher:
    y[i] = x[π(i)]
When the text is longer than the sum of the lengths, the permutations start again from the first. The last segment is filled with the last character of the alphabet.

# Decryption
Every segment is rearranged with the inverse of its permutation. You type the same key as for encryption; the app does the inversion.

# Example
The key (2 3 1)(4 1 5 3 2)(2 1) has the lengths 3 + 5 + 2 = 10.
    PRO FESOR UL  ->  ROP OFRSE LU
Segment FESOR with (4 1 5 3 2): x4 = O, x1 = F, x5 = R, x3 = S, x2 = E.

# Security
The letters stay the same, so frequency analysis shows right away that it is a transposition. The key is harder to guess than a single permutation, because the segments have different lengths.

# How to use the app
Type the key as permutations in brackets. Inside a bracket separate the numbers with spaces or commas; (2314) written without spaces is read digit by digit.
""",
    "ru": """
# Что это?
Шифр Ришелье, названный в честь кардинала Ришелье (XVII век), — это перестановка с несколькими перестановочными ключами. Ключ — последовательность перестановок разной длины в скобках, например (2 3 1)(4 1 5 3 2)(2 1).

# Шифрование
Текст делится на отрезки: первый длиной в первую перестановку, второй — во вторую и так далее. Каждый отрезок переставляется своей перестановкой, как в шифре перестановки:
    y[i] = x[π(i)]
Если текст длиннее суммы длин, перестановки начинаются снова с первой. Последний отрезок дополняется последним символом алфавита.

# Расшифровка
Каждый отрезок переставляется обратной перестановкой. Вводится тот же ключ, что и для шифрования; обращение выполняет приложение.

# Пример
У ключа (2 3 1)(4 1 5 3 2)(2 1) длины 3 + 5 + 2 = 10.
    PRO FESOR UL  ->  ROP OFRSE LU
Отрезок FESOR с (4 1 5 3 2): x4 = O, x1 = F, x5 = R, x3 = S, x2 = E.

# Стойкость
Буквы остаются прежними, поэтому частотный анализ сразу показывает, что это перестановка. Ключ угадать труднее, чем одну перестановку, потому что отрезки разной длины.

# Как пользоваться приложением
Введите ключ как перестановки в скобках. Внутри скобок числа разделяются пробелом или запятой; (2314) без пробелов читается по одной цифре.
""",
}

teorie.TEORIE["richelieu"] = TEORIE_RICHELIEU

if __name__ == "__main__":
    AplicatieCifru(
        FOLDER,
        campuri_cheie=[Camp("permutarile", "(2 3 1)(4 1 5 3 2)(2 1)", tip=PERMUTARI)],
        alfabet=alfabet.LATIN,
        pastreaza_restul=False,
    ).mainloop()
