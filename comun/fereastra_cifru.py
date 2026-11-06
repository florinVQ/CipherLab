"""Fereastra folosita de fiecare cifru: teorie, criptare, decriptare si (la unele cifruri) atac.

Fiecare cifru isi descrie doar campurile cheii; criptarea propriu-zisa o face
motorul C++ (motor.cpp) din folderul cifrului.
"""

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, ttk

import bara_setari
import setari
import tema
from motor_cpp import LUNGIME_MAXIMA, EroareMotor, pregateste, ruleaza_motor
from teorie import TEORIE
import traduceri
from traduceri import t

COMENZI = {"cr": "cripteaza", "dec": "decripteaza"}
LITERE_FRECVENTE = "EAITNRSOULCD"


@dataclass
class Camp:
    """Un camp pentru cheie. `eticheta` este un simbol (k, a, b) sau o cheie de traducere."""
    eticheta: str
    implicit: str = ""
    numar: bool = False


def scor_text(text: str) -> int:
    """Cate litere din text sunt dintre cele mai frecvente (mai mare = seamana mai mult a text)."""
    return sum(1 for litera in text if litera in LITERE_FRECVENTE)


class AplicatieCifru(tk.Tk):
    def __init__(self, folder: Path, campuri_cheie: list[Camp],
                 campuri_atac: list[Camp] | None = None,
                 campuri_decriptare: list[Camp] | None = None):
        """`campuri_atac=None` inseamna ca cifrul nu are tab de atac;
        `campuri_decriptare=None` inseamna ca decriptarea foloseste aceeasi cheie."""
        super().__init__()
        setari.incarca()
        self.folder = folder
        self.cod = folder.name
        self.campuri = {"cr": campuri_cheie}
        self.valori = {"cr": self._valori_noi(campuri_cheie)}
        if campuri_decriptare is None:
            self.campuri["dec"] = self.campuri["cr"]
            self.valori["dec"] = self.valori["cr"]  # cheia se scrie o singura data
        else:
            self.campuri["dec"] = campuri_decriptare
            self.valori["dec"] = self._valori_noi(campuri_decriptare)
        if campuri_atac is not None:
            self.campuri["atac"] = campuri_atac
            self.valori["atac"] = self._valori_noi(campuri_atac)

        self.mesaj = tk.StringVar()
        self.zone = {}          # casutele de text, ca sa le putem pastra la schimbarea limbii
        self.randuri_atac = []  # rezultatele ultimului atac: (cheie, text clar)
        self.geometry("1080x820")
        self.minsize(940, 740)
        self._construieste()

    def _valori_noi(self, campuri: list[Camp]) -> list[tk.StringVar]:
        return [tk.StringVar(value=camp.implicit) for camp in campuri]

    # ---------- construirea ferestrei ----------

    def _construieste(self) -> None:
        self.title(t("titlu_" + self.cod))
        self.configure(bg=tema.FUNDAL)
        tema.aplica_stilul(self)

        self._construieste_antet()
        self._construieste_bara_de_stare()
        self.carnet = ttk.Notebook(self)
        self.carnet.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        self._tab_teorie()
        self._tab_transformare("cr")
        self._tab_transformare("dec")
        if "atac" in self.campuri:
            self._tab_atac()

    def _reconstruieste(self) -> None:
        """Reface fereastra dupa schimbarea limbii sau a temei, pastrand textele scrise."""
        texte = {nume: zona.get("1.0", "end-1c") for nume, zona in self.zone.items()}
        tab_curent = self.carnet.index(self.carnet.select())
        selectat = self._index_selectat_atac()

        for element in self.winfo_children():
            element.destroy()
        self.zone = {}
        self.mesaj.set("")
        self._construieste()

        for nume, continut in texte.items():
            tema.scrie_in_zona(self.zone[nume], continut)
        if "atac" in self.campuri:
            self._umple_tabel_atac(selectat)
        self.carnet.select(tab_curent)

    def _construieste_antet(self) -> None:
        antet = tk.Frame(self, bg=tema.FUNDAL)
        antet.pack(fill="x", padx=20, pady=(16, 12))
        # Bara de setari se aseaza prima, ca sa nu o impinga titlul afara din fereastra.
        bara_setari.construieste_bara_setari(antet, self._reconstruieste).pack(side="right", anchor="n")
        titlu = tk.Frame(antet, bg=tema.FUNDAL)
        titlu.pack(side="left")
        tk.Label(titlu, text=t("titlu_" + self.cod), bg=tema.FUNDAL, fg=tema.TEXT,
                 font=tema.FONT_TITLU, wraplength=640, justify="left").pack(anchor="w")
        tk.Frame(titlu, bg=tema.ACCENT, height=3, width=64).pack(anchor="w", pady=6)

    def _construieste_bara_de_stare(self) -> None:
        bara = tk.Frame(self, bg=tema.FUNDAL)
        bara.pack(side="bottom", fill="x", padx=20, pady=(0, 12))
        self.eticheta_mesaj = tk.Label(
            bara, textvariable=self.mesaj, bg=tema.FUNDAL, fg=tema.TEXT_SLAB,
            font=tema.FONT_MIC, anchor="w", justify="left", wraplength=980)
        self.eticheta_mesaj.pack(fill="x")

    def _tab_teorie(self) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t("teorie_tab"))

        zona = tema.zona_text(tab, 10)
        zona.configure(font=tema.FONT_UI, padx=16, pady=12, spacing2=3)
        zona.tag_configure("titlu", foreground=tema.ACCENT, font=tema.FONT_UI_BOLD,
                           spacing1=12, spacing3=4)
        zona.tag_configure("formula", font=tema.FONT_COD, foreground=tema.SUCCES,
                           lmargin1=24, lmargin2=24)
        for linie in TEORIE[self.cod][traduceri.limba].strip().splitlines():
            if linie.startswith("# "):
                zona.insert("end", linie[2:] + "\n", "titlu")
            elif linie.startswith("    "):
                zona.insert("end", linie.strip() + "\n", "formula")
            else:
                zona.insert("end", linie + "\n")
        zona.configure(state="disabled")

        derulare = ttk.Scrollbar(tab, command=zona.yview)
        zona.configure(yscrollcommand=derulare.set)
        derulare.pack(side="right", fill="y")
        zona.pack(fill="both", expand=True)

    def _tab_transformare(self, prefix: str) -> None:
        """Tabul de criptare (prefix "cr") sau de decriptare (prefix "dec")."""
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t(f"{prefix}_tab"))

        intrare = tema.zona_text(tab, 6)
        iesire = tema.zona_text(tab, 6, doar_citire=True)
        self.zone[f"{prefix}_in"] = intrare
        self.zone[f"{prefix}_out"] = iesire

        def executa(_eveniment=None) -> None:
            self._transforma(prefix)

        self._rand_titlu(tab, t(f"{prefix}_intrare"), t(f"{prefix}_citeste"),
                         lambda: self._citeste_din_fisier(intrare))
        intrare.pack(fill="x")

        rand_cheie = ttk.Frame(tab)
        rand_cheie.pack(fill="x", pady=14)
        ttk.Button(rand_cheie, text=t(f"{prefix}_buton"), style="Accent.TButton", cursor="hand2",
                   command=executa).pack(side="right")
        ttk.Label(rand_cheie, text=t(f"{prefix}_cheie"), font=tema.FONT_UI_BOLD).pack(side="left", padx=(0, 12))
        self._campuri_in_rand(rand_cheie, prefix, executa)

        # La criptare, rezultatul este "textul criptat"; la decriptare, "textul clar".
        self._rand_titlu(tab, t(f"{prefix}_iesire"), t(f"{prefix}_scrie"),
                         lambda: self._scrie_in_fisier(iesire))
        iesire.pack(fill="both", expand=True)

    def _tab_atac(self) -> None:
        tab = ttk.Frame(self.carnet, padding=16)
        self.carnet.add(tab, text=t("atac_tab"))

        intrare = tema.zona_text(tab, 3)
        self.clar_atac = tema.zona_text(tab, 3, doar_citire=True)
        self.zone["atac_in"] = intrare
        self.zone["atac_clar"] = self.clar_atac

        def porneste(_eveniment=None) -> None:
            self._porneste_atac()

        self._rand_titlu(tab, t("atac_intrare"), t("dec_citeste"),
                         lambda: self._citeste_din_fisier(intrare))
        intrare.pack(fill="x")

        rand_atac = ttk.Frame(tab)
        rand_atac.pack(fill="x", pady=12)
        ttk.Button(rand_atac, text=t("atac_buton"), style="Accent.TButton", cursor="hand2",
                   command=porneste).pack(side="right")
        self._campuri_in_rand(rand_atac, "atac", porneste)

        self._construieste_tabel_atac(tab)

        rand_cheie = ttk.Frame(tab)
        rand_cheie.pack(fill="x", pady=(12, 8))
        ttk.Label(rand_cheie, text=t("atac_cheie_este"), font=tema.FONT_UI_BOLD).pack(side="left")
        self.cheie_gasita = ttk.Label(rand_cheie, text="—", foreground=tema.ACCENT, font=tema.FONT_COD)
        self.cheie_gasita.pack(side="left", padx=10)

        self._rand_titlu(tab, t("dec_iesire"), t("dec_scrie"),
                         lambda: self._scrie_in_fisier(self.clar_atac))
        self.clar_atac.pack(fill="x")

    def _construieste_tabel_atac(self, parinte: ttk.Frame) -> None:
        cadru = ttk.Frame(parinte)
        cadru.pack(fill="both", expand=True)
        self.tabel_atac = ttk.Treeview(cadru, columns=("cheie", "text"), show="headings", height=5)
        self.tabel_atac.heading("cheie", text=t("atac_col_cheie"))
        self.tabel_atac.heading("text", text=t("atac_col_text"))
        self.tabel_atac.column("cheie", width=230, stretch=False)
        self.tabel_atac.column("text", width=600)
        self.tabel_atac.bind("<<TreeviewSelect>>", lambda _eveniment: self._arata_selectia())

        derulare = ttk.Scrollbar(cadru, command=self.tabel_atac.yview)
        self.tabel_atac.configure(yscrollcommand=derulare.set)
        derulare.pack(side="right", fill="y")
        self.tabel_atac.pack(fill="both", expand=True)

    # ---------- piese mici refolosite ----------

    def _rand_titlu(self, parinte, eticheta: str, text_buton: str, la_apasare) -> None:
        """Un rand cu o eticheta la stanga si un buton (citire/scriere fisier) la dreapta."""
        rand = ttk.Frame(parinte)
        rand.pack(fill="x", pady=(0, 6))
        ttk.Label(rand, text=eticheta, font=tema.FONT_UI_BOLD).pack(side="left")
        ttk.Button(rand, text=text_buton, cursor="hand2", command=la_apasare).pack(side="right")

    def _campuri_in_rand(self, parinte, prefix: str, la_enter) -> None:
        for camp, valoare in zip(self.campuri[prefix], self.valori[prefix]):
            ttk.Label(parinte, text=f"{t(camp.eticheta)} =").pack(side="left", padx=(0, 6))
            intrare = ttk.Entry(parinte, textvariable=valoare, width=5 if camp.numar else 20)
            intrare.pack(side="left", padx=(0, 16))
            intrare.bind("<Return>", la_enter)

    def _mesaj(self, text: str, eroare: bool = False) -> None:
        self.mesaj.set(" ".join(text.split())[:300])
        self.eticheta_mesaj.configure(fg=tema.EROARE if eroare else tema.SUCCES)

    def _text_eroare(self, eroare: EroareMotor) -> str:
        mesaj = t("eroare_" + eroare.cod, max=LUNGIME_MAXIMA)
        return f"{mesaj} {eroare.detalii}" if eroare.detalii else mesaj

    def _citeste_valori(self, prefix: str) -> list[str]:
        """Citeste cheia din campuri: fara spatii, cu majuscule, iar numerele verificate."""
        rezultat = []
        for camp, valoare in zip(self.campuri[prefix], self.valori[prefix]):
            text = "".join(pregateste(valoare.get()).split())
            if not text:
                raise ValueError(t("camp_gol", camp=t(camp.eticheta)))
            if camp.numar:
                try:
                    int(text)
                except ValueError:
                    raise ValueError(t("camp_numar", camp=t(camp.eticheta)))
            rezultat.append(text)
        return rezultat

    # ---------- actiunile butoanelor ----------

    def _transforma(self, prefix: str) -> None:
        text = self.zone[f"{prefix}_in"].get("1.0", "end-1c")
        if not text.strip():
            self._mesaj(t("mesaj_text_gol"), eroare=True)
            return
        try:
            parametri = [COMENZI[prefix], *self._citeste_valori(prefix)]
            rezultat = ruleaza_motor(self.folder, parametri, text)
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return
        tema.scrie_in_zona(self.zone[f"{prefix}_out"], rezultat)
        self._mesaj(t("mesaj_gata"))

    def _porneste_atac(self) -> None:
        text = self.zone["atac_in"].get("1.0", "end-1c")
        if not text.strip():
            self._mesaj(t("mesaj_atac_text_gol"), eroare=True)
            return
        try:
            parametri = ["atac", *self._citeste_valori("atac")]
            self._mesaj(t("mesaj_atac_ruleaza"))
            self.update_idletasks()
            iesire = ruleaza_motor(self.folder, parametri, text)
        except ValueError as eroare:
            self._mesaj(str(eroare), eroare=True)
            return
        except EroareMotor as eroare:
            self._mesaj(self._text_eroare(eroare), eroare=True)
            return

        self.randuri_atac = []
        for linie in iesire.splitlines():
            cheie, _, clar = linie.partition("\t")
            self.randuri_atac.append((cheie, clar))
        self.randuri_atac.sort(key=lambda rand: scor_text(rand[1]), reverse=True)

        if not self.randuri_atac:
            self._mesaj(t("mesaj_atac_nimic"), eroare=True)
            return
        self._umple_tabel_atac(0)
        self._mesaj(t("mesaj_atac_gata", n=len(self.randuri_atac)))

    def _umple_tabel_atac(self, index_selectat: int) -> None:
        """Afiseaza `self.randuri_atac` in tabel si selecteaza randul cerut."""
        self.tabel_atac.delete(*self.tabel_atac.get_children())
        for cheie, clar in self.randuri_atac:
            self.tabel_atac.insert("", "end", values=(cheie, clar))
        randuri = self.tabel_atac.get_children()
        if randuri:
            self.tabel_atac.selection_set(randuri[index_selectat])
            self.tabel_atac.see(randuri[index_selectat])

    def _index_selectat_atac(self) -> int:
        if "atac" not in self.campuri or not self.tabel_atac.selection():
            return 0
        return self.tabel_atac.index(self.tabel_atac.selection()[0])

    def _arata_selectia(self) -> None:
        selectie = self.tabel_atac.selection()
        if not selectie:
            return
        self.cheie_gasita.configure(text=self.tabel_atac.set(selectie[0], "cheie"))
        tema.scrie_in_zona(self.clar_atac, self.tabel_atac.set(selectie[0], "text"))

    def _citeste_din_fisier(self, zona: tk.Text) -> None:
        cale = filedialog.askopenfilename(title=t("dialog_alege"), filetypes=self._tipuri_fisiere())
        if not cale:
            return
        try:
            continut = Path(cale).read_text(encoding="utf-8-sig", errors="replace")
        except OSError as eroare:
            self._mesaj(t("mesaj_fisier_eroare_citire", motiv=eroare.strerror), eroare=True)
            return
        zona.delete("1.0", "end")
        zona.insert("1.0", continut)
        self._mesaj(t("mesaj_fisier_citit", nume=Path(cale).name))

    def _scrie_in_fisier(self, zona: tk.Text) -> None:
        continut = zona.get("1.0", "end-1c")
        if not continut.strip():
            self._mesaj(t("mesaj_nimic_de_salvat"), eroare=True)
            return
        cale = filedialog.asksaveasfilename(title=t("dialog_salveaza"), defaultextension=".txt",
                                            filetypes=self._tipuri_fisiere())
        if not cale:
            return
        try:
            Path(cale).write_text(continut, encoding="utf-8")
        except OSError as eroare:
            self._mesaj(t("mesaj_fisier_eroare_scriere", motiv=eroare.strerror), eroare=True)
            return
        self._mesaj(t("mesaj_salvat", nume=Path(cale).name))

    def _tipuri_fisiere(self) -> list[tuple[str, str]]:
        return [(t("dialog_text"), "*.txt"), (t("dialog_toate"), "*.*")]
