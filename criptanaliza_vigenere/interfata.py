"""Mini-aplicatia Criptanaliza cifrului Vigenere: interfata. Calculele se fac in motor.cpp.

Pasul 1 (Kasiski): secventele repetate, distantele dintre ele si lungimea probabila a cheii.
Pasul 2: textul se imparte in m linii, se numara frecventele si se propun literele cheii;
cu cheia aleasa textul se decripteaza folosind motorul cifrului Vigenere.
"""

from __future__ import annotations

import sys
import tkinter as tk
from collections import defaultdict
from pathlib import Path
from tkinter import ttk

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER.parent / "comun"))

import alfabet as alf  # noqa: E402
import tema  # noqa: E402
import teorie  # noqa: E402
import traduceri  # noqa: E402
from fereastra_cifru import NUMAR, TEXT, AplicatieCifru, Camp  # noqa: E402
from motor_cpp import EroareMotor, ruleaza_motor  # noqa: E402
from traduceri import t  # noqa: E402

FOLDER_VIGENERE = FOLDER.parent / "vigenere"
CAMPURI_KASISKI = [Camp("kas_minim", "3", tip=NUMAR), Camp("kas_maxim", "12", tip=NUMAR)]
CAMP_LUNGIME = Camp("kas_m", "3", tip=NUMAR)
CAMP_CHEIE = Camp("cuvant_cheie", "", tip=TEXT)
CATE_FRECVENTE = 5  # cate caractere frecvente se arata pentru fiecare linie

# Textul clar din exemplul de la curs, criptat cu cheia MAC.
TEXT_EXEMPLU = """UNPAARFECFRGOUVMPGXAWZCGMSFGPCPOKEPTQZGOECYFQETVDE
BUTFUNUAMPGLFGLEQCGSUUFAOBRKZUPLIPSAKFMGFANUCEMRGY
AOURCFFQMRVQMWXTPQFKUNFABKENWUTCMUBUAUQMGZECMROANK
QLCOECEUTUAVMTFQTCDZKUAEQLUGNGFMKEERMRGMCCHEPQAFUN
HGNFGLQPAKUSKOAKQSGMDKZTTACWFIQMRCPEHULFQSUMPCFAEQ
SGLATQARQMCEAKZRCLENQLWZIKOATQRCLBCFECBRKZFGDECETT
M"""

# Frecventa literelor (in procente). Pentru romana: text fara diacritice (ă in A, ș in S ...),
# plus valori separate pentru Ă, Â, Î, Ș, Ț, folosite cand alfabetul le contine.
FRECVENTE = {
    "ro": dict(A=13.5, B=1.1, C=5.3, D=3.4, E=11.5, F=1.2, G=1.0, H=0.5, I=10.5, J=0.2, K=0.1,
               L=4.5, M=3.1, N=6.4, O=4.7, P=3.0, Q=0.01, R=6.8, S=4.8, T=6.6, U=6.2, V=1.2,
               W=0.05, X=0.1, Y=0.1, Z=0.7, Ă=4.0, Â=0.9, Î=1.4, Ș=1.4, Ț=1.0),
    "en": dict(A=8.2, B=1.5, C=2.8, D=4.3, E=12.7, F=2.2, G=2.0, H=6.1, I=7.0, J=0.15, K=0.8,
               L=4.0, M=2.4, N=6.7, O=7.5, P=1.9, Q=0.1, R=6.0, S=6.3, T=9.1, U=2.8, V=1.0,
               W=2.4, X=0.15, Y=2.0, Z=0.07),
    "ru": dict(О=10.97, Е=8.45, А=8.01, И=7.35, Н=6.70, Т=6.26, С=5.47, Р=4.73, В=4.54, Л=4.40,
               К=3.49, М=3.21, Д=2.98, П=2.81, У=2.62, Я=2.01, Ы=1.90, Ь=1.74, Г=1.70, З=1.65,
               Б=1.59, Ч=1.44, Й=1.21, Х=0.97, Ж=0.94, Ш=0.73, Ю=0.64, Ц=0.48, Щ=0.36, Э=0.32,
               Ф=0.26, Ъ=0.04, Ё=0.04),
}
# Perechi de litere foarte frecvente in fiecare limba; cu ele se da scorul unei chei.
PERECHI_FRECVENTE = {
    "ro": "EA RE IN TE AR DE ER CE ST UL LE NT RI EN AT TA CA UN RA IE LA NE SE TI IA OR ON AN".split(),
    "en": "TH HE IN ER AN RE ON AT EN ND TI ES OR TE OF ED IS IT AL AR ST TO NT NG SE HA AS OU".split(),
    "ru": "СТ НО ЕН ТО НА ОВ НИ РА ВО КО ЕТ ПО ГО ЕР ПР ОС АЛ ЛИ ОР ТА ОЛ АН РО ЕС НЕ ЛЕ ОМ ВА".split(),
}
FRECVENTA_NECUNOSCUTA = 0.01  # caracterele alfabetului care lipsesc din tabelul limbii

