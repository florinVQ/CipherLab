"""Mini-aplicatia Sisteme cu chei fluide (sincrone si asincrone): interfata.

Criptarea se face in motor.cpp; aici se alege generatorul cheii fluide si se afiseaza,
pentru fiecare caracter, numarul lui, cheia K(i) si rezultatul (ca in exemplele de la curs).
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
from fereastra_cifru import COMENZI, NUMAR, NUMERE, TEXT, LATIME_CAMP, AplicatieCifru, Camp  # noqa: E402
from motor_cpp import ruleaza_motor  # noqa: E402
from traduceri import t  # noqa: E402

# Generatorul cheii fluide (cum il numeste motorul) si campurile lui.
GENERATOARE = {
    "cuvant": [Camp("cuvant_cheie", "VINERI", tip=TEXT)],
    "fibonacci": [Camp("F₁", "1", tip=NUMAR), Camp("F₂", "1", tip=NUMAR)],
    "sir": [Camp("fluide_sir", "3 1 4 1 5 9 2 6", tip=NUMERE)],
    "asincron": [Camp("k₁", "13", tip=NUMAR)],
}
COLOANE_PASI = ("i", "caracter", "numar", "cheie", "rezultat_numar", "rezultat")

TEXTE_FLUIDE = {
    "ro": {
        "fluide_cheia": "Cheia fluidă:",
        "fluide_gen_cuvant": "Sincron: cuvânt-cheie (Vigenère)",
        "fluide_gen_fibonacci": "Sincron: șirul lui Fibonacci",
        "fluide_gen_sir": "Sincron: șir de numere dat",
        "fluide_gen_asincron": "Asincron (auto-sincronizant)",
        "fluide_ind_cuvant": "K(i) = numărul literei i din cuvântul-cheie; cuvântul se repetă.",
        "fluide_ind_fibonacci": "K(1) = F₁, K(2) = F₂, K(i) = K(i-1) + K(i-2), totul modulo m.",
        "fluide_ind_sir": "K(i) = numerele scrise de tine, luate pe rând și reluate de la început.",
        "fluide_ind_asincron": "K(1) = k₁, apoi K(i+1) = y(i): cheia următoare este caracterul criptat chiar înainte.",
        "fluide_sir": "numerele",
        "fluide_pasi": "Calculul, caracter cu caracter:",
        "fluide_cr_formula": "y(i) = (x(i) + K(i)) mod m",
        "fluide_dec_formula": "x(i) = (y(i) - K(i)) mod m",
    },
    "en": {
        "fluide_cheia": "Keystream:",
        "fluide_gen_cuvant": "Synchronous: keyword (Vigenère)",
        "fluide_gen_fibonacci": "Synchronous: Fibonacci sequence",
        "fluide_gen_sir": "Synchronous: given number sequence",
        "fluide_gen_asincron": "Asynchronous (self-synchronizing)",
        "fluide_ind_cuvant": "K(i) = the number of letter i of the keyword; the keyword repeats.",
        "fluide_ind_fibonacci": "K(1) = F₁, K(2) = F₂, K(i) = K(i-1) + K(i-2), all modulo m.",
        "fluide_ind_sir": "K(i) = the numbers you type, taken in turn and repeated from the start.",
        "fluide_ind_asincron": "K(1) = k₁, then K(i+1) = y(i): the next key is the character encrypted just before.",
        "fluide_sir": "numbers",
        "fluide_pasi": "The calculation, character by character:",
        "fluide_cr_formula": "y(i) = (x(i) + K(i)) mod m",
        "fluide_dec_formula": "x(i) = (y(i) - K(i)) mod m",
    },
    "ru": {
        "fluide_cheia": "Поточный ключ:",
        "fluide_gen_cuvant": "Синхронный: ключевое слово (Виженер)",
        "fluide_gen_fibonacci": "Синхронный: последовательность Фибоначчи",
        "fluide_gen_sir": "Синхронный: заданная последовательность чисел",
        "fluide_gen_asincron": "Асинхронный (самосинхронизирующийся)",
        "fluide_ind_cuvant": "K(i) = номер i-й буквы ключевого слова; слово повторяется.",
        "fluide_ind_fibonacci": "K(1) = F₁, K(2) = F₂, K(i) = K(i-1) + K(i-2), всё по модулю m.",
        "fluide_ind_sir": "K(i) = введённые вами числа, по очереди и снова с начала.",
        "fluide_ind_asincron": "K(1) = k₁, затем K(i+1) = y(i): следующий ключ — только что зашифрованный символ.",
        "fluide_sir": "числа",
        "fluide_pasi": "Вычисления, символ за символом:",
        "fluide_cr_formula": "y(i) = (x(i) + K(i)) mod m",
        "fluide_dec_formula": "x(i) = (y(i) - K(i)) mod m",
    },
}

# Capetele coloanelor din tabelul de pasi, la criptare si la decriptare.
CAPETE = {
    "cr": ("i", "x", "Im(x)", "K(i)", "Im(y)", "y"),
    "dec": ("i", "y", "Im(y)", "K(i)", "Im(x)", "x"),
}

TEORIE_FLUIDE = {
    "ro": """
