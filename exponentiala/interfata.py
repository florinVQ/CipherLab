"""Mini-aplicatia Criptarea exponentiala: interfata. Calculele se fac in motor.cpp.

Fiecare caracter primeste un cod de doua cifre (primul din alfabet = 10), blocurile de k
caractere devin numere M, iar criptarea este Y = M^e mod p. Pentru fiecare bloc se arata
exponentierea modulara pas cu pas, ca in tabelele de la curs.
"""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet as alf  # noqa: E402
import tema  # noqa: E402
import teorie  # noqa: E402
import traduceri  # noqa: E402
from fereastra_cifru import NUMAR, AplicatieCifru, Camp  # noqa: E402
from motor_cpp import EroareMotor, ruleaza_motor  # noqa: E402
from traduceri import t  # noqa: E402

PRIMUL_COD = 10  # la fel ca in motor.cpp
CAMPURI_CHEIE = [Camp("p", "5869", tip=NUMAR), Camp("e", "6089", tip=NUMAR),
                 Camp("exp_k", "2", tip=NUMAR)]
CAMPURI_PUTERE = [Camp("x", "2210", tip=NUMAR), Camp("c", "6089", tip=NUMAR),
                  Camp("n", "5869", tip=NUMAR)]

TEXTE_EXPONENTIALA = {
    "ro": {
        "exp_cheia": "Cheia:",
        "exp_k": "caractere pe bloc",
        "exp_indiciu": "Codurile caracterelor: {coduri}",
        "exp_verifica": "Verifică cheia",
        "exp_cheie_buna": "Cheia este bună: p este prim și (e, p - 1) = 1. Pentru decriptare a = e⁻¹ mod (p - 1) = {a}.",
        "exp_calcul": "Calculul, bloc cu bloc:",
        "exp_tab_putere": "Exponențiere modulară",
        "exp_putere_intro": "Calculează x^c mod n cu algoritmul ridicării repetate la pătrat: c se scrie în baza 2, apoi pentru fiecare cifră cᵢ se face z = z² mod n și, dacă cᵢ = 1, z = z · x mod n.",
        "exp_calculeaza": "Calculează",
        "exp_rezultat": "Rezultat: {x}^{c} mod {n} = {r}",
        "exp_bloc_cr": "Blocul {nr}: {text} → M = {m}",
        "exp_bloc_dec": "Blocul {nr}: Y = {y}",
        "exp_binar": "{nume} = {c} = {binar} (în baza 2)",
        "exp_cap": "pas  cᵢ   z = z² mod {n}    z = z · {x} mod {n}",
        "exp_y": "Y = {m}^{e} mod {p} = {y}",
        "exp_m": "M = {y}^{a} mod {p} = {m} → {text}",
        "exp_invers": "a = e⁻¹ mod (p - 1) = {a}  (verificare: {e} · {a} mod {p1} = 1)",
        "eroare_exp_p": "p trebuie să fie un număr prim între 3 și 2 000 000 000.",
        "eroare_exp_e": "e trebuie să fie prim cu p - 1, adică (e, p - 1) = 1.",
        "eroare_exp_k": "Un bloc poate avea între 1 și 4 caractere.",
        "eroare_exp_bloc": "Un bloc M a ieșit mai mare decât p. Alege un p mai mare sau mai puține caractere pe bloc.",
        "eroare_exp_y": "Fiecare număr criptat trebuie să fie mai mic decât p.",
        "eroare_exp_cod": "Un bloc decriptat nu se poate împărți în coduri de caractere. Verifică p, e și numerele criptate.",
        "eroare_exp_putere": "Trebuie ca x ≥ 0, c ≥ 0 și 2 ≤ n ≤ 2 000 000 000.",
    },
    "en": {
        "exp_cheia": "Key:",
        "exp_k": "characters per block",
        "exp_indiciu": "Character codes: {coduri}",
        "exp_verifica": "Check the key",
        "exp_cheie_buna": "The key is good: p is prime and (e, p - 1) = 1. For decryption a = e⁻¹ mod (p - 1) = {a}.",
        "exp_calcul": "The calculation, block by block:",
        "exp_tab_putere": "Modular exponentiation",
        "exp_putere_intro": "Computes x^c mod n by repeated squaring: c is written in base 2, then for every digit cᵢ we do z = z² mod n and, if cᵢ = 1, z = z · x mod n.",
        "exp_calculeaza": "Calculate",
        "exp_rezultat": "Result: {x}^{c} mod {n} = {r}",
        "exp_bloc_cr": "Block {nr}: {text} → M = {m}",
        "exp_bloc_dec": "Block {nr}: Y = {y}",
        "exp_binar": "{nume} = {c} = {binar} (base 2)",
        "exp_cap": "step cᵢ   z = z² mod {n}    z = z · {x} mod {n}",
        "exp_y": "Y = {m}^{e} mod {p} = {y}",
        "exp_m": "M = {y}^{a} mod {p} = {m} → {text}",
        "exp_invers": "a = e⁻¹ mod (p - 1) = {a}  (check: {e} · {a} mod {p1} = 1)",
        "eroare_exp_p": "p must be a prime number between 3 and 2,000,000,000.",
        "eroare_exp_e": "e must be coprime with p - 1, that is (e, p - 1) = 1.",
        "eroare_exp_k": "A block can have 1 to 4 characters.",
        "eroare_exp_bloc": "A block M came out larger than p. Choose a larger p or fewer characters per block.",
        "eroare_exp_y": "Every encrypted number must be smaller than p.",
        "eroare_exp_cod": "A decrypted block cannot be split into character codes. Check p, e and the encrypted numbers.",
        "eroare_exp_putere": "It must hold that x ≥ 0, c ≥ 0 and 2 ≤ n ≤ 2,000,000,000.",
    },
    "ru": {
        "exp_cheia": "Ключ:",
        "exp_k": "символов в блоке",
        "exp_indiciu": "Коды символов: {coduri}",
        "exp_verifica": "Проверить ключ",
        "exp_cheie_buna": "Ключ подходит: p простое и (e, p - 1) = 1. Для расшифровки a = e⁻¹ mod (p - 1) = {a}.",
        "exp_calcul": "Вычисления по блокам:",
        "exp_tab_putere": "Модульное возведение в степень",
        "exp_putere_intro": "Вычисляет x^c mod n повторным возведением в квадрат: c записывается в двоичной системе, затем для каждой цифры cᵢ выполняется z = z² mod n и, если cᵢ = 1, z = z · x mod n.",
        "exp_calculeaza": "Вычислить",
        "exp_rezultat": "Результат: {x}^{c} mod {n} = {r}",
        "exp_bloc_cr": "Блок {nr}: {text} → M = {m}",
        "exp_bloc_dec": "Блок {nr}: Y = {y}",
        "exp_binar": "{nume} = {c} = {binar} (в двоичной системе)",
        "exp_cap": "шаг cᵢ   z = z² mod {n}    z = z · {x} mod {n}",
        "exp_y": "Y = {m}^{e} mod {p} = {y}",
        "exp_m": "M = {y}^{a} mod {p} = {m} → {text}",
        "exp_invers": "a = e⁻¹ mod (p - 1) = {a}  (проверка: {e} · {a} mod {p1} = 1)",
        "eroare_exp_p": "p должно быть простым числом от 3 до 2 000 000 000.",
        "eroare_exp_e": "e должно быть взаимно простым с p - 1, то есть (e, p - 1) = 1.",
        "eroare_exp_k": "В блоке может быть от 1 до 4 символов.",
        "eroare_exp_bloc": "Блок M получился больше p. Выберите большее p или меньше символов в блоке.",
        "eroare_exp_y": "Каждое зашифрованное число должно быть меньше p.",
        "eroare_exp_cod": "Расшифрованный блок не делится на коды символов. Проверьте p, e и зашифрованные числа.",
        "eroare_exp_putere": "Должно быть x ≥ 0, c ≥ 0 и 2 ≤ n ≤ 2 000 000 000.",
    },
}

