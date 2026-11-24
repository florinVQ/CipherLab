#include <iostream>
#include <string>
#include <iomanip>
using namespace std;

const int MAX = 10000;
const int MAX_CARACTERE = 90;
const int MAX_LUNGIME_CHEIE = 40;
const int CANDIDATI = 3;  // cate litere-cheie propunem pentru fiecare linie
const long long MAX_COMBINATII = 20000;  // cate chei incercam cel mult (26^3 = 17 576 incap toate)
const int LUNGIME_INCEPUT = 60;          // cate caractere din textul clar arata fiecare cheie

// Testul Kasiski: secventele de cel putin L caractere care apar de doua ori.
// Pentru fiecare pereche de aparitii se scrie "SECV  secventa  pozitia1  pozitia2" (pozitii de la 0).
// Se iau doar secventele maximale: nu pot fi prelungite nici la stanga, nici la dreapta.
void kasiski(string text, int L)
{
    int n = text.length();
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j + L <= n; j++)
        {
            if (i > 0 && text[i - 1] == text[j - 1])
                continue;  // face parte dintr-o secventa care incepe mai devreme
            int lungime = 0;
            while (j + lungime < n && text[i + lungime] == text[j + lungime])
                lungime++;
            if (lungime >= L)
                cout << "SECV\t" << text.substr(i, lungime) << "\t" << i << "\t" << j << endl;
        }
    }
}

// Indicele de coincidenta mediu cand textul se imparte in m linii (caracterele i, i+m, i+2m, ...).
// Pentru un text obisnuit este aproape de 0.06-0.08; pentru litere la intamplare, de 1/m.
void indiceDeCoincidenta(string text, string Alfabet, int maxLungime)
{
    int alfabet = Alfabet.length();
    for (int m = 1; m <= maxLungime && m <= text.length(); m++)
    {
        double suma = 0;
        for (int linie = 0; linie < m; linie++)
        {
            int frecventa[MAX_CARACTERE] = {0};
            int n = 0;
            for (int i = linie; i < text.length(); i += m)
            {
                frecventa[Alfabet.find(text[i])]++;
                n++;
            }
            double coincidente = 0;
            for (int c = 0; c < alfabet; c++)
                coincidente += (double)frecventa[c] * (frecventa[c] - 1);
            if (n > 1)
                suma += coincidente / ((double)n * (n - 1));
        }
        cout << "IC\t" << m << "\t" << fixed << setprecision(4) << suma / m << endl;
    }
}

// Deplasarile fiecarei linii, ordonate de la cea mai potrivita la cea mai putin potrivita.
int ordine[MAX_LUNGIME_CHEIE][MAX_CARACTERE];

// Imparte textul in m linii si, pentru fiecare, scrie frecventele si literele-cheie candidate.
// Litera-cheie s este buna daca, deplasand linia inapoi cu s, frecventele seamana cu cele ale
// limbii (testul chi-patrat: suma (observat - asteptat)^2 / asteptat, cat mai mica).
void frecvente(string text, string Alfabet, int m, double limba[])
{
    int alfabet = Alfabet.length();
    double totalLimba = 0;
    for (int c = 0; c < alfabet; c++)
        totalLimba += limba[c];

    for (int linie = 0; linie < m; linie++)
    {
        string caractere = "";
        int frecventa[MAX_CARACTERE] = {0};
        for (int i = linie; i < text.length(); i += m)
        {
            caractere = caractere + text[i];
            frecventa[Alfabet.find(text[i])]++;
        }
        int n = caractere.length();
        cout << "LINIE\t" << linie + 1 << "\t" << caractere << endl;
        cout << "FRECV\t" << linie + 1;
        for (int c = 0; c < alfabet; c++)
            cout << "\t" << frecventa[c];
        cout << endl;

        double chi[MAX_CARACTERE];
        for (int s = 0; s < alfabet; s++)
        {
            chi[s] = 0;
            for (int c = 0; c < alfabet; c++)
            {
                double asteptat = n * limba[c] / totalLimba;
                double diferenta = frecventa[(c + s) % alfabet] - asteptat;
                chi[s] += diferenta * diferenta / asteptat;
            }
        }
        // Ordonam deplasarile dupa chi-patrat (cel mai mic primul).
        bool ales[MAX_CARACTERE] = {false};
        for (int k = 0; k < alfabet; k++)
        {
            int cel_mai_bun = -1;
            for (int s = 0; s < alfabet; s++)
                if (!ales[s] && (cel_mai_bun == -1 || chi[s] < chi[cel_mai_bun]))
                    cel_mai_bun = s;
            ales[cel_mai_bun] = true;
            ordine[linie][k] = cel_mai_bun;
        }
        cout << "CANDIDATI\t" << linie + 1;
        for (int k = 0; k < CANDIDATI && k < alfabet; k++)
            cout << "\t" << ordine[linie][k];
        cout << endl;
    }
}

