"""Mini-aplicatia Playfair: interfata. Criptarea se face in motor.cpp."""

from __future__ import annotations

import sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet  # noqa: E402
import teorie  # noqa: E402
import traduceri  # noqa: E402
from fereastra_cifru import TEXT, AplicatieCifru, Camp  # noqa: E402

TEORIE_PLAYFAIR = {
    "ro": """
# Ce este?
Cifrul Playfair a fost inventat de Charles Wheatstone în 1854 și poartă numele lordului Playfair, care l-a popularizat. Criptează perechi de litere, nu litere singure. Cheia este un cuvânt cu care se completează un pătrat 5 × 5.

# Pătratul
Se scriu literele cuvântului-cheie, fără repetări, apoi restul alfabetului. A-Z are 26 de litere, dar pătratul doar 25 de căsuțe, așa că J se scrie ca I. Cu cuvântul PLAYFAIR EXAMPLE:
    P L A Y F
    I R E X M
    B C D G H
    K N O Q S
    T U V W Z

# Pregătirea textului
Textul se împarte în perechi. Când o pereche ar avea două litere la fel (EE), între ele intră caracterul de completare, de obicei X. Dacă la sfârșit rămâne o literă singură, primește și ea un X.

# Criptarea
    aceeași linie: fiecare literă trece în cea din dreapta ei
    aceeași coloană: fiecare literă trece în cea de dedesubt
    altfel: literele sunt colțurile unui dreptunghi; fiecare ia litera de pe rândul ei, din coloana celeilalte
La capătul rândului sau al coloanei se continuă de la început.

# Decriptarea
Aceleași reguli, dar spre stânga și în sus. X-urile adăugate rămân în textul decriptat; le recunoști ușor la citire.

# Exemplu
    HI DE TH EG OL DI NT HE TR EX ES TU MP
    BM OD ZB XD NA BE KU DM UI XM MO UV IF
Perechea EE din TREE a devenit EX ES.

# Cum folosești aplicația
Scrii cuvântul-cheie și caracterul de completare. Caracterele alfabetului trebuie să umple exact un dreptunghi: 25 = 5 × 5, 30 = 5 × 6, 36 = 6 × 6 (A-Z plus cifrele). Din text rămân doar caracterele din alfabet.
""",
    "en": """
# What is it?
The Playfair cipher was invented by Charles Wheatstone in 1854 and carries the name of Lord Playfair, who promoted it. It encrypts pairs of letters instead of single letters. The key is a word used to fill a 5 × 5 square.

# The square
Write the letters of the keyword without repeats, then the rest of the alphabet. A-Z has 26 letters but the square only 25 cells, so J is written as I. With the keyword PLAYFAIR EXAMPLE:
    P L A Y F
    I R E X M
    B C D G H
    K N O Q S
    T U V W Z

# Preparing the text
The text is split into pairs. When a pair would have two equal letters (EE), the filler character, usually X, goes between them. If a single letter is left at the end, it also gets an X.

# Encryption
    same row: each letter becomes the one to its right
    same column: each letter becomes the one below it
    otherwise: the letters are corners of a rectangle; each takes the letter in its own row and the other's column
At the end of a row or column you wrap around to the start.

# Decryption
The same rules, but to the left and upwards. The added X letters stay in the decrypted text; they are easy to spot when reading.

# Example
    HI DE TH EG OL DI NT HE TR EX ES TU MP
    BM OD ZB XD NA BE KU DM UI XM MO UV IF
The pair EE in TREE became EX ES.

# How to use the app
Type the keyword and the filler character. The alphabet must fill a rectangle exactly: 25 = 5 × 5, 30 = 5 × 6, 36 = 6 × 6 (A-Z plus digits). Only the characters found in the alphabet are kept from the text.
""",
    "ru": """
# Что это?
Шифр Плейфера изобрёл Чарльз Уитстон в 1854 году, а назван он в честь лорда Плейфера, который его продвигал. Шифруются пары букв, а не отдельные буквы. Ключ — слово, которым заполняется квадрат 5 × 5.

# Квадрат
Сначала записываются буквы ключевого слова без повторов, затем остальные буквы алфавита. В A-Z 26 букв, а в квадрате 25 клеток, поэтому J записывается как I. С ключом PLAYFAIR EXAMPLE:
    P L A Y F
    I R E X M
    B C D G H
    K N O Q S
    T U V W Z

# Подготовка текста
Текст делится на пары. Если в паре две одинаковые буквы (EE), между ними вставляется символ-заполнитель, обычно X. Если в конце остаётся одна буква, к ней тоже добавляется X.

# Шифрование
    одна строка: каждая буква заменяется соседней справа
    один столбец: каждая буква заменяется буквой под ней
    иначе: буквы — углы прямоугольника; каждая берёт букву из своей строки и столбца другой
В конце строки или столбца переходим к началу.

# Расшифровка
Те же правила, но влево и вверх. Добавленные X остаются в расшифрованном тексте; при чтении их легко заметить.

# Пример
    HI DE TH EG OL DI NT HE TR EX ES TU MP
    BM OD ZB XD NA BE KU DM UI XM MO UV IF
Пара EE в слове TREE стала EX ES.

# Как пользоваться приложением
Введите ключевое слово и символ-заполнитель. Символы алфавита должны точно заполнить прямоугольник: 25 = 5 × 5, 30 = 5 × 6, 36 = 6 × 6 (A-Z и цифры). Из текста остаются только символы алфавита.
""",
}

teorie.TEORIE["playfair"] = TEORIE_PLAYFAIR
traduceri.adauga_texte({
    "ro": {"eroare_playfair_impar": "Textul criptat trebuie să aibă un număr par de caractere din alfabet."},
    "en": {"eroare_playfair_impar": "The encrypted text must have an even number of alphabet characters."},
    "ru": {"eroare_playfair_impar": "В шифртексте должно быть чётное число символов алфавита."},
})

if __name__ == "__main__":
    AplicatieCifru(
        FOLDER,
        campuri_cheie=[Camp("cuvant_cheie", "PLAYFAIR EXAMPLE", tip=TEXT),
                       Camp("completare", "X", tip=TEXT)],
        alfabet=alfabet.LATIN_FARA_J,
        pastreaza_restul=False,
        inlocuiri={"J": "I"},
    ).mainloop()
