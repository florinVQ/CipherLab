"""Mini-aplicatia Hill (matrice n x n): interfata. Criptarea se face in motor.cpp.

Foloseste fereastra comuna din ../comun si ii adauga doar ce e specific cifrului Hill:
alfabetul, numarul modular m, dimensiunea n si matricea (cheia sau matricea modular inversa).
"""

from __future__ import annotations

import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import teorie  # noqa: E402
import tema  # noqa: E402
import traduceri  # noqa: E402
from fereastra_cifru import COMENZI, AplicatieCifru  # noqa: E402
from motor_cpp import EroareMotor, pregateste, ruleaza_motor  # noqa: E402
from traduceri import t  # noqa: E402

MAX_N = 10                  # la fel ca in motor.cpp
DIMENSIUNI = tuple(range(2, MAX_N + 1))
N_CU_CASETE = 4             # pana la n = 4 matricea se scrie in casete, peste 4 intr-o zona de text
ALFABET_LATIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_CARACTERE = 90          # fiecare caracter al alfabetului primeste un cod 33, 34, ... in motor
PRIMUL_COD = 33

# Exemple valide pentru alfabetul latin (m = 26): matricea cheie si matricea ei modular inversa.
CHEIE_2 = [[3, 3], [2, 5]]
INVERSA_2 = [[15, 17], [20, 9]]
CHEIE_4 = [[4, 1, 3, 5], [4, 3, 6, 2], [3, 4, 3, 2], [2, 1, 6, 1]]
INVERSA_4 = [[9, 16, 23, 7], [18, 3, 22, 16], [3, 22, 8, 3], [24, 15, 14, 5]]
CHEIE_1 = [[1]]


def blocuri_pentru(n: int) -> tuple[list, list]:
    """Imparte n in blocuri 4x4, 2x2 si 1x1 (valide mod 26) si intoarce listele de chei si de inverse."""
    chei, inverse = [], []
    ramas = n
    for marime, cheie, inversa in ((4, CHEIE_4, INVERSA_4), (2, CHEIE_2, INVERSA_2), (1, CHEIE_1, CHEIE_1)):
        while ramas >= marime:
            chei.append(cheie)
            inverse.append(inversa)
            ramas -= marime
    return chei, inverse