# Ce este?
La un sistem cu cheie fluidă fiecare caracter al textului se criptează cu altă cheie. Cheile formează un șir K(1), K(2), K(3), ..., numit cheie fluidă, iar fiecare caracter se criptează ca la Cezar:
    y(i) = (x(i) + K(i)) mod m
    x(i) = (y(i) - K(i)) mod m

# Sisteme sincrone
Cheia fluidă nu depinde de text, ci doar de cheia de pornire. Aplicația are trei variante:
    Vigenère: K(i) sunt literele cuvântului-cheie, repetate
    Fibonacci: K(1) = F₁, K(2) = F₂, K(i) = K(i-1) + K(i-2), luate mod m
    șir de numere: numerele scrise de tine, repetate
Dacă un caracter se pierde pe drum, tot ce urmează după el se decriptează greșit: expeditorul și destinatarul nu mai sunt sincronizați.

# Exemplu sincron (Fibonacci, m = 26)
    text clar:    M  I  H  A  E  L  A  B  A  L  A  N  E  S  C  U
    K(i) mod 26:  1  1  2  3  5  8 13 21  8  3 11 14 25 13 12 25
    criptat:      N  J  J  D  J  T  N  W  I  O  L  B  D  F  O  T
De exemplu E(U) = (20 + 25) mod 26 = 19, adică T.

# Sisteme asincrone (auto-sincronizante)
Aici cheia depinde de textul criptat. Se pornește de la o cheie inițială k₁, iar fiecare cheie următoare este caracterul criptat chiar înainte:
    K(1) = k₁,   K(i+1) = y(i)
Destinatarul știe k₁ și vede textul criptat, deci poate reface toate cheile. Dacă se pierde un caracter, se strică doar caracterul următor; după aceea sistemul se sincronizează singur.

# Exemplu asincron (k₁ = 13, m = 26)
    text clar:  M  A  R  I  A  M  A  G  D  A  L  E  N  A
    K(i):      13 25 25 16 24 24 10 10 16 19 19  4  8 21
    criptat:    Z  Z  Q  Y  Y  K  K  Q  T  T  E  I  V  V
E(M) = (12 + 13) mod 26 = 25 (Z), apoi E(A) = (0 + 25) mod 26 = 25 (Z), E(R) = (17 + 25) mod 26 = 16 (Q).

# Cum folosești aplicația
Alegi tipul cheii fluide și îi completezi datele. După criptare sau decriptare, tabelul arată pentru fiecare caracter numărul lui, cheia K(i) și rezultatul, la fel ca în exemplele de mai sus. Spațiile și semnele care nu sunt în alfabet se elimină.
""",
    "en": """
# What is it?
In a keystream system every character of the text is encrypted with a different key. The keys form a sequence K(1), K(2), K(3), ..., called the keystream, and each character is encrypted as in the Caesar cipher:
    y(i) = (x(i) + K(i)) mod m
    x(i) = (y(i) - K(i)) mod m

# Synchronous systems
The keystream does not depend on the text, only on the starting key. The app has three variants:
    Vigenère: K(i) are the letters of the keyword, repeated
    Fibonacci: K(1) = F₁, K(2) = F₂, K(i) = K(i-1) + K(i-2), taken mod m
    number sequence: the numbers you type, repeated
If one character is lost on the way, everything after it decrypts wrongly: sender and receiver are no longer synchronized.

# Synchronous example (Fibonacci, m = 26)
    plain text:   M  I  H  A  E  L  A  B  A  L  A  N  E  S  C  U
    K(i) mod 26:  1  1  2  3  5  8 13 21  8  3 11 14 25 13 12 25
    encrypted:    N  J  J  D  J  T  N  W  I  O  L  B  D  F  O  T
For example E(U) = (20 + 25) mod 26 = 19, which is T.

# Asynchronous (self-synchronizing) systems
Here the key depends on the encrypted text. You start from an initial key k₁, and every next key is the character encrypted just before:
    K(1) = k₁,   K(i+1) = y(i)
