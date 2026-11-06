"""Mini-aplicatia Hill (matrice n x n): interfata. Criptarea se face in motor.cpp.

Foloseste fereastra comuna din ../comun si ii adauga doar ce e specific cifrului Hill:
alfabetul, numarul modular m, dimensiunea n si matricea (cheia sau matricea modular inversa).
"""

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

DIMENSIUNI = (2, 4, 6, 8)   # n trebuie sa fie par; la fel ca in motor.cpp
MAX_N = 8
N_CU_CASETE = 4             # pana la n = 4 matricea se scrie in casete, peste 4 intr-o zona de text
ALFABET_LATIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_CARACTERE = 90          # fiecare caracter al alfabetului primeste un cod 33, 34, ... in motor
PRIMUL_COD = 33

# Exemple valide pentru alfabetul latin (m = 26): matricea cheie si matricea ei modular inversa.
CHEIE_2 = [[3, 3], [2, 5]]
INVERSA_2 = [[15, 17], [20, 9]]
CHEIE_4 = [[4, 1, 3, 5], [4, 3, 6, 2], [3, 4, 3, 2], [2, 1, 6, 1]]
INVERSA_4 = [[9, 16, 23, 7], [18, 3, 22, 16], [3, 22, 8, 3], [24, 15, 14, 5]]
BLOCURI = {2: [CHEIE_2], 4: [CHEIE_4], 6: [CHEIE_4, CHEIE_2], 8: [CHEIE_4, CHEIE_4]}
BLOCURI_INVERSE = {2: [INVERSA_2], 4: [INVERSA_4], 6: [INVERSA_4, INVERSA_2], 8: [INVERSA_4, INVERSA_4]}

TEXTE_HILL = {
    "ro": {
        "titlu_hill": "Sistemul simetric de criptare Hill (matrice n×n)",
        "cr_cheie": "Matricea cheie K:",
        "dec_cheie": "Matricea cheie = matricea modular inversă K⁻¹:",
        "hill_setari": "Date de intrare",
        "hill_alfabet": "Alfabetul:",
        "hill_alfabet_fisier": "Citește alfabetul din fișier",
        "hill_numar_modular": "număr modular m =",
        "hill_dimensiune": "dimensiunea n:",
        "hill_matrice_fisier": "Citește matricea din fișier",
        "hill_indiciu_cr": "m = numărul de caractere ale alfabetului. Matricea trebuie să aibă determinantul prim cu m.",
        "hill_indiciu_dec": "Aici introduci matricea modular inversă K⁻¹ (mod m), creată cu același m: K · K⁻¹ = I (mod m). Programul nu o calculează.",
        "eroare_hill_dim": "Dimensiunea n trebuie să fie 2, 4, 6 sau 8.",
        "eroare_hill_modul": "Numărul modular m trebuie să fie egal cu numărul de caractere ale alfabetului.",
        "eroare_hill_alfabet": "Alfabetul trebuie să aibă între 2 și 90 de caractere, fără caractere repetate.",
        "eroare_hill_matrice": "Matricea trebuie să aibă {asteptat} numere (n × n), dar ai scris {gasite}.",
        "eroare_hill_fara_litere": "Textul nu conține niciun caracter din alfabet.",
    },
    "en": {
        "titlu_hill": "Hill symmetric encryption system (n×n matrix)",
        "cr_cheie": "Key matrix K:",
        "dec_cheie": "Key matrix = modular inverse matrix K⁻¹:",
        "hill_setari": "Input data",
        "hill_alfabet": "Alphabet:",
        "hill_alfabet_fisier": "Read alphabet from file",
        "hill_numar_modular": "modular number m =",
        "hill_dimensiune": "size n:",
        "hill_matrice_fisier": "Read matrix from file",
        "hill_indiciu_cr": "m = the number of characters in the alphabet. The matrix determinant must be coprime with m.",
        "hill_indiciu_dec": "Enter the modular inverse matrix K⁻¹ (mod m), created with the same m: K · K⁻¹ = I (mod m). The program does not calculate it.",
        "eroare_hill_dim": "The size n must be 2, 4, 6 or 8.",
        "eroare_hill_modul": "The modular number m must equal the number of characters in the alphabet.",
        "eroare_hill_alfabet": "The alphabet must have 2 to 90 characters, with no repeated characters.",
        "eroare_hill_matrice": "The matrix needs {asteptat} numbers (n × n), but you wrote {gasite}.",
        "eroare_hill_fara_litere": "The text contains no character from the alphabet.",
    },
    "ru": {
        "titlu_hill": "Симметричная система шифрования: шифр Хилла (матрица n×n)",
        "cr_cheie": "Ключевая матрица K:",
        "dec_cheie": "Ключ = модулярно обратная матрица K⁻¹:",
        "hill_setari": "Входные данные",
        "hill_alfabet": "Алфавит:",
        "hill_alfabet_fisier": "Прочитать алфавит из файла",
        "hill_numar_modular": "модульное число m =",
        "hill_dimensiune": "размер n:",
        "hill_matrice_fisier": "Прочитать матрицу из файла",
        "hill_indiciu_cr": "m = количество символов алфавита. Определитель матрицы должен быть взаимно прост с m.",
        "hill_indiciu_dec": "Введите модулярно обратную матрицу K⁻¹ (mod m), созданную с тем же m: K · K⁻¹ = I (mod m). Программа её не вычисляет.",
        "eroare_hill_dim": "Размер n должен быть равен 2, 4, 6 или 8.",
        "eroare_hill_modul": "Модульное число m должно быть равно количеству символов алфавита.",
        "eroare_hill_alfabet": "В алфавите должно быть от 2 до 90 символов, без повторов.",
        "eroare_hill_matrice": "В матрице должно быть {asteptat} чисел (n × n), а вы ввели {gasite}.",
        "eroare_hill_fara_litere": "В тексте нет ни одного символа из алфавита.",
    },
}