TEXTE_HILL = {
    "ro": {
        "titlu_hill": "Sistemul simetric de criptare Hill (matrice n×n)",
        "hill_tab_date": "Date: alfabet și matrici",
        "hill_matrice_k": "Matricea cheie K (pentru criptare)",
        "hill_matrice_inv": "Matricea cheie inversă K⁻¹ (pentru decriptare)",
        "hill_verifica": "Verifică K · K⁻¹ = I",
        "hill_verificare_ok": "Corect: K · K⁻¹ = I (mod {m}).",
        "hill_verificare_gresit": "Atenție: K · K⁻¹ nu este matricea unitate (mod {m}).",
        "hill_foloseste_cr": "Se folosește matricea cheie K din tabul „Date”.",
        "hill_foloseste_dec": "Se folosește matricea modular inversă K⁻¹ din tabul „Date”.",
        "hill_setari": "Date de intrare",
        "hill_alfabet": "Alfabetul:",
        "hill_alfabet_fisier": "Citește alfabetul din fișier",
        "hill_numar_modular": "număr modular m =",
        "hill_dimensiune": "dimensiunea n:",
        "hill_matrice_fisier": "Citește matricea din fișier",
        "hill_indiciu_date": "m = numărul de caractere ale alfabetului. K⁻¹ este matricea modular inversă, creată cu același m: K · K⁻¹ = I (mod m). Programul nu o calculează; o introduci tu. Matricile se scriu în casete (n ≤ 4), într-o zonă de text (n > 4) sau se citesc din fișier.",
        "eroare_hill_dim": "Dimensiunea n trebuie să fie între 2 și 10.",
        "eroare_hill_modul": "Numărul modular m trebuie să fie egal cu numărul de caractere ale alfabetului.",
        "eroare_hill_alfabet": "Alfabetul trebuie să aibă între 2 și 90 de caractere, fără caractere repetate.",
        "eroare_hill_matrice": "Matricea trebuie să aibă {asteptat} numere (n × n), dar ai scris {gasite}.",
        "eroare_hill_fara_litere": "Textul nu conține niciun caracter din alfabet.",
    },
    "en": {
        "titlu_hill": "Hill symmetric encryption system (n×n matrix)",
        "hill_tab_date": "Data: alphabet and matrices",
        "hill_matrice_k": "Key matrix K (for encryption)",
        "hill_matrice_inv": "Inverse key matrix K⁻¹ (for decryption)",
        "hill_verifica": "Check K · K⁻¹ = I",
        "hill_verificare_ok": "Correct: K · K⁻¹ = I (mod {m}).",
        "hill_verificare_gresit": "Warning: K · K⁻¹ is not the identity matrix (mod {m}).",
        "hill_foloseste_cr": "The key matrix K from the \"Data\" tab is used.",
        "hill_foloseste_dec": "The modular inverse matrix K⁻¹ from the \"Data\" tab is used.",
        "hill_setari": "Input data",
        "hill_alfabet": "Alphabet:",
        "hill_alfabet_fisier": "Read alphabet from file",
        "hill_numar_modular": "modular number m =",
        "hill_dimensiune": "size n:",
        "hill_matrice_fisier": "Read matrix from file",
        "hill_indiciu_date": "m = the number of characters in the alphabet. K⁻¹ is the modular inverse matrix, created with the same m: K · K⁻¹ = I (mod m). The program does not calculate it; you enter it. Matrices are written in boxes (n ≤ 4), in a text area (n > 4) or read from a file.",
        "eroare_hill_dim": "The size n must be between 2 and 10.",
        "eroare_hill_modul": "The modular number m must equal the number of characters in the alphabet.",
        "eroare_hill_alfabet": "The alphabet must have 2 to 90 characters, with no repeated characters.",
        "eroare_hill_matrice": "The matrix needs {asteptat} numbers (n × n), but you wrote {gasite}.",
        "eroare_hill_fara_litere": "The text contains no character from the alphabet.",
    },
    "ru": {
        "titlu_hill": "Симметричная система шифрования: шифр Хилла (матрица n×n)",
        "hill_tab_date": "Данные: алфавит и матрицы",
        "hill_matrice_k": "Ключевая матрица K (для шифрования)",
        "hill_matrice_inv": "Обратная ключевая матрица K⁻¹ (для расшифровки)",
        "hill_verifica": "Проверить K · K⁻¹ = I",
        "hill_verificare_ok": "Верно: K · K⁻¹ = I (mod {m}).",
        "hill_verificare_gresit": "Внимание: K · K⁻¹ не является единичной матрицей (mod {m}).",
        "hill_foloseste_cr": "Используется ключевая матрица K из вкладки «Данные».",
        "hill_foloseste_dec": "Используется модулярно обратная матрица K⁻¹ из вкладки «Данные».",
        "hill_setari": "Входные данные",
        "hill_alfabet": "Алфавит:",
        "hill_alfabet_fisier": "Прочитать алфавит из файла",
        "hill_numar_modular": "модульное число m =",
        "hill_dimensiune": "размер n:",
        "hill_matrice_fisier": "Прочитать матрицу из файла",
        "hill_indiciu_date": "m = количество символов алфавита. K⁻¹ — модулярно обратная матрица, созданная с тем же m: K · K⁻¹ = I (mod m). Программа её не вычисляет, вы вводите её сами. Матрицы вводятся в клетках (n ≤ 4), в текстовой области (n > 4) или читаются из файла.",
        "eroare_hill_dim": "Размер n должен быть от 2 до 10.",
        "eroare_hill_modul": "Модульное число m должно быть равно количеству символов алфавита.",
        "eroare_hill_alfabet": "В алфавите должно быть от 2 до 90 символов, без повторов.",
        "eroare_hill_matrice": "В матрице должно быть {asteptat} чисел (n × n), а вы ввели {gasite}.",
        "eroare_hill_fara_litere": "В тексте нет ни одного символа из алфавита.",
    },
}

