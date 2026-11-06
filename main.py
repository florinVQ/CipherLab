"""CriptoLab - meniul principal. Fiecare cartonas deschide mini-aplicatia unui cifru."""

import subprocess
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import ttk

RADACINA = Path(__file__).resolve().parent
sys.path.insert(0, str(RADACINA / "comun"))

import bara_setari  # noqa: E402
import setari  # noqa: E402
import tema  # noqa: E402
import traduceri  # noqa: E402
from traduceri import t  # noqa: E402

COLOANE = 4


@dataclass
class Cifru:
    cod: str  # numele folderului cifrului, ca in traduceri: nume_<cod>, desc_<cod>
    tip: str  # monoalfabetic, polialfabetic, omofonic sau poligrafic


CIFRURI_SIMETRICE = [
    Cifru("cezar", "monoalfabetic"),
    Cifru("cezar_cheie", "monoalfabetic"),
    Cifru("afin", "monoalfabetic"),
    Cifru("polibius", "monoalfabetic"),
    Cifru("homofonic", "omofonic"),
    Cifru("vigenere", "polialfabetic"),
    Cifru("hill", "poligrafic"),
]


class Cartonas(tk.Frame):
    """Un cartonas apasabil, cu efect la trecerea mouse-ului si la focus de la tastatura."""

    def __init__(self, parinte: tk.Misc, cifru: Cifru, la_atingere, la_deschidere):
        super().__init__(parinte, bg=tema.PANOU, highlightthickness=2, cursor="hand2",
                         highlightbackground=tema.BORDURA, highlightcolor=tema.ACCENT,
                         takefocus=True, padx=18, pady=14)
        culoare_tip = getattr(tema, "TIP_" + cifru.tip.upper())
        nume = tk.Label(self, text=t("nume_" + cifru.cod), font=("Segoe UI", 15, "bold"),
                        bg=tema.PANOU, fg=tema.TEXT, anchor="w")
        tip = tk.Label(self, text=t("tip_" + cifru.tip).upper(), font=("Segoe UI", 9, "bold"),
                       bg=tema.PANOU, fg=culoare_tip, anchor="w")
        descriere = tk.Label(self, text=t("desc_" + cifru.cod), font=tema.FONT_MIC, bg=tema.PANOU,
                             fg=tema.TEXT_SLAB, anchor="w", justify="left", wraplength=210)
        deschide = tk.Label(self, text=t("deschide") + "  →", font=("Segoe UI", 10, "bold"),
                            bg=tema.PANOU, fg=tema.ACCENT, anchor="w")
        for eticheta in (nume, tip, descriere, deschide):
            eticheta.pack(fill="x", pady=2)

        self.etichete = [nume, tip, descriere, deschide]
        self.descriere = t("desc_" + cifru.cod)
        self.la_atingere = la_atingere
        for element in [self, *self.etichete]:
            element.bind("<Enter>", lambda _e: self._evidentiaza(True))
            element.bind("<Leave>", lambda _e: self._evidentiaza(False))
            element.bind("<Button-1>", lambda _e: la_deschidere(cifru))
        self.bind("<FocusIn>", lambda _e: self._evidentiaza(True))
        self.bind("<FocusOut>", lambda _e: self._evidentiaza(False))
        self.bind("<Return>", lambda _e: la_deschidere(cifru))
        self.bind("<space>", lambda _e: la_deschidere(cifru))

    def _evidentiaza(self, activ: bool) -> None:
        fundal = tema.PANOU_HOVER if activ else tema.PANOU
        self.configure(bg=fundal, highlightbackground=tema.ACCENT if activ else tema.BORDURA)
        for eticheta in self.etichete:
            eticheta.configure(bg=fundal)
        self.la_atingere(self.descriere if activ else t("mesaj_implicit"))


class MeniuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        setari.incarca()
        self.geometry("1180x760")
        self.minsize(1000, 700)
        self.info = tk.StringVar()
        self._construieste()

    def _construieste(self) -> None:
        """Construieste (sau reconstruieste, dupa schimbarea limbii/temei) tot meniul."""
        self.title("CriptoLab")
        self.configure(bg=tema.FUNDAL)
        tema.aplica_stilul(self)
        self.info.set(t("mesaj_implicit"))

        self._construieste_antet()
        self._construieste_bara_info()
        self._construieste_sectiune_simetrica()
        self._construieste_sectiune_asimetrica()

    def _reconstruieste(self) -> None:
        for element in self.winfo_children():
            element.destroy()
        self._construieste()

    def _construieste_antet(self) -> None:
        antet = tk.Frame(self, bg=tema.FUNDAL)
        antet.pack(fill="x", padx=28, pady=(24, 8))
        titlu = tk.Frame(antet, bg=tema.FUNDAL)
        titlu.pack(side="left")
        tk.Label(titlu, text="CriptoLab", font=("Segoe UI", 28, "bold"),
                 bg=tema.FUNDAL, fg=tema.TEXT).pack(anchor="w")
        tk.Frame(titlu, bg=tema.ACCENT, height=3, width=72).pack(anchor="w", pady=6)

        dreapta = tk.Frame(antet, bg=tema.FUNDAL)
        dreapta.pack(side="right", anchor="n")
        bara_setari.construieste_bara_setari(dreapta, self._reconstruieste).pack(anchor="e")
        ttk.Button(dreapta, text=t("buton_terminologie"), cursor="hand2",
                   command=self._arata_terminologia).pack(anchor="e", pady=(8, 0))

    def _construieste_bara_info(self) -> None:
        bara = tk.Frame(self, bg=tema.PANOU)
        bara.pack(side="bottom", fill="x")
        tk.Label(bara, textvariable=self.info, font=tema.FONT_UI, bg=tema.PANOU, fg=tema.TEXT,
                 anchor="w", padx=28, pady=12).pack(fill="x")

    def _titlu_sectiune(self, text: str) -> None:
        tk.Label(self, text=text, font=("Segoe UI", 13, "bold"), bg=tema.FUNDAL,
                 fg=tema.ACCENT, anchor="w").pack(fill="x", padx=28, pady=(18, 8))

    def _construieste_sectiune_simetrica(self) -> None:
        self._titlu_sectiune(t("sectiune_simetrice"))
        grila = tk.Frame(self, bg=tema.FUNDAL)
        grila.pack(fill="x", padx=22)
        for coloana in range(COLOANE):
            grila.columnconfigure(coloana, weight=1, uniform="cartonase")
        for pozitie, cifru in enumerate(CIFRURI_SIMETRICE):
            cartonas = Cartonas(grila, cifru, self.info.set, self._deschide)
            cartonas.grid(row=pozitie // COLOANE, column=pozitie % COLOANE,
                          padx=6, pady=6, sticky="nsew")

    def _construieste_sectiune_asimetrica(self) -> None:
        self._titlu_sectiune(t("sectiune_asimetrice"))
        tk.Label(self, text=t("in_curand"), font=tema.FONT_UI, bg=tema.FUNDAL,
                 fg=tema.TEXT_SLAB, anchor="w").pack(fill="x", padx=28)

    def _deschide(self, cifru: Cifru) -> None:
        cale = RADACINA / cifru.cod / "interfata.py"
        subprocess.Popen([sys.executable, str(cale)])
        self.info.set(t("mesaj_deschis", nume=t("nume_" + cifru.cod)))

    def _arata_terminologia(self) -> None:
        fereastra = tk.Toplevel(self)
        fereastra.title(t("titlu_terminologie"))
        fereastra.geometry("720x560")
        fereastra.configure(bg=tema.FUNDAL)
        zona = tema.zona_text(fereastra, 10)
        zona.configure(font=tema.FONT_UI, padx=20, pady=16, spacing3=8)
        zona.tag_configure("termen", foreground=tema.ACCENT, font=tema.FONT_UI_BOLD)
        for termen, definitie in traduceri.terminologie():
            zona.insert("end", termen + "\n", "termen")
            zona.insert("end", definitie + "\n\n")
        zona.configure(state="disabled")

        derulare = ttk.Scrollbar(fereastra, command=zona.yview)
        zona.configure(yscrollcommand=derulare.set)
        derulare.pack(side="right", fill="y", pady=16, padx=(0, 16))
        zona.pack(fill="both", expand=True, padx=(16, 0), pady=16)


if __name__ == "__main__":
    MeniuPrincipal().mainloop()