TEORIE_HILL = {
    "ro": """
# Ce este?
Cifrul Hill (Lester Hill, 1929) criptează caracterele în blocuri, nu unul câte unul. Dimensiunea blocului este n (par: 2, 4, 6 sau 8), iar cheia este o matrice pătratică n × n. Alfabetul îl alegi tu: poate avea orice caractere, nu doar A-Z.

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
2. Alege n. Pentru n = 2 și 4 matricea se scrie în casete; pentru n = 6 și 8 într-o zonă de text (numere separate prin spații sau virgule, rând cu rând) sau o citești dintr-un fișier.
3. La criptare scrii matricea cheie K, la decriptare matricea modular inversă K⁻¹.
Din text se păstrează doar caracterele care se află în alfabet (literele mici se transformă în mari dacă alfabetul are litere mari).
""",
    "en": """
# What is it?
The Hill cipher (Lester Hill, 1929) encrypts characters in blocks, not one at a time. The block size is n (even: 2, 4, 6 or 8), and the key is an n × n square matrix. You choose the alphabet: it can have any characters, not only A-Z.

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
2. Choose n. For n = 2 and 4 the matrix is written in boxes; for n = 6 and 8 in a text area (numbers separated by spaces or commas, row by row) or you read it from a file.
3. For encryption you write the key matrix K, for decryption the modular inverse matrix K⁻¹.
Only the characters found in the alphabet are kept from the text (lowercase letters become uppercase if the alphabet has uppercase letters).
""",
    "ru": """
# Что это?
Шифр Хилла (Лестер Хилл, 1929) шифрует символы блоками, а не по одному. Размер блока — n (чётное: 2, 4, 6 или 8), а ключ — квадратная матрица n × n. Алфавит выбираете вы: в нём могут быть любые символы, не только A-Z.

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
2. Выберите n. Для n = 2 и 4 матрица вводится в клетках; для n = 6 и 8 — в текстовой области (числа через пробел или запятую, строка за строкой) или читается из файла.
3. При шифровании вводите ключевую матрицу K, при расшифровке — модулярно обратную матрицу K⁻¹.
Из текста остаются только символы, которые есть в алфавите (строчные буквы становятся заглавными, если в алфавите заглавные).
""",
}