TEXTE_CRIPTANALIZA = {
    "ro": {
        "kas_tab_1": "Pasul 1: lungimea cheii",
        "kas_tab_2": "Pasul 2: cheia",
        "kas_intrare": "Textul criptat interceptat:",
        "kas_minim": "lungimea minimă a secvenței",
        "kas_maxim": "lungimea maximă a cheii",
        "kas_m": "lungimea cheii m",
        "kas_cauta": "Caută repetițiile",
        "kas_secvente": "Secvențe repetate (Kasiski)",
        "kas_col_secventa": "Secvența",
        "kas_col_pozitii": "Pozițiile",
        "kas_col_distante": "Distanțele",
        "kas_lungimi": "Lungimi posibile ale cheii",
        "kas_col_m": "m",
        "kas_col_divizibile": "Distanțe divizibile cu m",
        "kas_col_ic": "Indice de coincidență",
        "kas_sugestie": "Lungimea probabilă a cheii: m = {m} (împarte cele mai multe distanțe: {nr} din {total}).",
        "kas_fara_secvente": "Nu am găsit secvențe repetate. Încearcă o lungime minimă mai mică sau un text mai lung.",
        "kas_continua": "Continuă la pasul 2",
        "kas_limba": "limba textului:",
        "kas_limba_ro": "română",
        "kas_limba_en": "engleză",
        "kas_limba_ru": "rusă",
        "kas_analizeaza": "Analizează frecvențele",
        "kas_linii": "Liniile textului (caracterele 1, 1+m, 1+2m, ... pe linia 1 și așa mai departe)",
        "kas_col_linia": "Linia",
        "kas_col_n": "n",
        "kas_col_frecvente": "Cele mai frecvente",
        "kas_col_candidati": "Litere-cheie candidate",
        "kas_frecvente_detaliu": "Frecvența fiecărui caracter, pe linii:",
        "kas_cheia": "Cheia:",
        "kas_cheie_propusa": "Am încercat {n} chei. Cea mai probabilă este {cuvant}; alege alt rând din tabel ca să vezi alt text clar.",
        "kas_toate": "Toate cheile încercate ({n}), de la cea mai probabilă",
        "kas_col_nr": "Nr.",
        "kas_col_cheie": "Cheia",
        "kas_col_scor": "Scor",
        "kas_col_inceput": "Începutul textului clar",
        "kas_doar_unele": "Toate combinațiile ar fi fost prea multe, așa că pe fiecare linie am încercat cele mai potrivite {k} litere.",
        "kas_scor": "Scorul = câte perechi de litere frecvente în limbă (EA, RE, IN ...) apar în textul clar.",
        "eroare_kasiski_date": "Lungimea minimă a secvenței trebuie să fie cel puțin 2, iar lungimea maximă a cheii între 1 și 40.",
        "eroare_kasiski_m": "Lungimea cheii m trebuie să fie între 1 și 40 și mai mică decât textul.",
    },
    "en": {
        "kas_tab_1": "Step 1: key length",
        "kas_tab_2": "Step 2: the key",
        "kas_intrare": "Intercepted encrypted text:",
        "kas_minim": "minimum sequence length",
        "kas_maxim": "maximum key length",
        "kas_m": "key length m",
        "kas_cauta": "Find repetitions",
        "kas_secvente": "Repeated sequences (Kasiski)",
        "kas_col_secventa": "Sequence",
        "kas_col_pozitii": "Positions",
        "kas_col_distante": "Distances",
        "kas_lungimi": "Possible key lengths",
        "kas_col_m": "m",
        "kas_col_divizibile": "Distances divisible by m",
        "kas_col_ic": "Index of coincidence",
        "kas_sugestie": "Probable key length: m = {m} (it divides the most distances: {nr} of {total}).",
        "kas_fara_secvente": "No repeated sequences found. Try a smaller minimum length or a longer text.",
        "kas_continua": "Go to step 2",
        "kas_limba": "language of the text:",
        "kas_limba_ro": "Romanian",
        "kas_limba_en": "English",
        "kas_limba_ru": "Russian",
        "kas_analizeaza": "Analyze frequencies",
        "kas_linii": "Lines of the text (characters 1, 1+m, 1+2m, ... on line 1, and so on)",
        "kas_col_linia": "Line",
        "kas_col_n": "n",
        "kas_col_frecvente": "Most frequent",
        "kas_col_candidati": "Candidate key letters",
        "kas_frecvente_detaliu": "Frequency of every character, by line:",
        "kas_cheia": "Key:",
        "kas_cheie_propusa": "I tried {n} keys. The most likely is {cuvant}; pick another row in the table to see another plain text.",
        "kas_toate": "All keys tried ({n}), most likely first",
        "kas_col_nr": "No.",
        "kas_col_cheie": "Key",
        "kas_col_scor": "Score",
        "kas_col_inceput": "Start of the plain text",
        "kas_doar_unele": "All combinations would have been too many, so on every line I tried the {k} best-fitting letters.",
        "kas_scor": "Score = how many common letter pairs of the language (TH, HE, IN ...) appear in the plain text.",
        "eroare_kasiski_date": "The minimum sequence length must be at least 2, and the maximum key length between 1 and 40.",
        "eroare_kasiski_m": "The key length m must be between 1 and 40 and shorter than the text.",
    },
    "ru": {
        "kas_tab_1": "Шаг 1: длина ключа",
        "kas_tab_2": "Шаг 2: ключ",
        "kas_intrare": "Перехваченный шифртекст:",
        "kas_minim": "минимальная длина последовательности",
        "kas_maxim": "максимальная длина ключа",
        "kas_m": "длина ключа m",
        "kas_cauta": "Найти повторы",
        "kas_secvente": "Повторяющиеся последовательности (Касиски)",
        "kas_col_secventa": "Последовательность",
        "kas_col_pozitii": "Позиции",
        "kas_col_distante": "Расстояния",
        "kas_lungimi": "Возможные длины ключа",
        "kas_col_m": "m",
        "kas_col_divizibile": "Расстояний, кратных m",
        "kas_col_ic": "Индекс совпадений",
        "kas_sugestie": "Вероятная длина ключа: m = {m} (делит больше всего расстояний: {nr} из {total}).",
        "kas_fara_secvente": "Повторов не найдено. Уменьшите минимальную длину или возьмите текст длиннее.",
        "kas_continua": "Перейти к шагу 2",
        "kas_limba": "язык текста:",
        "kas_limba_ro": "румынский",
        "kas_limba_en": "английский",
        "kas_limba_ru": "русский",
        "kas_analizeaza": "Анализ частот",
        "kas_linii": "Строки текста (символы 1, 1+m, 1+2m, ... в строке 1 и так далее)",
        "kas_col_linia": "Строка",
        "kas_col_n": "n",
        "kas_col_frecvente": "Самые частые",
        "kas_col_candidati": "Возможные буквы ключа",
        "kas_frecvente_detaliu": "Частота каждого символа по строкам:",
        "kas_cheia": "Ключ:",
        "kas_cheie_propusa": "Проверено ключей: {n}. Самый вероятный — {cuvant}; выберите другую строку таблицы, чтобы увидеть другой открытый текст.",
        "kas_toate": "Все проверенные ключи ({n}), сначала самые вероятные",
        "kas_col_nr": "№",
        "kas_col_cheie": "Ключ",
        "kas_col_scor": "Баллы",
        "kas_col_inceput": "Начало открытого текста",
        "kas_doar_unele": "Всех комбинаций было бы слишком много, поэтому в каждой строке проверены {k} самых подходящих букв.",
        "kas_scor": "Баллы = сколько частых пар букв языка (СТ, НО, ЕН ...) встречается в открытом тексте.",
        "eroare_kasiski_date": "Минимальная длина последовательности — не меньше 2, максимальная длина ключа — от 1 до 40.",
        "eroare_kasiski_m": "Длина ключа m должна быть от 1 до 40 и меньше длины текста.",
    },
}