// Fiecare linie este un cifru Cezar, deci incercam toate cheile: pe fiecare linie fiecare
// deplasare posibila. Daca toate combinatiile nu incap in MAX_COMBINATII, pe fiecare linie se
// iau doar primele k deplasari din `ordine`. Pentru fiecare cheie se scrie
// "COMB  cheia  scorul  inceputul textului clar"; scorul = cate perechi de litere frecvente
// in limba (EA, RE, IN ...) apar in textul decriptat. Cu cat e mai mare, cu atat textul
// seamana mai mult a limba.
void combinatii(string text, string Alfabet, int m, bool bigrama[][MAX_CARACTERE])
{
    int alfabet = Alfabet.length();
    int n = text.length();
    int pozitie[MAX];
    for (int i = 0; i < n; i++)
        pozitie[i] = Alfabet.find(text[i]);

    // k = cate deplasari incercam pe fiecare linie, astfel incat k^m <= MAX_COMBINATII
    int k = alfabet;
    while (k > 1)
    {
        long long total = 1;
        for (int linie = 0; linie < m && total <= MAX_COMBINATII; linie++)
            total *= k;
        if (total <= MAX_COMBINATII)
            break;
        k--;
    }
    cout << "PE_LINIE\t" << k << endl;

    int indice[MAX_LUNGIME_CHEIE] = {0};  // a cata deplasare din ordine, pe fiecare linie
    while (true)
    {
        string cheie = "";
        for (int linie = 0; linie < m; linie++)
            cheie = cheie + Alfabet[ordine[linie][indice[linie]]];

        int scor = 0, anterior = -1;
        string inceput = "";
        for (int i = 0; i < n; i++)
        {
            int x = (pozitie[i] - ordine[i % m][indice[i % m]] + alfabet) % alfabet;
            if (anterior >= 0 && bigrama[anterior][x])
                scor++;
            anterior = x;
            if (i < LUNGIME_INCEPUT)
                inceput = inceput + Alfabet[x];
        }
        cout << "COMB\t" << cheie << "\t" << scor << "\t" << inceput << endl;

        // Urmatoarea combinatie, ca la un contor: ultima linie se schimba cel mai des.
        int linie = m - 1;
        while (linie >= 0)
        {
            indice[linie]++;
            if (indice[linie] < k)
                break;
            indice[linie] = 0;
            linie--;
        }
        if (linie < 0)
            break;
    }
}

// Intrare:
//   kasiski L maxLungime                    + alfabetul + textul
//   frecvente m  nr f1 ... f(nr)  nrPerechi p1 ... p(nrPerechi)  + alfabetul + textul
//     (f = frecventa fiecarui caracter in limba textului, la 10 000 de litere;
//      p = perechile de litere frecvente in limba, fiecare scrisa ca doua caractere)
int main()
{
    string comanda, Alfabet, text;
    cin >> comanda;

    if (comanda == "kasiski")
    {
        int L, maxLungime;
        cin >> L >> maxLungime >> Alfabet >> text;
        if (text.length() > MAX)
        {
            cerr << "text_lung";
            return 1;
        }
        if (L < 2 || maxLungime < 1 || maxLungime > MAX_LUNGIME_CHEIE)
        {
            cerr << "kasiski_date";
            return 1;
        }
        kasiski(text, L);
        indiceDeCoincidenta(text, Alfabet, maxLungime);
        return 0;
    }

    int m, nrFrecvente, nrPerechi;
    double limba[MAX_CARACTERE];
    static string perechi[MAX_CARACTERE * MAX_CARACTERE];
    static bool bigrama[MAX_CARACTERE][MAX_CARACTERE];
    cin >> m >> nrFrecvente;
    for (int c = 0; c < nrFrecvente && c < MAX_CARACTERE; c++)
        cin >> limba[c];
    cin >> nrPerechi;
    for (int i = 0; i < nrPerechi; i++)
        cin >> perechi[i];
    cin >> Alfabet >> text;
    if (text.length() > MAX)
    {
        cerr << "text_lung";
        return 1;
    }
    if (m < 1 || m > MAX_LUNGIME_CHEIE || m > text.length())
    {
        cerr << "kasiski_m";
        return 1;
    }
    for (int i = 0; i < nrPerechi; i++)
        bigrama[Alfabet.find(perechi[i][0])][Alfabet.find(perechi[i][1])] = true;

    frecvente(text, Alfabet, m, limba);
    combinatii(text, Alfabet, m, bigrama);
    return 0;
}