The receiver knows k₁ and sees the encrypted text, so all keys can be rebuilt. If a character is lost, only the next character is damaged; after that the system synchronizes by itself.

# Asynchronous example (k₁ = 13, m = 26)
    plain text: M  A  R  I  A  M  A  G  D  A  L  E  N  A
    K(i):      13 25 25 16 24 24 10 10 16 19 19  4  8 21
    encrypted:  Z  Z  Q  Y  Y  K  K  Q  T  T  E  I  V  V
E(M) = (12 + 13) mod 26 = 25 (Z), then E(A) = (0 + 25) mod 26 = 25 (Z), E(R) = (17 + 25) mod 26 = 16 (Q).

# How to use the app
Pick the kind of keystream and fill in its data. After encryption or decryption, the table shows for every character its number, the key K(i) and the result, just like the examples above. Spaces and symbols that are not in the alphabet are removed.
""",
    "ru": """
# Что это?
В системе с поточным ключом каждый символ текста шифруется своим ключом. Ключи образуют последовательность K(1), K(2), K(3), ..., которая называется поточным ключом, а каждый символ шифруется как в шифре Цезаря:
    y(i) = (x(i) + K(i)) mod m
    x(i) = (y(i) - K(i)) mod m

# Синхронные системы
Поточный ключ не зависит от текста, только от начального ключа. В приложении три варианта:
    Виженер: K(i) — буквы ключевого слова, повторяющиеся
    Фибоначчи: K(1) = F₁, K(2) = F₂, K(i) = K(i-1) + K(i-2), по модулю m
    последовательность чисел: введённые вами числа, повторяющиеся
Если при передаче теряется символ, всё, что идёт после него, расшифровывается неверно: отправитель и получатель больше не синхронизированы.

# Синхронный пример (Фибоначчи, m = 26)
    открытый:     M  I  H  A  E  L  A  B  A  L  A  N  E  S  C  U
    K(i) mod 26:  1  1  2  3  5  8 13 21  8  3 11 14 25 13 12 25
    шифр:         N  J  J  D  J  T  N  W  I  O  L  B  D  F  O  T
Например, E(U) = (20 + 25) mod 26 = 19, то есть T.

# Асинхронные (самосинхронизирующиеся) системы
Здесь ключ зависит от шифртекста. Начинаем с начального ключа k₁, а каждый следующий ключ — это символ, зашифрованный непосредственно перед ним:
    K(1) = k₁,   K(i+1) = y(i)
Получатель знает k₁ и видит шифртекст, поэтому может восстановить все ключи. Если теряется символ, портится только следующий; после этого система синхронизируется сама.

# Асинхронный пример (k₁ = 13, m = 26)
    открытый:   M  A  R  I  A  M  A  G  D  A  L  E  N  A
    K(i):      13 25 25 16 24 24 10 10 16 19 19  4  8 21
    шифр:       Z  Z  Q  Y  Y  K  K  Q  T  T  E  I  V  V
E(M) = (12 + 13) mod 26 = 25 (Z), затем E(A) = (0 + 25) mod 26 = 25 (Z), E(R) = (17 + 25) mod 26 = 16 (Q).