TEORIE_CRIPTANALIZA = {
    "ro": """
# Ce este?
Criptanaliza înseamnă găsirea textului clar fără să știi cheia. La cifrul Vigenère se lucrează în doi pași: întâi afli lungimea cheii m, apoi fiecare literă a cheii, separat.

# Pasul 1: testul Kasiski
Dacă în textul clar o secvență (de exemplu un cuvânt) se repetă, iar distanța dintre cele două apariții este un multiplu al lungimii cheii, atunci și în textul criptat apare aceeași secvență. Căutăm deci secvențe de cel puțin 3 caractere care se repetă și măsurăm distanța dintre ele:
    UNP  ->  60
    PTUN ->  213
    cmmdc(60, 213) = 3
Lungimea cheii divide majoritatea distanțelor. Unele repetiții apar întâmplător, așa că nu toate distanțele se potrivesc; de aceea tabelul arată câte distanțe se împart la fiecare m.

# Indicele de coincidență
O verificare în plus: textul se împarte în m linii. Dacă m este lungimea corectă, fiecare linie e criptată cu o singură deplasare Cezar și frecvențele ei seamănă cu ale limbii (indicele e în jur de 0,06–0,08). La un m greșit literele par aleatoare și indicele scade spre 1/26 ≈ 0,038.

# Pasul 2: literele cheii
Cu m cunoscut, textul se scrie pe m linii: linia 1 are caracterele 1, 1 + m, 1 + 2m, ..., linia 2 caracterele 2, 2 + m, ... Fiecare linie e un cifru Cezar. Se numără frecvențele: litera cea mai des întâlnită pe o linie corespunde, probabil, unei litere frecvente din limbă (E, A, I în română). Aplicația încearcă toate deplasările și le ordonează după testul chi-pătrat, adică după cât de mult seamănă linia decriptată cu limba aleasă.

# Exemplu
Pentru textul clar din curs, criptat cu cheia MAC, se găsește m = 3, iar candidații pe linii dau cheia MAC:
    UNP AAR FEC FRG ...
    MAC MAC MAC MAC ...
    INN OAP TEA TRE ...  ->  IN NOAPTEA TRECUTA ...

# Cum folosești aplicația
Lipești textul criptat (exemplul din curs este deja completat) și apeși „Caută repetițiile”. Treci la pasul 2 cu lungimea propusă, alegi limba textului și apeși „Analizează frecvențele”. Fiecare linie este un cifru Cezar, așa că aplicația încearcă toate cheile posibile (pentru m = 3: 26 · 26 · 26 = 17 576) și le ordonează după cât de mult seamănă textul clar cu limba aleasă. Cea mai probabilă se alege singură; dai clic pe alt rând ca să vezi alt text clar sau scrii tu cheia și apeși „Decriptează”.
""",
    "en": """
# What is it?
Cryptanalysis means finding the plain text without knowing the key. For the Vigenère cipher it takes two steps: first find the key length m, then every letter of the key, one at a time.

# Step 1: the Kasiski test
If a sequence (a word, say) repeats in the plain text and the distance between the two occurrences is a multiple of the key length, the same sequence also appears in the encrypted text. So we look for sequences of at least 3 characters that repeat and measure the distance between them:
    UNP  ->  60
    PTUN ->  213
    gcd(60, 213) = 3
The key length divides most of the distances. Some repetitions happen by chance, so not every distance fits; that is why the table shows how many distances are divisible by each m.

# Index of coincidence
An extra check: the text is split into m lines. If m is the right length, every line is encrypted with a single Caesar shift and its frequencies look like the language (the index is around 0.06–0.08). With a wrong m the letters look random and the index drops towards 1/26 ≈ 0.038.

# Step 2: the key letters
With m known, the text is written on m lines: line 1 holds characters 1, 1 + m, 1 + 2m, ..., line 2 characters 2, 2 + m, ... Each line is a Caesar cipher. Count the frequencies: the most common letter on a line probably stands for a common letter of the language (E, T, A in English). The app tries every shift and orders them by the chi-squared test, that is by how closely the decrypted line matches the chosen language.

# Example
For the plain text from the course, encrypted with the key MAC, m = 3 is found, and the candidates on the lines give the key MAC:
    UNP AAR FEC FRG ...
    MAC MAC MAC MAC ...
    INN OAP TEA TRE ...  ->  IN NOAPTEA TRECUTA ...

# How to use the app
Paste the encrypted text (the course example is already filled in) and press "Find repetitions". Go to step 2 with the proposed length, pick the language of the text and press "Analyze frequencies". Every line is a Caesar cipher, so the app tries every possible key (for m = 3: 26 · 26 · 26 = 17,576) and orders them by how closely the plain text looks like the chosen language. The most likely one is picked by itself; click another row to see another plain text, or type a key and press "Decrypt".
""",
    "ru": """
# Что это?
Криптоанализ — это поиск открытого текста без знания ключа. Для шифра Виженера он идёт в два шага: сначала находим длину ключа m, затем каждую букву ключа по отдельности.

# Шаг 1: тест Касиски
Если в открытом тексте повторяется последовательность (например, слово) и расстояние между её появлениями кратно длине ключа, то и в шифртексте появится одинаковая последовательность. Поэтому ищем повторяющиеся последовательности не короче 3 символов и измеряем расстояние между ними:
    UNP  ->  60
    PTUN ->  213
    НОД(60, 213) = 3
Длина ключа делит большинство расстояний. Некоторые повторы случайны, поэтому подходят не все расстояния; таблица показывает, сколько расстояний делится на каждое m.

# Индекс совпадений
Дополнительная проверка: текст делится на m строк. Если m правильное, каждая строка зашифрована одним сдвигом Цезаря, и её частоты похожи на частоты языка (индекс около 0,06–0,08). При неверном m буквы выглядят случайными, и индекс падает к 1/26 ≈ 0,038.

# Шаг 2: буквы ключа
Зная m, записываем текст в m строк: в строке 1 символы 1, 1 + m, 1 + 2m, ..., в строке 2 символы 2, 2 + m, ... Каждая строка — шифр Цезаря. Считаем частоты: самая частая буква строки, вероятно, соответствует частой букве языка (О, Е, А в русском). Приложение перебирает все сдвиги и упорядочивает их по критерию хи-квадрат, то есть по сходству расшифрованной строки с выбранным языком.

# Пример
Для открытого текста из курса, зашифрованного ключом MAC, находится m = 3, а кандидаты по строкам дают ключ MAC:
    UNP AAR FEC FRG ...
    MAC MAC MAC MAC ...
    INN OAP TEA TRE ...  ->  IN NOAPTEA TRECUTA ...

# Как пользоваться приложением
Вставьте шифртекст (пример из курса уже введён) и нажмите «Найти повторы». Перейдите к шагу 2 с предложенной длиной, выберите язык текста и нажмите «Анализ частот». Каждая строка — шифр Цезаря, поэтому приложение перебирает все возможные ключи (для m = 3: 26 · 26 · 26 = 17 576) и упорядочивает их по сходству открытого текста с выбранным языком. Самый вероятный выбирается сам; щёлкните другую строку, чтобы увидеть другой открытый текст, или введите ключ и нажмите «Расшифровать».
""",
}