# Textele si teoria specifice cifrului Hill se adauga la cele comune (doar in acest proces).
for cod_limba, texte in TEXTE_HILL.items():
    traduceri.TEXTE[cod_limba].update(texte)
teorie.TEORIE["hill"] = TEORIE_HILL


def matrice_pentru(n: int, inversa: bool) -> list[list[int]]:
    """Matricea n x n de exemplu (cheie sau inversa), formata din blocuri 4x4 si 2x2 pe diagonala."""
    blocuri = (BLOCURI_INVERSE if inversa else BLOCURI)[n]
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
        self.geometry("1080x900")
        self.minsize(940, 820)

    def _construieste(self) -> None:
        if not hasattr(self, "celule"):
            self._creeaza_variabile()
        super()._construieste()
        self._stilul_listei_derulante()

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
        self.cadre_matrice = {}  # prefix -> (cadrul matricii, functia apelata la Enter)
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
        self._incarca_exemplul(int(self.dimensiune.get()))
        for prefix in self.cadre_matrice:
            self._deseneaza_matricea(prefix)

    # ---------- fereastra: taburile de criptare / decriptare ----------

    def _tab_transformare(self, prefix: str) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t(f"{prefix}_tab"))
        intrare = tema.zona_text(tab, 4)
        iesire = tema.zona_text(tab, 4, doar_citire=True)
        self.zone[f"{prefix}_in"] = intrare
        self.zone[f"{prefix}_out"] = iesire

        def executa(_eveniment=None) -> None:
            self._transforma(prefix)

        self._rand_titlu(tab, t(f"{prefix}_intrare"), t(f"{prefix}_citeste"),
                         lambda: self._citeste_din_fisier(intrare))
        intrare.pack(fill="x")

        date = ttk.LabelFrame(tab, text=t("hill_setari"), padding=10)
        date.pack(fill="x", pady=10)
        self._rand_alfabet(date, executa)
        self._rand_dimensiune(date, prefix)
        self.cadre_matrice[prefix] = (ttk.Frame(date), executa)
        self.cadre_matrice[prefix][0].pack(fill="x", pady=(8, 0))
        self._deseneaza_matricea(prefix)
        ttk.Label(date, text=t(f"hill_indiciu_{prefix}"), foreground=tema.TEXT_SLAB,
                  wraplength=960, justify="left").pack(fill="x", pady=(8, 0))

        ttk.Button(tab, text=t(f"{prefix}_buton"), style="Accent.TButton", cursor="hand2",
                   command=executa).pack(anchor="e", pady=(0, 10))
        self._rand_titlu(tab, t(f"{prefix}_iesire"), t(f"{prefix}_scrie"),
                         lambda: self._scrie_in_fisier(iesire))
        iesire.pack(fill="both", expand=True)

    def _rand_alfabet(self, parinte, la_enter) -> None:
        rand = ttk.Frame(parinte)
        rand.pack(fill="x")
        ttk.Label(rand, text=t("hill_alfabet"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 8))
        casuta = ttk.Entry(rand, textvariable=self.alfabet, font=tema.FONT_COD)
        casuta.pack(side="left", fill="x", expand=True, padx=(0, 12))
        casuta.bind("<Return>", la_enter)
        ttk.Label(rand, text=t("hill_numar_modular")).pack(side="left", padx=(0, 6))
        modular = ttk.Entry(rand, textvariable=self.numar_modular, width=5, justify="center")
        modular.pack(side="left", padx=(0, 12))
        modular.bind("<Return>", la_enter)
        ttk.Button(rand, text=t("hill_alfabet_fisier"), cursor="hand2",
                   command=self._citeste_alfabetul).pack(side="left")

    def _rand_dimensiune(self, parinte, prefix: str) -> None:
        rand = ttk.Frame(parinte)
        rand.pack(fill="x", pady=(10, 0))
        ttk.Label(rand, text=t(f"{prefix}_cheie"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 16))
        ttk.Label(rand, text=t("hill_dimensiune")).pack(side="left", padx=(0, 6))
        selector = ttk.Combobox(rand, textvariable=self.dimensiune, values=[str(n) for n in DIMENSIUNI],
                                width=3, state="readonly", justify="center")
        selector.pack(side="left")
        selector.bind("<<ComboboxSelected>>", lambda _eveniment: self._alege_dimensiunea())
        ttk.Button(rand, text=t("hill_matrice_fisier"), cursor="hand2",
                   command=lambda: self._citeste_matricea(prefix)).pack(side="right")

    def _deseneaza_matricea(self, prefix: str) -> None:
        """Casete pentru n <= 4, zona de text pentru n mai mare."""
        cadru, la_enter = self.cadre_matrice[prefix]
        self.zone.pop(f"{prefix}_matrice", None)
        for element in cadru.winfo_children():
            element.destroy()
        n = int(self.dimensiune.get())
        if n <= N_CU_CASETE:
            for i in range(n):
                for j in range(n):
                    casuta = ttk.Entry(cadru, textvariable=self.celule[prefix][i][j], width=5, justify="center")
                    casuta.grid(row=i, column=j, padx=2, pady=2)
                    casuta.bind("<Return>", la_enter)
            return
        zona = tema.zona_text(cadru, n)
        zona.configure(wrap="none", width=60)
        zona.insert("1.0", self.text_matrice[prefix])
        zona.pack(anchor="w")
        self.zone[f"{prefix}_matrice"] = zona

    # ---------- citirea datelor ----------

    def _citeste_alfabet(self) -> str:
        alfabet = self.alfabet.get()
        if not 2 <= len(alfabet) <= MAX_CARACTERE or len(set(alfabet)) != len(alfabet):
            raise ValueError(t("eroare_hill_alfabet"))
        return alfabet

    def _citeste_valori(self, prefix: str) -> list[str]:
        """Intoarce [n, m, a11, a12, ...] in ordinea in care le citeste motor.cpp."""
        n = int(self.dimensiune.get())
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
            self._mesaj(t("eroare_hill_matrice", asteptat="n × n (n = 2, 4, 6, 8)", gasite=len(numere)), eroare=True)
            return
        matrice = [numere[i * n:(i + 1) * n] for i in range(n)]
        if str(n) != self.dimensiune.get():
            self.dimensiune.set(str(n))
            self._incarca_exemplul(n)
        self._pune_matricea(prefix, matrice)
        for p in self.cadre_matrice:
            self._deseneaza_matricea(p)
        self._mesaj(t("mesaj_fisier_citit", nume=fisier[1]))

    def _stilul_listei_derulante(self) -> None:
        """Casuta de alegere a lui n are nevoie de culorile temei curente."""
        stil = ttk.Style(self)
        stil.configure("TCombobox", fieldbackground=tema.INPUT, background=tema.PANOU_HOVER,
                       foreground=tema.TEXT, arrowcolor=tema.TEXT, padding=4)
        stil.map("TCombobox", fieldbackground=[("readonly", tema.INPUT)],
                 foreground=[("readonly", tema.TEXT)],
                 selectbackground=[("readonly", tema.INPUT)],
                 selectforeground=[("readonly", tema.TEXT)])
        self.option_add("*TCombobox*Listbox.background", tema.INPUT)
        self.option_add("*TCombobox*Listbox.foreground", tema.TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", tema.SELECTIE)
        self.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")


if __name__ == "__main__":
    AplicatieHill().mainloop()