TEORIE_EXPONENTIALA = {
    "ro": """
# Ce este?
Criptarea exponențială lucrează cu numere, nu cu litere. Textul se transformă întâi într-un mesaj numeric, apoi fiecare număr se ridică la o putere modulo un număr prim p.

# Textul devine număr
Fiecare caracter primește un cod de două cifre: primul caracter din alfabet are codul 10, al doilea 11 și așa mai departe (pentru A-Z: A = 10, B = 11, ..., Z = 35). Textul se taie în blocuri de k caractere, iar codurile unui bloc se scriu unul după altul:
    MART  ->  MA RT  ->  M = (2210, 2729)

# Cheia
Se alege un număr prim p mai mare decât orice bloc M și un exponent e cu (e, p - 1) = 1. E bine ca și e să fie prim.
    E(M) = M^e mod p
    D(Y) = Y^a mod p,   unde a = e⁻¹ mod (p - 1), adică e · a ≡ 1 (mod p - 1)
Inversul a se află cu algoritmul lui Euclid extins.

# Exponențierea modulară
M^e nu se calculează direct, ar ieși un număr uriaș. Exponentul se scrie în baza 2 și se parcurge cifră cu cifră, de la stânga:
    z = 1
    pentru fiecare cifră cᵢ:  z = z² mod p;  dacă cᵢ = 1, atunci z = z · M mod p
Tabelul din aplicație arată exact acești pași.

# Exemplu
p = 5869, e = 6089; (6089, 5868) = 1, iar 6089 = 1011111001001 în baza 2.
    E(2210) = 2210^6089 mod 5869 = 3097
    E(2729) = 2729^6089 mod 5869 = 4235
    a = 6089⁻¹ mod 5868 = 2549
    D(3097) = 3097^2549 mod 5869 = 2210  ->  22 10  ->  MA
La decriptare numărul M se împarte în grupe de câte 2 cifre, de la dreapta spre stânga.

# Cum folosești aplicația
Completezi p, e și câte caractere intră într-un bloc, apoi apeși „Verifică cheia”: aplicația îți spune dacă p e prim, dacă (e, p - 1) = 1 și cât este a. Pe tabul „Exponențiere modulară” poți calcula orice x^c mod n, pas cu pas.
""",
    "en": """
# What is it?
Exponential encryption works with numbers, not letters. The text is first turned into a numeric message, then every number is raised to a power modulo a prime p.

# Text becomes a number
Every character gets a two-digit code: the first character of the alphabet has code 10, the second 11 and so on (for A-Z: A = 10, B = 11, ..., Z = 35). The text is cut into blocks of k characters, and the codes of a block are written one after another:
    MART  ->  MA RT  ->  M = (2210, 2729)

# The key
Choose a prime p larger than any block M and an exponent e with (e, p - 1) = 1. It is good if e is prime too.
    E(M) = M^e mod p
    D(Y) = Y^a mod p,   where a = e⁻¹ mod (p - 1), that is e · a ≡ 1 (mod p - 1)
The inverse a is found with the extended Euclidean algorithm.

# Modular exponentiation
M^e is not computed directly; it would be a huge number. The exponent is written in base 2 and read digit by digit, from the left:
    z = 1
    for every digit cᵢ:  z = z² mod p;  if cᵢ = 1, then z = z · M mod p
The table in the app shows exactly these steps.

# Example
p = 5869, e = 6089; (6089, 5868) = 1, and 6089 = 1011111001001 in base 2.
    E(2210) = 2210^6089 mod 5869 = 3097
    E(2729) = 2729^6089 mod 5869 = 4235
    a = 6089⁻¹ mod 5868 = 2549
    D(3097) = 3097^2549 mod 5869 = 2210  ->  22 10  ->  MA
For decryption the number M is split into groups of 2 digits, from right to left.

# How to use the app
Fill in p, e and how many characters go into a block, then press "Check the key": the app tells you whether p is prime, whether (e, p - 1) = 1 and what a is. On the "Modular exponentiation" tab you can compute any x^c mod n, step by step.
""",
    "ru": """
# Что это?
Экспоненциальное шифрование работает с числами, а не с буквами. Сначала текст превращается в числовое сообщение, затем каждое число возводится в степень по модулю простого числа p.

# Текст становится числом
Каждый символ получает двузначный код: первый символ алфавита — 10, второй — 11 и так далее (для A-Z: A = 10, B = 11, ..., Z = 35). Текст делится на блоки по k символов, а коды блока записываются подряд:
    MART  ->  MA RT  ->  M = (2210, 2729)

# Ключ
Выбирается простое число p, большее любого блока M, и показатель e, для которого (e, p - 1) = 1. Желательно, чтобы e тоже было простым.
    E(M) = M^e mod p
    D(Y) = Y^a mod p,   где a = e⁻¹ mod (p - 1), то есть e · a ≡ 1 (mod p - 1)
Обратное число a находится расширенным алгоритмом Евклида.

# Модульное возведение в степень
M^e не вычисляется напрямую — получилось бы огромное число. Показатель записывается в двоичной системе и читается по цифрам слева направо:
    z = 1
    для каждой цифры cᵢ:  z = z² mod p;  если cᵢ = 1, то z = z · M mod p
Таблица в приложении показывает именно эти шаги.

# Пример
p = 5869, e = 6089; (6089, 5868) = 1, а 6089 = 1011111001001 в двоичной системе.
    E(2210) = 2210^6089 mod 5869 = 3097
    E(2729) = 2729^6089 mod 5869 = 4235
    a = 6089⁻¹ mod 5868 = 2549
    D(3097) = 3097^2549 mod 5869 = 2210  ->  22 10  ->  MA
При расшифровке число M делится на группы по 2 цифры справа налево.

# Как пользоваться приложением
Введите p, e и количество символов в блоке, затем нажмите «Проверить ключ»: приложение скажет, простое ли p, выполняется ли (e, p - 1) = 1 и чему равно a. На вкладке «Модульное возведение в степень» можно вычислить любое x^c mod n по шагам.
""",
}