TEORIE_HILL = {
    "ro": """
# Ce este?
Cifrul Hill (Lester Hill, 1929) criptează caracterele în blocuri, nu unul câte unul. Dimensiunea blocului este n (de la 2 la 10), iar cheia este o matrice pătratică n × n. Alfabetul îl alegi tu: poate avea orice caractere, nu doar A-Z.

# Numărul modular m
m este numărul de caractere ale alfabetului (pentru A-Z, m = 26). Toate calculele se fac modulo m, iar fiecare caracter are un număr: primul din alfabet = 0, al doilea = 1, ..., ultimul = m - 1.

# Criptarea
Blocul de n caractere formează un vector P. El se înmulțește cu matricea cheie K, modulo m:
    C = K · P  (mod m)
    Ci = (ai1·P1 + ai2·P2 + ... + ain·Pn) mod m
Dacă numărul de caractere nu se împarte exact la n, se adaugă la final ultimul caracter al alfabetului.

# Decriptarea cu matricea modular inversă
Pentru decriptare matricea cheie este matricea modular inversă K⁻¹, creată cu același număr modular m:
    K · K⁻¹ = I  (mod m)
    P = K⁻¹ · C  (mod m)
Aplicația nu calculează inversa; o introduci tu (din casete, din text sau dintr-un fișier). Ca să o afli:
    det = det(K) mod m
    d = numărul cu det · d = 1 (mod m)
    K⁻¹ = d · adjuncta lui K  (mod m)
Inversa există doar dacă det este prim cu m (pentru m = 26: nu este par și nu se împarte la 13).

# Exemplu 2 × 2 (alfabet A-Z, m = 26)
K = [3 3 ; 2 5], iar K⁻¹ = [15 17 ; 20 9] (verificare: 3·15 + 3·20 = 105 = 1 mod 26).
    HELP  ->  HIAT   (cu K)
    HIAT  ->  HELP   (cu K⁻¹)

# Exemplu 4 × 4 (alfabet A-Z, m = 26)
K = [4 1 3 5 ; 4 3 6 2 ; 3 4 3 2 ; 2 1 6 1], iar K⁻¹ = [9 16 23 7 ; 18 3 22 16 ; 3 22 8 3 ; 24 15 14 5].
    HELP  ->  KGWV   (cu K)
Verificare: prima literă = 4·7 + 1·4 + 3·11 + 5·15 = 140, iar 140 mod 26 = 10, adică K.

# Cum folosești aplicația
1. Scrie alfabetul (sau citește-l dintr-un fișier). m se completează singur cu numărul de caractere.
2. Scrie n (2–10). Pentru n ≤ 4 matricile se scriu în casete; pentru n > 4 într-o zonă de text (numere separate prin spații sau virgule, rând cu rând) sau o citești dintr-un fișier.
3. În tabul „Date” scrii ambele matrici: matricea cheie K (folosită la criptare) și matricea modular inversă K⁻¹ (folosită la decriptare).
Din text se păstrează doar caracterele care se află în alfabet (literele mici se transformă în mari dacă alfabetul are litere mari).
""",
    "en": """
# What is it?
The Hill cipher (Lester Hill, 1929) encrypts characters in blocks, not one at a time. The block size is n (from 2 to 10), and the key is an n × n square matrix. You choose the alphabet: it can have any characters, not only A-Z.

# The modular number m
m is the number of characters in the alphabet (for A-Z, m = 26). All calculations are done modulo m, and every character has a number: the first in the alphabet = 0, the second = 1, ..., the last = m - 1.

# Encryption
A block of n characters forms a vector P. It is multiplied by the key matrix K, modulo m:
    C = K · P  (mod m)
    Ci = (ai1·P1 + ai2·P2 + ... + ain·Pn) mod m
If the number of characters is not divisible by n, the last character of the alphabet is added at the end.

# Decryption with the modular inverse matrix
For decryption the key matrix is the modular inverse matrix K⁻¹, created with the same modular number m:
    K · K⁻¹ = I  (mod m)
    P = K⁻¹ · C  (mod m)
The app does not calculate the inverse; you enter it (in boxes, as text or from a file). To find it:
    det = det(K) mod m
    d = the number with det · d = 1 (mod m)
    K⁻¹ = d · adjugate of K  (mod m)
The inverse exists only if det is coprime with m (for m = 26: not even and not divisible by 13).

# 2 × 2 example (alphabet A-Z, m = 26)
K = [3 3 ; 2 5], and K⁻¹ = [15 17 ; 20 9] (check: 3·15 + 3·20 = 105 = 1 mod 26).
    HELP  ->  HIAT   (with K)
    HIAT  ->  HELP   (with K⁻¹)

# 4 × 4 example (alphabet A-Z, m = 26)
K = [4 1 3 5 ; 4 3 6 2 ; 3 4 3 2 ; 2 1 6 1], and K⁻¹ = [9 16 23 7 ; 18 3 22 16 ; 3 22 8 3 ; 24 15 14 5].
    HELP  ->  KGWV   (with K)
Check: the first letter = 4·7 + 1·4 + 3·11 + 5·15 = 140, and 140 mod 26 = 10, which is K.

# How to use the app
1. Write the alphabet (or read it from a file). m fills in by itself with the number of characters.
2. Write n (2–10). For n ≤ 4 the matrices are written in boxes; for n > 4 in a text area (numbers separated by spaces or commas, row by row) or you read it from a file.
3. In the "Data" tab you write both matrices: the key matrix K (used for encryption) and the modular inverse matrix K⁻¹ (used for decryption).
Only the characters found in the alphabet are kept from the text (lowercase letters become uppercase if the alphabet has uppercase letters).
""",
    "ru": """
# Что это?
Шифр Хилла (Лестер Хилл, 1929) шифрует символы блоками, а не по одному. Размер блока — n (от 2 до 10), а ключ — квадратная матрица n × n. Алфавит выбираете вы: в нём могут быть любые символы, не только A-Z.

# Модульное число m
m — это количество символов алфавита (для A-Z m = 26). Все вычисления выполняются по модулю m, а у каждого символа есть номер: первый в алфавите = 0, второй = 1, ..., последний = m - 1.

# Шифрование
Блок из n символов образует вектор P. Он умножается на ключевую матрицу K по модулю m:
    C = K · P  (mod m)
    Ci = (ai1·P1 + ai2·P2 + ... + ain·Pn) mod m
Если число символов не делится нацело на n, в конец добавляется последний символ алфавита.

# Расшифровка с модулярно обратной матрицей
При расшифровке ключевая матрица — это модулярно обратная матрица K⁻¹, созданная с тем же модульным числом m:
    K · K⁻¹ = I  (mod m)
    P = K⁻¹ · C  (mod m)
Приложение не вычисляет обратную матрицу; вы вводите её сами (в клетках, текстом или из файла). Чтобы найти её:
    det = det(K) mod m
    d = число, для которого det · d = 1 (mod m)
    K⁻¹ = d · присоединённая матрица K  (mod m)
Обратная матрица существует, только если det взаимно прост с m (для m = 26: не чётный и не делится на 13).

# Пример 2 × 2 (алфавит A-Z, m = 26)
K = [3 3 ; 2 5], а K⁻¹ = [15 17 ; 20 9] (проверка: 3·15 + 3·20 = 105 = 1 mod 26).
    HELP  ->  HIAT   (с K)
    HIAT  ->  HELP   (с K⁻¹)

# Пример 4 × 4 (алфавит A-Z, m = 26)
K = [4 1 3 5 ; 4 3 6 2 ; 3 4 3 2 ; 2 1 6 1], а K⁻¹ = [9 16 23 7 ; 18 3 22 16 ; 3 22 8 3 ; 24 15 14 5].
    HELP  ->  KGWV   (с K)
Проверка: первая буква = 4·7 + 1·4 + 3·11 + 5·15 = 140, а 140 mod 26 = 10, то есть K.

# Как пользоваться приложением
1. Введите алфавит (или прочитайте его из файла). m подставится сам — по количеству символов.
2. Введите n (2–10). Для n ≤ 4 матрицы вводятся в клетках; для n > 4 — в текстовой области (числа через пробел или запятую, строка за строкой) или читается из файла.
3. На вкладке «Данные» вводятся обе матрицы: ключевая K (для шифрования) и модулярно обратная K⁻¹ (для расшифровки).
Из текста остаются только символы, которые есть в алфавите (строчные буквы становятся заглавными, если в алфавите заглавные).
""",
}