traduceri.adauga_texte(TEXTE_CRIPTANALIZA)
teorie.TEORIE["criptanaliza_vigenere"] = TEORIE_CRIPTANALIZA


def tabel(parinte: tk.Misc, coloane: dict[str, int], inaltime: int) -> ttk.Treeview:
    """Un tabel cu bara de derulare; `coloane` = {cheia textului de antet: latime}."""
    cadru = ttk.Frame(parinte)
    cadru.pack(fill="both", expand=True)
    arbore = ttk.Treeview(cadru, columns=list(coloane), show="headings", height=inaltime)
    for cheie, latime in coloane.items():
        arbore.heading(cheie, text=t(cheie))
        arbore.column(cheie, width=latime, anchor="w")
    derulare = ttk.Scrollbar(cadru, command=arbore.yview)
    arbore.configure(yscrollcommand=derulare.set)
    derulare.pack(side="right", fill="y")
    arbore.pack(fill="both", expand=True)
    return arbore


def umple(arbore: ttk.Treeview, randuri: list[tuple]) -> None:
    arbore.delete(*arbore.get_children())
    for rand in randuri:
        arbore.insert("", "end", values=rand)


def lungimea_probabila(distante: list[int], maxim: int) -> int:
    """Lungimea m care divide cele mai multe distante (la egalitate, cea mai mare)."""
    numar = {m: sum(1 for d in distante if d % m == 0) for m in range(2, maxim + 1)}
    return max(numar, key=lambda m: (numar[m], m))