# Как пользоваться приложением
Выберите вид поточного ключа и заполните его данные. После шифрования или расшифровки таблица показывает для каждого символа его номер, ключ K(i) и результат, как в примерах выше. Пробелы и знаки, которых нет в алфавите, удаляются.
""",
}

traduceri.adauga_texte(TEXTE_FLUIDE)
teorie.TEORIE["fluide"] = TEORIE_FLUIDE


class AplicatieFluide(AplicatieCifru):
    def __init__(self):
        super().__init__(FOLDER, campuri_cheie=[], alfabet=alf.LATIN, pastreaza_restul=False)
        self.potriveste_marimea(1080, 900)

    def _construieste(self) -> None:
        if not hasattr(self, "generator"):
            self.generator = tk.StringVar(value="fibonacci")
            self.valori_generator = {cod: [tk.StringVar(value=c.implicit) for c in campuri]
                                     for cod, campuri in GENERATOARE.items()}
            self.pasi = {"cr": [], "dec": []}  # randurile tabelelor, pastrate la schimbarea limbii
            self.tabele = {}
        super()._construieste()
        self._construieste_cheia()
        for prefix, randuri in self.pasi.items():
            self._umple_pasii(prefix, randuri)

    # ---------- cheia fluida ----------

    def _construieste_cheia(self) -> None:
        cadru = ttk.Frame(self, padding=(14, 8))
        cadru.pack(fill="x", padx=16, pady=(0, 8), before=self.carnet)
        rand = ttk.Frame(cadru)
        rand.pack(fill="x")
        ttk.Label(rand, text=t("fluide_cheia"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 8))

        nume = {cod: t(f"fluide_gen_{cod}") for cod in GENERATOARE}
        alegere = ttk.Combobox(rand, state="readonly", width=36, values=list(nume.values()))
        alegere.set(nume[self.generator.get()])
        alegere.pack(side="left", padx=(0, 16))
        self.cadru_campuri = ttk.Frame(rand)
        self.cadru_campuri.pack(side="left", fill="x", expand=True)
        self.indiciu_generator = ttk.Label(cadru, foreground=tema.TEXT_SLAB, font=tema.FONT_MIC)
        self.indiciu_generator.pack(fill="x", pady=(4, 0))

        def la_alegere(_eveniment=None) -> None:
            ales = list(nume.values()).index(alegere.get())
            self.generator.set(list(GENERATOARE)[ales])
            self._deseneaza_campurile()

        alegere.bind("<<ComboboxSelected>>", la_alegere)
        self._deseneaza_campurile()

    def _deseneaza_campurile(self) -> None:
        for element in self.cadru_campuri.winfo_children():
            element.destroy()
        cod = self.generator.get()
        for camp, valoare in zip(GENERATOARE[cod], self.valori_generator[cod]):
            ttk.Label(self.cadru_campuri, text=f"{t(camp.eticheta)} =").pack(side="left", padx=(0, 6))
            ttk.Entry(self.cadru_campuri, textvariable=valoare,
                      width=LATIME_CAMP[camp.tip]).pack(side="left", padx=(0, 16))
        self.indiciu_generator.configure(text=t(f"fluide_ind_{cod}"))

    def _parametri_generator(self) -> list[str]:
        cod = self.generator.get()
        alfabet = self._alfabet_valid()
        valori = [self._valoare_pentru_motor(camp, valoare.get(), alfabet)
                  for camp, valoare in zip(GENERATOARE[cod], self.valori_generator[cod])]
        return [cod, *valori]

    # ---------- taburile de criptare / decriptare ----------

    def _tab_transformare(self, prefix: str) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t(f"{prefix}_tab"))
        self._intrare_si_iesire_alaturi(tab, prefix, 3)
        rand = ttk.Frame(tab)
        rand.pack(fill="x", pady=(10, 6))
        ttk.Label(rand, text=t("fluide_pasi"), font=tema.FONT_UI_BOLD).pack(side="left")
        ttk.Label(rand, text=t(f"fluide_{prefix}_formula"), font=tema.FONT_COD,
                  foreground=tema.SUCCES).pack(side="left", padx=(16, 0))
        ttk.Button(rand, text=t(f"{prefix}_buton"), style="Accent.TButton", cursor="hand2",
                   command=lambda: self._transforma(prefix)).pack(side="right")
        cadru = ttk.Frame(tab)
        cadru.pack(fill="both", expand=True)
        tabel = ttk.Treeview(cadru, columns=COLOANE_PASI, show="headings", height=6)
        for coloana, cap in zip(COLOANE_PASI, CAPETE[prefix]):
            tabel.heading(coloana, text=cap)
            tabel.column(coloana, width=110, anchor="center")
        derulare = ttk.Scrollbar(cadru, command=tabel.yview)
        tabel.configure(yscrollcommand=derulare.set)
        derulare.pack(side="right", fill="y")
        tabel.pack(fill="both", expand=True)
        self.tabele[prefix] = tabel

    def _ruleaza(self, prefix: str, text: str) -> str:
        alfabet = self._alfabet_valid()
        parametri = [COMENZI[prefix], *self._parametri_generator(), alf.coduri_alfabet(alfabet)]
        iesire = ruleaza_motor(self.folder, parametri, self._codifica_text(text), curata_text=False)

        randuri = []
        for i, linie in enumerate(iesire.split("\n")[:-1], start=1):
            x, k, y = (int(numar) for numar in linie.split())
            randuri.append((i, alfabet[x], x, k, y, alfabet[y]))
        self.pasi[prefix] = randuri
        self._umple_pasii(prefix, randuri)
        return "".join(rand[-1] for rand in randuri)

    def _umple_pasii(self, prefix: str, randuri: list[tuple]) -> None:
        tabel = self.tabele[prefix]
        tabel.delete(*tabel.get_children())
        for rand in randuri:
            tabel.insert("", "end", values=rand)


if __name__ == "__main__":
    AplicatieFluide().mainloop()