# Textele si teoria specifice cifrului Hill se adauga la cele comune (doar in acest proces).
for cod_limba, texte in TEXTE_HILL.items():
    traduceri.TEXTE[cod_limba].update(texte)
teorie.TEORIE["hill"] = TEORIE_HILL


def matrice_pentru(n: int, inversa: bool) -> list[list[int]]:
    """Matricea n x n de exemplu (cheie sau inversa), formata din blocuri 4x4, 2x2 si 1x1 pe diagonala."""
    chei, inverse = blocuri_pentru(n)
    blocuri = inverse if inversa else chei
    matrice = [[0] * n for _ in range(n)]
    start = 0
    for bloc in blocuri:
        for i, rand in enumerate(bloc):
            for j, valoare in enumerate(rand):
                matrice[start + i][start + j] = valoare
        start += len(bloc)
    return matrice


class AplicatieHill(AplicatieCifru):
    def __init__(self):
        super().__init__(FOLDER, campuri_cheie=[])
        self.potriveste_marimea(1080, 900)

    def _construieste(self) -> None:
        if not hasattr(self, "celule"):
            self._creeaza_variabile()
        super()._construieste()
        self._tab_date()

    # ---------- datele ----------

    def _creeaza_variabile(self) -> None:
        self.alfabet = tk.StringVar(value=ALFABET_LATIN)
        self.numar_modular = tk.StringVar(value=str(len(ALFABET_LATIN)))
        self.alfabet.trace_add("write", lambda *_: self.numar_modular.set(str(len(self.alfabet.get()))))
        self.dimensiune = tk.StringVar(value="2")
        # casetele matricii (pana la 4 x 4) si textul matricii (pentru n mai mare) la criptare / decriptare
        self.celule = {p: [[tk.StringVar() for _ in range(N_CU_CASETE)] for _ in range(N_CU_CASETE)]
                       for p in ("cr", "dec")}
        self.text_matrice = {"cr": "", "dec": ""}
        self.cadre_matrice = {}  # prefix -> cadrul in care se deseneaza matricea
        self._incarca_exemplul(2)

    def _incarca_exemplul(self, n: int) -> None:
        for prefix, inversa in (("cr", False), ("dec", True)):
            self._pune_matricea(prefix, matrice_pentru(n, inversa))

    def _pune_matricea(self, prefix: str, matrice: list[list[int]]) -> None:
        n = len(matrice)
        for i in range(N_CU_CASETE):
            for j in range(N_CU_CASETE):
                in_matrice = i < n and j < n
                self.celule[prefix][i][j].set(str(matrice[i][j]) if in_matrice else "")
        self.text_matrice[prefix] = "\n".join(" ".join(str(x) for x in rand) for rand in matrice)

    def _alege_dimensiunea(self) -> None:
        try:
            n = self._dimensiune_valida()
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        if getattr(self, "n_afisat", None) == n:
            return
        self.n_afisat = n
        self._incarca_exemplul(n)
        for prefix in self.cadre_matrice:
            self._deseneaza_matricea(prefix)

    # ---------- fereastra: tabul cu datele si taburile de criptare / decriptare ----------

    def _tab_date(self) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.insert(1, tab, text=t("hill_tab_date"))
        self.cadre_matrice = {}

        alfabet = ttk.LabelFrame(tab, text=t("hill_setari"), padding=10)
        alfabet.pack(fill="x")
        self._rand_alfabet(alfabet)
        self._rand_dimensiune(alfabet)
        ttk.Label(alfabet, text=t("hill_indiciu_date"), foreground=tema.TEXT_SLAB,
                  wraplength=980, justify="left").pack(fill="x", pady=(8, 0))

        matrici = ttk.Frame(tab)
        matrici.pack(fill="x", pady=(12, 0))
        for coloana, prefix in enumerate(("cr", "dec")):
            matrici.columnconfigure(coloana, weight=1, uniform="matrici")
            cadru = ttk.LabelFrame(matrici, text=t("hill_matrice_k" if prefix == "cr" else "hill_matrice_inv"),
                                   padding=10)
            cadru.grid(row=0, column=coloana, sticky="nsew", padx=(0, 8) if coloana == 0 else (8, 0))
            ttk.Button(cadru, text=t("hill_matrice_fisier"), cursor="hand2",
                       command=lambda p=prefix: self._citeste_matricea(p)).pack(anchor="e", pady=(0, 8))
            self.cadre_matrice[prefix] = ttk.Frame(cadru)
            self.cadre_matrice[prefix].pack(anchor="w")
            self._deseneaza_matricea(prefix)

        verificare = ttk.Frame(tab)
        verificare.pack(fill="x", pady=(12, 0))
        ttk.Button(verificare, text=t("hill_verifica"), cursor="hand2",
                   command=self._verifica_inversa).pack(side="left")

    def _tab_transformare(self, prefix: str) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t(f"{prefix}_tab"))
        intrare = tema.zona_text(tab, 6)
        iesire = tema.zona_text(tab, 6, doar_citire=True)
        self.zone[f"{prefix}_in"] = intrare
        self.zone[f"{prefix}_out"] = iesire

        self._rand_titlu(tab, t(f"{prefix}_intrare"), t(f"{prefix}_citeste"),
                         lambda: self._citeste_din_fisier(intrare))
        intrare.pack(fill="x")
        ttk.Label(tab, text=t(f"hill_foloseste_{prefix}"), foreground=tema.TEXT_SLAB).pack(anchor="w", pady=(10, 0))
        ttk.Button(tab, text=t(f"{prefix}_buton"), style="Accent.TButton", cursor="hand2",
                   command=lambda: self._transforma(prefix)).pack(anchor="e", pady=(0, 10))
        self._rand_titlu(tab, t(f"{prefix}_iesire"), t(f"{prefix}_scrie"),
                         lambda: self._scrie_in_fisier(iesire))
        iesire.pack(fill="both", expand=True)

    def _rand_alfabet(self, parinte) -> None:
        rand = ttk.Frame(parinte)
        rand.pack(fill="x")
        ttk.Label(rand, text=t("hill_alfabet"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 8))
        ttk.Entry(rand, textvariable=self.alfabet, font=tema.FONT_COD).pack(
            side="left", fill="x", expand=True, padx=(0, 12))
        ttk.Label(rand, text=t("hill_numar_modular")).pack(side="left", padx=(0, 6))
        ttk.Entry(rand, textvariable=self.numar_modular, width=5, justify="center").pack(side="left", padx=(0, 12))
        ttk.Button(rand, text=t("hill_alfabet_fisier"), cursor="hand2",
                   command=self._citeste_alfabetul).pack(side="left")

    def _rand_dimensiune(self, parinte) -> None:
        rand = ttk.Frame(parinte)
        rand.pack(fill="x", pady=(10, 0))
        ttk.Label(rand, text=t("hill_dimensiune"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 6))
        selector = ttk.Spinbox(rand, from_=2, to=MAX_N, textvariable=self.dimensiune, width=4,
                               justify="center", command=self._alege_dimensiunea)
        selector.pack(side="left")
        selector.bind("<Return>", lambda _eveniment: self._alege_dimensiunea())
        selector.bind("<FocusOut>", lambda _eveniment: self._alege_dimensiunea())

    def _deseneaza_matricea(self, prefix: str) -> None:
        """Casete pentru n <= 4, zona de text pentru n mai mare."""
        cadru = self.cadre_matrice[prefix]
        self.zone.pop(f"{prefix}_matrice", None)
        for element in cadru.winfo_children():
            element.destroy()
        n = int(self.dimensiune.get())
        if n <= N_CU_CASETE:
            for i in range(n):
                for j in range(n):
                    ttk.Entry(cadru, textvariable=self.celule[prefix][i][j], width=5,
                              justify="center").grid(row=i, column=j, padx=2, pady=2)
            return
        zona = tema.zona_text(cadru, n)
        zona.configure(wrap="none", width=36)
        zona.insert("1.0", self.text_matrice[prefix])
        zona.pack(anchor="w")
        self.zone[f"{prefix}_matrice"] = zona

    def _dimensiune_valida(self) -> int:
        text = self.dimensiune.get().strip()
        if not text.isdigit() or not 2 <= int(text) <= MAX_N:
            raise ValueError(t("eroare_hill_dim"))
        return int(text)

    def _verifica_inversa(self) -> None:
        """Verifica in Python daca K * K^-1 = I (mod m), doar ca ajutor pentru utilizator."""
        try:
            n = self._dimensiune_valida()
            m = int(self._citeste_valori("cr")[1])
            k = [int(x) for x in self._citeste_valori("cr")[2:]]
            inversa = [int(x) for x in self._citeste_valori("dec")[2:]]
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        corect = m > 1
        for i in range(n):
            for j in range(n):
                suma = sum(k[i * n + x] * inversa[x * n + j] for x in range(n)) % m if m > 1 else 0
                corect = corect and suma == (1 if i == j else 0)
        self._mesaj(t("hill_verificare_ok" if corect else "hill_verificare_gresit", m=m), eroare=not corect)

    # ---------- citirea datelor ----------

    def _citeste_alfabet(self) -> str:
        alfabet = self.alfabet.get()
        if not 2 <= len(alfabet) <= MAX_CARACTERE or len(set(alfabet)) != len(alfabet):
            raise ValueError(t("eroare_hill_alfabet"))
        return alfabet

    def _citeste_valori(self, prefix: str) -> list[str]:
        """Intoarce [n, m, a11, a12, ...] in ordinea in care le citeste motor.cpp."""
        n = self._dimensiune_valida()
        m = self.numar_modular.get().strip()
        if not m:
            raise ValueError(t("camp_gol", camp="m"))
        if not m.lstrip("-").isdigit():
            raise ValueError(t("camp_numar", camp="m"))

        if n <= N_CU_CASETE:
            numere = []
            for i in range(n):
                for j in range(n):
                    numere.append(self._numar(f"a{i + 1}{j + 1}", self.celule[prefix][i][j].get()))
        else:
            bucati = re.split(r"[\s,;]+", self.zone[f"{prefix}_matrice"].get("1.0", "end-1c").strip())
            numere = [self._numar("a", bucata) for bucata in bucati if bucata]
            if len(numere) != n * n:
                raise ValueError(t("eroare_hill_matrice", asteptat=n * n, gasite=len(numere)))
        return [str(n), m, *numere]

    @staticmethod
    def _numar(nume: str, text: str) -> str:
        text = text.strip()
        if not text:
            raise ValueError(t("camp_gol", camp=nume))
        try:
            int(text)
        except ValueError:
            raise ValueError(t("camp_numar", camp=nume))
        return text

    # ---------- actiunile butoanelor ----------

    def _codifica(self, text: str, alfabet: str) -> str:
        """Fiecare caracter din alfabet devine un cod (33, 34, ...) pe care motorul il trateaza ca pe o litera."""
        rezultat = ""
        for caracter in text:
            variante = [caracter, caracter.upper(), caracter.lower(), pregateste(caracter), pregateste(caracter).lower()]
            for varianta in variante:
                if len(varianta) == 1 and varianta in alfabet:
                    rezultat += chr(PRIMUL_COD + alfabet.index(varianta))
                    break
        return rezultat

    def _transforma(self, prefix: str) -> None:
        text = self.zone[f"{prefix}_in"].get("1.0", "end-1c")
        if not text.strip():
            self._mesaj(t("mesaj_text_gol"), eroare=True)
            return
        try:
            alfabet = self._citeste_alfabet()
            parametri = [COMENZI[prefix], *self._citeste_valori(prefix)]
            parametri.append("".join(chr(PRIMUL_COD + i) for i in range(len(alfabet))))
            text_codat = self._codifica(text, alfabet)
            if not text_codat:
                raise ValueError(t("eroare_hill_fara_litere"))
            rezultat = ruleaza_motor(self.folder, parametri, text_codat, curata_text=False)
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return
        tema.scrie_in_zona(self.zone[f"{prefix}_out"], "".join(alfabet[ord(c) - PRIMUL_COD] for c in rezultat.strip()))
        self._mesaj(t("mesaj_gata"))

    def _citeste_fisier(self) -> tuple[str, str] | None:
        cale = filedialog.askopenfilename(title=t("dialog_alege"), filetypes=self._tipuri_fisiere())
        if not cale:
            return None
        try:
            return Path(cale).read_text(encoding="utf-8-sig", errors="replace"), Path(cale).name
        except OSError as eroare:
            self._mesaj(t("mesaj_fisier_eroare_citire", motiv=eroare.strerror), eroare=True)
            return None

    def _citeste_alfabetul(self) -> None:
        fisier = self._citeste_fisier()
        if fisier:
            self.alfabet.set(fisier[0].rstrip("\r\n").split("\n")[0].rstrip("\r"))
            self._mesaj(t("mesaj_fisier_citit", nume=fisier[1]))

    def _citeste_matricea(self, prefix: str) -> None:
        """Citeste matricea dintr-un fisier: numere separate prin spatii/virgule; n se deduce din cate sunt."""
        fisier = self._citeste_fisier()
        if not fisier:
            return
        try:
            numere = [int(x) for x in re.split(r"[\s,;]+", fisier[0].strip()) if x]
        except ValueError:
            self._mesaj(t("camp_numar", camp=fisier[1]), eroare=True)
            return
        n = round(len(numere) ** 0.5)
        if n not in DIMENSIUNI or n * n != len(numere):
            self._mesaj(t("eroare_hill_matrice", asteptat=f"n × n (n = 2 ... {MAX_N})", gasite=len(numere)), eroare=True)
            return
        matrice = [numere[i * n:(i + 1) * n] for i in range(n)]
        if str(n) != self.dimensiune.get():
            self.dimensiune.set(str(n))
            self.n_afisat = n
            self._incarca_exemplul(n)
        self._pune_matricea(prefix, matrice)
        for p in self.cadre_matrice:
            self._deseneaza_matricea(p)
        self._mesaj(t("mesaj_fisier_citit", nume=fisier[1]))


if __name__ == "__main__":
    AplicatieHill().mainloop()