class AplicatieCriptanaliza(AplicatieCifru):
    def __init__(self):
        super().__init__(FOLDER, campuri_cheie=[], alfabet=alf.LATIN, pastreaza_restul=False)
        self.potriveste_marimea(1100, 940)

    def _construieste_taburi(self) -> None:
        if not hasattr(self, "valori_kasiski"):
            self.valori_kasiski = [tk.StringVar(value=c.implicit) for c in CAMPURI_KASISKI]
            self.lungime = tk.StringVar(value=CAMP_LUNGIME.implicit)
            self.cheie = tk.StringVar()
            self.limba_text = tk.StringVar(value="ro")
            self.randuri = {"secvente": [], "lungimi": [], "linii": [], "chei": []}
            self.sugestie = ""
        self._tab_kasiski()
        self._tab_cheia()
        if not self.zone["kas_in"].get("1.0", "end-1c").strip():
            self.zone["kas_in"].insert("1.0", TEXT_EXEMPLU)
        for nume, arbore in self.tabele.items():
            umple(arbore, self.randuri[nume])
        self.eticheta_sugestie.configure(text=self.sugestie)

    # ---------- pasul 1 ----------

    def _tab_kasiski(self) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t("kas_tab_1"))
        self.tabele = {}
        intrare = tema.zona_text(tab, 5)
        self.zone["kas_in"] = intrare
        self._rand_titlu(tab, t("kas_intrare"), t("dec_citeste"), lambda: self._citeste_din_fisier(intrare))
        intrare.pack(fill="x")

        rand = ttk.Frame(tab)
        rand.pack(fill="x", pady=12)
        for camp, valoare in zip(CAMPURI_KASISKI, self.valori_kasiski):
            ttk.Label(rand, text=f"{t(camp.eticheta)} =").pack(side="left", padx=(0, 6))
            ttk.Entry(rand, textvariable=valoare, width=5).pack(side="left", padx=(0, 16))
        ttk.Button(rand, text=t("kas_cauta"), style="Accent.TButton", cursor="hand2",
                   command=self._cauta_repetitiile).pack(side="right")

        tabele = ttk.Frame(tab)
        tabele.pack(fill="both", expand=True)
        tabele.columnconfigure(0, weight=1, uniform="t")
        tabele.columnconfigure(1, weight=1, uniform="t")
        tabele.rowconfigure(0, weight=1)
        for coloana, (nume, titlu, coloane) in enumerate((
                ("secvente", "kas_secvente", {"kas_col_secventa": 120, "kas_col_pozitii": 150,
                                              "kas_col_distante": 150}),
                ("lungimi", "kas_lungimi", {"kas_col_m": 40, "kas_col_divizibile": 200,
                                            "kas_col_ic": 180}))):
            cadru = ttk.LabelFrame(tabele, text=t(titlu), padding=8)
            cadru.grid(row=0, column=coloana, sticky="nsew", padx=(0, 8) if coloana == 0 else (8, 0))
            self.tabele[nume] = tabel(cadru, coloane, 8)

        rand = ttk.Frame(tab)
        rand.pack(fill="x", pady=(12, 0))
        self.eticheta_sugestie = ttk.Label(rand, foreground=tema.ACCENT, font=tema.FONT_UI_BOLD)
        self.eticheta_sugestie.pack(side="left")
        ttk.Button(rand, text=t("kas_continua"), cursor="hand2",
                   command=lambda: self.carnet.select(2)).pack(side="right")

    def _cauta_repetitiile(self) -> None:
        try:
            minim, maxim = (str(self._intreg(t(c.eticheta), v.get()))
                            for c, v in zip(CAMPURI_KASISKI, self.valori_kasiski))
            text = self.zone["kas_in"].get("1.0", "end-1c")
            parametri = ["kasiski", minim, maxim, alf.coduri_alfabet(self._alfabet_valid())]
            iesire = ruleaza_motor(self.folder, parametri, self._codifica_text(text), curata_text=False)
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return

        pozitii = defaultdict(set)   # secventa -> pozitiile ei (de la 1)
        indici = []
        for linie in iesire.splitlines():
            bucati = linie.split("\t")
            if bucati[0] == "SECV":
                pozitii[bucati[1]].update({int(bucati[2]) + 1, int(bucati[3]) + 1})
            else:
                indici.append((int(bucati[1]), bucati[2]))

        alfabet = self._alfabet_valid()
        secvente, distante = [], []
        for secventa, locuri in sorted(pozitii.items(), key=lambda p: (-len(p[0]), min(p[1]))):
            locuri = sorted(locuri)
            d = [b - a for a, b in zip(locuri, locuri[1:])]
            distante += d
            secvente.append((alf.decodifica(secventa, alfabet), ", ".join(map(str, locuri)),
                             ", ".join(map(str, d))))
        self.randuri["secvente"] = secvente
        self.randuri["lungimi"] = [(m, sum(1 for d in distante if d % m == 0) if m > 1 else "", ic)
                                   for m, ic in indici]
        umple(self.tabele["secvente"], self.randuri["secvente"])
        umple(self.tabele["lungimi"], self.randuri["lungimi"])

        if not distante:
            self.sugestie = ""
            self._mesaj(t("kas_fara_secvente"), eroare=True)
        else:
            m = lungimea_probabila(distante, max(len(indici), 2))
            nr = sum(1 for d in distante if d % m == 0)
            self.sugestie = t("kas_sugestie", m=m, nr=nr, total=len(distante))
            self.lungime.set(str(m))
            self._mesaj(self.sugestie)
        self.eticheta_sugestie.configure(text=self.sugestie)

    # ---------- pasul 2 ----------

    def _tab_cheia(self) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t("kas_tab_2"))

        rand = ttk.Frame(tab)
        rand.pack(fill="x")
        ttk.Label(rand, text=f"{t('kas_m')} =").pack(side="left", padx=(0, 6))
        ttk.Entry(rand, textvariable=self.lungime, width=5).pack(side="left", padx=(0, 16))
        ttk.Label(rand, text=t("kas_limba")).pack(side="left", padx=(0, 6))
        nume_limbi = {cod: t(f"kas_limba_{cod}") for cod in FRECVENTE}
        alegere = ttk.Combobox(rand, state="readonly", width=12, values=list(nume_limbi.values()))
        alegere.set(nume_limbi[self.limba_text.get()])
        alegere.bind("<<ComboboxSelected>>", lambda _e: self.limba_text.set(
            list(nume_limbi)[list(nume_limbi.values()).index(alegere.get())]))
        alegere.pack(side="left")
        ttk.Button(rand, text=t("kas_analizeaza"), style="Accent.TButton", cursor="hand2",
                   command=self._analizeaza_frecventele).pack(side="right")

        # Partea de jos (cheia si textul clar) se aseaza prima, ca sa ramana vizibila
        # si pe ecrane mici; tabelele de deasupra se micsoreaza ele.
        jos = ttk.Frame(tab)
        jos.pack(side="bottom", fill="x")
        rand = ttk.Frame(jos)
        rand.pack(fill="x", pady=(10, 6))
        ttk.Label(rand, text=t("kas_cheia"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 8))
        intrare_cheie = ttk.Entry(rand, textvariable=self.cheie, width=24, font=tema.FONT_COD)
        intrare_cheie.pack(side="left")
        intrare_cheie.bind("<Return>", lambda _e: self._decripteaza())
        ttk.Button(rand, text=t("dec_scrie"), cursor="hand2",
                   command=lambda: self._scrie_in_fisier(self.zone["kas_out"])).pack(side="right")
        ttk.Button(rand, text=t("dec_buton"), style="Accent.TButton", cursor="hand2",
                   command=self._decripteaza).pack(side="right", padx=(0, 8))
        iesire = tema.zona_text(jos, 3, doar_citire=True)
        self.zone["kas_out"] = iesire
        iesire.pack(fill="x")

        mijloc = ttk.Frame(tab)
        mijloc.pack(fill="both", expand=True, pady=(10, 0))
        mijloc.columnconfigure(0, weight=1, uniform="m")
        mijloc.columnconfigure(1, weight=1, uniform="m")
        mijloc.rowconfigure(0, weight=1)

        stanga = ttk.Frame(mijloc)
        stanga.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        cadru = ttk.LabelFrame(stanga, text=t("kas_linii"), padding=6)
        cadru.pack(fill="both", expand=True)
        self.tabele["linii"] = tabel(cadru, {"kas_col_linia": 50, "kas_col_n": 45,
                                             "kas_col_frecvente": 220, "kas_col_candidati": 150}, 3)
        ttk.Label(stanga, text=t("kas_frecvente_detaliu"), font=tema.FONT_UI_BOLD).pack(anchor="w", pady=(8, 4))
        detaliu = tema.zona_text(stanga, 3, doar_citire=True)
        self.zone["kas_detaliu"] = detaliu
        detaliu.pack(fill="both", expand=True)

        self.cadru_chei = ttk.LabelFrame(mijloc, text=t("kas_toate", n=len(self.randuri["chei"])), padding=6)
        self.cadru_chei.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        self.tabele["chei"] = tabel(self.cadru_chei, {"kas_col_nr": 50, "kas_col_cheie": 80,
                                                      "kas_col_scor": 60, "kas_col_inceput": 400}, 6)
        self.tabele["chei"].bind("<<TreeviewSelect>>", lambda _e: self._alege_cheia())
        ttk.Label(self.cadru_chei, text=t("kas_scor"), foreground=tema.TEXT_SLAB, font=tema.FONT_MIC,
                  wraplength=520, justify="left").pack(fill="x", pady=(6, 0))

    def _frecvente_limba(self, alfabet: str) -> list[str]:
        """Frecventa fiecarui caracter din alfabet in limba aleasa, la 10 000 de litere."""
        tabel_limba = FRECVENTE[self.limba_text.get()]
        return [str(max(1, round(tabel_limba.get(c.upper(), FRECVENTA_NECUNOSCUTA) * 100))) for c in alfabet]

    def _perechi_limba(self, alfabet: str) -> list[str]:
        """Perechile frecvente ale limbii, codate; cele cu litere care lipsesc din alfabet se sar."""
        perechi = [alf.codifica(pereche, alfabet) for pereche in PERECHI_FRECVENTE[self.limba_text.get()]]
        return [pereche for pereche in perechi if len(pereche) == 2]

    def _analizeaza_frecventele(self) -> None:
        try:
            alfabet = self._alfabet_valid()
            m = str(self._intreg(t("kas_m"), self.lungime.get()))
            frecvente = self._frecvente_limba(alfabet)
            perechi = self._perechi_limba(alfabet)
            text = self.zone["kas_in"].get("1.0", "end-1c")
            parametri = ["frecvente", m, str(len(frecvente)), " ".join(frecvente),
                         str(len(perechi)), " ".join(perechi), alf.coduri_alfabet(alfabet)]
            iesire = ruleaza_motor(self.folder, parametri, self._codifica_text(text), curata_text=False)
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return

        linii, detalii, chei, pe_linie = [], [], [], 0
        for linie in iesire.splitlines():
            bucati = linie.split("\t")
            if bucati[0] == "LINIE":
                caractere = alf.decodifica(bucati[2], alfabet)
            elif bucati[0] == "FRECV":
                numar = [int(x) for x in bucati[2:]]
                ordine = sorted(range(len(alfabet)), key=lambda c: -numar[c])
                frecvente_mari = ", ".join(f"{alfabet[c]}-{numar[c]}" for c in ordine[:CATE_FRECVENTE] if numar[c])
                detalii.append(f"{bucati[1]} (n={len(caractere)}):  " +
                               "  ".join(f"{c}-{n}" for c, n in zip(alfabet, numar)))
            elif bucati[0] == "CANDIDATI":
                candidati = [alfabet[int(x)] for x in bucati[2:]]
                linii.append((bucati[1], len(caractere), frecvente_mari, "{" + ", ".join(candidati) + "}"))
            elif bucati[0] == "PE_LINIE":
                pe_linie = int(bucati[1])
            else:  # COMB
                chei.append((alf.decodifica(bucati[1], alfabet), int(bucati[2]),
                             alf.decodifica(bucati[3], alfabet)))

        chei.sort(key=lambda rand: -rand[1])  # sortare stabila: la egalitate ramane ordinea chi-patrat
        self.randuri["linii"] = linii
        self.randuri["chei"] = [(nr, *rand) for nr, rand in enumerate(chei, start=1)]
        umple(self.tabele["linii"], linii)
        umple(self.tabele["chei"], self.randuri["chei"])
        self.cadru_chei.configure(text=t("kas_toate", n=len(chei)))
        tema.scrie_in_zona(self.zone["kas_detaliu"], "\n".join(detalii))

        primul = self.tabele["chei"].get_children()[0]
        self.tabele["chei"].selection_set(primul)  # cheia cea mai probabila
        self.tabele["chei"].see(primul)
        self._alege_cheia()  # imediat, nu abia cand Tk trimite evenimentul de selectie
        nota = "" if pe_linie == len(alfabet) else " " + t("kas_doar_unele", k=pe_linie)
        self._mesaj(t("kas_cheie_propusa", cuvant=chei[0][0], n=len(chei)) + nota)

    def _alege_cheia(self) -> None:
        selectie = self.tabele["chei"].selection()
        if selectie:
            self.cheie.set(self.tabele["chei"].set(selectie[0], "kas_col_cheie"))
            self._decripteaza(cu_mesaj=False)

    def _decripteaza(self, cu_mesaj: bool = True) -> None:
        try:
            alfabet = self._alfabet_valid()
            cheie = self._valoare_pentru_motor(CAMP_CHEIE, self.cheie.get(), alfabet)
            text = self.zone["kas_in"].get("1.0", "end-1c")
            parametri = ["decripteaza", cheie, alf.coduri_alfabet(alfabet)]
            iesire = ruleaza_motor(FOLDER_VIGENERE, parametri, self._codifica_text(text), curata_text=False)
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return
        tema.scrie_in_zona(self.zone["kas_out"], alf.decodifica(iesire.strip(), alfabet))
        if cu_mesaj:
            self._mesaj(t("mesaj_gata"))


if __name__ == "__main__":
    AplicatieCriptanaliza().mainloop()