traduceri.adauga_texte(TEXTE_EXPONENTIALA)
teorie.TEORIE["exponentiala"] = TEORIE_EXPONENTIALA


def citeste_raspunsul(iesire: str) -> list[list[str]]:
    """Randurile motorului, fiecare impartit dupa tab: ["PAS", "1", "1", "1", "2210"]."""
    return [linie.split("\t") for linie in iesire.splitlines() if linie.strip()]


def tabel_pasi(pasi: list[list[str]], n: str, x: str) -> list[str]:
    """Pasii exponentierii modulare, aliniati ca un tabel."""
    randuri = [t("exp_cap", n=n, x=x)]
    for _, numar, bit, patrat, produs in pasi:
        randuri.append(f"{numar:>3}   {bit}    {patrat:>12}    {produs:>12}")
    return randuri


class AplicatieExponentiala(AplicatieCifru):
    def __init__(self):
        super().__init__(FOLDER, campuri_cheie=CAMPURI_CHEIE, alfabet=alf.LATIN, pastreaza_restul=False)
        self.potriveste_marimea(1080, 920)

    def _construieste(self) -> None:
        if not hasattr(self, "valori_putere"):
            self.valori_putere = [tk.StringVar(value=c.implicit) for c in CAMPURI_PUTERE]
        super()._construieste()
        self._construieste_cheia()
        self._tab_putere()

    # ---------- cheia ----------

    def _construieste_cheia(self) -> None:
        cadru = ttk.Frame(self, padding=(14, 8))
        cadru.pack(fill="x", padx=16, pady=(0, 8), before=self.carnet)
        rand = ttk.Frame(cadru)
        rand.pack(fill="x")
        ttk.Label(rand, text=t("exp_cheia"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 12))
        self._campuri_in_rand(rand, "cr", lambda _e=None: self._verifica_cheia())
        ttk.Button(rand, text=t("exp_verifica"), cursor="hand2",
                   command=self._verifica_cheia).pack(side="right")
        indiciu = ttk.Label(cadru, foreground=tema.TEXT_SLAB, font=tema.FONT_MIC,
                            wraplength=980, justify="left")
        indiciu.pack(fill="x", pady=(4, 0))

        def arata_codurile(*_):
            caractere = self.alfabet.get()
            coduri = " ".join(f"{c}={PRIMUL_COD + i}" for i, c in enumerate(caractere))
            indiciu.configure(text=t("exp_indiciu", coduri=coduri))

        arata_codurile()
        self.alfabet.trace_add("write", arata_codurile)

    def _verifica_cheia(self) -> None:
        try:
            p, e, _ = self._citeste_valori("cr")
            iesire = ruleaza_motor(self.folder, ["decripteaza", p, e, alf.coduri_alfabet(self._alfabet_valid())],
                                   "", curata_text=False)
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return
        a = citeste_raspunsul(iesire)[0][1]
        self._mesaj(t("exp_cheie_buna", a=a))

    # ---------- criptare si decriptare ----------

    def _tab_transformare(self, prefix: str) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t(f"{prefix}_tab"))
        self._intrare_si_iesire_alaturi(tab, prefix, 3)
        rand = ttk.Frame(tab)
        rand.pack(fill="x", pady=(10, 6))
        ttk.Label(rand, text=t("exp_calcul"), font=tema.FONT_UI_BOLD).pack(side="left")
        ttk.Button(rand, text=t(f"{prefix}_buton"), style="Accent.TButton", cursor="hand2",
                   command=lambda: self._transforma(prefix)).pack(side="right")
        self.zone[f"{prefix}_calcul"] = self._zona_cu_derulare(tab, 8)

    def _ruleaza(self, prefix: str, text: str) -> str:
        p, e, k = self._citeste_valori("cr")
        alfabet = self._alfabet_valid()
        if prefix == "cr":
            parametri = ["cripteaza", p, e, k, alf.coduri_alfabet(alfabet)]
            iesire = ruleaza_motor(self.folder, parametri, self._codifica_text(text), curata_text=False)
            rezultat, raport = self._raport_criptare(citeste_raspunsul(iesire), p, e)
        else:
            parametri = ["decripteaza", p, e, alf.coduri_alfabet(alfabet)]
            iesire = ruleaza_motor(self.folder, parametri, text, curata_text=False)
            rezultat, raport = self._raport_decriptare(citeste_raspunsul(iesire), p, e)
        tema.scrie_in_zona(self.zone[f"{prefix}_calcul"], "\n".join(raport))
        return rezultat

    def _raport_criptare(self, randuri: list[list[str]], p: str, e: str) -> tuple[str, list[str]]:
        alfabet = self._alfabet_valid()
        raport = [t("exp_binar", nume="e", c=randuri[1][1], binar=randuri[1][2]), ""]
        numere, pasi, nr = [], [], 0
        for rand in randuri[2:]:
            if rand[0] == "BLOC":
                nr += 1
                bloc, m = alf.decodifica(rand[1], alfabet), rand[2]
                raport.append(t("exp_bloc_cr", nr=nr, text=bloc, m=m))
                pasi = []
            elif rand[0] == "PAS":
                pasi.append(rand)
            else:  # Y
                raport += tabel_pasi(pasi, p, "M")
                raport += [t("exp_y", m=m, e=e, p=p, y=rand[1]), ""]
                numere.append(rand[1])
        return " ".join(numere), raport

    def _raport_decriptare(self, randuri: list[list[str]], p: str, e: str) -> tuple[str, list[str]]:
        alfabet = self._alfabet_valid()
        a = randuri[0][1]
        raport = [t("exp_invers", a=a, e=e, p1=int(p) - 1),
                  t("exp_binar", nume="a", c=randuri[1][1], binar=randuri[1][2]), ""]
        text, pasi, nr = "", [], 0
        for rand in randuri[2:]:
            if rand[0] == "BLOC_Y":
                nr += 1
                y = rand[1]
                raport.append(t("exp_bloc_dec", nr=nr, y=y))
                pasi = []
            elif rand[0] == "PAS":
                pasi.append(rand)
            else:  # M
                bloc = alf.decodifica(rand[2], alfabet)
                raport += tabel_pasi(pasi, p, "Y")
                raport += [t("exp_m", y=y, a=a, p=p, m=rand[1], text=" ".join(
                    f"{PRIMUL_COD + alfabet.index(c)}" for c in bloc) + f" → {bloc}"), ""]
                text += bloc
        return text, raport

    # ---------- exponentierea modulara x^c mod n ----------

    def _tab_putere(self) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t("exp_tab_putere"))
        ttk.Label(tab, text=t("exp_putere_intro"), foreground=tema.TEXT_SLAB,
                  wraplength=980, justify="left").pack(fill="x")
        rand = ttk.Frame(tab)
        rand.pack(fill="x", pady=12)
        for camp, valoare in zip(CAMPURI_PUTERE, self.valori_putere):
            ttk.Label(rand, text=f"{camp.eticheta} =").pack(side="left", padx=(0, 6))
            intrare = ttk.Entry(rand, textvariable=valoare, width=14)
            intrare.pack(side="left", padx=(0, 16))
            intrare.bind("<Return>", lambda _e: self._calculeaza_puterea())
        ttk.Button(rand, text=t("exp_calculeaza"), style="Accent.TButton", cursor="hand2",
                   command=self._calculeaza_puterea).pack(side="right")
        self.zone["putere"] = self._zona_cu_derulare(tab, 12)

    def _calculeaza_puterea(self) -> None:
        try:
            x, c, n = (str(self._intreg(camp.eticheta, valoare.get()))
                       for camp, valoare in zip(CAMPURI_PUTERE, self.valori_putere))
            randuri = citeste_raspunsul(ruleaza_motor(self.folder, ["putere", x, c, n], "0", curata_text=False))
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return
        rezultat = t("exp_rezultat", x=x, c=c, n=n, r=randuri[-1][1])
        raport = [t("exp_binar", nume="c", c=c, binar=randuri[0][2]), "",
                  *tabel_pasi(randuri[1:-1], n, "x"), "", rezultat]
        tema.scrie_in_zona(self.zone["putere"], "\n".join(raport))
        self._mesaj(rezultat)


if __name__ == "__main__":
    AplicatieExponentiala().mainloop()
